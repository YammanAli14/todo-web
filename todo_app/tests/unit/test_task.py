"""Unit tests for the Task entity."""

import pytest

from src.domain.task import Task


class TestTaskCreation:
    """Tests for Task instantiation."""

    def test_task_creation(self) -> None:
        """Task created with correct fields."""
        task = Task(id=1, title="Buy groceries")
        assert task.id == 1
        assert task.title == "Buy groceries"
        assert task.is_complete is False

    def test_task_creation_with_complete_status(self) -> None:
        """Task can be created with is_complete=True."""
        task = Task(id=1, title="Done task", is_complete=True)
        assert task.is_complete is True

    def test_task_default_incomplete(self) -> None:
        """New task is_complete defaults to False."""
        task = Task(id=1, title="Test")
        assert task.is_complete is False


class TestValidateTitle:
    """Tests for title validation."""

    def test_validate_title_valid(self) -> None:
        """Valid title passes and is stripped."""
        result = Task.validate_title("  Buy groceries  ")
        assert result == "Buy groceries"

    def test_validate_title_empty(self) -> None:
        """Empty title raises ValueError."""
        with pytest.raises(ValueError) as exc_info:
            Task.validate_title("")
        assert str(exc_info.value) == "Task title cannot be empty."

    def test_validate_title_whitespace(self) -> None:
        """Whitespace-only title raises ValueError."""
        with pytest.raises(ValueError) as exc_info:
            Task.validate_title("   ")
        assert str(exc_info.value) == "Task title cannot be empty."

    def test_validate_title_too_long(self) -> None:
        """Title exceeding 200 chars raises ValueError."""
        long_title = "a" * 201
        with pytest.raises(ValueError) as exc_info:
            Task.validate_title(long_title)
        assert str(exc_info.value) == "Task title must be 200 characters or less."

    def test_validate_title_exactly_200(self) -> None:
        """Title with exactly 200 chars passes."""
        title_200 = "a" * 200
        result = Task.validate_title(title_200)
        assert result == title_200
        assert len(result) == 200


class TestToggleComplete:
    """Tests for toggle_complete method."""

    def test_toggle_complete_to_complete(self) -> None:
        """Toggling incomplete task makes it complete."""
        task = Task(id=1, title="Test", is_complete=False)
        task.toggle_complete()
        assert task.is_complete is True

    def test_toggle_complete_to_incomplete(self) -> None:
        """Toggling complete task makes it incomplete."""
        task = Task(id=1, title="Test", is_complete=True)
        task.toggle_complete()
        assert task.is_complete is False
