"""User domain entity."""
from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional


class User(SQLModel, table=True):
    """
    User entity for authentication and authorization.

    Attributes:
        id: Primary key
        email: Unique email address for authentication
        password_hash: Bcrypt hashed password
        created_at: Timestamp when user was created
        updated_at: Timestamp when user was last updated
    """
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True, max_length=255)
    password_hash: str = Field(max_length=255)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        """SQLModel configuration."""
        json_schema_extra = {
            "example": {
                "id": 1,
                "email": "user@example.com",
                "password_hash": "$2b$12$...",
                "created_at": "2024-01-01T00:00:00",
                "updated_at": "2024-01-01T00:00:00"
            }
        }
