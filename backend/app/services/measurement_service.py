"""Measurement persistence and queue-state updates."""

from dataclasses import dataclass
from typing import Optional
from sqlalchemy.orm import Session

from app.core.config import Settings
from app.models.enums import QueueStatus
from app.models.alert import Alert
from app.models.enums import AlertSeverity
from app.models.measurement import QueueMeasurement
from app.models.queue import Queue
from app.schemas.measurement import MeasurementCreate
from app.services.queue_service import calculate_status, estimate_wait_time


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
    wait_time = estimate_wait_time(payload.person_count, settings.default_service_rate_per_minute)
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
