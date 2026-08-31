"""Explicit development-only seed command."""

from sqlalchemy import select

from app.core.database import SessionLocal
from app.models.camera import Camera
from app.models.enums import CameraSourceType
from app.models.location import Location
from app.models.queue import Queue


def seed_development_data() -> None:
    """Create repeatable example data without modifying existing production data."""

    with SessionLocal() as session:
        location = session.scalar(select(Location).where(Location.name == "Demo Terminal"))
        if location is None:
            location = Location(name="Demo Terminal", description="Development-only example location")
            session.add(location)
            session.flush()
        queues = list(session.scalars(select(Queue).where(Queue.location_id == location.id)))
        if not queues:
            queues = [
                Queue(name="Security Check", location_id=location.id, capacity=40),
                Queue(name="Ticket Counter", location_id=location.id, capacity=25),
            ]
            session.add_all(queues)
            session.flush()
        camera_exists = session.scalar(select(Camera).where(Camera.name == "Demo Simulated Camera"))
        if camera_exists is None:
            session.add(Camera(name="Demo Simulated Camera", location_id=location.id, queue_id=queues[0].id, source_type=CameraSourceType.SIMULATED))
        session.commit()


if __name__ == "__main__":
    seed_development_data()
    print("Development seed data is ready.")
