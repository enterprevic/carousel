from __future__ import annotations
import uuid
from datetime import datetime
from typing import Optional, Literal
from pydantic import BaseModel, Field


class CarouselFormat(BaseModel):
    slides_count: int = Field(default=8, ge=6, le=10)
    language: Literal["ru", "en", "fr"] = "ru"
    style_hint: str = ""


class CarouselDesign(BaseModel):
    template: Literal["classic", "bold", "minimal"] = "classic"
    bg_color: str = "#ffffff"
    bg_image_url: Optional[str] = None
    darkening: float = Field(default=0.0, ge=0.0, le=1.0)
    padding: int = Field(default=40, ge=20, le=80)
    align_h: Literal["left", "center", "right"] = "center"
    align_v: Literal["top", "center", "bottom"] = "center"
    show_header: bool = False
    header_text: str = ""
    show_footer: bool = False
    footer_text: str = ""


class CarouselCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    source_type: Literal["text", "video", "links"]
    source_payload: dict = {}
    format: CarouselFormat = CarouselFormat()


class CarouselUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    format: Optional[CarouselFormat] = None
    design: Optional[CarouselDesign] = None


class CarouselRead(BaseModel):
    id: uuid.UUID
    title: str
    source_type: str
    source_payload: dict
    format: dict
    design: dict
    status: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
