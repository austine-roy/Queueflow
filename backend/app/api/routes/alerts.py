"""Queue alert listing and lifecycle endpoints."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.alert import Alert
from app.schemas.alert import AlertRead

router = APIRouter(prefix="/alerts", tags=["Alerts"])


@router.get("", response_model=list[AlertRead], summary="List queue alerts")
def list_alerts(
    active: Optional[bool] = Query(default=None),
    queue_id: Optional[int] = Query(default=None, gt=0),
    session: Session = Depends(get_db),
) -> list[Alert]:
    query = session.query(Alert)
    if active is not None:
        query = query.filter(Alert.is_active == active)
    if queue_id is not None:
        query = query.filter(Alert.queue_id == queue_id)
    return list(query.order_by(Alert.created_at.desc(), Alert.id.desc()).all())


@router.post("/{alert_id}/resolve", response_model=AlertRead, summary="Resolve an active alert")
def resolve_alert(alert_id: int, session: Session = Depends(get_db)) -> Alert:
    alert = session.get(Alert, alert_id)
    if alert is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Alert not found")
    if alert.is_active:
        alert.is_active = False
        alert.resolved_at = datetime.now(timezone.utc)
        session.commit()
        session.refresh(alert)
    return alert
