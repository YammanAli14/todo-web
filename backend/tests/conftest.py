"""Pytest configuration and shared fixtures."""
import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlalchemy.pool import StaticPool

from src.presentation.main import app
from src.presentation.dependencies import get_db_session


@pytest.fixture(name="session")
def session_fixture():
    """
    Create an in-memory SQLite database session for testing.

    Yields:
        Session: Test database session
    """
    # Create in-memory SQLite engine for testing
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    # Create all tables
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    """
    Create a FastAPI test client with test database session.

    Args:
        session: Test database session

    Yields:
        TestClient: FastAPI test client
    """
    def get_session_override():
        return session

    app.dependency_overrides[get_db_session] = get_session_override

    client = TestClient(app)
    yield client

    app.dependency_overrides.clear()


# Additional fixtures will be added in later phases
# @pytest.fixture
# def test_user(session: Session):
#     """Create a test user."""
#     pass
#
# @pytest.fixture
# def auth_headers(test_user):
#     """Get authentication headers for test user."""
#     pass
