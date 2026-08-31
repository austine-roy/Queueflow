from datetime import datetime, timezone

import pytest

from ai.analytics.measurements import QueueObservation, density_for_count
from ai.detection.person_detector import BoundingBox, PersonDetection
from ai.queue.region import QueueRegion
from ai.queue.video_pipeline import VideoQueueAnalyzer
from ai.tracking.centroid_tracker import CentroidTracker


def detection(x: float, y: float) -> PersonDetection:
    return PersonDetection(BoundingBox(x, y, 10, 10), confidence=0.9)


def test_tracker_preserves_identity_for_nearby_person() -> None:
    tracker = CentroidTracker(max_distance=20)
    first = tracker.update([detection(10, 10)])
    second = tracker.update([detection(14, 12)])
    assert first[0].track_id == second[0].track_id
    assert second[0].missed_frames == 0


def test_tracker_expires_missing_person() -> None:
    tracker = CentroidTracker(max_missed_frames=1)
    tracker.update([detection(10, 10)])
    assert len(tracker.update([])) == 1
    assert tracker.update([]) == []


def test_region_counts_only_tracked_people_inside_polygon() -> None:
    region = QueueRegion("Security", ((0, 0), (100, 0), (100, 100), (0, 100)))
    tracks = CentroidTracker().update([detection(10, 10), detection(150, 10)])
    assert region.count(tracks) == 1


def test_density_is_bounded_and_validated() -> None:
    assert density_for_count(15, 10) == 1.0
    assert density_for_count(3, 10) == 0.3
    with pytest.raises(ValueError):
        density_for_count(-1, 10)


def test_observation_records_measurement_fields() -> None:
    observation = QueueObservation("Security", 3, 0.3, datetime(2026, 9, 1, tzinfo=timezone.utc))
    assert observation.queue_name == "Security"
    assert observation.person_count == 3


def test_video_pipeline_counts_detection_inside_region_without_opencv() -> None:
    class FakeDetector:
        def detect(self, frame: object) -> list[PersonDetection]:
            return [detection(10, 10), detection(150, 10)]

    analyzer = VideoQueueAnalyzer(
        FakeDetector(),
        CentroidTracker(),
        QueueRegion("Security", ((0, 0), (100, 0), (100, 100), (0, 100))),
        capacity=10,
    )
    observation = analyzer.analyze_frame(object(), datetime(2026, 9, 1, tzinfo=timezone.utc))
    assert observation.person_count == 1
    assert observation.density == 0.1
