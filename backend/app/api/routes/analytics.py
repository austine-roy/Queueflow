"""Historical analytics assembled close to the database."""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session, selectinload

from app.core.database import get_db
from app.models.queue import Queue
from app.schemas.analytics import QueueAnalyticsRead
from app.schemas.measurement import MeasurementRead

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/queues", response_model=list[QueueAnalyticsRead], summary="Get queue history and analytics")
def queue_analytics(
    measurement_limit: int = Query(default=200, ge=1, le=1000),
    session: Session = Depends(get_db),
) -> list[QueueAnalyticsRead]:
    queues = session.query(Queue).options(selectinload(Queue.measurements)).order_by(Queue.id).all()
    response: list[QueueAnalyticsRead] = []
    for queue in queues:
        measurements = sorted(queue.measurements, key=lambda item: (item.recorded_at, item.id), reverse=True)[:measurement_limit]
        measurements.reverse()
        response.append(
            QueueAnalyticsRead(
                queue_id=queue.id,
                queue_name=queue.name,
                measurement_count=len(queue.measurements),
                average_wait_time=sum(item.estimated_wait_time for item in measurements) / len(measurements) if measurements else 0,
                peak_person_count=max((item.person_count for item in measurements), default=0),
                latest_measurement_at=measurements[-1].recorded_at if measurements else None,
                measurements=[MeasurementRead.model_validate(item) for item in measurements],
            )
        )
    return response
