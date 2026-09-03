"""Decode browser camera frames and count people with pre-trained YOLOv8."""

from __future__ import annotations

import base64

from app.core.config import get_settings


class CameraFrameAnalyzer:
    """CPU-only YOLOv8 person counter for sampled browser camera frames.

    The detector intentionally loads lazily: deployments that do not use live
    browser cameras do not pay the OpenCV startup cost.
    """

    def __init__(self) -> None:
        self._model: object | None = None

    def analyze(self, frame_data: str, capacity: int) -> tuple[int, float]:
        if capacity <= 0:
            raise ValueError("Queue capacity must be positive")
        encoded = frame_data.split(",", 1)[-1]
        try:
            raw = base64.b64decode(encoded, validate=True)
        except (ValueError, TypeError) as error:
            raise ValueError("Camera frame is invalid") from error
        if not raw:
            raise ValueError("Camera frame is empty")
        try:
            import cv2
            import numpy
            from ultralytics import YOLO
        except ImportError as error:  # pragma: no cover - deployment dependency
            raise RuntimeError("Camera analysis is unavailable") from error
        if self._model is None:
            self._model = YOLO(get_settings().yolo_model_path)
        frame = cv2.imdecode(numpy.frombuffer(raw, dtype=numpy.uint8), cv2.IMREAD_COLOR)
        if frame is None:
            raise ValueError("Camera frame could not be decoded")
        result = self._model.predict(frame, classes=[0], conf=get_settings().yolo_confidence, imgsz=640, verbose=False)[0]
        count = len(result.boxes)
        return count, min(1.0, count / capacity)


camera_frame_analyzer = CameraFrameAnalyzer()
