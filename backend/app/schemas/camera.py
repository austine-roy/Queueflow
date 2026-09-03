"""Camera API schemas for future camera administration endpoints."""

from __future__ import annotations

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field

from app.models.enums import CameraSourceType, QueueStatus


class CameraCreate(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    location_id: int = Field(gt=0)
    queue_id: Optional[int] = Field(default=None, gt=0)
    source_type: CameraSourceType
    source_url: Optional[str] = Field(default=None, max_length=2048)
    is_active: bool = True


class CameraRead(CameraCreate):
    id: int
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)


class CameraUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=200)
    location_id: Optional[int] = Field(default=None, gt=0)
    queue_id: Optional[int] = Field(default=None, gt=0)
    source_type: Optional[CameraSourceType] = None
    source_url: Optional[str] = Field(default=None, max_length=2048)
    is_active: Optional[bool] = None


class CameraObservationCreate(BaseModel):
    """The subset of a vision observation needed by the backend measurement service."""

    person_count: int = Field(ge=0)
    density: float = Field(ge=0, le=1)


class CameraFrameCreate(BaseModel):
    """A sampled JPEG data URL captured by an authenticated browser client."""

    frame_data: str = Field(min_length=32, max_length=5_000_000)


class CameraAnalysisRead(BaseModel):
    camera_id: int
    queue_id: int
    person_count: int
    density: float
    estimated_wait_time: float
    status: QueueStatus
    recorded_at: datetime
