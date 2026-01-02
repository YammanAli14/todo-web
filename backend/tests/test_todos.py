"""Test todo endpoints."""
from fastapi.testclient import TestClient


def test_get_todos_empty(client: TestClient):
    """Test getting todos for a new user (should be empty)."""
    # Signup
    signup_response = client.post(
        "/auth/signup",
        json={
            "email": "todos1@example.com",
            "password": "testpassword123"
        }
    )
    token = signup_response.json()["access_token"]

    # Get todos
    response = client.get(
        "/todos",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 0


def test_create_todo_success(client: TestClient):
    """Test creating a new todo."""
    # Signup
    signup_response = client.post(
        "/auth/signup",
        json={
            "email": "todos2@example.com",
            "password": "testpassword123"
        }
    )
    token = signup_response.json()["access_token"]

    # Create todo
    response = client.post(
        "/todos",
        headers={"Authorization": f"Bearer {token}"},
        json={"title": "Buy groceries"}
    )

    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Buy groceries"
    assert data["is_complete"] is False
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data


def test_create_todo_empty_title(client: TestClient):
    """Test creating a todo with empty title."""
    # Signup
    signup_response = client.post(
        "/auth/signup",
        json={
            "email": "todos3@example.com",
            "password": "testpassword123"
        }
    )
    token = signup_response.json()["access_token"]

    # Create todo with empty title
    response = client.post(
        "/todos",
        headers={"Authorization": f"Bearer {token}"},
        json={"title": "   "}
    )

    assert response.status_code == 400
    assert "empty" in response.json()["detail"].lower()


def test_create_todo_unauthorized(client: TestClient):
    """Test creating a todo without authentication."""
    response = client.post(
        "/todos",
        json={"title": "Buy groceries"}
    )

    assert response.status_code == 401


def test_get_all_todos(client: TestClient):
    """Test getting all todos for a user."""
    # Signup
    signup_response = client.post(
        "/auth/signup",
        json={
            "email": "todos4@example.com",
            "password": "testpassword123"
        }
    )
    token = signup_response.json()["access_token"]

    # Create multiple todos
    client.post(
        "/todos",
        headers={"Authorization": f"Bearer {token}"},
        json={"title": "Todo 1"}
    )
    client.post(
        "/todos",
        headers={"Authorization": f"Bearer {token}"},
        json={"title": "Todo 2"}
    )
    client.post(
        "/todos",
        headers={"Authorization": f"Bearer {token}"},
        json={"title": "Todo 3"}
    )

    # Get all todos
    response = client.get(
        "/todos",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3
    assert data[0]["title"] == "Todo 3"  # Newest first
    assert data[1]["title"] == "Todo 2"
    assert data[2]["title"] == "Todo 1"


def test_get_todo_by_id(client: TestClient):
    """Test getting a specific todo by ID."""
    # Signup
    signup_response = client.post(
        "/auth/signup",
        json={
            "email": "todos5@example.com",
            "password": "testpassword123"
        }
    )
    token = signup_response.json()["access_token"]

    # Create todo
    create_response = client.post(
        "/todos",
        headers={"Authorization": f"Bearer {token}"},
        json={"title": "Test todo"}
    )
    todo_id = create_response.json()["id"]

    # Get todo by ID
    response = client.get(
        f"/todos/{todo_id}",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == todo_id
    assert data["title"] == "Test todo"


def test_get_todo_not_found(client: TestClient):
    """Test getting a non-existent todo."""
    # Signup
    signup_response = client.post(
        "/auth/signup",
        json={
            "email": "todos6@example.com",
            "password": "testpassword123"
        }
    )
    token = signup_response.json()["access_token"]

    # Get non-existent todo
    response = client.get(
        "/todos/99999",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 404


def test_update_todo(client: TestClient):
    """Test updating a todo's title."""
    # Signup
    signup_response = client.post(
        "/auth/signup",
        json={
            "email": "todos7@example.com",
            "password": "testpassword123"
        }
    )
    token = signup_response.json()["access_token"]

    # Create todo
    create_response = client.post(
        "/todos",
        headers={"Authorization": f"Bearer {token}"},
        json={"title": "Original title"}
    )
    todo_id = create_response.json()["id"]

    # Update todo
    response = client.put(
        f"/todos/{todo_id}",
        headers={"Authorization": f"Bearer {token}"},
        json={"title": "Updated title"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == todo_id
    assert data["title"] == "Updated title"


def test_toggle_todo_completion(client: TestClient):
    """Test toggling todo completion status."""
    # Signup
    signup_response = client.post(
        "/auth/signup",
        json={
            "email": "todos8@example.com",
            "password": "testpassword123"
        }
    )
    token = signup_response.json()["access_token"]

    # Create todo
    create_response = client.post(
        "/todos",
        headers={"Authorization": f"Bearer {token}"},
        json={"title": "Test todo"}
    )
    todo_id = create_response.json()["id"]

    # Toggle to complete
    response = client.patch(
        f"/todos/{todo_id}/toggle",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["is_complete"] is True

    # Toggle back to incomplete
    response = client.patch(
        f"/todos/{todo_id}/toggle",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["is_complete"] is False


def test_delete_todo(client: TestClient):
    """Test deleting a todo."""
    # Signup
    signup_response = client.post(
        "/auth/signup",
        json={
            "email": "todos9@example.com",
            "password": "testpassword123"
        }
    )
    token = signup_response.json()["access_token"]

    # Create todo
    create_response = client.post(
        "/todos",
        headers={"Authorization": f"Bearer {token}"},
        json={"title": "Test todo"}
    )
    todo_id = create_response.json()["id"]

    # Delete todo
    response = client.delete(
        f"/todos/{todo_id}",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 204

    # Verify todo is deleted
    get_response = client.get(
        f"/todos/{todo_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert get_response.status_code == 404


def test_user_isolation(client: TestClient):
    """Test that users can only access their own todos."""
    # Signup user 1
    signup1 = client.post(
        "/auth/signup",
        json={
            "email": "user1@example.com",
            "password": "testpassword123"
        }
    )
    token1 = signup1.json()["access_token"]

    # Signup user 2
    signup2 = client.post(
        "/auth/signup",
        json={
            "email": "user2@example.com",
            "password": "testpassword123"
        }
    )
    token2 = signup2.json()["access_token"]

    # User 1 creates a todo
    create_response = client.post(
        "/todos",
        headers={"Authorization": f"Bearer {token1}"},
        json={"title": "User 1 todo"}
    )
    todo_id = create_response.json()["id"]

    # User 2 tries to access user 1's todo
    response = client.get(
        f"/todos/{todo_id}",
        headers={"Authorization": f"Bearer {token2}"}
    )

    assert response.status_code == 404

    # User 1 can access their own todo
    response = client.get(
        f"/todos/{todo_id}",
        headers={"Authorization": f"Bearer {token1}"}
    )

    assert response.status_code == 200
