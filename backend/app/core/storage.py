import aioboto3
from botocore.config import Config
from app.core.config import settings

_session = aioboto3.Session(
    aws_access_key_id=settings.minio_access_key,
    aws_secret_access_key=settings.minio_secret_key,
)

ENDPOINT_URL = f"{'https' if settings.minio_secure else 'http'}://{settings.minio_endpoint}"


def get_s3_client():
    return _session.client(
        "s3",
        endpoint_url=ENDPOINT_URL,
        config=Config(signature_version="s3v4"),
    )


def get_s3_client_public():
    """Client whose endpoint matches the public URL — presigned URLs must be signed with the same host the browser will use."""
    return _session.client(
        "s3",
        endpoint_url=settings.minio_public_url,
        config=Config(signature_version="s3v4"),
    )


async def ensure_bucket():
    async with get_s3_client() as s3:
        try:
            await s3.head_bucket(Bucket=settings.minio_bucket)
        except Exception:
            await s3.create_bucket(Bucket=settings.minio_bucket)
            await s3.put_bucket_policy(
                Bucket=settings.minio_bucket,
                Policy=f'{{"Version":"2012-10-17","Statement":[{{"Effect":"Allow","Principal":"*","Action":["s3:GetObject"],"Resource":["arn:aws:s3:::{settings.minio_bucket}/*"]}}]}}',
            )
