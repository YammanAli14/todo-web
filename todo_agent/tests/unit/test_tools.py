"""Unit Tests for MCP Tools.

This module contains unit tests for all MCP task tools.
Tests use mocked API client to verify tool behavior.
"""

import pytest
from unittest.mock import patch


class TestCreateTask:
    """Tests for the create_task tool."""

    def test_create_task_success(self, patched_api_client, sample_task):
        """Test successful task creation."""
        from src.tools.task_tools import _impl_create_task

        patched_api_client.create_task.return_value = sample_task

        result = _impl_create_task(title="Buy groceries")

        assert "Task created successfully!" in result
        assert "ID: 1" in result
        assert "Title: Buy groceries" in result
        assert "Status: Incomplete" in result
        patched_api_client.create_task.assert_called_once_with("Buy groceries")

    def test_create_task_validation_error(self, patched_api_client):
        """Test task creation with validation error."""
        from src.tools.task_tools import _impl_create_task

        patched_api_client.create_task.side_effect = ValueError("Invalid input: Title too long")

        result = _impl_create_task(title="x" * 300)

        assert "Error:" in result
        assert "Invalid input" in result

    def test_create_task_connection_error(self, patched_api_client):
        """Test task creation when API is unavailable."""
        from src.tools.task_tools import _impl_create_task

        patched_api_client.create_task.side_effect = Exception("Connection failed")

        result = _impl_create_task(title="Test task")

        assert "Error creating task" in result
        assert "Unable to connect" in result


class TestListTasks:
    """Tests for the list_tasks tool."""

    def test_list_tasks_empty(self, patched_api_client):
        """Test listing tasks when list is empty."""
        from src.tools.task_tools import _impl_list_tasks

        patched_api_client.list_tasks.return_value = []

        result = _impl_list_tasks()

        assert "No tasks found" in result
        assert "empty" in result

    def test_list_tasks_with_data(self, patched_api_client, sample_task_list):
        """Test listing tasks with existing tasks."""
        from src.tools.task_tools import _impl_list_tasks

        patched_api_client.list_tasks.return_value = sample_task_list

        result = _impl_list_tasks()

        assert "Your tasks:" in result
        assert "[ ] Task 1: Buy groceries" in result
        assert "[x] Task 2: Finish homework" in result

    def test_list_tasks_connection_error(self, patched_api_client):
        """Test listing tasks when API is unavailable."""
        from src.tools.task_tools import _impl_list_tasks

        patched_api_client.list_tasks.side_effect = Exception("Connection failed")

        result = _impl_list_tasks()

        assert "Error listing tasks" in result


class TestGetTask:
    """Tests for the get_task tool."""

    def test_get_task_success(self, patched_api_client, sample_task):
        """Test getting a task successfully."""
        from src.tools.task_tools import _impl_get_task

        patched_api_client.get_task.return_value = sample_task

        result = _impl_get_task(task_id=1)

        assert "Task 1:" in result
        assert "Title: Buy groceries" in result
        assert "Status: Incomplete" in result
        patched_api_client.get_task.assert_called_once_with(1)

    def test_get_task_not_found(self, patched_api_client):
        """Test getting a task that doesn't exist."""
        from src.tools.task_tools import _impl_get_task

        patched_api_client.get_task.return_value = None

        result = _impl_get_task(task_id=999)

        assert "Error" in result
        assert "999" in result
        assert "not found" in result

    def test_get_task_connection_error(self, patched_api_client):
        """Test getting a task when API is unavailable."""
        from src.tools.task_tools import _impl_get_task

        patched_api_client.get_task.side_effect = Exception("Connection failed")

        result = _impl_get_task(task_id=1)

        assert "Error getting task" in result


