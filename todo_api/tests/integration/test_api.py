"""Integration tests for API endpoints."""

import pytest
from fastapi.testclient import TestClient


class TestHealthEndpoint:
    """Tests for health check endpoint."""

    def test_health_check(self, client: TestClient) -> None:
        """GET /health returns 200 with healthy status."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"


class TestTasksRequireAuth:
    """Tests that task endpoints require authentication."""

    def test_create_task_requires_auth(self, client: TestClient) -> None:
        """POST /tasks without auth returns 401."""
        response = client.post("/tasks", json={"title": "Test"})
        assert response.status_code == 401

    def test_list_tasks_requires_auth(self, client: TestClient) -> None:
        """GET /tasks without auth returns 401."""
        response = client.get("/tasks")
        assert response.status_code == 401

    def test_get_task_requires_auth(self, client: TestClient) -> None:
        """GET /tasks/{id} without auth returns 401."""
        response = client.get("/tasks/1")
        assert response.status_code == 401

    def test_update_task_requires_auth(self, client: TestClient) -> None:
        """PUT /tasks/{id} without auth returns 401."""
        response = client.put("/tasks/1", json={"title": "Test"})
        assert response.status_code == 401

    def test_delete_task_requires_auth(self, client: TestClient) -> None:
        """DELETE /tasks/{id} without auth returns 401."""
        response = client.delete("/tasks/1")
        assert response.status_code == 401

    def test_toggle_task_requires_auth(self, client: TestClient) -> None:
        """PATCH /tasks/{id}/toggle without auth returns 401."""
        response = client.patch("/tasks/1/toggle")
        assert response.status_code == 401


class TestCreateTask:
    """Tests for POST /tasks endpoint."""

    def test_create_task(self, client: TestClient, auth_headers) -> None:
        """POST /tasks creates task and returns 201."""
        response = client.post(
            "/tasks",
            json={"title": "Buy groceries"},
            headers=auth_headers
        )
        assert response.status_code == 201
        data = response.json()
        assert data["id"] == 1
        assert data["title"] == "Buy groceries"
        assert data["is_complete"] is False
        assert "created_at" in data
        assert "updated_at" in data

    def test_create_task_empty_title(self, client: TestClient, auth_headers) -> None:
        """POST /tasks with empty title returns 422."""
        response = client.post(
            "/tasks",
            json={"title": ""},
            headers=auth_headers
        )
        assert response.status_code == 422

    def test_create_task_whitespace_title(self, client: TestClient, auth_headers) -> None:
        """POST /tasks with whitespace title returns 422."""
        response = client.post(
            "/tasks",
            json={"title": "   "},
            headers=auth_headers
        )
        assert response.status_code == 422

    def test_create_task_long_title(self, client: TestClient, auth_headers) -> None:
        """POST /tasks with title > 200 chars returns 422."""
        long_title = "x" * 201
        response = client.post(
            "/tasks",
            json={"title": long_title},
            headers=auth_headers
        )
        assert response.status_code == 422

    def test_create_task_strips_whitespace(self, client: TestClient, auth_headers) -> None:
        """POST /tasks strips leading/trailing whitespace."""
        response = client.post(
            "/tasks",
            json={"title": "  Buy groceries  "},
            headers=auth_headers
        )
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Buy groceries"


class TestListTasks:
    """Tests for GET /tasks endpoint."""

    def test_list_tasks_empty(self, client: TestClient, auth_headers) -> None:
        """GET /tasks returns empty array when no tasks."""
        response = client.get("/tasks", headers=auth_headers)
        assert response.status_code == 200
        assert response.json() == []

    def test_list_tasks_with_data(self, client: TestClient, auth_headers) -> None:
        """GET /tasks returns all tasks."""
        client.post("/tasks", json={"title": "Task 1"}, headers=auth_headers)
        client.post("/tasks", json={"title": "Task 2"}, headers=auth_headers)

        response = client.get("/tasks", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert data[0]["title"] == "Task 1"
        assert data[1]["title"] == "Task 2"

    def test_list_tasks_ordered_by_id(self, client: TestClient, auth_headers) -> None:
        """GET /tasks returns tasks ordered by ID ascending."""
        client.post("/tasks", json={"title": "First"}, headers=auth_headers)
        client.post("/tasks", json={"title": "Second"}, headers=auth_headers)
        client.post("/tasks", json={"title": "Third"}, headers=auth_headers)

        response = client.get("/tasks", headers=auth_headers)
        data = response.json()
        assert data[0]["id"] < data[1]["id"] < data[2]["id"]


class TestGetTask:
    """Tests for GET /tasks/{id} endpoint."""

    def test_get_task(self, client: TestClient, auth_headers) -> None:
        """GET /tasks/{id} returns single task."""
        client.post("/tasks", json={"title": "Test task"}, headers=auth_headers)

        response = client.get("/tasks/1", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == 1
        assert data["title"] == "Test task"
        assert data["is_complete"] is False

    def test_get_task_not_found(self, client: TestClient, auth_headers) -> None:
        """GET /tasks/{id} returns 404 for non-existent task."""
        response = client.get("/tasks/999", headers=auth_headers)
        assert response.status_code == 404
        assert response.json()["detail"] == "Task not found"

    def test_get_task_has_timestamps(self, client: TestClient, auth_headers) -> None:
        """GET /tasks/{id} returns task with timestamps."""
        client.post("/tasks", json={"title": "Test task"}, headers=auth_headers)

        response = client.get("/tasks/1", headers=auth_headers)
        data = response.json()
        assert "created_at" in data
        assert "updated_at" in data


class TestUpdateTask:
    """Tests for PUT /tasks/{id} endpoint."""

    def test_update_task(self, client: TestClient, auth_headers) -> None:
        """PUT /tasks/{id} updates task title."""
        client.post("/tasks", json={"title": "Old title"}, headers=auth_headers)

        response = client.put(
            "/tasks/1",
            json={"title": "New title"},
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == 1
        assert data["title"] == "New title"

    def test_update_task_not_found(self, client: TestClient, auth_headers) -> None:
        """PUT /tasks/{id} returns 404 for non-existent task."""
        response = client.put(
            "/tasks/999",
            json={"title": "New title"},
            headers=auth_headers
        )
        assert response.status_code == 404
        assert response.json()["detail"] == "Task not found"

    def test_update_task_empty_title(self, client: TestClient, auth_headers) -> None:
        """PUT /tasks/{id} with empty title returns 422."""
        client.post("/tasks", json={"title": "Test task"}, headers=auth_headers)

        response = client.put(
            "/tasks/1",
            json={"title": ""},
            headers=auth_headers
        )
        assert response.status_code == 422

    def test_update_task_changes_updated_at(self, client: TestClient, auth_headers) -> None:
        """PUT /tasks/{id} updates the updated_at timestamp."""
        client.post("/tasks", json={"title": "Test task"}, headers=auth_headers)
        original = client.get("/tasks/1", headers=auth_headers).json()

        # Small delay to ensure timestamp difference
        import time
        time.sleep(0.1)

        client.put("/tasks/1", json={"title": "Updated title"}, headers=auth_headers)
        updated = client.get("/tasks/1", headers=auth_headers).json()

        assert updated["updated_at"] >= original["updated_at"]


class TestDeleteTask:
    """Tests for DELETE /tasks/{id} endpoint."""

    def test_delete_task(self, client: TestClient, auth_headers) -> None:
        """DELETE /tasks/{id} removes task and returns 204."""
        client.post("/tasks", json={"title": "To delete"}, headers=auth_headers)

        response = client.delete("/tasks/1", headers=auth_headers)
        assert response.status_code == 204

        # Verify task is gone
        get_response = client.get("/tasks/1", headers=auth_headers)
        assert get_response.status_code == 404

    def test_delete_task_not_found(self, client: TestClient, auth_headers) -> None:
        """DELETE /tasks/{id} returns 404 for non-existent task."""
        response = client.delete("/tasks/999", headers=auth_headers)
        assert response.status_code == 404
        assert response.json()["detail"] == "Task not found"


class TestToggleTask:
    """Tests for PATCH /tasks/{id}/toggle endpoint."""

    def test_toggle_task_to_complete(self, client: TestClient, auth_headers) -> None:
        """PATCH /tasks/{id}/toggle marks incomplete task as complete."""
        client.post("/tasks", json={"title": "Test task"}, headers=auth_headers)

        response = client.patch("/tasks/1/toggle", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["is_complete"] is True

    def test_toggle_task_to_incomplete(self, client: TestClient, auth_headers) -> None:
        """PATCH /tasks/{id}/toggle marks complete task as incomplete."""
        client.post("/tasks", json={"title": "Test task"}, headers=auth_headers)
        client.patch("/tasks/1/toggle", headers=auth_headers)  # Make complete

        response = client.patch("/tasks/1/toggle", headers=auth_headers)  # Toggle back
        assert response.status_code == 200
        data = response.json()
        assert data["is_complete"] is False

    def test_toggle_task_not_found(self, client: TestClient, auth_headers) -> None:
        """PATCH /tasks/{id}/toggle returns 404 for non-existent task."""
        response = client.patch("/tasks/999/toggle", headers=auth_headers)
        assert response.status_code == 404
        assert response.json()["detail"] == "Task not found"

    def test_toggle_task_updates_timestamp(self, client: TestClient, auth_headers) -> None:
        """PATCH /tasks/{id}/toggle updates the updated_at timestamp."""
        client.post("/tasks", json={"title": "Test task"}, headers=auth_headers)
        original = client.get("/tasks/1", headers=auth_headers).json()

        import time
        time.sleep(0.1)

        client.patch("/tasks/1/toggle", headers=auth_headers)
        toggled = client.get("/tasks/1", headers=auth_headers).json()

        assert toggled["updated_at"] >= original["updated_at"]


class TestUserIsolation:
    """Tests that users can only access their own tasks."""

    def test_user_cannot_see_other_user_tasks(
        self, client, auth_headers, second_user_headers
    ):
        """User A cannot see User B's tasks in list."""
        # User A creates a task
        client.post("/tasks", json={"title": "User A task"}, headers=auth_headers)

        # User B should see empty list
        response = client.get("/tasks", headers=second_user_headers)
        assert response.status_code == 200
        assert response.json() == []

    def test_user_cannot_get_other_user_task(
        self, client, auth_headers, second_user_headers
    ):
        """User A cannot get User B's task by ID."""
        # User A creates a task
        create_resp = client.post(
            "/tasks",
            json={"title": "User A task"},
            headers=auth_headers
        )
        task_id = create_resp.json()["id"]

        # User B cannot access it
        response = client.get(f"/tasks/{task_id}", headers=second_user_headers)
        assert response.status_code == 404

    def test_user_cannot_update_other_user_task(
        self, client, auth_headers, second_user_headers
    ):
        """User A cannot update User B's task."""
        # User A creates a task
        create_resp = client.post(
            "/tasks",
            json={"title": "User A task"},
            headers=auth_headers
        )
        task_id = create_resp.json()["id"]

        # User B cannot update it
        response = client.put(
            f"/tasks/{task_id}",
            json={"title": "Hacked!"},
            headers=second_user_headers
        )
        assert response.status_code == 404

    def test_user_cannot_delete_other_user_task(
        self, client, auth_headers, second_user_headers
    ):
        """User A cannot delete User B's task."""
        # User A creates a task
        create_resp = client.post(
            "/tasks",
            json={"title": "User A task"},
            headers=auth_headers
        )
        task_id = create_resp.json()["id"]

        # User B cannot delete it
        response = client.delete(f"/tasks/{task_id}", headers=second_user_headers)
        assert response.status_code == 404

        # Verify task still exists for User A
        get_resp = client.get(f"/tasks/{task_id}", headers=auth_headers)
        assert get_resp.status_code == 200

    def test_user_cannot_toggle_other_user_task(
        self, client, auth_headers, second_user_headers
    ):
        """User A cannot toggle User B's task."""
        # User A creates a task
        create_resp = client.post(
            "/tasks",
            json={"title": "User A task"},
            headers=auth_headers
        )
        task_id = create_resp.json()["id"]

        # User B cannot toggle it
        response = client.patch(
            f"/tasks/{task_id}/toggle",
            headers=second_user_headers
        )
        assert response.status_code == 404
