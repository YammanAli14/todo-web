"""Todo API Client - HTTP client for Phase II API.

This module provides an HTTP client for communicating with the Phase II
Todo REST API. It handles all CRUD operations for tasks.
"""

import httpx
from typing import Any


class TodoAPIClient:
    """HTTP client for the Todo API.

    This client provides methods for all task operations:
    - Create, Read, Update, Delete tasks
    - Toggle task completion status

    Attributes:
        base_url: The base URL of the Todo API.
        timeout: Request timeout in seconds.
    """

    def __init__(self, base_url: str = "http://localhost:8000", timeout: float = 10.0):
        """Initialize the API client.

        Args:
            base_url: The base URL of the Todo API.
            timeout: Request timeout in seconds.
        """
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self._client = httpx.Client(timeout=timeout)

    def _make_request(
        self,
        method: str,
        endpoint: str,
        json_data: dict[str, Any] | None = None
    ) -> httpx.Response:
        """Make an HTTP request to the API.

        Args:
            method: HTTP method (GET, POST, PUT, PATCH, DELETE).
            endpoint: API endpoint path.
            json_data: Optional JSON data for request body.

        Returns:
            The HTTP response.

        Raises:
            httpx.HTTPError: If the request fails.
        """
        url = f"{self.base_url}{endpoint}"
        return self._client.request(method, url, json=json_data)

    def create_task(self, title: str) -> dict[str, Any]:
        """Create a new task.

        Args:
            title: The title of the task to create.

        Returns:
            The created task as a dictionary.

        Raises:
            httpx.HTTPStatusError: If the API returns an error status.
            ValueError: If the request fails with validation error.
        """
        response = self._make_request("POST", "/tasks", {"title": title})
        if response.status_code == 422:
            error_detail = response.json().get("detail", "Validation error")
            raise ValueError(f"Invalid input: {error_detail}")
        response.raise_for_status()
        return response.json()

    def list_tasks(self) -> list[dict[str, Any]]:
        """List all tasks.

        Returns:
            A list of task dictionaries.

        Raises:
            httpx.HTTPStatusError: If the API returns an error status.
        """
        response = self._make_request("GET", "/tasks")
        response.raise_for_status()
        return response.json()

    def get_task(self, task_id: int) -> dict[str, Any] | None:
        """Get a specific task by ID.

        Args:
            task_id: The ID of the task to retrieve.

        Returns:
            The task dictionary, or None if not found.

        Raises:
            httpx.HTTPStatusError: If the API returns an error status other than 404.
        """
        response = self._make_request("GET", f"/tasks/{task_id}")
        if response.status_code == 404:
            return None
        response.raise_for_status()
        return response.json()

    def update_task(self, task_id: int, title: str) -> dict[str, Any] | None:
        """Update a task's title.

        Args:
            task_id: The ID of the task to update.
            title: The new title for the task.

        Returns:
            The updated task dictionary, or None if not found.

        Raises:
            httpx.HTTPStatusError: If the API returns an error status other than 404.
            ValueError: If the request fails with validation error.
        """
        response = self._make_request("PUT", f"/tasks/{task_id}", {"title": title})
        if response.status_code == 404:
            return None
        if response.status_code == 422:
            error_detail = response.json().get("detail", "Validation error")
            raise ValueError(f"Invalid input: {error_detail}")
        response.raise_for_status()
        return response.json()

    def delete_task(self, task_id: int) -> bool:
        """Delete a task.

        Args:
            task_id: The ID of the task to delete.

        Returns:
            True if the task was deleted, False if not found.

        Raises:
            httpx.HTTPStatusError: If the API returns an error status other than 404.
        """
        response = self._make_request("DELETE", f"/tasks/{task_id}")
        if response.status_code == 404:
            return False
        response.raise_for_status()
        return True

    def toggle_task(self, task_id: int) -> dict[str, Any] | None:
        """Toggle a task's completion status.

        Args:
            task_id: The ID of the task to toggle.

        Returns:
            The updated task dictionary, or None if not found.

        Raises:
            httpx.HTTPStatusError: If the API returns an error status other than 404.
        """
        response = self._make_request("PATCH", f"/tasks/{task_id}/toggle")
        if response.status_code == 404:
            return None
        response.raise_for_status()
        return response.json()

    def close(self) -> None:
        """Close the HTTP client."""
        self._client.close()

    def __enter__(self) -> "TodoAPIClient":
        """Enter context manager."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Exit context manager."""
        self.close()


# Global client instance (lazy initialized)
_api_client: TodoAPIClient | None = None


def get_api_client() -> TodoAPIClient:
    """Get the global API client instance.

    Returns:
        The global TodoAPIClient instance.
    """
    global _api_client
    if _api_client is None:
        from src.agent.config import API_BASE_URL
        _api_client = TodoAPIClient(base_url=API_BASE_URL)
    return _api_client


def set_api_client(client: TodoAPIClient) -> None:
    """Set the global API client instance (for testing).

    Args:
        client: The TodoAPIClient instance to use.
    """
    global _api_client
    _api_client = client


def reset_api_client() -> None:
    """Reset the global API client instance."""
    global _api_client
    if _api_client is not None:
        _api_client.close()
    _api_client = None
