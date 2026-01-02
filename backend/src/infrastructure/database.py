"""Database connection and session management."""
from sqlmodel import SQLModel, create_engine, Session
from sqlalchemy.pool import StaticPool
import os
from typing import Generator

# Get database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./data/todo_dev.db")

# Create engine with appropriate settings
if DATABASE_URL.startswith("sqlite"):
    # SQLite: Use check_same_thread=False for FastAPI compatibility
    engine = create_engine(
        DATABASE_URL,
        echo=False,  # Set True to log SQL queries
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
else:
    # PostgreSQL: Use connection pooling
    engine = create_engine(
        DATABASE_URL,
        echo=False,
        pool_size=10,
        max_overflow=20,
        pool_pre_ping=True,  # Verify connections before use
    )


def create_db_and_tables():
    """Create database tables from SQLModel metadata."""
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    """
    Get a database session for dependency injection.

    Yields:
        Session: Database session

    Example:
        @app.get("/items")
        def get_items(session: Session = Depends(get_session)):
            return session.query(Item).all()
    """
    with Session(engine) as session:
        yield session
