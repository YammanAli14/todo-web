"""FastAPI application factory."""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.infrastructure.database import create_db_and_tables
from src.presentation.routes import health, tasks, auth


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler.

    Creates database tables on startup.

    Args:
        app: FastAPI application instance.
    """
    # Import models to ensure they are registered with SQLModel
    from src.domain.user import User  # noqa: F401
    from src.domain.task import Task  # noqa: F401

    create_db_and_tables()
    yield


def create_app() -> FastAPI:
    """Create and configure FastAPI application.

    Returns:
        Configured FastAPI application instance.
    """
    app = FastAPI(
        title="Todo API",
        description="Phase IV - Todo API with authentication",
        version="2.0.0",
        lifespan=lifespan
    )

    # Configure CORS for frontend
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:3000",
            "http://127.0.0.1:3000",
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include routers
    app.include_router(health.router)
    app.include_router(auth.router)
    app.include_router(tasks.router)

    return app


app = create_app()
