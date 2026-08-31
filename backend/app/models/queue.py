"""Queue persistence model."""

from datetime import datetime

from sqlalchemy import DateTime, Enum as SQLEnum, Float, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.enums import QueueStatus


class Queue(Base):
    __tablename__ = "queues"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    location_id: Mapped[int] = mapped_column(ForeignKey("locations.id", ondelete="CASCADE"), nullable=False, index=True)
    capacity: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[QueueStatus] = mapped_column(SQLEnum(QueueStatus, name="queue_status"), default=QueueStatus.NORMAL, nullable=False)
    current_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    estimated_wait_time: Mapped[float] = mapped_column(Float, default=0, nullable=False)
    density: Mapped[float] = mapped_column(Float, default=0, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    location: Mapped["Location"] = relationship(back_populates="queues")
    cameras: Mapped[list["Camera"]] = relationship(back_populates="queue")
    measurements: Mapped[list["QueueMeasurement"]] = relationship(back_populates="queue", cascade="all, delete-orphan")
    alerts: Mapped[list["Alert"]] = relationship(back_populates="queue", cascade="all, delete-orphan")
