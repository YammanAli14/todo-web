"""Unit tests for the TaskService."""

import pytest

from src.application.task_service import TaskService
from src.infrastructure.task_repository import TaskRepository


class TestAddTask:
    """Tests for add_task method."""

    def test_add_task(self) -> None:
        """Task added with correct ID and title."""
        repository = TaskRepository()
        service = TaskService(repository)

        task = service.add_task("Buy groceries")

        assert task.id == 1
        assert task.title == "Buy groceries"
        assert task.is_complete is False

    def test_add_task_increments_id(self) -> None:
        """Sequential IDs for multiple adds."""
        repository = TaskRepository()
        service = TaskService(repository)

        task1 = service.add_task("Task 1")
        task2 = service.add_task("Task 2")
        task3 = service.add_task("Task 3")

        assert task1.id == 1
        assert task2.id == 2
        assert task3.id == 3

    def test_add_task_invalid_title(self) -> None:
        """Raises ValueError for invalid title."""
        repository = TaskRepository()
        service = TaskService(repository)

        with pytest.raises(ValueError) as exc_info:
            service.add_task("")
        assert str(exc_info.value) == "Task title cannot be empty."


class TestGetAllTasks:
    """Tests for get_all_tasks method."""

    def test_get_all_tasks_empty(self) -> None:
        """Returns empty list when no tasks."""
        repository = TaskRepository()
        service = TaskService(repository)

        tasks = service.get_all_tasks()

        assert tasks == []

    def test_get_all_tasks_with_items(self) -> None:
        """Returns all tasks in creation order."""
        repository = TaskRepository()
        service = TaskService(repository)
        service.add_task("Task 1")
        service.add_task("Task 2")
        service.add_task("Task 3")

        tasks = service.get_all_tasks()

        assert len(tasks) == 3
        assert tasks[0].title == "Task 1"
        assert tasks[1].title == "Task 2"
        assert tasks[2].title == "Task 3"


class TestGetTask:
    """Tests for get_task method."""

    def test_get_task_exists(self) -> None:
        """Returns correct task for valid ID."""
        repository = TaskRepository()
        service = TaskService(repository)
        service.add_task("Test task")

        task = service.get_task(1)

        assert task is not None
        assert task.id == 1
        assert task.title == "Test task"

    def test_get_task_not_exists(self) -> None:
        """Returns None for invalid ID."""
        repository = TaskRepository()
        service = TaskService(repository)

        task = service.get_task(99)

        assert task is None


class TestUpdateTask:
    """Tests for update_task method."""

    def test_update_task_exists(self) -> None:
        """Updates title correctly for valid ID."""
        repository = TaskRepository()
        service = TaskService(repository)
        service.add_task("Old title")

        task = service.update_task(1, "New title")

        assert task is not None
        assert task.id == 1
        assert task.title == "New title"

    def test_update_task_not_exists(self) -> None:
        """Returns None for non-existent task."""
        repository = TaskRepository()
        service = TaskService(repository)

        task = service.update_task(99, "New title")

        assert task is None

    def test_update_task_invalid_title(self) -> None:
        """Raises ValueError for invalid title."""
        repository = TaskRepository()
        service = TaskService(repository)
        service.add_task("Test task")

        with pytest.raises(ValueError) as exc_info:
            service.update_task(1, "   ")
        assert str(exc_info.value) == "Task title cannot be empty."


class TestDeleteTask:
    """Tests for delete_task method."""

    def test_delete_task_exists(self) -> None:
        """Removes and returns task for valid ID."""
        repository = TaskRepository()
        service = TaskService(repository)
        service.add_task("Task to delete")

        deleted = service.delete_task(1)

        assert deleted is not None
        assert deleted.title == "Task to delete"
        assert service.get_task(1) is None

    def test_delete_task_not_exists(self) -> None:
        """Returns None for non-existent task."""
        repository = TaskRepository()
        service = TaskService(repository)

        deleted = service.delete_task(99)

        assert deleted is None


class TestToggleTaskComplete:
    """Tests for toggle_task_complete method."""

    def test_toggle_task_exists_to_complete(self) -> None:
        """Toggles incomplete task to complete."""
        repository = TaskRepository()
        service = TaskService(repository)
        service.add_task("Test task")

        task = service.toggle_task_complete(1)

        assert task is not None
        assert task.is_complete is True

    def test_toggle_task_exists_to_incomplete(self) -> None:
        """Toggles complete task to incomplete."""
        repository = TaskRepository()
        service = TaskService(repository)
        service.add_task("Test task")
        service.toggle_task_complete(1)  # Make it complete

        task = service.toggle_task_complete(1)  # Toggle back

        assert task is not None
        assert task.is_complete is False

    def test_toggle_task_not_exists(self) -> None:
        """Returns None for non-existent task."""
        repository = TaskRepository()
        service = TaskService(repository)

        task = service.toggle_task_complete(99)

        assert task is None
