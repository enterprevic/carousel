import uuid
import jwt
import json
import asyncio
import logging
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from fastapi.responses import StreamingResponse, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete

from app.core.database import get_db, AsyncSessionLocal
from app.api.deps import require_auth
from app.models.carousel import Carousel
from app.models.generation import Generation
from app.models.slide import Slide
from app.schemas.generation import GenerationCreate, GenerationRead
from app.services import llm as llm_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/generations", tags=["generations"])

# Simple in-memory rate limiting: user_id -> last generation timestamp
_last_generation: dict[uuid.UUID, datetime] = {}
_GENERATION_COOLDOWN_SECONDS = 30


async def _run_generation(generation_id: uuid.UUID, carousel_id: uuid.UUID):
    async with AsyncSessionLocal() as db:
        gen = await db.get(Generation, generation_id)
        carousel = await db.get(Carousel, carousel_id)
        if not gen or not carousel:
            return

        gen.status = "running"
        gen.updated_at = datetime.now(timezone.utc)
        carousel.status = "generating"
        carousel.updated_at = datetime.now(timezone.utc)
        await db.commit()

        try:
            slides_data, tokens_used = await llm_service.generate_slides(carousel)

            await db.execute(delete(Slide).where(Slide.carousel_id == carousel_id))

            for item in slides_data:
                slide = Slide(
                    carousel_id=carousel_id,
                    order=item.order,
                    title=item.title,
                    body=item.body,
                    footer_cta=item.footer_cta,
                )
                db.add(slide)

            gen.status = "done"
            gen.tokens_used = tokens_used
            gen.updated_at = datetime.now(timezone.utc)
            carousel.status = "ready"
            carousel.updated_at = datetime.now(timezone.utc)
            await db.commit()

        except Exception as e:
            logger.error("Generation %s failed: %s", generation_id, e, exc_info=True)
            gen.status = "failed"
            gen.error = str(e)[:1000]
            gen.updated_at = datetime.now(timezone.utc)
            carousel.status = "failed"
            carousel.updated_at = datetime.now(timezone.utc)
            await db.commit()


@router.post("", response_model=GenerationRead, status_code=201)
async def create_generation(
    body: GenerationCreate,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
    user_id: uuid.UUID = Depends(require_auth),
):
    carousel = await db.get(Carousel, body.carousel_id)
    if not carousel or carousel.user_id != user_id:
        raise HTTPException(404, "Carousel not found")

    # Rate limiting
    now = datetime.now(timezone.utc)
    last = _last_generation.get(user_id)
    if last:
        elapsed = (now - last).total_seconds()
        if elapsed < _GENERATION_COOLDOWN_SECONDS:
            wait = int(_GENERATION_COOLDOWN_SECONDS - elapsed)
            raise HTTPException(429, f"Please wait {wait}s before generating again")

    active = await db.execute(
        select(Generation).where(
            Generation.carousel_id == body.carousel_id,
            Generation.status.in_(["queued", "running"]),
        )
    )
    if active.scalar_one_or_none():
        raise HTTPException(409, "A generation is already in progress for this carousel")

    estimated = llm_service.estimate_tokens(carousel)

    gen = Generation(carousel_id=body.carousel_id, status="queued")
    db.add(gen)
    await db.commit()
    await db.refresh(gen)

    _last_generation[user_id] = now
    background_tasks.add_task(_run_generation, gen.id, body.carousel_id)

    result = GenerationRead.model_validate(gen)
    result.estimated_tokens = estimated
    return result


@router.get("/{generation_id}", response_model=GenerationRead)
async def get_generation(
    generation_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    user_id: uuid.UUID = Depends(require_auth),
):
    gen = await db.get(Generation, generation_id)
    if not gen:
        raise HTTPException(404, "Generation not found")
    # verify carousel ownership
    carousel = await db.get(Carousel, gen.carousel_id)
    if not carousel or carousel.user_id != user_id:
        raise HTTPException(404, "Generation not found")
    return gen


@router.get("/{generation_id}/stream")
async def stream_generation(generation_id: uuid.UUID, token: str = ""):
    """SSE endpoint — streams generation status updates until done or failed.
    Auth via ?token= (JWT) query param since EventSource doesn't support headers."""
    from app.api.auth import _secret
    try:
        jwt.decode(token, _secret(), algorithms=["HS256"])
    except Exception:
        return Response(status_code=401)

    async def event_generator():
        poll_interval = 1.0
        while True:
            async with AsyncSessionLocal() as db:
                gen = await db.get(Generation, generation_id)
            if gen is None:
                yield f"event: error\ndata: {json.dumps({'detail': 'Not found'})}\n\n"
                return
            payload = {
                "id": str(gen.id),
                "status": gen.status,
                "tokens_used": gen.tokens_used,
                "error": gen.error,
            }
            yield f"event: status\ndata: {json.dumps(payload)}\n\n"
            if gen.status in ("done", "failed"):
                return
            await asyncio.sleep(poll_interval)
            poll_interval = min(poll_interval * 1.5, 5.0)

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )
