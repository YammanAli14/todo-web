"""Task entity - SQLModel database model."""

from datetime import datetime, timezone

from sqlmodel import SQLModel, Field


def _utc_now() -> datetime:
    """Return current UTC time as timezone-aware datetime."""
    return datetime.now(timezone.utc)


class Task(SQLModel, table=True):
    """Task entity representing a todo item.

    Attributes:
        id: Primary key, auto-incremented.
        title: Task description, max 200 characters.
        is_complete: Completion status, defaults to False.
        user_id: Foreign key to the owning user.
        created_at: Timestamp of creation.
        updated_at: Timestamp of last update.
    """

    __tablename__ = "tasks"

    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(max_length=200)
    is_complete: bool = Field(default=False)
    user_id: int = Field(foreign_key="users.id", index=True)
    created_at: datetime = Field(default_factory=_utc_now)
    updated_at: datetime = Field(default_factory=_utc_now)
