"""Todo repository for database operations."""
from typing import List, Optional
from sqlmodel import Session, select

from src.domain.todo import Todo


class TodoRepository:
    """Repository for Todo entity database operations."""

    def __init__(self, session: Session):
        """
        Initialize repository with database session.

        Args:
            session: SQLModel database session
        """
        self.session = session

    def create(self, todo: Todo) -> Todo:
        """
        Create a new todo in the database.

        Args:
            todo: Todo entity to create

        Returns:
            Todo: Created todo with ID
        """
        self.session.add(todo)
        self.session.commit()
        self.session.refresh(todo)
        return todo

    def get_by_id(self, todo_id: int, user_id: int) -> Optional[Todo]:
        """
        Get todo by ID for a specific user.

        Args:
            todo_id: Todo ID
            user_id: User ID (for authorization)

        Returns:
            Optional[Todo]: Todo if found and belongs to user, None otherwise
        """
        statement = select(Todo).where(Todo.id == todo_id, Todo.user_id == user_id)
        return self.session.exec(statement).first()

    def get_all_by_user(self, user_id: int) -> List[Todo]:
        """
        Get all todos for a specific user.

        Args:
            user_id: User ID

        Returns:
            List[Todo]: List of todos belonging to user
        """
        statement = select(Todo).where(Todo.user_id == user_id).order_by(Todo.created_at.desc())
        return list(self.session.exec(statement).all())

    def update(self, todo: Todo) -> Todo:
        """
        Update todo in the database.

        Args:
            todo: Todo entity to update

        Returns:
            Todo: Updated todo
        """
        self.session.add(todo)
        self.session.commit()
        self.session.refresh(todo)
        return todo

    def delete(self, todo_id: int, user_id: int) -> bool:
        """
        Delete todo by ID for a specific user.

        Args:
            todo_id: Todo ID
            user_id: User ID (for authorization)

        Returns:
            bool: True if deleted, False if not found
        """
        todo = self.get_by_id(todo_id, user_id)
        if todo:
            self.session.delete(todo)
            self.session.commit()
            return True
        return False
