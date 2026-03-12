import uuid
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.api.deps import require_auth
from app.models.slide import Slide
from app.models.carousel import Carousel
from app.schemas.slide import SlideUpdate, SlideRead, SlideMoveBody

router = APIRouter(prefix="/carousels", tags=["slides"])


@router.get("/{carousel_id}/slides", response_model=list[SlideRead])
async def list_slides(
    carousel_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    user_id: uuid.UUID = Depends(require_auth),
):
    c = await db.get(Carousel, carousel_id)
    if not c or c.user_id != user_id:
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
    user_id: uuid.UUID = Depends(require_auth),
):
    c = await db.get(Carousel, carousel_id)
    if not c or c.user_id != user_id:
        raise HTTPException(404, "Carousel not found")
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
    if "footer_cta" in body.model_fields_set:
        slide.footer_cta = body.footer_cta  # allows null to clear it
    if body.overrides is not None:
        slide.overrides = body.overrides.model_dump(exclude_none=True)
    slide.updated_at = datetime.now(timezone.utc)
    await db.commit()
    await db.refresh(slide)
    return slide


@router.delete("/{carousel_id}/slides/{slide_id}", status_code=204)
async def delete_slide(
    carousel_id: uuid.UUID,
    slide_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    user_id: uuid.UUID = Depends(require_auth),
):
    c = await db.get(Carousel, carousel_id)
    if not c or c.user_id != user_id:
        raise HTTPException(404, "Carousel not found")
    result = await db.execute(
        select(Slide).where(Slide.id == slide_id, Slide.carousel_id == carousel_id)
    )
    slide = result.scalar_one_or_none()
    if not slide:
        raise HTTPException(404, "Slide not found")
    await db.delete(slide)
    # Reorder remaining slides
    remaining = await db.execute(
        select(Slide).where(Slide.carousel_id == carousel_id).order_by(Slide.order)
    )
    for i, s in enumerate(remaining.scalars().all()):
        s.order = i
    await db.commit()


@router.post("/{carousel_id}/slides/{slide_id}/duplicate", response_model=SlideRead, status_code=201)
async def duplicate_slide(
    carousel_id: uuid.UUID,
    slide_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    user_id: uuid.UUID = Depends(require_auth),
):
    c = await db.get(Carousel, carousel_id)
    if not c or c.user_id != user_id:
        raise HTTPException(404, "Carousel not found")
    result = await db.execute(
        select(Slide).where(Slide.id == slide_id, Slide.carousel_id == carousel_id)
    )
    slide = result.scalar_one_or_none()
    if not slide:
        raise HTTPException(404, "Slide not found")
    # Shift all slides after this one up by 1
    after = await db.execute(
        select(Slide).where(Slide.carousel_id == carousel_id, Slide.order > slide.order).order_by(Slide.order)
    )
    for s in after.scalars().all():
        s.order += 1
    new_slide = Slide(
        id=uuid.uuid4(),
        carousel_id=carousel_id,
        order=slide.order + 1,
        title=slide.title,
        body=slide.body,
        footer_cta=slide.footer_cta,
        overrides=dict(slide.overrides) if slide.overrides else {},
    )
    db.add(new_slide)
    await db.commit()
    await db.refresh(new_slide)
    return new_slide


@router.patch("/{carousel_id}/slides/{slide_id}/order", response_model=list[SlideRead])
async def move_slide(
    carousel_id: uuid.UUID,
    slide_id: uuid.UUID,
    body: SlideMoveBody,
    db: AsyncSession = Depends(get_db),
    user_id: uuid.UUID = Depends(require_auth),
):
    """Move a slide to a new position."""
    c = await db.get(Carousel, carousel_id)
    if not c or c.user_id != user_id:
        raise HTTPException(404, "Carousel not found")
    result = await db.execute(
        select(Slide).where(Slide.carousel_id == carousel_id).order_by(Slide.order)
    )
    all_slides = list(result.scalars().all())
    slide = next((s for s in all_slides if s.id == slide_id), None)
    if not slide:
        raise HTTPException(404, "Slide not found")
    new_order = max(0, min(body.new_order, len(all_slides) - 1))
    all_slides.remove(slide)
    all_slides.insert(new_order, slide)
    now = datetime.now(timezone.utc)
    for i, s in enumerate(all_slides):
        s.order = i
        s.updated_at = now
    await db.commit()
    return all_slides
