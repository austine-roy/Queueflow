"""Authentication and role-based access-control tests."""

import pytest
from fastapi.testclient import TestClient
from starlette.websockets import WebSocketDisconnect
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.models.enums import UserRole
from app.models.location import Location
from app.models.user import User
from app.services.auth_service import create_access_token, hash_password


def authorization_for(user: User) -> dict[str, str]:
    token = create_access_token(user.id, user.role, get_settings())
    return {"Authorization": f"Bearer {token}"}


def add_user(session: Session, email: str, role: UserRole) -> User:
    user = User(email=email, password_hash=hash_password("CorrectHorseBatteryStaple!"), role=role)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def test_login_me_logout_and_invalid_credentials(client: TestClient) -> None:
    response = client.post("/api/auth/login", json={"email": "admin@example.com", "password": "CorrectHorseBatteryStaple!"})
    assert response.status_code == 200
    body = response.json()
    assert body["token_type"] == "bearer"
    assert body["user"]["role"] == "admin"
    assert "password" not in body["user"]

    headers = {"Authorization": f"Bearer {body['access_token']}"}
    assert client.get("/api/auth/me", headers=headers).json()["email"] == "admin@example.com"
    assert client.post("/api/auth/logout", headers=headers).status_code == 204

    invalid = client.post("/api/auth/login", json={"email": "admin@example.com", "password": "wrong-password"})
    assert invalid.status_code == 401
    assert invalid.json()["detail"] == "Invalid email or password"


def test_protected_endpoint_requires_a_valid_token(client: TestClient) -> None:
    authorization = client.headers.pop("authorization")
    response = client.get("/api/queues")
    client.headers["authorization"] = authorization
    assert response.status_code == 401
    assert response.json()["detail"] == "Authentication required"
    assert response.headers["www-authenticate"] == "Bearer"


def test_cors_allows_bearer_authorization_header(client: TestClient) -> None:
    response = client.options(
        "/api/queues",
        headers={
            "Origin": "http://localhost:5173",
            "Access-Control-Request-Method": "GET",
            "Access-Control-Request-Headers": "authorization",
        },
    )
    assert response.status_code == 200
    assert "authorization" in response.headers["access-control-allow-headers"].lower()


def test_roles_enforce_read_and_operational_permissions(client: TestClient, session: Session) -> None:
    viewer = add_user(session, "viewer@example.com", UserRole.VIEWER)
    operator = add_user(session, "operator@example.com", UserRole.OPERATOR)
    location = Location(name="Test location")
    session.add(location)
    session.commit()
    session.refresh(location)

    admin_queue = client.post("/api/queues", json={"name": "Security", "location_id": location.id, "capacity": 20})
    assert admin_queue.status_code == 201
    queue_id = admin_queue.json()["id"]

    viewer_headers = authorization_for(viewer)
    operator_headers = authorization_for(operator)
    assert client.get("/api/queues", headers=viewer_headers).status_code == 200
    assert client.get("/api/analytics/queues", headers=viewer_headers).status_code == 200
    assert client.post("/api/queues", headers=viewer_headers, json={"name": "Blocked", "location_id": location.id, "capacity": 10}).status_code == 403
    assert client.post("/api/queues", headers=operator_headers, json={"name": "Blocked", "location_id": location.id, "capacity": 10}).status_code == 403
    assert client.post(f"/api/queues/{queue_id}/measurements", headers=viewer_headers, json={"person_count": 3, "density": 0.2}).status_code == 403
    assert client.post(f"/api/queues/{queue_id}/measurements", headers=operator_headers, json={"person_count": 3, "density": 0.2}).status_code == 201
    assert client.get("/api/users", headers=viewer_headers).status_code == 403


def test_websocket_requires_subprotocol_token_and_accepts_authorized_roles(client: TestClient, session: Session) -> None:
    viewer = add_user(session, "viewer@example.com", UserRole.VIEWER)
    with pytest.raises(WebSocketDisconnect) as disconnected:
        with client.websocket_connect("/ws/queues"):
            pass
    assert disconnected.value.code == 4401

    token = create_access_token(viewer.id, viewer.role, get_settings())
    with client.websocket_connect("/ws/queues", subprotocols=[f"queueflow.jwt.{token}"]) as websocket:
        assert websocket.accepted_subprotocol == f"queueflow.jwt.{token}"
