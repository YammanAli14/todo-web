# Phase II Technical Plan — API Layer

**Document ID:** PLAN-PHASE-II-001
**Version:** 1.0.0
**Status:** Draft — Pending Approval
**Specification Reference:** [PHASE-II-SPEC.md](../specs/PHASE-II-SPEC.md)
**Constitution Reference:** [CONSTITUTION.md](../CONSTITUTION.md)

---

## 1. Plan Overview

### 1.1 Purpose

This plan describes HOW the Phase II specification will be implemented. It transforms the Phase I in-memory console application into a RESTful API with database persistence using FastAPI and SQLModel.

### 1.2 Scope

This plan covers:

- Project structure and file organization
- Database configuration and connection management
- SQLModel entity implementation
- Repository pattern for database operations
- FastAPI application setup and routing
- Request/response schema definitions
- Error handling implementation
- Testing strategy

### 1.3 Constitutional Compliance

Per Constitution Article I, Section 1.4, this plan:

1. References the approved specification (SPEC-PHASE-II-001)
2. Breaks work into discrete, verifiable tasks
3. Defines the order of execution
4. Identifies files to be created
5. Specifies the testing approach

---

## 2. Application Architecture

### 2.1 Project Layout

Per specification Section 9.3:

```
todo_api/
├── src/
│   ├── __init__.py
│   ├── domain/
│   │   ├── __init__.py
│   │   └── task.py              # Task SQLModel entity
│   ├── application/
│   │   ├── __init__.py
│   │   └── task_service.py      # Business logic
│   ├── infrastructure/
│   │   ├── __init__.py
│   │   ├── database.py          # Database connection & session
│   │   └── task_repository.py   # Database CRUD operations
│   └── presentation/
│       ├── __init__.py
│       ├── api.py               # FastAPI app factory
│       ├── dependencies.py      # Dependency injection
│       ├── routes/
│       │   ├── __init__.py
│       │   ├── health.py        # Health endpoint
│       │   └── tasks.py         # Task endpoints
│       └── schemas.py           # Pydantic request/response schemas
├── tests/
│   ├── __init__.py
│   ├── conftest.py              # Pytest fixtures
│   ├── unit/
│   │   ├── __init__.py
│   │   └── test_task_service.py
│   └── integration/
│       ├── __init__.py
│       └── test_api.py          # API endpoint tests
├── data/                        # SQLite database directory (dev)
├── main.py                      # Application entry point
├── requirements.txt             # Dependencies
└── README.md
```

### 2.2 Layer Responsibilities

| Layer | Directory | Responsibility | Dependencies |
|-------|-----------|----------------|--------------|
| Domain | `src/domain/` | Task SQLModel entity, validation | SQLModel |
| Application | `src/application/` | Business logic, use case orchestration | Domain, Infrastructure |
| Infrastructure | `src/infrastructure/` | Database connection, repository | Domain, SQLModel |
| Presentation | `src/presentation/` | FastAPI routes, schemas, DI | Application, FastAPI |

### 2.3 Dependency Flow

```
Presentation (routes/*.py)
       │
       ▼
  Dependencies (dependencies.py)
       │
       ▼
Application (task_service.py)
       │
       ▼
Infrastructure (task_repository.py, database.py)
       │
       ▼
Domain (task.py)
```

---

## 3. Database Design

### 3.1 Connection Management

The database module handles connection configuration and session management.

**Database URL Resolution:**

```python
def get_database_url() -> str:
    """Get database URL based on environment."""
    environment = os.getenv("ENVIRONMENT", "development")
    if environment == "production":
        url = os.getenv("DATABASE_URL")
        if not url:
            raise ValueError("DATABASE_URL required in production")
        return url
    return "sqlite:///./data/todo.db"
```

**Engine Configuration:**

| Environment | Database | Connect Args |
|-------------|----------|--------------|
| Development | SQLite | `check_same_thread=False` |
| Production | PostgreSQL | SSL required |

### 3.2 Session Management

FastAPI dependency injection provides database sessions:

```python
def get_session() -> Generator[Session, None, None]:
    """Yield database session for request lifecycle."""
    with Session(engine) as session:
        yield session
```

### 3.3 Table Creation

Tables are created on application startup:

```python
def create_db_and_tables() -> None:
    """Create all database tables."""
    SQLModel.metadata.create_all(engine)
```

---

## 4. Domain Layer Implementation

### 4.1 Task Entity (SQLModel)

The Task entity extends SQLModel for ORM functionality:

```python
from datetime import datetime
from sqlmodel import SQLModel, Field

class Task(SQLModel, table=True):
    __tablename__ = "tasks"

    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(max_length=200, nullable=False)
    is_complete: bool = Field(default=False, nullable=False)
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False
    )
```

