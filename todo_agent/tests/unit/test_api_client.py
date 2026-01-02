"""Unit Tests for API Client.

This module contains unit tests for the TodoAPIClient class.
Tests use respx to mock HTTP responses.
"""

import pytest
import httpx
import respx
from src.tools.api_client import TodoAPIClient


class TestTodoAPIClient:
    """Tests for the TodoAPIClient class."""

    @pytest.fixture
    def client(self):
        """Create a TodoAPIClient instance."""
        return TodoAPIClient(base_url="http://testapi:8000")

    @pytest.fixture
    def sample_task(self):
        """Sample task response."""
        return {
            "id": 1,
            "title": "Buy groceries",
            "is_complete": False,
            "created_at": "2025-12-28T10:00:00Z",
            "updated_at": "2025-12-28T10:00:00Z"
        }

    @respx.mock
    def test_create_task_success(self, client, sample_task):
        """Test successful task creation."""
        respx.post("http://testapi:8000/tasks").mock(
            return_value=httpx.Response(201, json=sample_task)
        )

        result = client.create_task("Buy groceries")

        assert result == sample_task
        assert result["id"] == 1
        assert result["title"] == "Buy groceries"

    @respx.mock
    def test_create_task_validation_error(self, client):
        """Test task creation with validation error."""
        respx.post("http://testapi:8000/tasks").mock(
            return_value=httpx.Response(422, json={"detail": "Title too long"})
        )

        with pytest.raises(ValueError) as exc_info:
            client.create_task("x" * 300)

        assert "Invalid input" in str(exc_info.value)

    @respx.mock
    def test_list_tasks_success(self, client, sample_task):
        """Test successful task listing."""
        tasks = [sample_task, {**sample_task, "id": 2, "title": "Test"}]
        respx.get("http://testapi:8000/tasks").mock(
            return_value=httpx.Response(200, json=tasks)
        )

        result = client.list_tasks()

        assert len(result) == 2
        assert result[0]["id"] == 1
        assert result[1]["id"] == 2

    @respx.mock
    def test_list_tasks_empty(self, client):
        """Test listing when no tasks exist."""
        respx.get("http://testapi:8000/tasks").mock(
            return_value=httpx.Response(200, json=[])
        )

        result = client.list_tasks()

        assert result == []

    @respx.mock
    def test_get_task_success(self, client, sample_task):
        """Test getting a specific task."""
        respx.get("http://testapi:8000/tasks/1").mock(
            return_value=httpx.Response(200, json=sample_task)
        )

        result = client.get_task(1)

        assert result == sample_task

    @respx.mock
    def test_get_task_not_found(self, client):
        """Test getting a task that doesn't exist."""
        respx.get("http://testapi:8000/tasks/999").mock(
            return_value=httpx.Response(404, json={"detail": "Task not found"})
        )

        result = client.get_task(999)

        assert result is None

    @respx.mock
    def test_update_task_success(self, client, sample_task):
        """Test successful task update."""
        updated = {**sample_task, "title": "New title"}
        respx.put("http://testapi:8000/tasks/1").mock(
            return_value=httpx.Response(200, json=updated)
        )

        result = client.update_task(1, "New title")

        assert result["title"] == "New title"

    @respx.mock
    def test_update_task_not_found(self, client):
        """Test updating a task that doesn't exist."""
        respx.put("http://testapi:8000/tasks/999").mock(
            return_value=httpx.Response(404, json={"detail": "Task not found"})
        )

        result = client.update_task(999, "New title")

        assert result is None

    @respx.mock
    def test_update_task_validation_error(self, client):
        """Test updating with invalid data."""
        respx.put("http://testapi:8000/tasks/1").mock(
            return_value=httpx.Response(422, json={"detail": "Title too long"})
        )

        with pytest.raises(ValueError) as exc_info:
            client.update_task(1, "x" * 300)

        assert "Invalid input" in str(exc_info.value)

    @respx.mock
    def test_delete_task_success(self, client):
        """Test successful task deletion."""
        respx.delete("http://testapi:8000/tasks/1").mock(
            return_value=httpx.Response(204)
        )

        result = client.delete_task(1)

        assert result is True

    @respx.mock
    def test_delete_task_not_found(self, client):
        """Test deleting a task that doesn't exist."""
        respx.delete("http://testapi:8000/tasks/999").mock(
            return_value=httpx.Response(404, json={"detail": "Task not found"})
        )

        result = client.delete_task(999)

        assert result is False

    @respx.mock
    def test_toggle_task_success(self, client, sample_task):
        """Test successful task toggle."""
        toggled = {**sample_task, "is_complete": True}
        respx.patch("http://testapi:8000/tasks/1/toggle").mock(
            return_value=httpx.Response(200, json=toggled)
        )

        result = client.toggle_task(1)

        assert result["is_complete"] is True

    @respx.mock
    def test_toggle_task_not_found(self, client):
        """Test toggling a task that doesn't exist."""
        respx.patch("http://testapi:8000/tasks/999/toggle").mock(
            return_value=httpx.Response(404, json={"detail": "Task not found"})
        )

        result = client.toggle_task(999)

        assert result is None

    def test_context_manager(self):
        """Test that client works as context manager."""
        with TodoAPIClient() as client:
            assert client.base_url == "http://localhost:8000"


class TestAPIClientHelpers:
    """Tests for API client helper functions."""

    def test_get_api_client_singleton(self):
        """Test that get_api_client returns same instance."""
        from src.tools.api_client import get_api_client, reset_api_client, set_api_client

        reset_api_client()

        # Need to patch config import
        with pytest.MonkeyPatch.context() as mp:
            mp.setattr("src.agent.config.API_BASE_URL", "http://localhost:8000")
            client1 = get_api_client()
            client2 = get_api_client()

            assert client1 is client2

        reset_api_client()

    def test_set_api_client(self):
        """Test setting custom API client."""
        from src.tools.api_client import get_api_client, set_api_client, reset_api_client

        reset_api_client()

        custom_client = TodoAPIClient(base_url="http://custom:9000")
        set_api_client(custom_client)

        assert get_api_client() is custom_client

        reset_api_client()
