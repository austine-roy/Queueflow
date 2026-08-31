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
from app.services.measurement_service import record_measurement
from app.realtime.publisher import publish_measurement
from app.schemas.measurement import MeasurementCreate


class FakeSocket:
    def __init__(self) -> None:
        self.accepted = False
        self.events: list[dict] = []

    async def accept(self) -> None:
        self.accepted = True

    async def send_json(self, event: dict) -> None:
        self.events.append(event)


class FailingSocket(FakeSocket):
    async def send_json(self, event: dict) -> None:
        raise RuntimeError("connection is closed")


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


def test_connection_manager_removes_failed_client() -> None:
    websocket_manager = WebSocketManager()
    healthy, failed = FakeSocket(), FailingSocket()
    asyncio.run(websocket_manager.connect(healthy))
    asyncio.run(websocket_manager.connect(failed))
    asyncio.run(websocket_manager.broadcast({"type": "queue_update"}))
    assert websocket_manager.active_connections == [healthy]
    assert healthy.events == [{"type": "queue_update"}]


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


def test_publisher_sends_queue_and_transition_alert(session: Session) -> None:
    location = Location(name="Publisher test")
    session.add(location)
    session.commit(); session.refresh(location)
    queue = Queue(name="Queue", location_id=location.id, capacity=20, current_count=10)
    session.add(queue); session.commit(); session.refresh(queue)
    settings = Settings(database_url="sqlite://")
    record = record_measurement(session, queue, MeasurementCreate(person_count=16, density=0.8), settings)
    websocket_manager = WebSocketManager()
    socket = FakeSocket()
    asyncio.run(websocket_manager.connect(socket))
    asyncio.run(publish_measurement(record, websocket_manager))
    assert [event["type"] for event in socket.events] == ["queue_update", "alert"]
    assert socket.events[0]["queue"]["current_count"] == 16


def test_camera_observation_broadcasts_queue_update(client: TestClient, session: Session) -> None:
    location = Location(name="Camera broadcast")
    session.add(location)
    session.commit(); session.refresh(location)
    queue = Queue(name="Queue", location_id=location.id, capacity=20)
    session.add(queue); session.commit(); session.refresh(queue)
    camera = client.post("/api/cameras", json={"name": "Entrance", "location_id": location.id, "queue_id": queue.id, "source_type": "VIDEO_FILE"}).json()
    with client.websocket_connect("/ws/queues") as websocket:
        response = client.post(f"/api/cameras/{camera['id']}/observations", json={"person_count": 5, "density": 0.25})
        assert response.status_code == 200
        event = websocket.receive_json()
    assert event["type"] == "queue_update"
    assert event["queue"]["id"] == queue.id
    assert event["queue"]["current_count"] == 5
