"""FastAPI application initialization and configuration."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import os

from src.infrastructure.database import create_db_and_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    # Startup: Create database tables
    create_db_and_tables()
    yield
    # Shutdown: Cleanup if needed


# Create FastAPI application
app = FastAPI(
    title="Todo API",
    description="Phase II - Full-Stack Todo Application with Authentication",
    version="2.0.0",
    lifespan=lifespan,
)

# Configure CORS
cors_origins = os.getenv(
    "CORS_ORIGINS",
    "http://localhost:3000,http://127.0.0.1:3000"
).split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "version": "2.0.0",
        "service": "todo-api"
    }


# Router registration
from src.presentation.routers import auth, todos

app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(todos.router, prefix="/todos", tags=["Todos"])
