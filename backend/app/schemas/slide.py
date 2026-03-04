from __future__ import annotations
import uuid
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class SlideUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=255)
    body: Optional[str] = None
    footer_cta: Optional[str] = Field(None, max_length=255)


class SlideRead(BaseModel):
    id: uuid.UUID
    carousel_id: uuid.UUID
    order: int
    title: str
    body: str
    footer_cta: Optional[str]
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class SlideGeneratedItem(BaseModel):
    order: int
    title: str = Field(..., max_length=60)
    body: str = Field(..., max_length=280)
    footer_cta: Optional[str] = Field(None, max_length=80)
