"""API behavior tests using a temporary SQLite database."""

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models.location import Location


def create_location(session: Session) -> Location:
    location = Location(name="Test location")
    session.add(location)
    session.commit()
    session.refresh(location)
    return location


def test_health(client: TestClient) -> None:
    assert client.get("/api/health").json() == {"status": "ok", "service": "queueflow-backend"}


def test_api_allows_configured_frontend_origin(client: TestClient) -> None:
    response = client.get("/api/health", headers={"Origin": "http://localhost:5173"})
    assert response.headers["access-control-allow-origin"] == "http://localhost:5173"


def test_queue_crud(client: TestClient, session: Session) -> None:
    location = create_location(session)
    created = client.post("/api/queues", json={"name": "Security", "location_id": location.id, "capacity": 20})
    assert created.status_code == 201
    queue = created.json()
    assert queue["status"] == "NORMAL"

    listed = client.get("/api/queues")
    assert listed.status_code == 200
    assert [item["id"] for item in listed.json()] == [queue["id"]]

    fetched = client.get(f"/api/queues/{queue['id']}")
    assert fetched.status_code == 200
    assert fetched.json()["name"] == "Security"

    updated = client.put(f"/api/queues/{queue['id']}", json={"name": "Priority Security", "capacity": 30})
    assert updated.status_code == 200
    assert updated.json()["name"] == "Priority Security"

    deleted = client.delete(f"/api/queues/{queue['id']}")
    assert deleted.status_code == 204
    assert client.get(f"/api/queues/{queue['id']}").status_code == 404


def test_queue_validation_and_missing_location(client: TestClient) -> None:
    assert client.post("/api/queues", json={"name": "", "location_id": 1, "capacity": 0}).status_code == 422
    assert client.post("/api/queues", json={"name": "Security", "location_id": 999, "capacity": 10}).status_code == 404


def test_measurements_update_queue_and_preserve_closed_status(client: TestClient, session: Session) -> None:
    location = create_location(session)
    queue = client.post("/api/queues", json={"name": "Security", "location_id": location.id, "capacity": 20}).json()

    measurement = client.post(f"/api/queues/{queue['id']}/measurements", json={"person_count": 16, "density": 0.8})
    assert measurement.status_code == 201
    assert measurement.json()["estimated_wait_time"] == 8
    assert measurement.json()["status"] == "CROWDED"

    updated_queue = client.get(f"/api/queues/{queue['id']}").json()
    assert updated_queue["current_count"] == 16
    assert updated_queue["density"] == 0.8
    assert updated_queue["status"] == "CROWDED"
    assert len(client.get(f"/api/queues/{queue['id']}/measurements").json()) == 1

    client.put(f"/api/queues/{queue['id']}", json={"status": "CLOSED"})
    closed_measurement = client.post(f"/api/queues/{queue['id']}/measurements", json={"person_count": 20, "density": 1})
    assert closed_measurement.json()["status"] == "CLOSED"


def test_measurement_for_missing_queue_is_not_found(client: TestClient) -> None:
    assert client.post("/api/queues/999/measurements", json={"person_count": 1, "density": 0.1}).status_code == 404
