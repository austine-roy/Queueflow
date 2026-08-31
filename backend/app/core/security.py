"""Small in-process protections for the single-process QueueFlow deployment."""

import time
from collections import defaultdict, deque

from fastapi import HTTPException, Request, status

from app.core.config import get_settings


class LoginRateLimiter:
    def __init__(self) -> None:
        self.attempts: dict[str, deque[float]] = defaultdict(deque)

    def check(self, client: str) -> None:
        settings = get_settings()
        now = time.monotonic()
        entries = self.attempts[client]
        while entries and now - entries[0] >= settings.auth_login_rate_limit_window_seconds:
            entries.popleft()
        if len(entries) >= settings.auth_login_rate_limit_attempts:
            raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail="Too many login attempts. Try again later.", headers={"Retry-After": str(settings.auth_login_rate_limit_window_seconds)})
        entries.append(now)


login_rate_limiter = LoginRateLimiter()


async def security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers.update({"X-Content-Type-Options": "nosniff", "X-Frame-Options": "DENY", "Referrer-Policy": "strict-origin-when-cross-origin", "Permissions-Policy": "camera=(), microphone=(), geolocation=()"})
    if get_settings().environment == "production":
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    return response
