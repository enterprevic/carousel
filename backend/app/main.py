from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.storage import ensure_bucket
from app.api import auth as auth_routes
from app.api.routes import carousels, slides, generations, exports, assets
from app.models import user as _user_model  # noqa: F401 — ensures User is in metadata for Alembic


@asynccontextmanager
async def lifespan(app: FastAPI):
    await ensure_bucket()
    yield


app = FastAPI(title="Carousel Generator API", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_routes.router)
app.include_router(carousels.router)
app.include_router(slides.router)
app.include_router(generations.router)
app.include_router(exports.router)
app.include_router(assets.router)


@app.get("/health")
async def health():
    return {"status": "ok"}
