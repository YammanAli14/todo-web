"""TaskRepository - Database operations for Task entity."""

from sqlmodel import Session, select

from src.domain.task import Task


class TaskRepository:
    """Repository for Task database operations."""

    def __init__(self, session: Session) -> None:
        """Initialize repository with database session.

        Args:
            session: SQLModel database session.
        """
        self._session = session

    def create(self, task: Task) -> Task:
        """Create a new task in the database.

        Args:
            task: Task entity to create.

        Returns:
            Created task with assigned ID.
        """
        self._session.add(task)
        self._session.commit()
        self._session.refresh(task)
        return task

    def get_by_id(self, task_id: int, user_id: int) -> Task | None:
        """Get a task by ID for a specific user.

        Args:
            task_id: ID of task to retrieve.
            user_id: ID of the owning user.

        Returns:
            Task if found and owned by user, None otherwise.
        """
        statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
        return self._session.exec(statement).first()

    def get_all(self, user_id: int) -> list[Task]:
        """Get all tasks for a user ordered by ID.

        Args:
            user_id: ID of the owning user.

        Returns:
            List of user's tasks, ordered by ID ascending.
        """
        statement = select(Task).where(Task.user_id == user_id).order_by(Task.id)
        return list(self._session.exec(statement).all())

    def update(self, task: Task) -> Task:
        """Update an existing task.

        Args:
            task: Task entity with updated values.

        Returns:
            Updated task.
        """
        self._session.add(task)
        self._session.commit()
        self._session.refresh(task)
        return task

    def delete(self, task_id: int, user_id: int) -> bool:
        """Delete a task by ID for a specific user.

        Args:
            task_id: ID of task to delete.
            user_id: ID of the owning user.

        Returns:
            True if deleted, False if not found or not owned.
        """
        task = self.get_by_id(task_id, user_id)
        if task is None:
            return False
        self._session.delete(task)
        self._session.commit()
        return True
