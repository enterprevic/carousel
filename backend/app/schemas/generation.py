from __future__ import annotations
import uuid
from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class GenerationCreate(BaseModel):
    carousel_id: uuid.UUID


class GenerationRead(BaseModel):
    id: uuid.UUID
    carousel_id: uuid.UUID
    status: str
    tokens_used: Optional[int]
    error: Optional[str]
    estimated_tokens: Optional[int] = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