### 4.2 Title Validation

Title validation is performed at the schema level (Pydantic) before reaching the domain:

```python
from pydantic import field_validator

class TaskCreate(SQLModel):
    title: str

    @field_validator("title")
    @classmethod
    def validate_title(cls, v: str) -> str:
        stripped = v.strip()
        if not stripped:
            raise ValueError("Title cannot be empty")
        if len(stripped) > 200:
            raise ValueError("Title must be 200 characters or less")
        return stripped
```

---

## 5. Infrastructure Layer Implementation

### 5.1 Database Module

**File:** `src/infrastructure/database.py`

**Responsibilities:**
- Environment-based database URL resolution
- SQLModel engine creation
- Session factory
- Table creation function

**Implementation:**

```python
import os
from sqlmodel import SQLModel, Session, create_engine

_engine = None

def get_engine():
    global _engine
    if _engine is None:
        url = get_database_url()
        connect_args = {}
        if url.startswith("sqlite"):
            connect_args["check_same_thread"] = False
        _engine = create_engine(url, connect_args=connect_args)
    return _engine

def get_session():
    engine = get_engine()
    with Session(engine) as session:
        yield session

def create_db_and_tables():
    engine = get_engine()
    SQLModel.metadata.create_all(engine)
```

### 5.2 Task Repository

**File:** `src/infrastructure/task_repository.py`

**Responsibilities:**
- CRUD operations on Task table
- Database query execution
- Transaction management

**Interface:**

```python
class TaskRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def create(self, task: Task) -> Task: ...
    def get_by_id(self, task_id: int) -> Task | None: ...
    def get_all(self) -> list[Task]: ...
    def update(self, task: Task) -> Task: ...
    def delete(self, task_id: int) -> bool: ...
```

**Implementation Details:**

| Method | SQL Operation | Returns |
|--------|---------------|---------|
| `create` | INSERT | Created Task with ID |
| `get_by_id` | SELECT WHERE id= | Task or None |
| `get_all` | SELECT ORDER BY id | List of Tasks |
| `update` | UPDATE WHERE id= | Updated Task |
| `delete` | DELETE WHERE id= | True if deleted |

---

## 6. Application Layer Implementation

### 6.1 Task Service

**File:** `src/application/task_service.py`

**Responsibilities:**
- Business logic orchestration
- Validation enforcement
- Repository coordination
- Timestamp management

**Interface:**

```python
class TaskService:
    def __init__(self, repository: TaskRepository) -> None:
        self._repository = repository

    def create_task(self, title: str) -> Task: ...
    def get_all_tasks(self) -> list[Task]: ...
    def get_task(self, task_id: int) -> Task | None: ...
    def update_task(self, task_id: int, title: str) -> Task | None: ...
    def delete_task(self, task_id: int) -> bool: ...
    def toggle_task_complete(self, task_id: int) -> Task | None: ...
```

**Key Behaviors:**

| Method | Behavior |
|--------|----------|
| `create_task` | Creates with `is_complete=False`, auto timestamps |
| `update_task` | Updates title and `updated_at` timestamp |
| `toggle_task_complete` | Flips `is_complete`, updates `updated_at` |
| `delete_task` | Returns True if deleted, False if not found |

---

## 7. Presentation Layer Implementation

### 7.1 Request/Response Schemas

**File:** `src/presentation/schemas.py`

**Schemas:**

```python
from datetime import datetime
from pydantic import field_validator
from sqlmodel import SQLModel

class TaskCreate(SQLModel):
    """Request schema for creating a task."""
    title: str

    @field_validator("title")
    @classmethod
    def validate_title(cls, v: str) -> str:
        stripped = v.strip()
        if not stripped:
            raise ValueError("Title cannot be empty")
        if len(stripped) > 200:
            raise ValueError("Title must be 200 characters or less")
        return stripped

class TaskUpdate(SQLModel):
    """Request schema for updating a task."""
    title: str

    @field_validator("title")
    @classmethod
    def validate_title(cls, v: str) -> str:
        stripped = v.strip()
        if not stripped:
            raise ValueError("Title cannot be empty")
        if len(stripped) > 200:
            raise ValueError("Title must be 200 characters or less")
        return stripped

class TaskResponse(SQLModel):
    """Response schema for task data."""
    id: int
    title: str
    is_complete: bool
    created_at: datetime
    updated_at: datetime

class HealthResponse(SQLModel):
    """Response schema for health check."""
    status: str
```

### 7.2 Dependency Injection

**File:** `src/presentation/dependencies.py`

**Dependencies:**

