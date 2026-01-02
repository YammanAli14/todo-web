"""User repository for database operations."""
from typing import Optional
from sqlmodel import Session, select

from src.domain.user import User


class UserRepository:
    """Repository for User entity database operations."""

    def __init__(self, session: Session):
        """
        Initialize repository with database session.

        Args:
            session: SQLModel database session
        """
        self.session = session

    def create(self, user: User) -> User:
        """
        Create a new user in the database.

        Args:
            user: User entity to create

        Returns:
            User: Created user with ID

        Raises:
            IntegrityError: If email already exists
        """
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    def get_by_id(self, user_id: int) -> Optional[User]:
        """
        Get user by ID.

        Args:
            user_id: User ID

        Returns:
            Optional[User]: User if found, None otherwise
        """
        return self.session.get(User, user_id)

    def get_by_email(self, email: str) -> Optional[User]:
        """
        Get user by email address.

        Args:
            email: Email address

        Returns:
            Optional[User]: User if found, None otherwise
        """
        statement = select(User).where(User.email == email)
        return self.session.exec(statement).first()

    def update(self, user: User) -> User:
        """
        Update user in the database.

        Args:
            user: User entity to update

        Returns:
            User: Updated user
        """
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    def delete(self, user_id: int) -> bool:
        """
        Delete user by ID.

        Args:
            user_id: User ID

        Returns:
            bool: True if deleted, False if not found
        """
        user = self.get_by_id(user_id)
        if user:
            self.session.delete(user)
            self.session.commit()
            return True
        return False
