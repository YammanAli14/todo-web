"""Todo service for business logic."""
from datetime import datetime
from typing import List
from sqlmodel import Session

from src.domain.todo import Todo
from src.infrastructure.repositories.todo_repository import TodoRepository


class TodoService:
    """Service for handling todo operations."""

    def __init__(self, session: Session):
        """
        Initialize todo service with database session.

        Args:
            session: SQLModel database session
        """
        self.repository = TodoRepository(session)

    def create_todo(self, user_id: int, title: str) -> Todo:
        """
        Create a new todo for a user.

        Args:
            user_id: User ID (owner)
            title: Todo title

        Returns:
            Todo: Created todo

        Raises:
            ValueError: If title is empty or too long
        """
        # Validate title
        if not title or title.strip() == "":
            raise ValueError("Title cannot be empty")

        if len(title) > 500:
            raise ValueError("Title cannot exceed 500 characters")

        # Create todo
        todo = Todo(
            user_id=user_id,
            title=title.strip(),
            is_complete=False,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )

        return self.repository.create(todo)

    def get_all_todos(self, user_id: int) -> List[Todo]:
        """
        Get all todos for a user.

        Args:
            user_id: User ID

        Returns:
            List[Todo]: List of todos
        """
        return self.repository.get_all_by_user(user_id)

    def get_todo(self, todo_id: int, user_id: int) -> Todo:
        """
        Get a specific todo for a user.

        Args:
            todo_id: Todo ID
            user_id: User ID (for authorization)

        Returns:
            Todo: Todo if found

        Raises:
            ValueError: If todo not found or doesn't belong to user
        """
        todo = self.repository.get_by_id(todo_id, user_id)
        if not todo:
            raise ValueError("Todo not found")
        return todo

    def update_todo(self, todo_id: int, user_id: int, title: str) -> Todo:
        """
        Update todo title.

        Args:
            todo_id: Todo ID
            user_id: User ID (for authorization)
            title: New title

        Returns:
            Todo: Updated todo

        Raises:
            ValueError: If todo not found or validation fails
        """
        # Get existing todo
        todo = self.get_todo(todo_id, user_id)

        # Validate title
        if not title or title.strip() == "":
            raise ValueError("Title cannot be empty")

        if len(title) > 500:
            raise ValueError("Title cannot exceed 500 characters")

        # Update todo
        todo.title = title.strip()
        todo.updated_at = datetime.utcnow()

        return self.repository.update(todo)

    def toggle_complete(self, todo_id: int, user_id: int) -> Todo:
        """
        Toggle todo completion status.

        Args:
            todo_id: Todo ID
            user_id: User ID (for authorization)

        Returns:
            Todo: Updated todo

        Raises:
            ValueError: If todo not found
        """
        # Get existing todo
        todo = self.get_todo(todo_id, user_id)

        # Toggle completion
        todo.is_complete = not todo.is_complete
        todo.updated_at = datetime.utcnow()

        return self.repository.update(todo)

    def delete_todo(self, todo_id: int, user_id: int) -> bool:
        """
        Delete a todo.

        Args:
            todo_id: Todo ID
            user_id: User ID (for authorization)

        Returns:
            bool: True if deleted

        Raises:
            ValueError: If todo not found
        """
        deleted = self.repository.delete(todo_id, user_id)
        if not deleted:
            raise ValueError("Todo not found")
        return True
