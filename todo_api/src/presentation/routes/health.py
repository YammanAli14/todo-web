"""Health check endpoint."""

from fastapi import APIRouter

from src.presentation.schemas import HealthResponse

router = APIRouter(tags=["Health"])


@router.get("/health", response_model=HealthResponse)
def health_check() -> HealthResponse:
    """Check API health status.

    Returns:
        Health status response.
    """
    return HealthResponse(status="healthy")
