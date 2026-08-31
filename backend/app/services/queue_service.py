"""Shared queue business rules."""

from datetime import datetime
from typing import Sequence

from app.core.config import Settings
from app.models.enums import QueueStatus


def calculate_status(current_count: int, capacity: int, is_closed: bool, settings: Settings) -> QueueStatus:
    """Calculate a capacity-based status, preserving an explicitly closed queue."""

    if is_closed:
        return QueueStatus.CLOSED
    ratio = current_count / capacity
    if ratio >= settings.critical_threshold:
        return QueueStatus.CRITICAL
    if ratio >= settings.crowded_threshold:
        return QueueStatus.CROWDED
    if ratio >= settings.busy_threshold:
        return QueueStatus.BUSY
    return QueueStatus.NORMAL


def estimate_wait_time(current_count: int, service_rate_per_minute: float) -> float:
    """Estimate wait in minutes from throughput; this is not an ML prediction."""

    if service_rate_per_minute <= 0:
        raise ValueError("service_rate_per_minute must be greater than zero")
    if current_count < 0:
        raise ValueError("current_count cannot be negative")
    return current_count / service_rate_per_minute


def estimate_wait_from_history(
    current_count: int,
    default_service_rate_per_minute: float,
    observations: Sequence[tuple[datetime, int]],
) -> float:
    """Use observed queue decreases as a service-rate signal, with a safe fallback."""

    service_rates: list[float] = []
    for (earlier_time, earlier_count), (later_time, later_count) in zip(observations, observations[1:]):
        elapsed_minutes = (later_time - earlier_time).total_seconds() / 60
        served = earlier_count - later_count
        if elapsed_minutes > 0 and served > 0:
            service_rates.append(served / elapsed_minutes)
    service_rate = sum(service_rates) / len(service_rates) if service_rates else default_service_rate_per_minute
    return estimate_wait_time(current_count, service_rate)
