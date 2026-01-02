"""Integration tests for end-to-end CLI flows."""

from io import StringIO
from unittest.mock import patch

import pytest

from src.application.task_service import TaskService
from src.infrastructure.task_repository import TaskRepository
from src.presentation.cli import TodoCLI


def create_cli() -> TodoCLI:
    """Create a fresh CLI instance for testing."""
    repository = TaskRepository()
    service = TaskService(repository)
    return TodoCLI(service)


class TestAddTaskFlow:
    """Integration tests for add task operation."""

    def test_add_task_flow(self) -> None:
        """Full add operation with valid input."""
        cli = create_cli()

        with patch("builtins.input", return_value="Buy groceries"):
            with patch("sys.stdout", new=StringIO()) as output:
                cli.handle_add_task()

        result = output.getvalue()
        assert "Task added successfully!" in result
        assert "ID: 1" in result
        assert "Title: Buy groceries" in result
        assert "Status: Incomplete" in result

    def test_add_task_empty_title(self) -> None:
        """Error for empty title."""
        cli = create_cli()

        with patch("builtins.input", return_value=""):
            with patch("sys.stdout", new=StringIO()) as output:
                cli.handle_add_task()

        result = output.getvalue()
        assert "Error: Task title cannot be empty." in result


class TestViewTasksFlow:
    """Integration tests for view tasks operation."""

    def test_view_empty_list(self) -> None:
        """Shows 'No tasks found' message for empty list."""
        cli = create_cli()

        with patch("sys.stdout", new=StringIO()) as output:
            cli.handle_view_tasks()

        result = output.getvalue()
        assert "No tasks found." in result

    def test_view_with_tasks(self) -> None:
        """Correct task list display with multiple tasks."""
        cli = create_cli()

        # Add some tasks
        with patch("builtins.input", return_value="Task 1"):
            cli.handle_add_task()
        with patch("builtins.input", return_value="Task 2"):
            cli.handle_add_task()

        # Toggle first task to complete
        with patch("builtins.input", return_value="1"):
            cli.handle_toggle_complete()

        # View tasks
        with patch("sys.stdout", new=StringIO()) as output:
            cli.handle_view_tasks()

        result = output.getvalue()
        assert "[X] 1. Task 1" in result
        assert "[ ] 2. Task 2" in result
        assert "Total: 2 tasks (1 complete, 1 incomplete)" in result


class TestUpdateTaskFlow:
    """Integration tests for update task operation."""

    def test_update_task_flow(self) -> None:
        """Full update operation with valid input."""
        cli = create_cli()

        # Add a task first
        with patch("builtins.input", return_value="Old title"):
            cli.handle_add_task()

        # Update the task
        with patch("builtins.input", side_effect=["1", "New title"]):
            with patch("sys.stdout", new=StringIO()) as output:
                cli.handle_update_task()

        result = output.getvalue()
        assert "Task updated successfully!" in result
        assert "ID: 1" in result
        assert "New Title: New title" in result

    def test_update_task_not_found(self) -> None:
        """Error for non-existent task ID."""
        cli = create_cli()

        with patch("builtins.input", side_effect=["99", "New title"]):
            with patch("sys.stdout", new=StringIO()) as output:
                cli.handle_update_task()

        result = output.getvalue()
        assert "Error: Task with ID 99 not found." in result


class TestDeleteTaskFlow:
    """Integration tests for delete task operation."""

    def test_delete_task_flow(self) -> None:
        """Full delete operation with valid input."""
        cli = create_cli()

        # Add a task first
        with patch("builtins.input", return_value="Task to delete"):
            cli.handle_add_task()

        # Delete the task
        with patch("builtins.input", return_value="1"):
            with patch("sys.stdout", new=StringIO()) as output:
                cli.handle_delete_task()

        result = output.getvalue()
        assert "Task deleted successfully!" in result
        assert 'Deleted: "Task to delete"' in result

    def test_delete_task_not_found(self) -> None:
        """Error for non-existent task ID."""
        cli = create_cli()

        with patch("builtins.input", return_value="99"):
            with patch("sys.stdout", new=StringIO()) as output:
                cli.handle_delete_task()

        result = output.getvalue()
        assert "Error: Task with ID 99 not found." in result


class TestToggleTaskFlow:
    """Integration tests for toggle complete operation."""

    def test_toggle_task_flow(self) -> None:
        """Full toggle operation."""
        cli = create_cli()

        # Add a task first
        with patch("builtins.input", return_value="Test task"):
            cli.handle_add_task()

        # Toggle to complete
        with patch("builtins.input", return_value="1"):
            with patch("sys.stdout", new=StringIO()) as output:
                cli.handle_toggle_complete()

        result = output.getvalue()
        assert "Task status updated!" in result
        assert "Status: Complete" in result

        # Toggle back to incomplete
        with patch("builtins.input", return_value="1"):
            with patch("sys.stdout", new=StringIO()) as output:
                cli.handle_toggle_complete()

        result = output.getvalue()
        assert "Status: Incomplete" in result


class TestInvalidInput:
    """Integration tests for invalid input handling."""

    def test_invalid_menu_choice_out_of_range(self) -> None:
        """Error for choice outside 1-6 range."""
        cli = create_cli()

        with patch("builtins.input", return_value="9"):
            with patch("sys.stdout", new=StringIO()) as output:
                result = cli.get_menu_choice()

        assert result is None
        assert "Error: Invalid choice. Please enter a number between 1 and 6." in output.getvalue()

    def test_invalid_menu_choice_non_numeric(self) -> None:
        """Error for non-numeric menu input."""
        cli = create_cli()

        with patch("builtins.input", return_value="hello"):
            with patch("sys.stdout", new=StringIO()) as output:
                result = cli.get_menu_choice()

        assert result is None
        assert "Error: Invalid input. Please enter a number between 1 and 6." in output.getvalue()

    def test_invalid_task_id_non_numeric(self) -> None:
        """Error for non-numeric task ID."""
        cli = create_cli()

        with patch("builtins.input", return_value="abc"):
            with patch("sys.stdout", new=StringIO()) as output:
                cli.handle_update_task()

        result = output.getvalue()
        assert "Error: Invalid input. Please enter a numeric ID." in result


class TestExitFlow:
    """Integration tests for exit operation."""

    def test_exit_displays_farewell(self) -> None:
        """Exit shows farewell message."""
        cli = create_cli()

        with patch("sys.stdout", new=StringIO()) as output:
            cli.handle_exit()

        result = output.getvalue()
        assert "Thank you for using Todo Application. Goodbye!" in result
        assert cli._running is False
