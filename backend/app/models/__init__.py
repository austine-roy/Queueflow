"""Import models so SQLAlchemy and Alembic discover all metadata."""

from app.models.alert import Alert
from app.models.camera import Camera
from app.models.location import Location
from app.models.measurement import QueueMeasurement
from app.models.queue import Queue

__all__ = ["Alert", "Camera", "Location", "Queue", "QueueMeasurement"]
