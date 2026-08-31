"""Queue measurement endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.routes.queues import get_queue_or_404
from app.core.config import get_settings
from app.core.database import get_db
from app.models.measurement import QueueMeasurement
from app.realtime.publisher import publish_measurement
from app.realtime.websocket_manager import manager
from app.schemas.measurement import MeasurementCreate, MeasurementRead
from app.services.measurement_service import record_measurement

router = APIRouter(prefix="/queues/{queue_id}/measurements", tags=["Measurements"])


@router.get("", response_model=list[MeasurementRead], summary="List a queue's measurements")
def list_measurements(queue_id: int, session: Session = Depends(get_db)) -> list[QueueMeasurement]:
    get_queue_or_404(session, queue_id)
    return list(
        session.query(QueueMeasurement)
        .filter(QueueMeasurement.queue_id == queue_id)
        .order_by(QueueMeasurement.recorded_at.desc(), QueueMeasurement.id.desc())
        .all()
    )


@router.post("", response_model=MeasurementRead, status_code=status.HTTP_201_CREATED, summary="Record a queue measurement")
async def create_measurement(queue_id: int, payload: MeasurementCreate, session: Session = Depends(get_db)) -> QueueMeasurement:
    queue = get_queue_or_404(session, queue_id)
    record = record_measurement(session, queue, payload, get_settings())
    await publish_measurement(record, manager)
    return record.measurement
