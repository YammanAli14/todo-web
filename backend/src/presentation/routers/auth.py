"""Authentication router for signup and signin endpoints."""
from fastapi import APIRouter, HTTPException, status

from src.presentation.dependencies import SessionDep, CurrentUserDep
from src.presentation.schemas import (
    SignupRequest,
    SigninRequest,
    AuthResponse,
    UserResponse,
    ErrorResponse
)
from src.application.auth.auth_service import AuthService


router = APIRouter()


@router.post(
    "/signup",
    response_model=AuthResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        400: {
            "model": ErrorResponse,
            "description": "Validation error (email exists, weak password, etc.)"
        }
    }
)
async def signup(
    request: SignupRequest,
    session: SessionDep
):
    """
    Register a new user.

    Creates a new user account with the provided email and password.
    Returns the created user and JWT access token.

    - **email**: Valid email address (must be unique)
    - **password**: Password (minimum 8 characters)

    Returns:
    - **user**: Created user object (without password)
    - **access_token**: JWT token for authentication
    - **token_type**: Token type (bearer)
    """
    auth_service = AuthService(session)

    try:
        user, access_token = auth_service.signup(
            email=request.email,
            password=request.password
        )

        return AuthResponse(
            user=UserResponse(
                id=user.id,
                email=user.email,
                created_at=user.created_at,
                updated_at=user.updated_at
            ),
            access_token=access_token,
            token_type="bearer"
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post(
    "/signin",
    response_model=AuthResponse,
    responses={
        401: {
            "model": ErrorResponse,
            "description": "Invalid credentials"
        }
    }
)
async def signin(
    request: SigninRequest,
    session: SessionDep
):
    """
    Sign in an existing user.

    Authenticates a user with email and password.
    Returns the user and JWT access token.

    - **email**: User's email address
    - **password**: User's password

    Returns:
    - **user**: Authenticated user object (without password)
    - **access_token**: JWT token for authentication
    - **token_type**: Token type (bearer)
    """
    auth_service = AuthService(session)

    try:
        user, access_token = auth_service.signin(
            email=request.email,
            password=request.password
        )

        return AuthResponse(
            user=UserResponse(
                id=user.id,
                email=user.email,
                created_at=user.created_at,
                updated_at=user.updated_at
            ),
            access_token=access_token,
            token_type="bearer"
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )


@router.post(
    "/signout",
    status_code=status.HTTP_204_NO_CONTENT
)
async def signout():
    """
    Sign out the current user.

    Since we're using JWT tokens stored client-side,
    the client should simply delete the token.
    This endpoint exists for API completeness.

    Returns:
    - 204 No Content
    """
    # JWT tokens are stateless, so signout is handled client-side
    return None


@router.get(
    "/me",
    response_model=UserResponse,
    responses={
        401: {
            "model": ErrorResponse,
            "description": "Not authenticated or invalid token"
        }
    }
)
async def get_current_user_info(
    current_user: CurrentUserDep
):
    """
    Get current authenticated user information.

    Requires valid JWT token in Authorization header.

    Returns:
    - **user**: Current user object (without password)
    """
    return UserResponse(
        id=current_user.id,
        email=current_user.email,
        created_at=current_user.created_at,
        updated_at=current_user.updated_at
    )
