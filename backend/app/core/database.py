"""SQLAlchemy engine and request-session dependencies."""

from __future__ import annotations

from collections.abc import Generator
from typing import Optional

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.core.config import get_settings


class Base(DeclarativeBase):
    """Base class for QueueFlow persistence models."""


def build_engine(database_url: Optional[str] = None):
    """Create a synchronous database engine for the configured database."""

    return create_engine(database_url or get_settings().database_url, pool_pre_ping=True)


engine = build_engine()
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


def get_db() -> Generator[Session, None, None]:
    """Yield a database session and always close it after the request."""

    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
