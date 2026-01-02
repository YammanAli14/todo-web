"""TaskService - Business logic for task operations."""

from datetime import datetime, timezone

from src.domain.task import Task
from src.infrastructure.task_repository import TaskRepository


class TaskService:
    """Service layer for task business logic."""

    def __init__(self, repository: TaskRepository) -> None:
        """Initialize service with repository.

        Args:
            repository: Task repository for database operations.
        """
        self._repository = repository

    def create_task(self, title: str, user_id: int) -> Task:
        """Create a new task for a user.

        Args:
            title: Task title (already validated by schema).
            user_id: ID of the owning user.

        Returns:
            Created task with assigned ID.
        """
        now = datetime.now(timezone.utc)
        task = Task(
            title=title,
            is_complete=False,
            user_id=user_id,
            created_at=now,
            updated_at=now
        )
        return self._repository.create(task)

    def get_all_tasks(self, user_id: int) -> list[Task]:
        """Get all tasks for a user.

        Args:
            user_id: ID of the owning user.

        Returns:
            List of user's tasks ordered by ID.
        """
        return self._repository.get_all(user_id)

    def get_task(self, task_id: int, user_id: int) -> Task | None:
        """Get a task by ID for a specific user.

        Args:
            task_id: ID of task to retrieve.
            user_id: ID of the owning user.

        Returns:
            Task if found and owned by user, None otherwise.
        """
        return self._repository.get_by_id(task_id, user_id)

    def update_task(self, task_id: int, title: str, user_id: int) -> Task | None:
        """Update a task's title for a specific user.

        Args:
            task_id: ID of task to update.
            title: New title (already validated by schema).
            user_id: ID of the owning user.

        Returns:
            Updated task if found and owned, None otherwise.
        """
        task = self._repository.get_by_id(task_id, user_id)
        if task is None:
            return None
        task.title = title
        task.updated_at = datetime.now(timezone.utc)
        return self._repository.update(task)

    def delete_task(self, task_id: int, user_id: int) -> bool:
        """Delete a task for a specific user.

        Args:
            task_id: ID of task to delete.
            user_id: ID of the owning user.

        Returns:
            True if deleted, False if not found or not owned.
        """
        return self._repository.delete(task_id, user_id)

    def toggle_task_complete(self, task_id: int, user_id: int) -> Task | None:
        """Toggle a task's completion status for a specific user.

        Args:
            task_id: ID of task to toggle.
            user_id: ID of the owning user.

        Returns:
            Updated task if found and owned, None otherwise.
        """
        task = self._repository.get_by_id(task_id, user_id)
        if task is None:
            return None
        task.is_complete = not task.is_complete
        task.updated_at = datetime.now(timezone.utc)
        return self._repository.update(task)
