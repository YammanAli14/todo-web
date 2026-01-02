"""Authentication endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from src.application.auth_service import AuthService
from src.domain.user import User
from src.presentation.dependencies import get_auth_service, get_current_user
from src.presentation.schemas import (
    UserCreate,
    UserResponse,
    LoginRequest,
    Token,
)

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
def register(
    user_data: UserCreate,
    service: AuthService = Depends(get_auth_service)
) -> UserResponse:
    """Register a new user.

    Args:
        user_data: User registration data.
        service: AuthService from dependency.

    Returns:
        Created user data (without password).

    Raises:
        HTTPException: 409 if email already registered.
    """
    user = service.register(user_data.email, user_data.password)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )
    return UserResponse(
        id=user.id,
        email=user.email,
        created_at=user.created_at
    )


@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    service: AuthService = Depends(get_auth_service)
) -> Token:
    """Login and get access token.

    Uses OAuth2 password flow for compatibility with OpenAPI.
    Username field is used for email.

    Args:
        form_data: OAuth2 form with username (email) and password.
        service: AuthService from dependency.

    Returns:
        JWT access token.

    Raises:
        HTTPException: 401 if credentials are invalid.
    """
    user = service.authenticate(form_data.username, form_data.password)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = service.create_access_token(user.id, user.email)
    return Token(access_token=access_token)


@router.post("/login/json", response_model=Token)
def login_json(
    login_data: LoginRequest,
    service: AuthService = Depends(get_auth_service)
) -> Token:
    """Login with JSON body and get access token.

    Alternative to OAuth2 form-based login.

    Args:
        login_data: Login credentials as JSON.
        service: AuthService from dependency.

    Returns:
        JWT access token.

    Raises:
        HTTPException: 401 if credentials are invalid.
    """
    user = service.authenticate(login_data.email, login_data.password)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = service.create_access_token(user.id, user.email)
    return Token(access_token=access_token)


@router.get("/me", response_model=UserResponse)
def get_current_user_info(
    current_user: User = Depends(get_current_user)
) -> UserResponse:
    """Get current user information.

    Args:
        current_user: Authenticated user from dependency.

    Returns:
        Current user data.
    """
    return UserResponse(
        id=current_user.id,
        email=current_user.email,
        created_at=current_user.created_at
    )