class TestUpdateTask:
    """Tests for the update_task tool."""

    def test_update_task_success(self, patched_api_client, sample_task):
        """Test updating a task successfully."""
        from src.tools.task_tools import _impl_update_task

        updated_task = {**sample_task, "title": "Buy groceries and milk"}
        patched_api_client.update_task.return_value = updated_task

        result = _impl_update_task(task_id=1, title="Buy groceries and milk")

        assert "updated successfully" in result
        assert "New title: Buy groceries and milk" in result
        patched_api_client.update_task.assert_called_once_with(1, "Buy groceries and milk")

    def test_update_task_not_found(self, patched_api_client):
        """Test updating a task that doesn't exist."""
        from src.tools.task_tools import _impl_update_task

        patched_api_client.update_task.return_value = None

        result = _impl_update_task(task_id=999, title="New title")

        assert "Error" in result
        assert "999" in result
        assert "not found" in result

    def test_update_task_validation_error(self, patched_api_client):
        """Test updating a task with invalid input."""
        from src.tools.task_tools import _impl_update_task

        patched_api_client.update_task.side_effect = ValueError("Invalid input: Title too long")

        result = _impl_update_task(task_id=1, title="x" * 300)

        assert "Error:" in result
        assert "Invalid input" in result

    def test_update_task_connection_error(self, patched_api_client):
        """Test updating a task when API is unavailable."""
        from src.tools.task_tools import _impl_update_task

        patched_api_client.update_task.side_effect = Exception("Connection failed")

        result = _impl_update_task(task_id=1, title="New title")

        assert "Error updating task" in result


class TestDeleteTask:
    """Tests for the delete_task tool."""

    def test_delete_task_success(self, patched_api_client):
        """Test deleting a task successfully."""
        from src.tools.task_tools import _impl_delete_task

        patched_api_client.delete_task.return_value = True

        result = _impl_delete_task(task_id=1)

        assert "deleted successfully" in result
        assert "1" in result
        patched_api_client.delete_task.assert_called_once_with(1)

    def test_delete_task_not_found(self, patched_api_client):
        """Test deleting a task that doesn't exist."""
        from src.tools.task_tools import _impl_delete_task

        patched_api_client.delete_task.return_value = False

        result = _impl_delete_task(task_id=999)

        assert "Error" in result
        assert "999" in result
        assert "not found" in result

    def test_delete_task_connection_error(self, patched_api_client):
        """Test deleting a task when API is unavailable."""
        from src.tools.task_tools import _impl_delete_task

        patched_api_client.delete_task.side_effect = Exception("Connection failed")

        result = _impl_delete_task(task_id=1)

        assert "Error deleting task" in result


class TestToggleTask:
    """Tests for the toggle_task tool."""

    def test_toggle_task_to_complete(self, patched_api_client, sample_task):
        """Test toggling a task to complete."""
        from src.tools.task_tools import _impl_toggle_task

        toggled_task = {**sample_task, "is_complete": True}
        patched_api_client.toggle_task.return_value = toggled_task

        result = _impl_toggle_task(task_id=1)

        assert "Task 1" in result
        assert "complete" in result
        patched_api_client.toggle_task.assert_called_once_with(1)

    def test_toggle_task_to_incomplete(self, patched_api_client, sample_task_complete):
        """Test toggling a task to incomplete."""
        from src.tools.task_tools import _impl_toggle_task

        toggled_task = {**sample_task_complete, "is_complete": False}
        patched_api_client.toggle_task.return_value = toggled_task

        result = _impl_toggle_task(task_id=2)

        assert "Task 2" in result
        assert "incomplete" in result

    def test_toggle_task_not_found(self, patched_api_client):
        """Test toggling a task that doesn't exist."""
        from src.tools.task_tools import _impl_toggle_task

        patched_api_client.toggle_task.return_value = None

        result = _impl_toggle_task(task_id=999)

        assert "Error" in result
        assert "999" in result
        assert "not found" in result

    def test_toggle_task_connection_error(self, patched_api_client):
        """Test toggling a task when API is unavailable."""
        from src.tools.task_tools import _impl_toggle_task

        patched_api_client.toggle_task.side_effect = Exception("Connection failed")

        result = _impl_toggle_task(task_id=1)

        assert "Error toggling task" in result
