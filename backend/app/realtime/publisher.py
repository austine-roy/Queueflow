"""Translate persisted measurements into real-time client events."""

from app.realtime.websocket_manager import WebSocketManager
from app.schemas.alert import AlertRead
from app.schemas.realtime import AlertEvent, QueueUpdateEvent, RealtimeQueue
from app.services.measurement_service import MeasurementRecord


async def publish_measurement(record: MeasurementRecord, websocket_manager: WebSocketManager) -> None:
    """Broadcast the current projection and its one-time transition alert."""

    queue = record.measurement.queue
    await websocket_manager.broadcast(
        QueueUpdateEvent(
            queue=RealtimeQueue(
                id=queue.id,
                name=queue.name,
                current_count=queue.current_count,
                density=queue.density,
                estimated_wait_time=queue.estimated_wait_time,
                status=queue.status,
                timestamp=record.measurement.recorded_at,
            )
        ).model_dump(mode="json")
    )
    if record.alert is not None:
        await websocket_manager.broadcast(
            AlertEvent(alert=AlertRead.model_validate(record.alert)).model_dump(mode="json")
        )
