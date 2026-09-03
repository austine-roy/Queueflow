"""API behavior tests using a temporary SQLite database."""

import json
import logging
import time
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models.location import Location
from app.core.config import get_settings
from app.core.database import get_db
from app.main import app


def create_location(session: Session) -> Location:
    location = Location(name="Test location")
    session.add(location)
    session.commit()
    session.refresh(location)
    return location


def test_health(client: TestClient) -> None:
    assert client.get("/api/health").json() == {"status": "ok", "service": "queueflow-backend"}


def test_readiness_and_metrics(client: TestClient) -> None:
    assert client.get("/api/ready").json() == {"status": "ready", "database": "ok"}
    metrics = client.get("/api/metrics")
    assert metrics.status_code == 200
    assert metrics.headers["content-type"].startswith("text/plain; version=0.0.4")
    assert "queueflow_http_requests_total" in metrics.text
    assert "queueflow_websocket_connections_active" in metrics.text


def test_readiness_returns_503_when_database_is_unavailable(client: TestClient) -> None:
    class BrokenSession:
        def execute(self, _statement):
            raise RuntimeError("database unavailable")

    def broken_database():
        yield BrokenSession()

    app.dependency_overrides[get_db] = broken_database
    response = client.get("/api/ready")
    app.dependency_overrides.pop(get_db)
    assert response.status_code == 503
    assert response.json()["detail"] == "Database unavailable"


def test_request_logging_and_request_ids_are_safe(client: TestClient, caplog: pytest.LogCaptureFixture) -> None:
    logging.getLogger("queueflow").propagate = True
    caplog.set_level("INFO", logger="queueflow")
    response = client.post("/api/auth/login", headers={"X-Request-ID": "request-123", "Authorization": "Bearer private-token"}, json={"email": "admin@example.com", "password": "CorrectHorseBatteryStaple!"})
    assert response.headers["x-request-id"] == "request-123"
    records = "\n".join(record.message for record in caplog.records)
    complete = next(json.loads(record.message) for record in caplog.records if '"event":"request_complete"' in record.message)
    assert complete["request_id"] == "request-123"
    assert complete["path"] == "/api/auth/login"
    assert "CorrectHorseBatteryStaple!" not in records
    assert "private-token" not in records
    assert "Authorization" not in records
    logging.getLogger("queueflow").propagate = False


def test_api_allows_configured_frontend_origin(client: TestClient) -> None:
    origin = get_settings().frontend_origin
    response = client.get("/api/health", headers={"Origin": origin})
    assert response.headers["access-control-allow-origin"] == origin


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


def test_locations_are_available_for_queue_setup(client: TestClient, session: Session) -> None:
    location = create_location(session)
    response = client.get("/api/locations")
    assert response.status_code == 200
    assert response.json()[0]["id"] == location.id
    assert response.json()[0]["name"] == "Test location"


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


def test_camera_configuration_and_observation_ingestion(client: TestClient, session: Session) -> None:
    location = create_location(session)
    queue = client.post("/api/queues", json={"name": "Security", "location_id": location.id, "capacity": 20}).json()
    camera = client.post("/api/cameras", json={"name": "Entrance", "location_id": location.id, "queue_id": queue["id"], "source_type": "VIDEO_FILE", "source_url": "entrance.mp4"})
    assert camera.status_code == 201

    observation = client.post(f"/api/cameras/{camera.json()['id']}/observations", json={"person_count": 16, "density": 0.8})
    assert observation.status_code == 200
    assert client.get(f"/api/queues/{queue['id']}").json()["status"] == "CROWDED"
    assert len(client.get(f"/api/queues/{queue['id']}/measurements").json()) == 1


def test_browser_camera_frame_analysis_persists_and_publishes_observation(client: TestClient, session: Session, monkeypatch: pytest.MonkeyPatch) -> None:
    location = create_location(session)
    queue = client.post("/api/queues", json={"name": "Live vision", "location_id": location.id, "capacity": 20}).json()
    camera = client.post("/api/cameras", json={"name": "Browser camera", "location_id": location.id, "queue_id": queue["id"], "source_type": "WEBCAM"}).json()
    monkeypatch.setattr("app.api.routes.cameras.camera_frame_analyzer.analyze", lambda _frame, _capacity: (8, 0.4))

    response = client.post(f"/api/cameras/{camera['id']}/analyze-frame", json={"frame_data": "data:image/jpeg;base64,ZmFrZS1mcmFtZS1kYXRh"})
    assert response.status_code == 200
    assert response.json()["person_count"] == 8
    assert response.json()["density"] == 0.4
    assert response.json()["estimated_wait_time"] == 4
    assert response.json()["status"] == "NORMAL"
    updated_queue = client.get(f"/api/queues/{queue['id']}").json()
    assert updated_queue["current_count"] == 8
    assert len(client.get(f"/api/queues/{queue['id']}/measurements").json()) == 1


def test_observation_ingestion_baseline_preserves_every_measurement(client: TestClient, session: Session) -> None:
    """A controlled single-worker baseline; production workers submit independently."""
    location = create_location(session)
    queue = client.post("/api/queues", json={"name": "Throughput", "location_id": location.id, "capacity": 100}).json()
    camera = client.post("/api/cameras", json={"name": "Throughput camera", "location_id": location.id, "queue_id": queue["id"], "source_type": "VIDEO_FILE"}).json()
    started = time.perf_counter()
    for count in range(20):
        assert client.post(f"/api/cameras/{camera['id']}/observations", json={"person_count": count, "density": 0.1}).status_code == 200
    elapsed = time.perf_counter() - started
    assert len(client.get(f"/api/queues/{queue['id']}/measurements").json()) == 20
    assert client.get(f"/api/queues/{queue['id']}").json()["current_count"] == 19
    assert elapsed < 5.0


