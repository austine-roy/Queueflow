"""Replaceable development queue-data provider; no camera or AI processing."""

import asyncio
import random
from abc import ABC, abstractmethod
from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import select

from app.core.config import Settings
from app.core.database import SessionLocal
from app.models.queue import Queue
from app.realtime.websocket_manager import WebSocketManager
from app.schemas.alert import AlertRead
from app.schemas.measurement import MeasurementCreate
from app.schemas.realtime import AlertEvent, QueueUpdateEvent, RealtimeQueue
from app.services.measurement_service import record_measurement


class QueueDataProvider(ABC):
    """Interface future AI providers will implement."""

    @abstractmethod
    async def run(self) -> None: ...


class SimulatorProvider(QueueDataProvider):
    def __init__(self, settings: Settings, websocket_manager: WebSocketManager, rng: Optional[random.Random] = None) -> None:
        self.settings, self.websocket_manager, self.rng = settings, websocket_manager, rng or random.Random()
        self._running = False

    def next_count(self, current: int, capacity: int) -> int:
        """Generate gradual independent arrivals/departures within valid bounds."""
        interval_minutes = self.settings.queueflow_simulation_interval / 60
        arrives = self.rng.random() < min(1, self.settings.queueflow_simulation_arrival_rate * interval_minutes)
        served = self.rng.random() < min(1, self.settings.queueflow_simulation_service_rate * interval_minutes)
        return max(0, min(capacity, current + int(arrives) - int(served)))

    async def update_once(self) -> None:
        with SessionLocal() as session:
            queues = list(session.scalars(select(Queue).where(Queue.status != "CLOSED")))
            for queue in queues:
                count = self.next_count(queue.current_count, queue.capacity)
                if count == queue.current_count:
                    continue
                result = record_measurement(session, queue, MeasurementCreate(person_count=count, density=count / queue.capacity), self.settings)
                event = QueueUpdateEvent(queue=RealtimeQueue(id=queue.id, name=queue.name, current_count=queue.current_count, density=queue.density, estimated_wait_time=queue.estimated_wait_time, status=queue.status, timestamp=datetime.now(timezone.utc)))
                await self.websocket_manager.broadcast(event.model_dump(mode="json"))
                if result.alert is not None:
                    await self.websocket_manager.broadcast(AlertEvent(alert=AlertRead.model_validate(result.alert)).model_dump(mode="json"))

    async def run(self) -> None:
        self._running = True
        while self._running:
            await self.update_once()
            await asyncio.sleep(self.settings.queueflow_simulation_interval)

    def stop(self) -> None:
        self._running = False
