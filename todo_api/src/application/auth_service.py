"""AuthService - Business logic for authentication operations."""

import os
from datetime import datetime, timedelta, timezone

import bcrypt
from jose import jwt, JWTError

from src.domain.user import User
from src.infrastructure.user_repository import UserRepository


# JWT Configuration
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "dev-secret-key-change-in-production")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "1440"))


class AuthService:
    """Service layer for authentication business logic."""

    def __init__(self, user_repository: UserRepository) -> None:
        """Initialize service with repository.

        Args:
            user_repository: User repository for database operations.
        """
        self._repository = user_repository

    def hash_password(self, password: str) -> str:
        """Hash a password using bcrypt.

        Args:
            password: Plain text password.

        Returns:
            Hashed password string.
        """
        salt = bcrypt.gensalt(rounds=12)
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify a password against its hash.

        Args:
            plain_password: Plain text password.
            hashed_password: Hashed password to compare against.

        Returns:
            True if password matches, False otherwise.
        """
        return bcrypt.checkpw(
            plain_password.encode('utf-8'),
            hashed_password.encode('utf-8')
        )

    def create_access_token(self, user_id: int, email: str) -> str:
        """Create a JWT access token.

        Args:
            user_id: User's ID.
            email: User's email.

        Returns:
            Encoded JWT token string.
        """
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode = {
            "sub": str(user_id),
            "email": email,
            "exp": expire,
            "iat": datetime.now(timezone.utc)
        }
        return jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)

    def verify_token(self, token: str) -> dict | None:
        """Verify and decode a JWT token.

        Args:
            token: JWT token string.

        Returns:
            Token payload dict if valid, None otherwise.
        """
        try:
            payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
            return payload
        except JWTError:
            return None

    def register(self, email: str, password: str) -> User | None:
        """Register a new user.

        Args:
            email: User's email address.
            password: User's plain text password.

        Returns:
            Created user if successful, None if email already exists.
        """
        if self._repository.email_exists(email):
            return None

        now = datetime.now(timezone.utc)
        user = User(
            email=email,
            password_hash=self.hash_password(password),
            created_at=now,
            updated_at=now
        )
        return self._repository.create(user)

    def authenticate(self, email: str, password: str) -> User | None:
        """Authenticate a user with email and password.

        Args:
            email: User's email address.
            password: User's plain text password.

        Returns:
            User if credentials are valid, None otherwise.
        """
        user = self._repository.get_by_email(email)
        if user is None:
            return None
        if not self.verify_password(password, user.password_hash):
            return None
        return user

    def get_user_by_id(self, user_id: int) -> User | None:
        """Get a user by ID.

        Args:
            user_id: User's ID.

        Returns:
            User if found, None otherwise.
        """
        return self._repository.get_by_id(user_id)
