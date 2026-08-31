"""Alert API schemas for future alert endpoints."""

from __future__ import annotations

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field

from app.models.enums import AlertSeverity


class AlertCreate(BaseModel):
    queue_id: int = Field(gt=0)
    type: str = Field(min_length=1, max_length=100)
    message: str = Field(min_length=1)
    severity: AlertSeverity


class AlertRead(AlertCreate):
    id: int
    is_active: bool
    created_at: datetime
    resolved_at: Optional[datetime]
    model_config = ConfigDict(from_attributes=True)
