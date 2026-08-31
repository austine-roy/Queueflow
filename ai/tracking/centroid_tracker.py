"""Deterministic centroid tracker suitable for a replaceable baseline."""

from __future__ import annotations

from dataclasses import dataclass
from math import hypot
from typing import Sequence

from ai.detection.person_detector import PersonDetection


@dataclass(frozen=True)
class TrackedPerson:
    track_id: int
    detection: PersonDetection
    missed_frames: int = 0

    @property
    def centroid(self) -> tuple[float, float]:
        return self.detection.box.centroid


class CentroidTracker:
    """Associate nearest detections while bounding lost-track lifetime."""

    def __init__(self, max_distance: float = 80, max_missed_frames: int = 5) -> None:
        if max_distance <= 0 or max_missed_frames < 0:
            raise ValueError("Tracker limits must be positive (or zero for missed frames).")
        self.max_distance = max_distance
        self.max_missed_frames = max_missed_frames
        self._next_track_id = 1
        self._tracks: dict[int, TrackedPerson] = {}

    def update(self, detections: Sequence[PersonDetection]) -> list[TrackedPerson]:
        unmatched_tracks = set(self._tracks)
        unmatched_detections = set(range(len(detections)))
        candidates: list[tuple[float, int, int]] = []
        for track_id, track in self._tracks.items():
            for index, detection in enumerate(detections):
                candidates.append((hypot(track.centroid[0] - detection.box.centroid[0], track.centroid[1] - detection.box.centroid[1]), track_id, index))
        for distance, track_id, index in sorted(candidates):
            if distance > self.max_distance or track_id not in unmatched_tracks or index not in unmatched_detections:
                continue
            self._tracks[track_id] = TrackedPerson(track_id, detections[index])
            unmatched_tracks.remove(track_id)
            unmatched_detections.remove(index)
        for track_id in unmatched_tracks:
            previous = self._tracks[track_id]
            missed = previous.missed_frames + 1
            if missed > self.max_missed_frames:
                del self._tracks[track_id]
            else:
                self._tracks[track_id] = TrackedPerson(track_id, previous.detection, missed)
        for index in unmatched_detections:
            track = TrackedPerson(self._next_track_id, detections[index])
            self._tracks[track.track_id] = track
            self._next_track_id += 1
        return list(sorted(self._tracks.values(), key=lambda track: track.track_id))
