import uuid
import logging
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks

logger = logging.getLogger(__name__)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db, AsyncSessionLocal
from app.models.carousel import Carousel
from app.models.export import Export
from app.models.slide import Slide
from app.schemas.export import ExportCreate, ExportRead
from app.services import export_svc

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

            file_url = await export_svc.render_slides_to_zip(carousel, slides)

            exp.status = "done"
            exp.file_url = file_url
            await db.commit()
        except Exception as e:
            logger.error("Export %s failed: %s", export_id, e, exc_info=True)
            exp.status = "failed"
            exp.error = str(e)[:1000]
            await db.commit()


@router.post("", response_model=ExportRead, status_code=201)
async def create_export(
    body: ExportCreate,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
):
    carousel = await db.get(Carousel, body.carousel_id)
    if not carousel:
        raise HTTPException(404, "Carousel not found")

    exp = Export(carousel_id=body.carousel_id, status="queued")
    db.add(exp)
    await db.commit()
    await db.refresh(exp)

    background_tasks.add_task(_run_export, exp.id, body.carousel_id)
    return exp


@router.get("/{export_id}", response_model=ExportRead)
async def get_export(export_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    exp = await db.get(Export, export_id)
    if not exp:
        raise HTTPException(404, "Export not found")
    return exp
