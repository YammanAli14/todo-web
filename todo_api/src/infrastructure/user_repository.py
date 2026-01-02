"""UserRepository - Database operations for User entity."""

from sqlmodel import Session, select

from src.domain.user import User


class UserRepository:
    """Repository for User database operations."""

    def __init__(self, session: Session) -> None:
        """Initialize repository with database session.

        Args:
            session: SQLModel database session.
        """
        self._session = session

    def create(self, user: User) -> User:
        """Create a new user in the database.

        Args:
            user: User entity to create.

        Returns:
            Created user with assigned ID.
        """
        self._session.add(user)
        self._session.commit()
        self._session.refresh(user)
        return user

    def get_by_id(self, user_id: int) -> User | None:
        """Get a user by ID.

        Args:
            user_id: ID of user to retrieve.

        Returns:
            User if found, None otherwise.
        """
        return self._session.get(User, user_id)

    def get_by_email(self, email: str) -> User | None:
        """Get a user by email.

        Args:
            email: Email address to search for.

        Returns:
            User if found, None otherwise.
        """
        statement = select(User).where(User.email == email)
        return self._session.exec(statement).first()

    def email_exists(self, email: str) -> bool:
        """Check if email is already registered.

        Args:
            email: Email address to check.

        Returns:
            True if email exists, False otherwise.
        """
        return self.get_by_email(email) is not None
