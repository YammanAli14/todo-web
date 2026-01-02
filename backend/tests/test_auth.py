"""Test authentication endpoints."""
from fastapi.testclient import TestClient


def test_signup_success(client: TestClient):
    """Test successful user signup."""
    response = client.post(
        "/auth/signup",
        json={
            "email": "test@example.com",
            "password": "testpassword123"
        }
    )

    assert response.status_code == 201
    data = response.json()
    assert "user" in data
    assert "access_token" in data
    assert data["user"]["email"] == "test@example.com"
    assert data["token_type"] == "bearer"


def test_signup_duplicate_email(client: TestClient):
    """Test signup with duplicate email."""
    # First signup
    client.post(
        "/auth/signup",
        json={
            "email": "duplicate@example.com",
            "password": "testpassword123"
        }
    )

    # Second signup with same email
    response = client.post(
        "/auth/signup",
        json={
            "email": "duplicate@example.com",
            "password": "testpassword123"
        }
    )

    assert response.status_code == 400
    assert "already registered" in response.json()["detail"].lower()


def test_signup_weak_password(client: TestClient):
    """Test signup with weak password."""
    response = client.post(
        "/auth/signup",
        json={
            "email": "test2@example.com",
            "password": "short"
        }
    )

    assert response.status_code == 400
    assert "8 characters" in response.json()["detail"]


def test_signin_success(client: TestClient):
    """Test successful user signin."""
    # First signup
    client.post(
        "/auth/signup",
        json={
            "email": "signin@example.com",
            "password": "testpassword123"
        }
    )

    # Then signin
    response = client.post(
        "/auth/signin",
        json={
            "email": "signin@example.com",
            "password": "testpassword123"
        }
    )

    assert response.status_code == 200
    data = response.json()
    assert "user" in data
    assert "access_token" in data
    assert data["user"]["email"] == "signin@example.com"


def test_signin_invalid_credentials(client: TestClient):
    """Test signin with invalid credentials."""
    response = client.post(
        "/auth/signin",
        json={
            "email": "nonexistent@example.com",
            "password": "wrongpassword"
        }
    )

    assert response.status_code == 401


def test_get_current_user(client: TestClient):
    """Test getting current user with valid token."""
    # Signup
    signup_response = client.post(
        "/auth/signup",
        json={
            "email": "me@example.com",
            "password": "testpassword123"
        }
    )

    token = signup_response.json()["access_token"]

    # Get current user
    response = client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "me@example.com"


def test_get_current_user_no_token(client: TestClient):
    """Test getting current user without token."""
    response = client.get("/auth/me")

    assert response.status_code == 401  # HTTPBearer returns 401 when no credentials provided


def test_get_current_user_invalid_token(client: TestClient):
    """Test getting current user with invalid token."""
    response = client.get(
        "/auth/me",
        headers={"Authorization": "Bearer invalid_token_here"}
    )

    assert response.status_code == 401
