"""Request and response schemas for the API."""

from datetime import datetime

from pydantic import EmailStr, field_validator
from sqlmodel import SQLModel


# =============================================================================
# Task Schemas
# =============================================================================

class TaskCreate(SQLModel):
    """Request schema for creating a task."""

    title: str

    @field_validator("title")
    @classmethod
    def validate_title(cls, v: str) -> str:
        """Validate title is not empty and within length limit.

        Args:
            v: Title value to validate.

        Returns:
            Stripped title if valid.

        Raises:
            ValueError: If title is empty or too long.
        """
        stripped = v.strip()
        if not stripped:
            raise ValueError("Title cannot be empty")
        if len(stripped) > 200:
            raise ValueError("Title must be 200 characters or less")
        return stripped


class TaskUpdate(SQLModel):
    """Request schema for updating a task."""

    title: str

    @field_validator("title")
    @classmethod
    def validate_title(cls, v: str) -> str:
        """Validate title is not empty and within length limit.

        Args:
            v: Title value to validate.

        Returns:
            Stripped title if valid.

        Raises:
            ValueError: If title is empty or too long.
        """
        stripped = v.strip()
        if not stripped:
            raise ValueError("Title cannot be empty")
        if len(stripped) > 200:
            raise ValueError("Title must be 200 characters or less")
        return stripped


class TaskResponse(SQLModel):
    """Response schema for task data."""

    id: int
    title: str
    is_complete: bool
    created_at: datetime
    updated_at: datetime


# =============================================================================
# Auth Schemas
# =============================================================================

class UserCreate(SQLModel):
    """Request schema for user registration."""

    email: EmailStr
    password: str

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        """Validate password meets minimum length.

        Args:
            v: Password value to validate.

        Returns:
            Password if valid.

        Raises:
            ValueError: If password is too short.
        """
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        return v


class UserResponse(SQLModel):
    """Response schema for user data (excludes password)."""

    id: int
    email: str
    created_at: datetime


class LoginRequest(SQLModel):
    """Request schema for user login."""

    email: EmailStr
    password: str


class Token(SQLModel):
    """Response schema for JWT token."""

    access_token: str
    token_type: str = "bearer"


# =============================================================================
# Health Schemas
# =============================================================================

class HealthResponse(SQLModel):
    """Response schema for health check."""

    status: str
