"""Historical queue measurement model."""

from datetime import datetime

from sqlalchemy import DateTime, Enum as SQLEnum, Float, ForeignKey, Integer, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.enums import QueueStatus


class QueueMeasurement(Base):
    __tablename__ = "queue_measurements"

    id: Mapped[int] = mapped_column(primary_key=True)
    queue_id: Mapped[int] = mapped_column(ForeignKey("queues.id", ondelete="CASCADE"), nullable=False, index=True)
    person_count: Mapped[int] = mapped_column(Integer, nullable=False)
    density: Mapped[float] = mapped_column(Float, nullable=False)
    estimated_wait_time: Mapped[float] = mapped_column(Float, nullable=False)
    status: Mapped[QueueStatus] = mapped_column(SQLEnum(QueueStatus, name="queue_status", create_type=False), nullable=False)
    recorded_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False, index=True)

    queue: Mapped["Queue"] = relationship(back_populates="measurements")
