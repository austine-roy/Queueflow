"""Measurement persistence and queue-state updates."""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from sqlalchemy.orm import Session

from app.core.config import Settings
from app.models.enums import QueueStatus
from app.models.alert import Alert
from app.models.enums import AlertSeverity
from app.models.measurement import QueueMeasurement
from app.models.queue import Queue
from app.schemas.measurement import MeasurementCreate
from app.services.queue_service import calculate_status, estimate_wait_from_history


@dataclass
class MeasurementRecord:
    measurement: QueueMeasurement
    alert: Optional[Alert]


def record_measurement(session: Session, queue: Queue, payload: MeasurementCreate, settings: Settings) -> MeasurementRecord:
    """Persist a measurement and synchronize the current queue projection."""

    previous_status = queue.status
    status = calculate_status(
        current_count=payload.person_count,
        capacity=queue.capacity,
        is_closed=queue.status == QueueStatus.CLOSED,
        settings=settings,
    )
    previous_measurements = list(
        session.query(QueueMeasurement)
        .filter(QueueMeasurement.queue_id == queue.id)
        .order_by(QueueMeasurement.recorded_at.desc(), QueueMeasurement.id.desc())
        .limit(20)
        .all()
    )
    history = [(item.recorded_at.replace(tzinfo=None), item.person_count) for item in reversed(previous_measurements)]
    history.append((datetime.utcnow(), payload.person_count))
    wait_time = estimate_wait_from_history(payload.person_count, settings.default_service_rate_per_minute, history)
    measurement = QueueMeasurement(
        queue_id=queue.id,
        person_count=payload.person_count,
        density=payload.density,
        estimated_wait_time=wait_time,
        status=status,
    )
    queue.current_count = payload.person_count
    queue.density = payload.density
    queue.estimated_wait_time = wait_time
    queue.status = status
    session.add(measurement)
    alert = create_transition_alert(queue, previous_status, status)
    resolve_transition_alerts(session, queue.id, status)
    if alert is not None:
        session.add(alert)
    session.commit()
    session.refresh(measurement)
    if alert is not None:
        session.refresh(alert)
    return MeasurementRecord(measurement=measurement, alert=alert)


def create_transition_alert(queue: Queue, previous: QueueStatus, current: QueueStatus) -> Optional[Alert]:
    """Create one alert when a queue enters a crowded/critical state."""
    concerning = {QueueStatus.CROWDED, QueueStatus.CRITICAL}
    if current not in concerning or previous in concerning:
        return None
    severity = AlertSeverity.CRITICAL if current == QueueStatus.CRITICAL else AlertSeverity.WARNING
    return Alert(queue_id=queue.id, type=f"QUEUE_{current.value}", message=f"{queue.name} entered {current.value} status.", severity=severity)


def resolve_transition_alerts(session: Session, queue_id: int, status: QueueStatus) -> None:
    """Resolve active crowding alerts once the queue returns to a non-concerning state."""

    if status in {QueueStatus.CROWDED, QueueStatus.CRITICAL}:
        return
    for alert in session.query(Alert).filter(Alert.queue_id == queue_id, Alert.is_active.is_(True)).all():
        alert.is_active = False
        alert.resolved_at = datetime.utcnow()
