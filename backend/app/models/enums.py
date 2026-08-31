"""Database-backed enumerations for controlled QueueFlow states."""

from enum import Enum


class QueueStatus(str, Enum):
    NORMAL = "NORMAL"
    BUSY = "BUSY"
    CROWDED = "CROWDED"
    CRITICAL = "CRITICAL"
    CLOSED = "CLOSED"


class CameraSourceType(str, Enum):
    VIDEO_FILE = "VIDEO_FILE"
    RTSP = "RTSP"
    WEBCAM = "WEBCAM"
    SIMULATED = "SIMULATED"


class AlertSeverity(str, Enum):
    INFO = "INFO"
    WARNING = "WARNING"
    CRITICAL = "CRITICAL"


class UserRole(str, Enum):
    ADMIN = "admin"
    OPERATOR = "operator"
    VIEWER = "viewer"
