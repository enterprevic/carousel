import uuid
from datetime import datetime, timezone
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.api.deps import require_auth
from app.models.carousel import Carousel
from app.models.generation import Generation
from app.schemas.carousel import CarouselCreate, CarouselUpdate, CarouselRead, CarouselDesign
from app.schemas.generation import GenerationRead

router = APIRouter(prefix="/carousels", tags=["carousels"])


@router.get("", response_model=list[CarouselRead])
async def list_carousels(
    status: Optional[str] = None,
    lang: Optional[str] = None,
    limit: int = 50,
    offset: int = 0,
    db: AsyncSession = Depends(get_db),
    user_id: uuid.UUID = Depends(require_auth),
):
    q = (
        select(Carousel)
        .where(Carousel.user_id == user_id)
        .order_by(Carousel.created_at.desc())
        .limit(limit)
        .offset(offset)
    )
    if status:
        q = q.where(Carousel.status == status)
    if lang:
        q = q.where(Carousel.format["language"].astext == lang)
    result = await db.execute(q)
    return result.scalars().all()


@router.get("/{carousel_id}", response_model=CarouselRead)
async def get_carousel(
    carousel_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    user_id: uuid.UUID = Depends(require_auth),
):
    c = await db.get(Carousel, carousel_id)
    if not c or c.user_id != user_id:
        raise HTTPException(404, "Carousel not found")
    return c


@router.post("", response_model=CarouselRead, status_code=201)
async def create_carousel(
    body: CarouselCreate,
    db: AsyncSession = Depends(get_db),
    user_id: uuid.UUID = Depends(require_auth),
):
    c = Carousel(
        user_id=user_id,
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
async def update_carousel(
    carousel_id: uuid.UUID,
    body: CarouselUpdate,
    db: AsyncSession = Depends(get_db),
    user_id: uuid.UUID = Depends(require_auth),
):
    c = await db.get(Carousel, carousel_id)
    if not c or c.user_id != user_id:
        raise HTTPException(404, "Carousel not found")
    if body.title is not None:
        c.title = body.title
    if body.format is not None:
        c.format = body.format.model_dump()
    if body.design is not None:
        c.design = body.design.model_dump()
    c.updated_at = datetime.now(timezone.utc)
    await db.commit()
    await db.refresh(c)
    return c


@router.patch("/{carousel_id}/design", response_model=CarouselRead)
async def update_design(
    carousel_id: uuid.UUID,
    body: CarouselDesign,
    db: AsyncSession = Depends(get_db),
    user_id: uuid.UUID = Depends(require_auth),
):
    c = await db.get(Carousel, carousel_id)
    if not c or c.user_id != user_id:
        raise HTTPException(404, "Carousel not found")
    c.design = body.model_dump()
    c.updated_at = datetime.now(timezone.utc)
    await db.commit()
    await db.refresh(c)
    return c


@router.get("/{carousel_id}/generations", response_model=list[GenerationRead])
async def list_generations(
    carousel_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    user_id: uuid.UUID = Depends(require_auth),
):
    c = await db.get(Carousel, carousel_id)
    if not c or c.user_id != user_id:
        raise HTTPException(404, "Carousel not found")
    result = await db.execute(
        select(Generation)
        .where(Generation.carousel_id == carousel_id)
        .order_by(Generation.created_at.desc())
    )
    return result.scalars().all()


@router.delete("/{carousel_id}", status_code=204)
async def delete_carousel(
    carousel_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    user_id: uuid.UUID = Depends(require_auth),
):
    c = await db.get(Carousel, carousel_id)
    if not c or c.user_id != user_id:
        raise HTTPException(404, "Carousel not found")
    await db.delete(c)
    await db.commit()
