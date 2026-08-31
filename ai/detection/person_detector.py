"""Person detector contracts and an optional OpenCV baseline adapter."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol, Sequence


@dataclass(frozen=True)
class BoundingBox:
    """Pixel bounding box using top-left coordinates and positive dimensions."""

    x: float
    y: float
    width: float
    height: float

    @property
    def centroid(self) -> tuple[float, float]:
        return (self.x + self.width / 2, self.y + self.height / 2)


@dataclass(frozen=True)
class PersonDetection:
    box: BoundingBox
    confidence: float


class PersonDetector(Protocol):
    def detect(self, frame: object) -> Sequence[PersonDetection]: ...


class OpenCVHogPersonDetector:
    """CPU-only baseline detector; replace with a trained detector in production."""

    def __init__(self, hit_threshold: float = 0.0) -> None:
        try:
            import cv2
        except ImportError as error:  # pragma: no cover - depends on optional runtime extra
            raise RuntimeError("OpenCV is required for video analysis. Install ai/requirements.txt.") from error
        self.cv2 = cv2
        self.hit_threshold = hit_threshold
        self._hog = cv2.HOGDescriptor()
        self._hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

    def detect(self, frame: object) -> Sequence[PersonDetection]:
        boxes, weights = self._hog.detectMultiScale(frame, hitThreshold=self.hit_threshold)
        return [
            PersonDetection(BoundingBox(float(x), float(y), float(width), float(height)), float(weight))
            for (x, y, width, height), weight in zip(boxes, weights)
        ]
