"""WebSocket manager, simulator bounds, and alert transition tests."""

import asyncio
import random

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import Settings
from app.models.location import Location
from app.models.queue import Queue
from app.realtime.simulator import SimulatorProvider
from app.realtime.websocket_manager import WebSocketManager, manager


class FakeSocket:
    def __init__(self) -> None:
        self.accepted = False
        self.events: list[dict] = []

    async def accept(self) -> None:
        self.accepted = True

    async def send_json(self, event: dict) -> None:
        self.events.append(event)


def test_connection_manager_broadcasts_to_multiple_clients() -> None:
    websocket_manager = WebSocketManager()
    first, second = FakeSocket(), FakeSocket()
    asyncio.run(websocket_manager.connect(first))
    asyncio.run(websocket_manager.connect(second))
    asyncio.run(websocket_manager.broadcast({"type": "queue_update"}))
    assert first.accepted and second.accepted
    assert first.events == second.events == [{"type": "queue_update"}]
    websocket_manager.disconnect(first)
    assert websocket_manager.active_connections == [second]


def test_websocket_endpoint_connects_and_disconnects(client: TestClient) -> None:
    with client.websocket_connect("/ws/queues") as websocket:
        assert len(manager.active_connections) == 1
    assert not manager.active_connections


def test_simulator_counts_stay_within_queue_capacity() -> None:
    settings = Settings(database_url="sqlite://", queueflow_simulation_interval=2, queueflow_simulation_arrival_rate=60, queueflow_simulation_service_rate=0)
    simulator = SimulatorProvider(settings, WebSocketManager(), random.Random(1))
    count = 0
    for _ in range(30):
        count = simulator.next_count(count, 5)
        assert 0 <= count <= 5


def test_alert_created_once_when_queue_enters_crowded(client: TestClient, session: Session) -> None:
    location = Location(name="Realtime test")
    session.add(location)
    session.commit(); session.refresh(location)
    queue = Queue(name="Queue", location_id=location.id, capacity=20, current_count=10)
    session.add(queue); session.commit(); session.refresh(queue)
    assert client.post(f"/api/queues/{queue.id}/measurements", json={"person_count": 16, "density": 0.8}).status_code == 201
    assert client.post(f"/api/queues/{queue.id}/measurements", json={"person_count": 17, "density": 0.85}).status_code == 201
    alerts = client.get("/api/alerts")
    assert alerts.status_code == 200
    assert len(alerts.json()) == 1
    assert alerts.json()[0]["type"] == "QUEUE_CROWDED"
