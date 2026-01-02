"""Password hashing and verification utilities."""
import bcrypt


def hash_password(password: str) -> str:
    """
    Hash a plaintext password using bcrypt.

    Args:
        password: Plaintext password

    Returns:
        str: Hashed password

    Example:
        >>> hashed = hash_password("mysecretpassword")
        >>> hashed.startswith("$2b$")
        True
    """
    # Convert password to bytes and hash
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plaintext password against a hashed password.

    Args:
        plain_password: Plaintext password to verify
        hashed_password: Hashed password from database

    Returns:
        bool: True if password matches, False otherwise

    Example:
        >>> hashed = hash_password("mysecretpassword")
        >>> verify_password("mysecretpassword", hashed)
        True
        >>> verify_password("wrongpassword", hashed)
        False
    """
    password_bytes = plain_password.encode('utf-8')
    hashed_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hashed_bytes)
