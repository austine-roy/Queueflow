"""Camera configuration and AI-observation ingestion endpoints."""

from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.database import get_db
from app.api.dependencies import require_roles
from app.models.enums import UserRole
from app.models.camera import Camera
from app.models.location import Location
from app.models.queue import Queue
from app.realtime.publisher import publish_measurement
from app.realtime.websocket_manager import manager
from app.schemas.camera import CameraCreate, CameraObservationCreate, CameraRead, CameraUpdate
from app.services.measurement_service import record_measurement

router = APIRouter(prefix="/cameras", tags=["Cameras"])


def get_camera_or_404(session: Session, camera_id: int) -> Camera:
    camera = session.get(Camera, camera_id)
    if camera is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Camera not found")
    return camera


def validate_camera_assignment(session: Session, location_id: int, queue_id: int | None) -> None:
    if session.get(Location, location_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Location not found")
    if queue_id is not None:
        queue = session.get(Queue, queue_id)
        if queue is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Queue not found")
        if queue.location_id != location_id:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail="Camera queue must belong to its location")


@router.get("", response_model=list[CameraRead], summary="List configured cameras")
def list_cameras(
    location_id: Optional[int] = Query(default=None, gt=0),
    queue_id: Optional[int] = Query(default=None, gt=0),
    active: Optional[bool] = Query(default=None),
    session: Session = Depends(get_db),
    _: object = Depends(require_roles(UserRole.VIEWER, UserRole.OPERATOR, UserRole.ADMIN)),
) -> list[Camera]:
    query = session.query(Camera)
    if location_id is not None:
        query = query.filter(Camera.location_id == location_id)
    if queue_id is not None:
        query = query.filter(Camera.queue_id == queue_id)
    if active is not None:
        query = query.filter(Camera.is_active == active)
    return list(query.order_by(Camera.id).all())


@router.post("", response_model=CameraRead, status_code=status.HTTP_201_CREATED, summary="Configure a camera")
def create_camera(payload: CameraCreate, session: Session = Depends(get_db), _: object = Depends(require_roles(UserRole.ADMIN))) -> Camera:
    validate_camera_assignment(session, payload.location_id, payload.queue_id)
    camera = Camera(**payload.model_dump())
    session.add(camera)
    session.commit()
    session.refresh(camera)
    return camera


@router.get("/{camera_id}", response_model=CameraRead, summary="Get a camera")
def get_camera(camera_id: int, session: Session = Depends(get_db), _: object = Depends(require_roles(UserRole.VIEWER, UserRole.OPERATOR, UserRole.ADMIN))) -> Camera:
    return get_camera_or_404(session, camera_id)


@router.put("/{camera_id}", response_model=CameraRead, summary="Update a camera")
def update_camera(camera_id: int, payload: CameraUpdate, session: Session = Depends(get_db), _: object = Depends(require_roles(UserRole.ADMIN))) -> Camera:
    camera = get_camera_or_404(session, camera_id)
    changes = payload.model_dump(exclude_unset=True)
    location_id = changes.get("location_id", camera.location_id)
    queue_id = changes.get("queue_id", camera.queue_id)
    validate_camera_assignment(session, location_id, queue_id)
    for field, value in changes.items():
        setattr(camera, field, value)
    session.commit()
    session.refresh(camera)
    return camera


@router.post("/{camera_id}/observations", response_model=CameraRead, summary="Ingest an AI queue observation")
async def ingest_observation(camera_id: int, payload: CameraObservationCreate, session: Session = Depends(get_db), _: object = Depends(require_roles(UserRole.OPERATOR, UserRole.ADMIN))) -> CameraRead:
    """Persist a camera observation and deliver the resulting real-time events."""

    camera = get_camera_or_404(session, camera_id)
    if not camera.is_active:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Camera is inactive")
    if camera.queue_id is None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Camera is not assigned to a queue")
    queue = session.get(Queue, camera.queue_id)
    if queue is None:  # Defensive guard for a queue removed after camera configuration.
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Camera queue is unavailable")
    record = record_measurement(session, queue, payload, get_settings())
    await publish_measurement(record, manager)
    return CameraRead.model_validate(camera)
