"""Explicit, environment-driven initial-admin bootstrap command."""

from sqlalchemy import select

from app.core.config import get_settings
from app.core.database import SessionLocal
from app.models.enums import UserRole
from app.models.user import User
from app.services.auth_service import hash_password


def bootstrap_admin() -> None:
    settings = get_settings()
    if not settings.auth_bootstrap_admin_email or not settings.auth_bootstrap_admin_password:
        raise SystemExit("Set AUTH_BOOTSTRAP_ADMIN_EMAIL and AUTH_BOOTSTRAP_ADMIN_PASSWORD before running this command.")
    email = settings.auth_bootstrap_admin_email.lower()
    with SessionLocal() as session:
        if session.scalar(select(User).where(User.email == email)) is not None:
            print("Admin account already exists; no changes made.")
            return
        if session.scalar(select(User.id).limit(1)) is not None:
            raise SystemExit("Refusing bootstrap: accounts already exist. Use the admin user-management API instead.")
        session.add(User(email=email, password_hash=hash_password(settings.auth_bootstrap_admin_password.get_secret_value()), role=UserRole.ADMIN))
        session.commit()
    print("Initial admin account created.")


if __name__ == "__main__":
    bootstrap_admin()
