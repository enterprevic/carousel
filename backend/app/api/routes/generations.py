import uuid
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db, AsyncSessionLocal
from app.models.carousel import Carousel
from app.models.generation import Generation
from app.models.slide import Slide
from app.schemas.generation import GenerationCreate, GenerationRead
from app.services import llm as llm_service

router = APIRouter(prefix="/generations", tags=["generations"])


async def _run_generation(generation_id: uuid.UUID, carousel_id: uuid.UUID):
    async with AsyncSessionLocal() as db:
        gen = await db.get(Generation, generation_id)
        carousel = await db.get(Carousel, carousel_id)
        if not gen or not carousel:
            return

        gen.status = "running"
        gen.updated_at = datetime.utcnow()
        carousel.status = "generating"
        carousel.updated_at = datetime.utcnow()
        await db.commit()

        try:
            slides_data, tokens_used = await llm_service.generate_slides(carousel)

            # delete existing slides
            from sqlalchemy import delete
            await db.execute(delete(Slide).where(Slide.carousel_id == carousel_id))

            # insert new slides
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
            gen.updated_at = datetime.utcnow()
            carousel.status = "ready"
            carousel.updated_at = datetime.utcnow()
            await db.commit()

        except Exception as e:
            gen.status = "failed"
            gen.error = str(e)[:1000]
            gen.updated_at = datetime.utcnow()
            carousel.status = "failed"
            carousel.updated_at = datetime.utcnow()
            await db.commit()


@router.post("", response_model=GenerationRead, status_code=201)
async def create_generation(
    body: GenerationCreate,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
):
    carousel = await db.get(Carousel, body.carousel_id)
    if not carousel:
        raise HTTPException(404, "Carousel not found")

    estimated = llm_service.estimate_tokens(carousel)

    gen = Generation(carousel_id=body.carousel_id, status="queued")
    db.add(gen)
    await db.commit()
    await db.refresh(gen)

    background_tasks.add_task(_run_generation, gen.id, body.carousel_id)

    result = GenerationRead.model_validate(gen)
    result.estimated_tokens = estimated
    return result


@router.get("/{generation_id}", response_model=GenerationRead)
async def get_generation(generation_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    gen = await db.get(Generation, generation_id)
    if not gen:
        raise HTTPException(404, "Generation not found")
    return gen
