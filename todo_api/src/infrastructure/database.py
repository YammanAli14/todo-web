"""Database configuration and session management."""

import os
from typing import Generator

from sqlmodel import SQLModel, Session, create_engine

# Engine singleton
_engine = None


def get_database_url() -> str:
    """Get database URL based on environment.

    Returns:
        Database connection URL string.

    Raises:
        ValueError: If DATABASE_URL not set in production.
    """
    environment = os.getenv("ENVIRONMENT", "development")
    if environment == "production":
        url = os.getenv("DATABASE_URL")
        if not url:
            raise ValueError(
                "DATABASE_URL environment variable required in production"
            )
        return url
    return "sqlite:///./data/todo.db"


def get_connect_args() -> dict:
    """Get connection arguments based on database type.

    Returns:
        Dictionary of connection arguments.
    """
    url = get_database_url()
    if url.startswith("sqlite"):
        return {"check_same_thread": False}
    return {}


def get_engine():
    """Get or create database engine singleton.

    Returns:
        SQLAlchemy engine instance.
    """
    global _engine
    if _engine is None:
        _engine = create_engine(
            get_database_url(),
            connect_args=get_connect_args()
        )
    return _engine


def reset_engine() -> None:
    """Reset engine singleton (for testing)."""
    global _engine
    _engine = None


def get_session() -> Generator[Session, None, None]:
    """Yield database session for request lifecycle.

    Yields:
        Database session that auto-closes after use.
    """
    engine = get_engine()
    with Session(engine) as session:
        yield session


def create_db_and_tables() -> None:
    """Create all database tables."""
    engine = get_engine()
    SQLModel.metadata.create_all(engine)