def test_camera_observation_requires_active_queue_assignment(client: TestClient, session: Session) -> None:
    location = create_location(session)
    camera = client.post("/api/cameras", json={"name": "Unassigned", "location_id": location.id, "source_type": "VIDEO_FILE"}).json()
    assert client.post(f"/api/cameras/{camera['id']}/observations", json={"person_count": 1, "density": 0.1}).status_code == 409
    client.put(f"/api/cameras/{camera['id']}", json={"is_active": False})
    assert client.post(f"/api/cameras/{camera['id']}/observations", json={"person_count": 1, "density": 0.1}).status_code == 409


def test_camera_rejects_queue_from_another_location(client: TestClient, session: Session) -> None:
    first, second = create_location(session), create_location(session)
    queue = client.post("/api/queues", json={"name": "Security", "location_id": first.id, "capacity": 20}).json()
    response = client.post("/api/cameras", json={"name": "Entrance", "location_id": second.id, "queue_id": queue["id"], "source_type": "VIDEO_FILE"})
    assert response.status_code == 422


def test_alert_lifecycle_and_filters(client: TestClient, session: Session) -> None:
    location = create_location(session)
    queue = client.post("/api/queues", json={"name": "Security", "location_id": location.id, "capacity": 20}).json()
    client.post(f"/api/queues/{queue['id']}/measurements", json={"person_count": 16, "density": 0.8})
    active = client.get("/api/alerts?active=true&queue_id=" + str(queue["id"])).json()
    assert len(active) == 1
    resolved = client.post(f"/api/alerts/{active[0]['id']}/resolve")
    assert resolved.status_code == 200
    assert resolved.json()["is_active"] is False
    assert len(client.get("/api/alerts?active=true").json()) == 0
    assert len(client.get("/api/alerts?active=false").json()) == 1


def test_queue_recovery_resolves_active_transition_alert(client: TestClient, session: Session) -> None:
    location = create_location(session)
    queue = client.post("/api/queues", json={"name": "Security", "location_id": location.id, "capacity": 20}).json()
    client.post(f"/api/queues/{queue['id']}/measurements", json={"person_count": 16, "density": 0.8})
    client.post(f"/api/queues/{queue['id']}/measurements", json={"person_count": 4, "density": 0.2})
    assert len(client.get("/api/alerts?active=true").json()) == 0
    resolved = client.get("/api/alerts?active=false").json()
    assert len(resolved) == 1
    assert resolved[0]["resolved_at"] is not None


def test_analytics_returns_persisted_history(client: TestClient, session: Session) -> None:
    location = create_location(session)
    queue = client.post("/api/queues", json={"name": "Security", "location_id": location.id, "capacity": 20}).json()
    client.post(f"/api/queues/{queue['id']}/measurements", json={"person_count": 4, "density": 0.2})
    client.post(f"/api/queues/{queue['id']}/measurements", json={"person_count": 8, "density": 0.4})
    response = client.get("/api/analytics/queues")
    assert response.status_code == 200
    analytics = response.json()[0]
    assert analytics["queue_name"] == "Security"
    assert analytics["measurement_count"] == 2
    assert analytics["peak_person_count"] == 8
    assert len(analytics["measurements"]) == 2


def test_analytics_limits_history_in_database_while_preserving_total_count(client: TestClient, session: Session) -> None:
    location = create_location(session)
    queue = client.post("/api/queues", json={"name": "History", "location_id": location.id, "capacity": 100}).json()
    for count in range(6):
        assert client.post(f"/api/queues/{queue['id']}/measurements", json={"person_count": count, "density": 0.1}).status_code == 201
    analytics = client.get("/api/analytics/queues?measurement_limit=2").json()[0]
    assert analytics["measurement_count"] == 6
    assert len(analytics["measurements"]) == 2
    assert [item["person_count"] for item in analytics["measurements"]] == [4, 5]


def test_queue_prediction_uses_history_and_has_a_safe_fallback(client: TestClient, session: Session) -> None:
    location = create_location(session)
    queue = client.post("/api/queues", json={"name": "Forecast", "location_id": location.id, "capacity": 100}).json()

    fallback = client.get(f"/api/analytics/queues/{queue['id']}/prediction")
    assert fallback.status_code == 200
    assert fallback.json() == {
        "queue_id": queue["id"],
        "predicted_count": 0,
        "model": "insufficient_history",
        "measurement_count": 0,
    }

    for count in (2, 4, 6, 8, 10):
        assert client.post(f"/api/queues/{queue['id']}/measurements", json={"person_count": count, "density": 0.2}).status_code == 201
    prediction = client.get(f"/api/analytics/queues/{queue['id']}/prediction")
    assert prediction.status_code == 200
    assert prediction.json()["model"] == "random_forest"
    assert prediction.json()["measurement_count"] == 5
    assert isinstance(prediction.json()["predicted_count"], int)
    assert prediction.json()["predicted_count"] >= 0


def test_camera_list_can_filter_by_queue_and_active_state(client: TestClient, session: Session) -> None:
    location = create_location(session)
    queue = client.post("/api/queues", json={"name": "Security", "location_id": location.id, "capacity": 20}).json()
    active = client.post("/api/cameras", json={"name": "Active", "location_id": location.id, "queue_id": queue["id"], "source_type": "VIDEO_FILE"}).json()
    client.post("/api/cameras", json={"name": "Inactive", "location_id": location.id, "queue_id": queue["id"], "source_type": "VIDEO_FILE", "is_active": False})
    assert [item["id"] for item in client.get(f"/api/cameras?queue_id={queue['id']}&active=true").json()] == [active["id"]]
