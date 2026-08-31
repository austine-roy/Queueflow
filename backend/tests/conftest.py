"""Isolated SQLite configuration for backend tests."""

import os

os.environ["DATABASE_URL"] = "sqlite://"
os.environ["AUTH_SECRET_KEY"] = "test-auth-secret-key-that-is-at-least-32-characters"

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.database import Base, get_db
from app.core.config import get_settings
from app.main import app
from app.models.enums import UserRole
from app.models.user import User
from app.services.auth_service import create_access_token, hash_password


@pytest.fixture()
def session():
    engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    Base.metadata.create_all(engine)
    testing_session = sessionmaker(bind=engine, autocommit=False, autoflush=False)
    with testing_session() as database_session:
        yield database_session
    Base.metadata.drop_all(engine)


@pytest.fixture()
def client(session):
    def override_get_db():
        yield session

    admin = User(email="admin@example.com", password_hash=hash_password("CorrectHorseBatteryStaple!"), role=UserRole.ADMIN)
    session.add(admin)
    session.commit()
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        test_client.headers.update({"Authorization": f"Bearer {create_access_token(admin.id, admin.role, get_settings())}"})
        yield test_client
    app.dependency_overrides.clear()
