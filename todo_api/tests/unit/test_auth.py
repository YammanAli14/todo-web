"""Tests for authentication endpoints."""

import pytest


class TestRegister:
    """Tests for POST /auth/register."""

    def test_register_success(self, client, test_user_data):
        """Test successful user registration."""
        response = client.post("/auth/register", json=test_user_data)

        assert response.status_code == 201
        data = response.json()
        assert data["email"] == test_user_data["email"]
        assert "id" in data
        assert "created_at" in data
        assert "password" not in data
        assert "password_hash" not in data

    def test_register_duplicate_email(self, client, registered_user, test_user_data):
        """Test registration with existing email fails."""
        response = client.post("/auth/register", json=test_user_data)

        assert response.status_code == 409
        assert "already registered" in response.json()["detail"]

    def test_register_invalid_email(self, client):
        """Test registration with invalid email format."""
        response = client.post("/auth/register", json={
            "email": "not-an-email",
            "password": "testpass123"
        })

        assert response.status_code == 422

    def test_register_short_password(self, client):
        """Test registration with password too short."""
        response = client.post("/auth/register", json={
            "email": "test@example.com",
            "password": "short"
        })

        assert response.status_code == 422
        assert "8 characters" in str(response.json())


class TestLogin:
    """Tests for POST /auth/login."""

    def test_login_success(self, client, registered_user, test_user_data):
        """Test successful login returns token."""
        response = client.post(
            "/auth/login",
            data={
                "username": test_user_data["email"],
                "password": test_user_data["password"]
            }
        )

        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    def test_login_invalid_password(self, client, registered_user, test_user_data):
        """Test login with wrong password fails."""
        response = client.post(
            "/auth/login",
            data={
                "username": test_user_data["email"],
                "password": "wrongpassword"
            }
        )

        assert response.status_code == 401
        assert "Invalid email or password" in response.json()["detail"]

    def test_login_nonexistent_user(self, client):
        """Test login with non-existent email fails."""
        response = client.post(
            "/auth/login",
            data={
                "username": "nobody@example.com",
                "password": "somepassword"
            }
        )

        assert response.status_code == 401


class TestLoginJson:
    """Tests for POST /auth/login/json."""

    def test_login_json_success(self, client, registered_user, test_user_data):
        """Test login with JSON body."""
        response = client.post("/auth/login/json", json=test_user_data)

        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data

    def test_login_json_invalid_credentials(self, client, registered_user):
        """Test JSON login with wrong credentials."""
        response = client.post("/auth/login/json", json={
            "email": "test@example.com",
            "password": "wrongpassword"
        })

        assert response.status_code == 401


class TestMe:
    """Tests for GET /auth/me."""

    def test_me_authenticated(self, client, auth_headers, test_user_data):
        """Test getting current user info."""
        response = client.get("/auth/me", headers=auth_headers)

        assert response.status_code == 200
        data = response.json()
        assert data["email"] == test_user_data["email"]
        assert "id" in data
        assert "password" not in data

    def test_me_unauthenticated(self, client):
        """Test /me without token fails."""
        response = client.get("/auth/me")

        assert response.status_code == 401

    def test_me_invalid_token(self, client):
        """Test /me with invalid token fails."""
        response = client.get(
            "/auth/me",
            headers={"Authorization": "Bearer invalid-token"}
        )

        assert response.status_code == 401
