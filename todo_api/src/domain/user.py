"""User entity - SQLModel database model."""

from datetime import datetime, timezone

from sqlmodel import SQLModel, Field


def _utc_now() -> datetime:
    """Return current UTC time as timezone-aware datetime."""
    return datetime.now(timezone.utc)


class User(SQLModel, table=True):
    """User entity representing a registered user.

    Attributes:
        id: Primary key, auto-incremented.
        email: Unique email address.
        password_hash: Bcrypt hashed password.
        created_at: Timestamp of creation.
        updated_at: Timestamp of last update.
    """

    __tablename__ = "users"

    id: int | None = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True, max_length=255)
    password_hash: str = Field(max_length=255)
    created_at: datetime = Field(default_factory=_utc_now)
    updated_at: datetime = Field(default_factory=_utc_now)
