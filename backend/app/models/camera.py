"""Camera configuration model; video processing is intentionally out of scope."""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, DateTime, Enum as SQLEnum, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.enums import CameraSourceType


class Camera(Base):
    __tablename__ = "cameras"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    location_id: Mapped[int] = mapped_column(ForeignKey("locations.id", ondelete="CASCADE"), nullable=False, index=True)
    queue_id: Mapped[Optional[int]] = mapped_column(ForeignKey("queues.id", ondelete="SET NULL"), nullable=True, index=True)
    source_type: Mapped[CameraSourceType] = mapped_column(SQLEnum(CameraSourceType, name="camera_source_type"), nullable=False)
    source_url: Mapped[Optional[str]] = mapped_column(String(2048), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    location: Mapped["Location"] = relationship(back_populates="cameras")
    queue: Mapped[Optional["Queue"]] = relationship(back_populates="cameras")
