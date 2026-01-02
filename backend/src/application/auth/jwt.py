"""JWT token creation and validation utilities."""
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
import os


SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-here-change-in-production-min-32-chars")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT access token.

    Args:
        data: Dictionary of claims to encode (typically {"sub": user_id})
        expires_delta: Optional custom expiration time

    Returns:
        str: Encoded JWT token

    Example:
        >>> token = create_access_token({"sub": "123"})
        >>> isinstance(token, str)
        True
    """
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def decode_access_token(token: str) -> Optional[dict]:
    """
    Decode and validate a JWT access token.

    Args:
        token: JWT token string

    Returns:
        Optional[dict]: Decoded token payload if valid, None if invalid

    Example:
        >>> token = create_access_token({"sub": "123"})
        >>> payload = decode_access_token(token)
        >>> payload["sub"]
        '123'
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None


def get_user_id_from_token(token: str) -> Optional[str]:
    """
    Extract user ID from JWT token.

    Args:
        token: JWT token string

    Returns:
        Optional[str]: User ID if token is valid, None otherwise

    Example:
        >>> token = create_access_token({"sub": "123"})
        >>> get_user_id_from_token(token)
        '123'
    """
    payload = decode_access_token(token)
    if payload is None:
        return None

    return payload.get("sub")
