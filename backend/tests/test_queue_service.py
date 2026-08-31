"""Unit tests for reusable queue rules."""

import pytest
import time
from datetime import datetime, timedelta

from app.core.config import Settings
from app.models.enums import QueueStatus
from app.services.queue_service import calculate_status, estimate_wait_from_history, estimate_wait_time


@pytest.fixture()
def settings() -> Settings:
    return Settings(database_url="sqlite://")


@pytest.mark.parametrize(
    ("count", "expected"),
    [(0, QueueStatus.NORMAL), (49, QueueStatus.NORMAL), (50, QueueStatus.BUSY), (75, QueueStatus.CROWDED), (90, QueueStatus.CRITICAL)],
)
def test_calculate_status_from_capacity(count: int, expected: QueueStatus, settings: Settings) -> None:
    assert calculate_status(count, 100, False, settings) == expected


def test_closed_queue_remains_closed(settings: Settings) -> None:
    assert calculate_status(100, 100, True, settings) == QueueStatus.CLOSED


def test_estimate_wait_time() -> None:
    assert estimate_wait_time(12, 2) == 6
    assert estimate_wait_time(0, 2) == 0


def test_estimate_wait_time_rejects_invalid_service_rate() -> None:
    with pytest.raises(ValueError, match="greater than zero"):
        estimate_wait_time(12, 0)


def test_historical_wait_uses_observed_departure_rate() -> None:
    start = datetime(2026, 9, 1, 9, 0)
    observations = [(start, 20), (start + timedelta(minutes=5), 10), (start + timedelta(minutes=10), 4)]
    assert estimate_wait_from_history(4, 2, observations) == 2.5


def test_historical_wait_falls_back_without_a_departure_signal() -> None:
    start = datetime(2026, 9, 1, 9, 0)
    observations = [(start, 2), (start + timedelta(minutes=5), 4)]
    assert estimate_wait_from_history(4, 2, observations) == 2


def test_historical_wait_baseline() -> None:
    """Keep the pure queue-estimation hot path comfortably sub-second."""
    started = time.perf_counter()
    history = [(datetime(2026, 9, 1, 9, 0), 10)]
    for count in range(500):
        estimate_wait_from_history(count % 100, 12, history)
    assert time.perf_counter() - started < 1.0
