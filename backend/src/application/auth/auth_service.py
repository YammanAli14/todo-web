"""Authentication service for user signup and signin."""
from datetime import datetime
from typing import Optional, Tuple
from sqlmodel import Session

from src.domain.user import User
from src.infrastructure.repositories.user_repository import UserRepository
from src.application.auth.password import hash_password, verify_password
from src.application.auth.jwt import create_access_token


class AuthService:
    """Service for handling authentication operations."""

    def __init__(self, session: Session):
        """
        Initialize auth service with database session.

        Args:
            session: SQLModel database session
        """
        self.repository = UserRepository(session)

    def signup(self, email: str, password: str) -> Tuple[User, str]:
        """
        Register a new user.

        Args:
            email: User email address
            password: User plaintext password

        Returns:
            Tuple[User, str]: Created user and JWT access token

        Raises:
            ValueError: If email already exists or validation fails
        """
        # Check if user already exists
        existing_user = self.repository.get_by_email(email)
        if existing_user:
            raise ValueError("Email already registered")

        # Validate email format (basic check)
        if "@" not in email or "." not in email:
            raise ValueError("Invalid email format")

        # Validate password strength (basic check)
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters long")

        # Create user with hashed password
        password_hash = hash_password(password)
        user = User(
            email=email,
            password_hash=password_hash,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )

        # Save to database
        user = self.repository.create(user)

        # Generate JWT token
        access_token = create_access_token(data={"sub": str(user.id)})

        return user, access_token

    def signin(self, email: str, password: str) -> Tuple[User, str]:
        """
        Authenticate a user and return JWT token.

        Args:
            email: User email address
            password: User plaintext password

        Returns:
            Tuple[User, str]: Authenticated user and JWT access token

        Raises:
            ValueError: If credentials are invalid
        """
        # Get user by email
        user = self.repository.get_by_email(email)
        if not user:
            raise ValueError("Invalid email or password")

        # Verify password
        if not verify_password(password, user.password_hash):
            raise ValueError("Invalid email or password")

        # Update last login time
        user.updated_at = datetime.utcnow()
        self.repository.update(user)

        # Generate JWT token
        access_token = create_access_token(data={"sub": str(user.id)})

        return user, access_token

    def get_current_user(self, user_id: int) -> Optional[User]:
        """
        Get user by ID (for JWT authentication).

        Args:
            user_id: User ID from JWT token

        Returns:
            Optional[User]: User if found, None otherwise
        """
        return self.repository.get_by_id(user_id)
