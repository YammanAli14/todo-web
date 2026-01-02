"""TaskRepository - In-memory storage for Task entities."""

from src.domain.task import Task


class TaskRepository:
    """In-memory repository for Task storage.

    Provides CRUD operations for tasks using a dictionary for O(1) lookups.
    IDs are generated sequentially starting at 1.
    """

    def __init__(self) -> None:
        """Initialize empty task storage with ID counter starting at 1."""
        self._tasks: dict[int, Task] = {}
        self._next_id: int = 1

    def get_next_id(self) -> int:
        """Get the next available task ID and increment counter.

        Returns:
            The next unique task ID.
        """
        current_id = self._next_id
        self._next_id += 1
        return current_id

    def add(self, task: Task) -> Task:
        """Add a task to storage.

        Args:
            task: The task to store.

        Returns:
            The stored task.
        """
        self._tasks[task.id] = task
        return task

    def get_by_id(self, task_id: int) -> Task | None:
        """Get a task by ID.

        Args:
            task_id: The ID of the task to retrieve.

        Returns:
            The task if found, None otherwise.
        """
        return self._tasks.get(task_id)

    def get_all(self) -> list[Task]:
        """Get all tasks in insertion order.

        Returns:
            List of all tasks, ordered by insertion (ID order).
        """
        return list(self._tasks.values())

    def update(self, task: Task) -> Task | None:
        """Update an existing task.

        Args:
            task: The task with updated values.

        Returns:
            The updated task if found, None if task ID doesn't exist.
        """
        if task.id not in self._tasks:
            return None
        self._tasks[task.id] = task
        return task

    def delete(self, task_id: int) -> Task | None:
        """Delete a task by ID.

        Args:
            task_id: The ID of the task to delete.

        Returns:
            The deleted task if found, None otherwise.
        """
        return self._tasks.pop(task_id, None)
