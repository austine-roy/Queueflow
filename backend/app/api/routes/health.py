"""Health endpoint."""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import PlainTextResponse
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.observability import metrics

router = APIRouter(tags=["Health"])


@router.get("/health", summary="Check backend availability")
def health_check() -> dict[str, str]:
    return {"status": "ok", "service": "queueflow-backend"}


@router.get("/ready", summary="Check backend dependencies")
def readiness_check(session: Session = Depends(get_db)) -> dict[str, str]:
    try:
        session.execute(text("SELECT 1"))
    except Exception as error:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Database unavailable") from error
    return {"status": "ready", "database": "ok"}


@router.get("/metrics", summary="Inspect operational metrics", response_class=PlainTextResponse)
def metrics_snapshot() -> PlainTextResponse:
    return PlainTextResponse(metrics.prometheus(), media_type="text/plain; version=0.0.4; charset=utf-8")
