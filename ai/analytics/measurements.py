"""Validated measurement values produced by the vision pipeline."""

from dataclasses import dataclass
from datetime import datetime


def density_for_count(person_count: int, capacity: int) -> float:
    if person_count < 0 or capacity <= 0:
        raise ValueError("Person count must be non-negative and capacity must be positive.")
    return min(1.0, person_count / capacity)


@dataclass(frozen=True)
class QueueObservation:
    queue_name: str
    person_count: int
    density: float
    observed_at: datetime
