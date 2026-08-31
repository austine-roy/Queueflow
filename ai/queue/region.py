"""Polygon queue regions independent of any camera implementation."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

from ai.tracking.centroid_tracker import TrackedPerson

Point = tuple[float, float]


@dataclass(frozen=True)
class QueueRegion:
    name: str
    points: tuple[Point, ...]

    def __post_init__(self) -> None:
        if len(self.points) < 3:
            raise ValueError("A queue region needs at least three points.")

    def contains(self, point: Point) -> bool:
        """Return whether a point falls in the polygon using ray casting."""
        x, y = point
        inside = False
        previous_x, previous_y = self.points[-1]
        for current_x, current_y in self.points:
            crosses = (current_y > y) != (previous_y > y)
            if crosses and x < (previous_x - current_x) * (y - current_y) / (previous_y - current_y) + current_x:
                inside = not inside
            previous_x, previous_y = current_x, current_y
        return inside

    def count(self, tracks: Sequence[TrackedPerson]) -> int:
        return sum(track.missed_frames == 0 and self.contains(track.centroid) for track in tracks)
