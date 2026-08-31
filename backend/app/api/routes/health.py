"""Health endpoint."""

from fastapi import APIRouter

router = APIRouter(tags=["Health"])


@router.get("/health", summary="Check backend availability")
def health_check() -> dict[str, str]:
    return {"status": "ok", "service": "queueflow-backend"}
