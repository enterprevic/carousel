from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from pydantic import BaseModel

from app.api.deps import require_auth
from app.services.storage_svc import upload_asset

router = APIRouter(prefix="/assets", tags=["assets"])

ALLOWED_TYPES = {"image/jpeg", "image/png", "image/webp", "image/gif"}
MAX_SIZE = 10 * 1024 * 1024  # 10 MB


class UploadResponse(BaseModel):
    url: str


@router.post("/upload", response_model=UploadResponse)
async def upload_file(file: UploadFile = File(...), _: object = Depends(require_auth)):
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(400, f"Unsupported file type: {file.content_type}")
    data = await file.read()
    if len(data) > MAX_SIZE:
        raise HTTPException(400, "File too large (max 10 MB)")
    url = await upload_asset(data, file.content_type, file.filename or "upload")
    return UploadResponse(url=url)