```python
from fastapi import Depends
from sqlmodel import Session
from src.infrastructure.database import get_session
from src.infrastructure.task_repository import TaskRepository
from src.application.task_service import TaskService

def get_repository(session: Session = Depends(get_session)) -> TaskRepository:
    return TaskRepository(session)

def get_task_service(repo: TaskRepository = Depends(get_repository)) -> TaskService:
    return TaskService(repo)
```

### 7.3 Route Handlers

#### Health Route

**File:** `src/presentation/routes/health.py`

```python
from fastapi import APIRouter
from src.presentation.schemas import HealthResponse

router = APIRouter()

@router.get("/health", response_model=HealthResponse)
def health_check() -> HealthResponse:
    return HealthResponse(status="healthy")
```

#### Task Routes

**File:** `src/presentation/routes/tasks.py`

| Route | Method | Handler | Response |
|-------|--------|---------|----------|
| `/tasks` | GET | `list_tasks()` | 200 + TaskResponse[] |
| `/tasks` | POST | `create_task()` | 201 + TaskResponse |
| `/tasks/{id}` | GET | `get_task()` | 200 + TaskResponse |
| `/tasks/{id}` | PUT | `update_task()` | 200 + TaskResponse |
| `/tasks/{id}` | DELETE | `delete_task()` | 204 No Content |
| `/tasks/{id}/toggle` | PATCH | `toggle_task()` | 200 + TaskResponse |

### 7.4 FastAPI Application

**File:** `src/presentation/api.py`

```python
from fastapi import FastAPI
from src.presentation.routes import health, tasks
from src.infrastructure.database import create_db_and_tables

def create_app() -> FastAPI:
    app = FastAPI(
        title="Todo API",
        description="Phase II - RESTful Todo API",
        version="1.0.0"
    )

    @app.on_event("startup")
    def on_startup():
        create_db_and_tables()

    app.include_router(health.router)
    app.include_router(tasks.router)

    return app

app = create_app()
```

---

## 8. Error Handling Strategy

### 8.1 Error Categories

| Category | HTTP Status | Handled By |
|----------|-------------|------------|
| Validation Errors | 422 | Pydantic/FastAPI |
| Not Found | 404 | Route handlers |
| Server Errors | 500 | FastAPI exception handler |

### 8.2 Custom HTTP Exceptions

```python
from fastapi import HTTPException, status

# Not found
raise HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Task not found"
)

# Validation (handled by Pydantic, but can be custom)
raise HTTPException(
    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
    detail="Title cannot be empty"
)
```

### 8.3 Error Response Format

All errors use FastAPI's standard format:

```json
{
  "detail": "Error message"
}
```

---

## 9. Testing Strategy

### 9.1 Test Structure

```
tests/
├── __init__.py
├── conftest.py              # Shared fixtures
├── unit/
│   ├── __init__.py
│   └── test_task_service.py # Service unit tests
└── integration/
    ├── __init__.py
    └── test_api.py          # API endpoint tests
```

### 9.2 Test Fixtures

**File:** `tests/conftest.py`

```python
import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, Session, create_engine
from sqlmodel.pool import StaticPool

@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session

@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()
```

### 9.3 Unit Tests

**File:** `tests/unit/test_task_service.py`

| Test Case | Description |
|-----------|-------------|
| `test_create_task` | Creates task with correct fields |
| `test_create_task_strips_whitespace` | Title is trimmed |
| `test_get_all_tasks_empty` | Returns empty list |
| `test_get_all_tasks_ordered` | Returns tasks by ID |
| `test_get_task_exists` | Returns task |
| `test_get_task_not_exists` | Returns None |
| `test_update_task_exists` | Updates title and timestamp |
| `test_update_task_not_exists` | Returns None |
| `test_delete_task_exists` | Returns True |
| `test_delete_task_not_exists` | Returns False |
| `test_toggle_to_complete` | is_complete becomes True |
| `test_toggle_to_incomplete` | is_complete becomes False |

### 9.4 Integration Tests

**File:** `tests/integration/test_api.py`

| Test Case | Description |
|-----------|-------------|
| `test_health_check` | GET /health returns 200 |
| `test_create_task` | POST /tasks returns 201 |
| `test_create_task_empty_title` | Returns 422 |
| `test_create_task_long_title` | Returns 422 |
| `test_list_tasks_empty` | Returns empty array |
| `test_list_tasks_with_data` | Returns all tasks |
| `test_get_task` | Returns single task |
| `test_get_task_not_found` | Returns 404 |
| `test_update_task` | Returns updated task |
| `test_update_task_not_found` | Returns 404 |
| `test_delete_task` | Returns 204 |
| `test_delete_task_not_found` | Returns 404 |
| `test_toggle_task` | Toggles is_complete |
| `test_toggle_task_not_found` | Returns 404 |

### 9.5 Test Execution

