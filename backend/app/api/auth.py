import secrets
import uuid
from datetime import datetime, timedelta, timezone

import bcrypt
import jwt
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.database import get_db
from app.api.deps import require_auth
from app.models.user import User
from app.models.carousel import Carousel
from app.models.generation import Generation
from app.schemas.user import RegisterBody, LoginBody, TokenResponse, UserRead, ChangePasswordBody

router = APIRouter(prefix="/auth", tags=["auth"])


def _hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def _verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed.encode())

# Per-process fallback secret (tokens won't survive restarts unless JWT_SECRET is set)
_PROCESS_SECRET = secrets.token_hex(32)


def _secret() -> str:
    return settings.jwt_secret or _PROCESS_SECRET


def _make_token(user_id: uuid.UUID) -> str:
    payload = {
        "sub": str(user_id),
        "exp": datetime.now(timezone.utc) + timedelta(hours=settings.jwt_expire_hours),
    }
    return jwt.encode(payload, _secret(), algorithm="HS256")


@router.post("/register", response_model=TokenResponse, status_code=201)
async def register(body: RegisterBody, db: AsyncSession = Depends(get_db)):
    existing = await db.execute(select(User).where(User.username == body.username))
    if existing.scalar_one_or_none():
        raise HTTPException(409, "Username already taken")
    user = User(
        username=body.username,
        hashed_password=_hash_password(body.password),
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return TokenResponse(token=_make_token(user.id))


@router.post("/login", response_model=TokenResponse)
async def login(body: LoginBody, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.username == body.username.lower()))
    user = result.scalar_one_or_none()
    if not user or not _verify_password(body.password, user.hashed_password):
        raise HTTPException(401, "Incorrect username or password")
    return TokenResponse(token=_make_token(user.id))


@router.get("/verify")
async def verify(token: str = ""):
    """Used by frontend middleware to check if a token is valid."""
    try:
        jwt.decode(token, _secret(), algorithms=["HS256"])
        return {"ok": True}
    except jwt.PyJWTError:
        raise HTTPException(401, "Invalid or expired token")



@router.get("/me", response_model=UserRead)
async def me(db: AsyncSession = Depends(get_db), user_id: uuid.UUID = Depends(require_auth)):
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(404, "User not found")
    return user


@router.post("/password", status_code=204)
async def change_password(
    body: ChangePasswordBody,
    db: AsyncSession = Depends(get_db),
    user_id: uuid.UUID = Depends(require_auth),
):
    user = await db.get(User, user_id)
    if not user or not _verify_password(body.current_password, user.hashed_password):
        raise HTTPException(400, "Incorrect password")
    user.hashed_password = _hash_password(body.new_password)
    await db.commit()


@router.get("/me/stats")
async def me_stats(db: AsyncSession = Depends(get_db), user_id: uuid.UUID = Depends(require_auth)):
    """Return usage statistics for the current user."""
    # Total carousels
    carousel_count_row = await db.execute(
        select(func.count()).where(Carousel.user_id == user_id)
    )
    carousel_count = carousel_count_row.scalar() or 0

    # Generations and token totals — join via carousels owned by this user
    gen_stats_row = await db.execute(
        select(
            func.count(Generation.id),
            func.coalesce(func.sum(Generation.tokens_used), 0),
        )
        .join(Carousel, Carousel.id == Generation.carousel_id)
        .where(Carousel.user_id == user_id)
        .where(Generation.status == "done")
    )
    gen_count, tokens_total = gen_stats_row.one()

    return {
        "carousels": carousel_count,
        "generations": int(gen_count),
        "tokens_used": int(tokens_total),
    }
