import uuid
import jwt
from fastapi import Header, HTTPException, status


async def require_auth(authorization: str = Header(default="")) -> uuid.UUID:
    """Validates Bearer JWT and returns the user_id UUID from the token sub claim."""
    if authorization.startswith("Bearer "):
        token = authorization[7:]
        try:
            from app.api.auth import _secret
            payload = jwt.decode(token, _secret(), algorithms=["HS256"])
            return uuid.UUID(payload["sub"])
        except (jwt.PyJWTError, KeyError, ValueError):
            pass
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication required")
