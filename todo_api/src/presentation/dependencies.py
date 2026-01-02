"""FastAPI dependency injection functions."""

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session

from src.infrastructure.database import get_session
from src.infrastructure.task_repository import TaskRepository
from src.infrastructure.user_repository import UserRepository
from src.application.task_service import TaskService
from src.application.auth_service import AuthService
from src.domain.user import User


# OAuth2 scheme for Bearer token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


# =============================================================================
# Repository Dependencies
# =============================================================================

def get_task_repository(
    session: Session = Depends(get_session)
) -> TaskRepository:
    """Get TaskRepository instance.

    Args:
        session: Database session from dependency.

    Returns:
        TaskRepository instance.
    """
    return TaskRepository(session)


def get_user_repository(
    session: Session = Depends(get_session)
) -> UserRepository:
    """Get UserRepository instance.

    Args:
        session: Database session from dependency.

    Returns:
        UserRepository instance.
    """
    return UserRepository(session)


# =============================================================================
# Service Dependencies
# =============================================================================

def get_task_service(
    repository: TaskRepository = Depends(get_task_repository)
) -> TaskService:
    """Get TaskService instance.

    Args:
        repository: TaskRepository from dependency.

    Returns:
        TaskService instance.
    """
    return TaskService(repository)


def get_auth_service(
    repository: UserRepository = Depends(get_user_repository)
) -> AuthService:
    """Get AuthService instance.

    Args:
        repository: UserRepository from dependency.

    Returns:
        AuthService instance.
    """
    return AuthService(repository)


# =============================================================================
# Auth Dependencies
# =============================================================================

def get_current_user(
    token: str = Depends(oauth2_scheme),
    auth_service: AuthService = Depends(get_auth_service)
) -> User:
    """Get current authenticated user from JWT token.

    Args:
        token: JWT token from Authorization header.
        auth_service: AuthService from dependency.

    Returns:
        Current authenticated user.

    Raises:
        HTTPException: 401 if token is invalid or user not found.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    payload = auth_service.verify_token(token)
    if payload is None:
        raise credentials_exception

    user_id = payload.get("sub")
    if user_id is None:
        raise credentials_exception

    try:
        user_id = int(user_id)
    except ValueError:
        raise credentials_exception

    user = auth_service.get_user_by_id(user_id)
    if user is None:
        raise credentials_exception

    return user
