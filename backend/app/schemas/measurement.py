"""Queue measurement API schemas."""

from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field

from app.models.enums import QueueStatus


class MeasurementCreate(BaseModel):
    person_count: int = Field(ge=0)
    density: float = Field(ge=0, le=1)


class MeasurementRead(BaseModel):
    id: int
    queue_id: int
    person_count: int
    density: float
    estimated_wait_time: float
    status: QueueStatus
    recorded_at: datetime
    model_config = ConfigDict(from_attributes=True)
