"""Password hashing and short-lived access-token helpers."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any

import jwt
from jwt import InvalidTokenError
from pwdlib import PasswordHash

from app.core.config import Settings
from app.models.enums import UserRole

password_hash = PasswordHash.recommended()
JWT_ALGORITHM = "HS256"


def hash_password(password: str) -> str:
    return password_hash.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return password_hash.verify(password, hashed_password)


def create_access_token(user_id: int, role: UserRole, settings: Settings) -> str:
    expires_at = datetime.now(timezone.utc) + timedelta(minutes=settings.auth_access_token_minutes)
    return jwt.encode({"sub": str(user_id), "role": role.value, "exp": expires_at, "iat": datetime.now(timezone.utc)}, settings.auth_secret_key.get_secret_value(), algorithm=JWT_ALGORITHM)


def decode_access_token(token: str, settings: Settings) -> dict[str, Any]:
    try:
        payload = jwt.decode(token, settings.auth_secret_key.get_secret_value(), algorithms=[JWT_ALGORITHM])
        if not isinstance(payload.get("sub"), str) or payload.get("role") not in {role.value for role in UserRole}:
            raise ValueError("Token claims are incomplete")
        return payload
    except (InvalidTokenError, ValueError) as error:
        raise ValueError("Invalid or expired access token") from error
