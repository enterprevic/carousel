import uuid
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.models.slide import Slide
from app.models.carousel import Carousel
from app.schemas.slide import SlideUpdate, SlideRead

router = APIRouter(prefix="/carousels", tags=["slides"])


@router.get("/{carousel_id}/slides", response_model=list[SlideRead])
async def list_slides(carousel_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    c = await db.get(Carousel, carousel_id)
    if not c:
        raise HTTPException(404, "Carousel not found")
    result = await db.execute(
        select(Slide).where(Slide.carousel_id == carousel_id).order_by(Slide.order)
    )
    return result.scalars().all()


@router.patch("/{carousel_id}/slides/{slide_id}", response_model=SlideRead)
async def update_slide(
    carousel_id: uuid.UUID,
    slide_id: uuid.UUID,
    body: SlideUpdate,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Slide).where(Slide.id == slide_id, Slide.carousel_id == carousel_id)
    )
    slide = result.scalar_one_or_none()
    if not slide:
        raise HTTPException(404, "Slide not found")
    if body.title is not None:
        slide.title = body.title
    if body.body is not None:
        slide.body = body.body
    if body.footer_cta is not None:
        slide.footer_cta = body.footer_cta
    if body.overrides is not None:
        slide.overrides = body.overrides.model_dump(exclude_none=True)
    slide.updated_at = datetime.utcnow()
    await db.commit()
    await db.refresh(slide)
    return slide
