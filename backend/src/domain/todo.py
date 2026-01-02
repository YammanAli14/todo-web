"""Todo domain entity."""
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional


class Todo(SQLModel, table=True):
    """
    Todo entity for task management.

    Attributes:
        id: Primary key
        user_id: Foreign key to user (owner)
        title: Todo title/description
        is_complete: Completion status
        created_at: Timestamp when todo was created
        updated_at: Timestamp when todo was last updated
    """
    __tablename__ = "todos"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    title: str = Field(max_length=500)
    is_complete: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        """SQLModel configuration."""
        json_schema_extra = {
            "example": {
                "id": 1,
                "user_id": 1,
                "title": "Buy groceries",
                "is_complete": False,
                "created_at": "2024-01-01T00:00:00",
                "updated_at": "2024-01-01T00:00:00"
            }
        }
