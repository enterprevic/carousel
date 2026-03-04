import uuid
from datetime import datetime
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update

from app.core.database import get_db
from app.models.carousel import Carousel
from app.schemas.carousel import CarouselCreate, CarouselUpdate, CarouselRead, CarouselDesign

router = APIRouter(prefix="/carousels", tags=["carousels"])


@router.get("", response_model=list[CarouselRead])
async def list_carousels(
    status: Optional[str] = None,
    lang: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
):
    q = select(Carousel).order_by(Carousel.created_at.desc())
    if status:
        q = q.where(Carousel.status == status)
    if lang:
        q = q.where(Carousel.format["language"].astext == lang)
    result = await db.execute(q)
    return result.scalars().all()


@router.get("/{carousel_id}", response_model=CarouselRead)
async def get_carousel(carousel_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    c = await db.get(Carousel, carousel_id)
    if not c:
        raise HTTPException(404, "Carousel not found")
    return c


@router.post("", response_model=CarouselRead, status_code=201)
async def create_carousel(body: CarouselCreate, db: AsyncSession = Depends(get_db)):
    c = Carousel(
        title=body.title,
        source_type=body.source_type,
        source_payload=body.source_payload,
        format=body.format.model_dump(),
        design=CarouselDesign().model_dump(),
        status="draft",
    )
    db.add(c)
    await db.commit()
    await db.refresh(c)
    return c


@router.patch("/{carousel_id}", response_model=CarouselRead)
async def update_carousel(carousel_id: uuid.UUID, body: CarouselUpdate, db: AsyncSession = Depends(get_db)):
    c = await db.get(Carousel, carousel_id)
    if not c:
        raise HTTPException(404, "Carousel not found")
    if body.title is not None:
        c.title = body.title
    if body.format is not None:
        c.format = body.format.model_dump()
    if body.design is not None:
        c.design = body.design.model_dump()
    c.updated_at = datetime.utcnow()
    await db.commit()
    await db.refresh(c)
    return c


@router.patch("/{carousel_id}/design", response_model=CarouselRead)
async def update_design(carousel_id: uuid.UUID, body: CarouselDesign, db: AsyncSession = Depends(get_db)):
    c = await db.get(Carousel, carousel_id)
    if not c:
        raise HTTPException(404, "Carousel not found")
    c.design = body.model_dump()
    c.updated_at = datetime.utcnow()
    await db.commit()
    await db.refresh(c)
    return c
