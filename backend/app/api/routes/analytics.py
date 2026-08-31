"""Historical analytics assembled close to the database."""

from fastapi import APIRouter, Depends, Query
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api.dependencies import require_roles
from app.models.enums import UserRole
from app.models.queue import Queue
from app.models.measurement import QueueMeasurement
from app.schemas.analytics import QueueAnalyticsRead
from app.schemas.measurement import MeasurementRead

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/queues", response_model=list[QueueAnalyticsRead], summary="Get queue history and analytics")
def queue_analytics(
    measurement_limit: int = Query(default=200, ge=1, le=1000),
    session: Session = Depends(get_db),
    _: object = Depends(require_roles(UserRole.VIEWER, UserRole.OPERATOR, UserRole.ADMIN)),
) -> list[QueueAnalyticsRead]:
    queues = session.query(Queue).order_by(Queue.id).all()
    counts = dict(session.query(QueueMeasurement.queue_id, func.count(QueueMeasurement.id)).group_by(QueueMeasurement.queue_id).all())
    ranked = select(
        QueueMeasurement.id,
        func.row_number().over(
            partition_by=QueueMeasurement.queue_id,
            order_by=(QueueMeasurement.recorded_at.desc(), QueueMeasurement.id.desc()),
        ).label("rank"),
    ).subquery()
    recent = (
        session.query(QueueMeasurement)
        .join(ranked, QueueMeasurement.id == ranked.c.id)
        .filter(ranked.c.rank <= measurement_limit)
        .order_by(QueueMeasurement.queue_id, QueueMeasurement.recorded_at, QueueMeasurement.id)
        .all()
    )
    histories: dict[int, list[QueueMeasurement]] = {}
    for measurement in recent:
        histories.setdefault(measurement.queue_id, []).append(measurement)
    response: list[QueueAnalyticsRead] = []
    for queue in queues:
        measurements = histories.get(queue.id, [])
        response.append(
            QueueAnalyticsRead(
                queue_id=queue.id,
                queue_name=queue.name,
                measurement_count=counts.get(queue.id, 0),
                average_wait_time=sum(item.estimated_wait_time for item in measurements) / len(measurements) if measurements else 0,
                peak_person_count=max((item.person_count for item in measurements), default=0),
                latest_measurement_at=measurements[-1].recorded_at if measurements else None,
                measurements=[MeasurementRead.model_validate(item) for item in measurements],
            )
        )
    return response
