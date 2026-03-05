from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "postgresql+asyncpg://carousel:carousel@postgres:5432/carousel"
    minio_endpoint: str = "minio:9000"
    minio_access_key: str = "minioadmin"
    minio_secret_key: str = "minioadmin"
    minio_bucket: str = "carousel-assets"
    minio_secure: bool = False
    minio_public_url: str = "http://localhost:9000"
    frontend_url: str = "http://localhost:3000"
    cors_origins: str = "*"  # comma-separated list or "*" for all

    # JWT auth
    jwt_secret: str = ""
    jwt_expire_hours: int = 72

    # LLM (OpenAI-compatible)
    llm_api_key: str = ""
    llm_base_url: str = "https://api.groq.com/openai/v1/chat/completions"
    llm_model: str = "llama-3.3-70b-versatile"

    class Config:
        env_file = ".env"


settings = Settings()
