import uuid
from app.core.config import settings
from app.core.storage import get_s3_client


async def upload_asset(file_bytes: bytes, content_type: str, filename: str) -> str:
    ext = filename.rsplit(".", 1)[-1] if "." in filename else "bin"
    key = f"assets/{uuid.uuid4()}.{ext}"
    async with get_s3_client() as s3:
        await s3.put_object(
            Bucket=settings.minio_bucket,
            Key=key,
            Body=file_bytes,
            ContentType=content_type,
        )
    # Return public URL using the publicly-reachable host (not internal docker hostname)
    public_base = settings.minio_public_url.rstrip("/")
    return f"{public_base}/{settings.minio_bucket}/{key}"
