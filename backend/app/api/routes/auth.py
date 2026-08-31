"""Login, current-user, and account-management endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user, require_roles
from app.core.config import get_settings
from app.core.database import get_db
from app.models.enums import UserRole
from app.models.user import User
from app.schemas.auth import LoginRequest, TokenRead, UserCreate, UserRead, UserUpdate
from app.services.auth_service import create_access_token, hash_password, verify_password

router = APIRouter(prefix="/auth", tags=["Authentication"])
users_router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/login", response_model=TokenRead, summary="Log in")
def login(payload: LoginRequest, session: Session = Depends(get_db)) -> TokenRead:
    user = session.query(User).filter(User.email == payload.email.lower()).one_or_none()
    if user is None or not user.is_active or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password", headers={"WWW-Authenticate": "Bearer"})
    return TokenRead(access_token=create_access_token(user.id, user.role, get_settings()), user=UserRead.model_validate(user))


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT, summary="Log out")
def logout(_: User = Depends(get_current_user)) -> None:
    """JWTs are stateless; the client removes its in-memory token."""


@router.get("/me", response_model=UserRead, summary="Get the current account")
def me(user: User = Depends(get_current_user)) -> User:
    return user


@users_router.get("", response_model=list[UserRead], summary="List accounts")
def list_users(session: Session = Depends(get_db), _: User = Depends(require_roles(UserRole.ADMIN))) -> list[User]:
    return list(session.query(User).order_by(User.id).all())


@users_router.post("", response_model=UserRead, status_code=status.HTTP_201_CREATED, summary="Create an account")
def create_user(payload: UserCreate, session: Session = Depends(get_db), _: User = Depends(require_roles(UserRole.ADMIN))) -> User:
    if session.query(User).filter(User.email == payload.email.lower()).first() is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email is already registered")
    user = User(email=payload.email.lower(), password_hash=hash_password(payload.password), role=payload.role)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@users_router.put("/{user_id}", response_model=UserRead, summary="Update an account")
def update_user(user_id: int, payload: UserUpdate, session: Session = Depends(get_db), _: User = Depends(require_roles(UserRole.ADMIN))) -> User:
    user = session.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(user, field, value)
    session.commit()
    session.refresh(user)
    return user
