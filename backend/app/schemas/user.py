import uuid
import re
from datetime import datetime
from pydantic import BaseModel, Field, field_validator


class RegisterBody(BaseModel):
    username: str = Field(..., min_length=3, max_length=32)
    password: str = Field(..., min_length=6)

    @field_validator("username")
    @classmethod
    def username_alphanumeric(cls, v: str) -> str:
        if not re.match(r"^[a-zA-Z0-9_]+$", v):
            raise ValueError("Username may only contain letters, numbers, and underscores")
        return v.lower()


class LoginBody(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    token: str


class UserRead(BaseModel):
    id: uuid.UUID
    username: str
    created_at: datetime

    model_config = {"from_attributes": True}


class ChangePasswordBody(BaseModel):
    current_password: str
    new_password: str = Field(..., min_length=6)
