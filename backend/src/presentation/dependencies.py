"""FastAPI dependency injection functions."""
from typing import Generator, Annotated
from fastapi import Depends
from sqlmodel import Session

from src.infrastructure.database import get_session


def get_db_session() -> Generator[Session, None, None]:
    """
    Dependency for database session injection.

    Yields:
        Session: Database session for the request

    Example:
        @app.get("/items")
        def get_items(session: Session = Depends(get_db_session)):
            return session.query(Item).all()
    """
    yield from get_session()


# Type alias for database session dependency
SessionDep = Annotated[Session, Depends(get_db_session)]


# Current user dependency
from fastapi import HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from src.domain.user import User
from src.application.auth.jwt import get_user_id_from_token
from src.application.auth.auth_service import AuthService


# HTTP Bearer token scheme
security = HTTPBearer()


async def get_current_user(
    session: SessionDep,
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> User:
    """
    Get current authenticated user from JWT token.

    Args:
        session: Database session
        credentials: HTTP Authorization header with Bearer token

    Returns:
        User: Current authenticated user

    Raises:
        HTTPException: If token is invalid or user not found
    """
    token = credentials.credentials

    # Decode token and extract user ID
    user_id_str = get_user_id_from_token(token)
    if user_id_str is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Get user from database
    try:
        user_id = int(user_id_str)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token format",
            headers={"WWW-Authenticate": "Bearer"},
        )

    auth_service = AuthService(session)
    user = auth_service.get_current_user(user_id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user


# Type alias for current user dependency
CurrentUserDep = Annotated[User, Depends(get_current_user)]
