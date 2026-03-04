import uuid
from datetime import datetime, timezone
from sqlalchemy import String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Enum as SAEnum

from app.core.database import Base


class Export(Base):
    __tablename__ = "exports"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    carousel_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("carousels.id", ondelete="CASCADE"))
    status: Mapped[str] = mapped_column(
        SAEnum("queued", "running", "done", "failed", name="export_status_enum"),
        default="queued",
    )
    file_url: Mapped[str | None] = mapped_column(String(1024), nullable=True)
    error: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    carousel: Mapped["Carousel"] = relationship("Carousel", back_populates="exports")
