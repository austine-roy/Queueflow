"""Queue CRUD endpoints."""

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.location import Location
from app.models.queue import Queue
from app.schemas.queue import QueueCreate, QueueRead, QueueUpdate

router = APIRouter(prefix="/queues", tags=["Queues"])


def get_queue_or_404(session: Session, queue_id: int) -> Queue:
    queue = session.get(Queue, queue_id)
    if queue is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Queue not found")
    return queue


@router.get("", response_model=list[QueueRead], summary="List queues")
def list_queues(session: Session = Depends(get_db)) -> list[Queue]:
    return list(session.query(Queue).order_by(Queue.id).all())


@router.post("", response_model=QueueRead, status_code=status.HTTP_201_CREATED, summary="Create a queue")
def create_queue(payload: QueueCreate, session: Session = Depends(get_db)) -> Queue:
    if session.get(Location, payload.location_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Location not found")
    queue = Queue(**payload.model_dump())
    session.add(queue)
    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Could not create queue") from None
    session.refresh(queue)
    return queue


@router.get("/{queue_id}", response_model=QueueRead, summary="Get one queue")
def get_queue(queue_id: int, session: Session = Depends(get_db)) -> Queue:
    return get_queue_or_404(session, queue_id)


@router.put("/{queue_id}", response_model=QueueRead, summary="Update a queue")
def update_queue(queue_id: int, payload: QueueUpdate, session: Session = Depends(get_db)) -> Queue:
    queue = get_queue_or_404(session, queue_id)
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(queue, field, value)
    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Could not update queue") from None
    session.refresh(queue)
    return queue


@router.delete("/{queue_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete a queue")
def delete_queue(queue_id: int, session: Session = Depends(get_db)) -> Response:
    queue = get_queue_or_404(session, queue_id)
    session.delete(queue)
    session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
