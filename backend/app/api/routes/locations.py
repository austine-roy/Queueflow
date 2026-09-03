"""Read-only location data used by queue and camera setup."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies import require_roles
from app.core.database import get_db
from app.models.enums import UserRole
from app.models.location import Location
from app.schemas.location import LocationRead

router = APIRouter(prefix="/locations", tags=["Locations"])


@router.get("", response_model=list[LocationRead], summary="List locations")
def list_locations(session: Session = Depends(get_db), _: object = Depends(require_roles(UserRole.VIEWER, UserRole.OPERATOR, UserRole.ADMIN))) -> list[Location]:
    return list(session.query(Location).order_by(Location.id).all())
