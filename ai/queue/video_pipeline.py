"""Video-file analysis orchestration; persistence is intentionally Milestone 6."""

from __future__ import annotations

from collections.abc import Iterator
from datetime import datetime, timezone
from pathlib import Path

from ai.analytics.measurements import QueueObservation, density_for_count
from ai.detection.person_detector import PersonDetector
from ai.queue.region import QueueRegion
from ai.tracking.centroid_tracker import CentroidTracker


class VideoQueueAnalyzer:
    """Sample a video stream and yield queue observations for each processed frame."""

    def __init__(self, detector: PersonDetector, tracker: CentroidTracker, region: QueueRegion, capacity: int, sample_every_frames: int = 5) -> None:
        if capacity <= 0 or sample_every_frames <= 0:
            raise ValueError("Capacity and sample interval must be positive.")
        self.detector = detector
        self.tracker = tracker
        self.region = region
        self.capacity = capacity
        self.sample_every_frames = sample_every_frames

    def analyze(self, source: str | Path) -> Iterator[QueueObservation]:
        try:
            import cv2
        except ImportError as error:  # pragma: no cover - depends on optional runtime extra
            raise RuntimeError("OpenCV is required for video analysis. Install ai/requirements.txt.") from error
        capture = cv2.VideoCapture(str(source))
        if not capture.isOpened():
            capture.release()
            raise ValueError(f"Unable to open video source: {source}")
        try:
            frame_number = 0
            while True:
                ok, frame = capture.read()
                if not ok:
                    break
                frame_number += 1
                if frame_number % self.sample_every_frames:
                    continue
                yield self.analyze_frame(frame)
        finally:
            capture.release()

    def analyze_frame(self, frame: object, observed_at: datetime | None = None) -> QueueObservation:
        """Analyze one decoded frame; useful for embedding and deterministic tests."""
        tracks = self.tracker.update(self.detector.detect(frame))
        count = self.region.count(tracks)
        return QueueObservation(
            self.region.name,
            count,
            density_for_count(count, self.capacity),
            observed_at or datetime.now(timezone.utc),
        )
