"""Pytest configuration and fixtures."""

import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, Session, create_engine
from sqlmodel.pool import StaticPool

from src.presentation.api import app
from src.infrastructure.database import get_session
from src.domain.user import User
from src.domain.task import Task


@pytest.fixture(name="engine")
def engine_fixture():
    """Create in-memory SQLite engine for testing."""
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    # Import models to register them
    _ = User
    _ = Task
    SQLModel.metadata.create_all(engine)
    yield engine
    SQLModel.metadata.drop_all(engine)


@pytest.fixture(name="session")
def session_fixture(engine):
    """Create database session for testing."""
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    """Create test client with overridden dependencies."""
    def get_session_override():
        yield session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


# =============================================================================
# Auth Fixtures
# =============================================================================

@pytest.fixture
def test_user_data():
    """Sample user registration data."""
    return {
        "email": "test@example.com",
        "password": "testpass123"
    }


@pytest.fixture
def registered_user(client, test_user_data):
    """Register a test user and return the response."""
    response = client.post("/auth/register", json=test_user_data)
    assert response.status_code == 201
    return response.json()


@pytest.fixture
def auth_token(client, registered_user, test_user_data):
    """Login and return the access token."""
    response = client.post(
        "/auth/login",
        data={
            "username": test_user_data["email"],
            "password": test_user_data["password"]
        }
    )
    assert response.status_code == 200
    return response.json()["access_token"]


@pytest.fixture
def auth_headers(auth_token):
    """Return authorization headers with Bearer token."""
    return {"Authorization": f"Bearer {auth_token}"}


@pytest.fixture
def second_user_data():
    """Sample data for a second user."""
    return {
        "email": "second@example.com",
        "password": "secondpass123"
    }


@pytest.fixture
def second_user_headers(client, second_user_data):
    """Register second user and return auth headers."""
    # Register
    client.post("/auth/register", json=second_user_data)
    # Login
    response = client.post(
        "/auth/login",
        data={
            "username": second_user_data["email"],
            "password": second_user_data["password"]
        }
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
