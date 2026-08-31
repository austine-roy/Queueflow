"""WebSocket event contracts."""

from datetime import datetime
from pydantic import BaseModel, ConfigDict

from app.models.enums import QueueStatus
from app.schemas.alert import AlertRead


class RealtimeQueue(BaseModel):
    id: int
    name: str
    current_count: int
    density: float
    estimated_wait_time: float
    status: QueueStatus
    timestamp: datetime
    model_config = ConfigDict(from_attributes=True)


class QueueUpdateEvent(BaseModel):
    type: str = "queue_update"
    queue: RealtimeQueue


class AlertEvent(BaseModel):
    type: str = "alert"
    alert: AlertRead
