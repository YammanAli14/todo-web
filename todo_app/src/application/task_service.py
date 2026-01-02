"""TaskService - Application layer for task operations."""

from src.domain.task import Task
from src.infrastructure.task_repository import TaskRepository


class TaskService:
    """Service layer for task operations.

    Orchestrates use cases by coordinating between repository and domain.
    """

    def __init__(self, repository: TaskRepository) -> None:
        """Initialize service with repository.

        Args:
            repository: The task repository for storage.
        """
        self._repository = repository

    def add_task(self, title: str) -> Task:
        """Add a new task.

        Args:
            title: The task title (will be validated).

        Returns:
            The created task.

        Raises:
            ValueError: If title is invalid.
        """
        validated_title = Task.validate_title(title)
        task_id = self._repository.get_next_id()
        task = Task(id=task_id, title=validated_title)
        return self._repository.add(task)

    def get_all_tasks(self) -> list[Task]:
        """Get all tasks.

        Returns:
            List of all tasks in creation order.
        """
        return self._repository.get_all()

    def get_task(self, task_id: int) -> Task | None:
        """Get a task by ID.

        Args:
            task_id: The ID of the task to retrieve.

        Returns:
            The task if found, None otherwise.
        """
        return self._repository.get_by_id(task_id)

    def update_task(self, task_id: int, new_title: str) -> Task | None:
        """Update a task's title.

        Args:
            task_id: The ID of the task to update.
            new_title: The new title (will be validated).

        Returns:
            The updated task if found, None otherwise.

        Raises:
            ValueError: If new_title is invalid.
        """
        validated_title = Task.validate_title(new_title)
        task = self._repository.get_by_id(task_id)
        if task is None:
            return None
        task.title = validated_title
        return self._repository.update(task)

    def delete_task(self, task_id: int) -> Task | None:
        """Delete a task.

        Args:
            task_id: The ID of the task to delete.

        Returns:
            The deleted task if found, None otherwise.
        """
        return self._repository.delete(task_id)

    def toggle_task_complete(self, task_id: int) -> Task | None:
        """Toggle a task's completion status.

        Args:
            task_id: The ID of the task to toggle.

        Returns:
            The updated task if found, None otherwise.
        """
        task = self._repository.get_by_id(task_id)
        if task is None:
            return None
        task.toggle_complete()
        return self._repository.update(task)
