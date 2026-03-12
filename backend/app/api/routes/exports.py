import uuid
import jwt
import json
import asyncio
import logging
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from fastapi.responses import StreamingResponse, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db, AsyncSessionLocal
from app.api.deps import require_auth
from app.models.carousel import Carousel
from app.models.export import Export
from app.models.slide import Slide
from app.schemas.export import ExportCreate, ExportRead
from app.services import export_svc

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/exports", tags=["exports"])


async def _run_export(export_id: uuid.UUID, carousel_id: uuid.UUID):
    async with AsyncSessionLocal() as db:
        exp = await db.get(Export, export_id)
        carousel = await db.get(Carousel, carousel_id)
        if not exp or not carousel:
            return

        exp.status = "running"
        await db.commit()

        try:
            result = await db.execute(
                select(Slide).where(Slide.carousel_id == carousel_id).order_by(Slide.order)
            )
            slides = result.scalars().all()

            if not slides:
                raise ValueError("No slides to export")

            file_url, slide_urls = await export_svc.render_slides_to_zip(carousel, slides)

            exp.status = "done"
            exp.file_url = file_url
            exp.slide_urls = slide_urls
            await db.commit()
        except Exception as e:
            logger.error("Export %s failed: %s", export_id, e, exc_info=True)
            exp.status = "failed"
            exp.error = str(e)[:1000]
            await db.commit()


@router.get("", response_model=ExportRead | None)
async def get_latest_export(
    carousel_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    user_id: uuid.UUID = Depends(require_auth),
):
    """Return the most recent done export for a carousel, or null if none exists."""
    carousel = await db.get(Carousel, carousel_id)
    if not carousel or carousel.user_id != user_id:
        raise HTTPException(404, "Carousel not found")
    result = await db.execute(
        select(Export)
        .where(Export.carousel_id == carousel_id, Export.status == "done", Export.file_url.isnot(None))
        .order_by(Export.created_at.desc())
        .limit(1)
    )
    return result.scalar_one_or_none()


@router.post("", response_model=ExportRead, status_code=201)
async def create_export(
    body: ExportCreate,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
    user_id: uuid.UUID = Depends(require_auth),
):
    carousel = await db.get(Carousel, body.carousel_id)
    if not carousel or carousel.user_id != user_id:
        raise HTTPException(404, "Carousel not found")

    exp = Export(carousel_id=body.carousel_id, status="queued")
    db.add(exp)
    await db.commit()
    await db.refresh(exp)

    background_tasks.add_task(_run_export, exp.id, body.carousel_id)
    return exp


@router.get("/{export_id}", response_model=ExportRead)
async def get_export(
    export_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    user_id: uuid.UUID = Depends(require_auth),
):
    exp = await db.get(Export, export_id)
    if not exp:
        raise HTTPException(404, "Export not found")
    carousel = await db.get(Carousel, exp.carousel_id)
    if not carousel or carousel.user_id != user_id:
        raise HTTPException(404, "Export not found")
    return exp


@router.get("/{export_id}/stream")
async def stream_export(export_id: uuid.UUID, token: str = ""):
    """SSE endpoint — streams export status updates until done or failed.
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
                exp = await db.get(Export, export_id)
            if exp is None:
                yield f"event: error\ndata: {json.dumps({'detail': 'Not found'})}\n\n"
                return
            payload = {
                "id": str(exp.id),
                "status": exp.status,
                "file_url": exp.file_url,
                "slide_urls": exp.slide_urls,
                "error": exp.error,
            }
            yield f"event: status\ndata: {json.dumps(payload)}\n\n"
            if exp.status in ("done", "failed"):
                return
            await asyncio.sleep(poll_interval)
            poll_interval = min(poll_interval * 1.5, 5.0)

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )
