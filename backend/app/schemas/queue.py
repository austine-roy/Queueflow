"""Queue API schemas."""

from __future__ import annotations

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field

from app.models.enums import QueueStatus


class QueueCreate(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    location_id: int = Field(gt=0)
    capacity: int = Field(gt=0)
    current_count: int = Field(default=0, ge=0)
    density: float = Field(default=0, ge=0, le=1)
    estimated_wait_time: float = Field(default=0, ge=0)
    status: QueueStatus = QueueStatus.NORMAL


class QueueUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=200)
    capacity: Optional[int] = Field(default=None, gt=0)
    current_count: Optional[int] = Field(default=None, ge=0)
    density: Optional[float] = Field(default=None, ge=0, le=1)
    estimated_wait_time: Optional[float] = Field(default=None, ge=0)
    status: Optional[QueueStatus] = None


class QueueRead(QueueCreate):
    id: int
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)
