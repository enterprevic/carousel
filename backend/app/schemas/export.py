from __future__ import annotations
import uuid
from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class ExportCreate(BaseModel):
    carousel_id: uuid.UUID


class ExportRead(BaseModel):
    id: uuid.UUID
    carousel_id: uuid.UUID
    status: str
    file_url: Optional[str]
    error: Optional[str] = None
    created_at: datetime

    model_config = {"from_attributes": True}
