"""Server-side historical queue analytics contracts."""

from __future__ import annotations

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

from app.schemas.measurement import MeasurementRead


class QueueAnalyticsRead(BaseModel):
    queue_id: int
    queue_name: str
    measurement_count: int = Field(ge=0)
    average_wait_time: float = Field(ge=0)
    peak_person_count: int = Field(ge=0)
    latest_measurement_at: Optional[datetime]
    measurements: list[MeasurementRead]
