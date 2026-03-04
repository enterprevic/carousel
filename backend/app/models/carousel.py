import uuid
from datetime import datetime
from sqlalchemy import String, DateTime, Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID, JSONB

from app.core.database import Base


class Carousel(Base):
    __tablename__ = "carousels"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(String(255))
    source_type: Mapped[str] = mapped_column(SAEnum("text", "video", "links", name="source_type_enum"))
    source_payload: Mapped[dict] = mapped_column(JSONB, default=dict)
    format: Mapped[dict] = mapped_column(JSONB, default=dict)
    design: Mapped[dict] = mapped_column(JSONB, default=dict)
    status: Mapped[str] = mapped_column(
        SAEnum("draft", "generating", "ready", "failed", name="carousel_status_enum"),
        default="draft",
    )
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    slides: Mapped[list["Slide"]] = relationship("Slide", back_populates="carousel", cascade="all, delete-orphan", order_by="Slide.order")
    generations: Mapped[list["Generation"]] = relationship("Generation", back_populates="carousel", cascade="all, delete-orphan")
    exports: Mapped[list["Export"]] = relationship("Export", back_populates="carousel", cascade="all, delete-orphan")
