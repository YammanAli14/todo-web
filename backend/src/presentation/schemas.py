"""Pydantic schemas for API request/response models."""
from pydantic import BaseModel
from typing import Optional


class ErrorResponse(BaseModel):
    """Standard error response schema."""
    detail: str
    code: Optional[str] = None
    field: Optional[str] = None

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "detail": "Invalid email format",
                    "code": "VALIDATION_ERROR",
                    "field": "email"
                }
            ]
        }
    }


class HealthResponse(BaseModel):
    """Health check response schema."""
    status: str
    version: str
    service: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "status": "healthy",
                    "version": "2.0.0",
                    "service": "todo-api"
                }
            ]
        }
    }


# Auth Schemas
from datetime import datetime
from pydantic import EmailStr


class SignupRequest(BaseModel):
    """User signup request schema."""
    email: EmailStr
    password: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "email": "user@example.com",
                    "password": "securepassword123"
                }
            ]
        }
    }


class SigninRequest(BaseModel):
    """User signin request schema."""
    email: EmailStr
    password: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "email": "user@example.com",
                    "password": "securepassword123"
                }
            ]
        }
    }


class UserResponse(BaseModel):
    """User response schema (excludes password_hash)."""
    id: int
    email: str
    created_at: datetime
    updated_at: datetime

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": 1,
                    "email": "user@example.com",
                    "created_at": "2024-01-01T00:00:00",
                    "updated_at": "2024-01-01T00:00:00"
                }
            ]
        }
    }


class AuthResponse(BaseModel):
    """Authentication response schema."""
    user: UserResponse
    access_token: str
    token_type: str = "bearer"

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "user": {
                        "id": 1,
                        "email": "user@example.com",
                        "created_at": "2024-01-01T00:00:00",
                        "updated_at": "2024-01-01T00:00:00"
                    },
                    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                    "token_type": "bearer"
                }
            ]
        }
    }


# Todo Schemas
class TodoCreateRequest(BaseModel):
    """Create todo request schema."""
    title: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "title": "Buy groceries"
                }
            ]
        }
    }


class TodoUpdateRequest(BaseModel):
    """Update todo request schema."""
    title: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "title": "Buy groceries and cook dinner"
                }
            ]
        }
    }


class TodoResponse(BaseModel):
    """Todo response schema."""
    id: int
    user_id: int
    title: str
    is_complete: bool
    created_at: datetime
    updated_at: datetime

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": 1,
                    "user_id": 1,
                    "title": "Buy groceries",
                    "is_complete": False,
                    "created_at": "2024-01-01T00:00:00",
                    "updated_at": "2024-01-01T00:00:00"
                }
            ]
        }
    }