```bash
# Run all tests
python -m pytest tests/ -v

# Run with coverage
python -m pytest tests/ -v --cov=src --cov-report=term-missing
```

---

## 10. Implementation Tasks

### 10.1 Task Summary

| Task ID | Category | Description | Files |
|---------|----------|-------------|-------|
| T-201 | Setup | Create project structure | Directories, `__init__.py` |
| T-202 | Setup | Create requirements.txt | `requirements.txt` |
| T-203 | Infra | Implement database module | `database.py` |
| T-204 | Domain | Implement Task SQLModel | `task.py` |
| T-205 | Infra | Implement TaskRepository | `task_repository.py` |
| T-206 | App | Implement TaskService | `task_service.py` |
| T-207 | Pres | Implement schemas | `schemas.py` |
| T-208 | Pres | Implement dependencies | `dependencies.py` |
| T-209 | Pres | Implement health route | `routes/health.py` |
| T-210 | Pres | Implement task routes | `routes/tasks.py` |
| T-211 | Pres | Implement FastAPI app | `api.py` |
| T-212 | Entry | Implement main.py | `main.py` |
| T-213 | Test | Create test fixtures | `conftest.py` |
| T-214 | Test | Write unit tests | `test_task_service.py` |
| T-215 | Test | Write integration tests | `test_api.py` |
| T-216 | Docs | Create README | `README.md` |
| T-217 | Verify | Final verification | — |

### 10.2 Task Execution Order

```
T-201 (Setup: Project Structure)
    │
    └── T-202 (Setup: requirements.txt)
            │
            └── T-203 (Infra: Database Module)
                    │
                    └── T-204 (Domain: Task SQLModel)
                            │
                            └── T-205 (Infra: TaskRepository)
                                    │
                                    └── T-206 (App: TaskService)
                                            │
                                            └── T-207 (Pres: Schemas)
                                                    │
                                                    └── T-208 (Pres: Dependencies)
                                                            │
                                                    ┌───────┴───────┐
                                                    │               │
                                                    ▼               ▼
                                            T-209           T-210
                                            (Health)        (Tasks)
                                                    │               │
                                                    └───────┬───────┘
                                                            │
                                                            ▼
                                                    T-211 (FastAPI App)
                                                            │
                                                            ▼
                                                    T-212 (main.py)
                                                            │
                                                            ▼
                                                    T-213 (Test Fixtures)
                                                            │
                                                    ┌───────┴───────┐
                                                    │               │
                                                    ▼               ▼
                                            T-214           T-215
                                            (Unit Tests)    (Integration)
                                                    │               │
                                                    └───────┬───────┘
                                                            │
                                                            ▼
                                                    T-216 (README)
                                                            │
                                                            ▼
                                                    T-217 (Verification)
```

---

## 11. Entry Point

### 11.1 Main Module

**File:** `main.py`

```python
"""Todo API - Phase II Entry Point."""

import uvicorn
from src.presentation.api import app

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
```

### 11.2 Running the Application

**Development:**
```bash
cd todo_api
python main.py
# Or
uvicorn main:app --reload
```

**Production:**
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

---

## 12. Verification Checklist

### 12.1 Specification Compliance

| Spec Section | Plan Coverage | Status |
|--------------|---------------|--------|
| 3. User Stories | Section 7.3 | Covered |
| 4. Data Model | Section 4 | Covered |
| 5. API Interface | Section 7 | Covered |
| 6. Error Handling | Section 8 | Covered |
| 7. Database Config | Section 3 | Covered |
| 8. Non-Functional | Section 9 | Covered |
| 9. Technical Constraints | Section 2 | Covered |

### 12.2 Constitutional Compliance

| Article | Requirement | Compliance |
|---------|-------------|------------|
| I.1.4 | References approved spec | Yes |
| I.1.4 | Discrete verifiable tasks | Yes (Section 10) |
| I.1.4 | Order of execution | Yes (Section 10.2) |
| I.1.4 | Files identified | Yes (Section 2.1) |
| I.1.4 | Testing approach | Yes (Section 9) |
| IV.4.1 | FastAPI, SQLModel | Yes |
| V.5.1 | Clean architecture | Yes (Section 2.2) |

---

## 13. Document Control

### 13.1 Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2025-12-28 | Agent | Initial plan |

### 13.2 Approval

| Role | Name | Date | Status |
|------|------|------|--------|
| Plan Author | Agent | 2025-12-28 | Draft |
| Human Reviewer | — | — | Pending |

---

## 14. References

- [PHASE-II-SPEC.md](../specs/PHASE-II-SPEC.md) — Phase II Specification
- [CONSTITUTION.md](../CONSTITUTION.md) — Global Constitution
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLModel Documentation](https://sqlmodel.tiangolo.com/)

---

*End of Phase II Technical Plan*
