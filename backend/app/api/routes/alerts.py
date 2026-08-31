"""Alert read endpoint."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.alert import Alert
from app.schemas.alert import AlertRead

router = APIRouter(prefix="/alerts", tags=["Alerts"])


@router.get("", response_model=list[AlertRead], summary="List queue alerts")
def list_alerts(session: Session = Depends(get_db)) -> list[Alert]:
    return list(session.query(Alert).order_by(Alert.created_at.desc(), Alert.id.desc()).all())
