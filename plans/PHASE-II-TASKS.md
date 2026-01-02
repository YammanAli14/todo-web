# Phase II Implementation Tasks

**Document ID:** TASKS-PHASE-II-001
**Version:** 1.0.0
**Status:** Draft — Pending Approval
**Plan Reference:** [PHASE-II-PLAN.md](./PHASE-II-PLAN.md)
**Specification Reference:** [../specs/PHASE-II-SPEC.md](../specs/PHASE-II-SPEC.md)
**Constitution Reference:** [../CONSTITUTION.md](../CONSTITUTION.md)

---

## 1. Overview

This document contains the atomic implementation tasks for Phase II. Each task is:

- Small and testable
- Sequential (dependencies clearly stated)
- Traceable to specification and plan sections
- Sufficient to fully implement Phase II

**Total Tasks:** 30
**Estimated Files:** 22

---

## 2. Task Index

| ID | Category | Description |
|----|----------|-------------|
| TASK-201 | Setup | Create project root directory |
| TASK-202 | Setup | Create source directory structure |
| TASK-203 | Setup | Create test directory structure |
| TASK-204 | Setup | Create all `__init__.py` files |
| TASK-205 | Setup | Create requirements.txt |
| TASK-206 | Setup | Create data directory for SQLite |
| TASK-207 | Infra | Implement database configuration |
| TASK-208 | Infra | Implement database session management |
| TASK-209 | Domain | Implement Task SQLModel entity |
| TASK-210 | Infra | Implement TaskRepository - create method |
| TASK-211 | Infra | Implement TaskRepository - read methods |
| TASK-212 | Infra | Implement TaskRepository - update method |
| TASK-213 | Infra | Implement TaskRepository - delete method |
| TASK-214 | App | Implement TaskService - create method |
| TASK-215 | App | Implement TaskService - read methods |
| TASK-216 | App | Implement TaskService - update method |
| TASK-217 | App | Implement TaskService - delete method |
| TASK-218 | App | Implement TaskService - toggle method |
| TASK-219 | Pres | Implement request/response schemas |
| TASK-220 | Pres | Implement dependency injection |
| TASK-221 | Pres | Implement health route |
| TASK-222 | Pres | Implement POST /tasks route |
| TASK-223 | Pres | Implement GET /tasks routes |
| TASK-224 | Pres | Implement PUT /tasks/{id} route |
| TASK-225 | Pres | Implement DELETE /tasks/{id} route |
| TASK-226 | Pres | Implement PATCH /tasks/{id}/toggle route |
| TASK-227 | Pres | Implement FastAPI application factory |
| TASK-228 | Entry | Implement main.py entry point |
| TASK-229 | Test | Create test fixtures and configuration |
| TASK-230 | Test | Write integration tests for all endpoints |
| TASK-231 | Docs | Create README documentation |
| TASK-232 | Verify | Final verification and acceptance testing |

---

## 3. Detailed Task Specifications

---

### TASK-201: Create Project Root Directory

**Category:** Setup
**Preconditions:** None
**Depends On:** None

**Description:**
Create the `todo_api` root directory for the Phase II FastAPI application.

**Artifacts to Create:**
- `todo_api/` (directory)

**Expected Output:**
- Empty directory `todo_api` exists at project root

**Spec Reference:** Section 9.3 (Project Structure)
**Plan Reference:** Section 2.1 (Project Layout)

**Completion Criteria:**
- [ ] Directory `todo_api/` exists

---

### TASK-202: Create Source Directory Structure

**Category:** Setup
**Preconditions:** TASK-201 complete
**Depends On:** TASK-201

**Description:**
Create the `src` directory and all layer subdirectories including routes.

**Artifacts to Create:**
- `todo_api/src/` (directory)
- `todo_api/src/domain/` (directory)
- `todo_api/src/application/` (directory)
- `todo_api/src/infrastructure/` (directory)
- `todo_api/src/presentation/` (directory)
- `todo_api/src/presentation/routes/` (directory)

**Expected Output:**
- All source directories exist with correct nesting

**Spec Reference:** Section 9.3 (Project Structure)
**Plan Reference:** Section 2.1 (Project Layout)

**Completion Criteria:**
- [ ] `todo_api/src/` exists
- [ ] `todo_api/src/domain/` exists
- [ ] `todo_api/src/application/` exists
- [ ] `todo_api/src/infrastructure/` exists
- [ ] `todo_api/src/presentation/` exists
- [ ] `todo_api/src/presentation/routes/` exists

---

### TASK-203: Create Test Directory Structure

**Category:** Setup
**Preconditions:** TASK-201 complete
**Depends On:** TASK-201

**Description:**
Create the `tests` directory with `unit` and `integration` subdirectories.

**Artifacts to Create:**
- `todo_api/tests/` (directory)
- `todo_api/tests/unit/` (directory)
- `todo_api/tests/integration/` (directory)

**Expected Output:**
- All test directories exist with correct nesting

**Spec Reference:** Section 9.3 (Project Structure)
**Plan Reference:** Section 9.1 (Test Structure)

**Completion Criteria:**
- [ ] `todo_api/tests/` exists
- [ ] `todo_api/tests/unit/` exists
- [ ] `todo_api/tests/integration/` exists

---

### TASK-204: Create All `__init__.py` Files

**Category:** Setup
**Preconditions:** TASK-202, TASK-203 complete
**Depends On:** TASK-202, TASK-203

**Description:**
Create `__init__.py` files in all directories to make them Python packages.

**Artifacts to Create:**
- `todo_api/src/__init__.py`
- `todo_api/src/domain/__init__.py`
- `todo_api/src/application/__init__.py`
- `todo_api/src/infrastructure/__init__.py`
- `todo_api/src/presentation/__init__.py`
- `todo_api/src/presentation/routes/__init__.py`
- `todo_api/tests/__init__.py`
- `todo_api/tests/unit/__init__.py`
- `todo_api/tests/integration/__init__.py`

**Expected Output:**
- All `__init__.py` files exist

**Spec Reference:** Section 9.3 (Project Structure)
**Plan Reference:** Section 2.1 (Project Layout)

**Completion Criteria:**
- [ ] 9 `__init__.py` files created
- [ ] All directories are valid Python packages

---

### TASK-205: Create requirements.txt

**Category:** Setup
**Preconditions:** TASK-201 complete
**Depends On:** TASK-201

**Description:**
Create requirements.txt with all Phase II dependencies.

**Artifacts to Create:**
- `todo_api/requirements.txt`

**Content:**
```
fastapi>=0.109.0
sqlmodel>=0.0.14
uvicorn[standard]>=0.27.0
pydantic>=2.0.0
pydantic-settings>=2.0.0
psycopg2-binary>=2.9.0
httpx>=0.26.0
pytest>=8.0.0
pytest-cov>=4.0.0
```

**Expected Output:**
- requirements.txt with pinned dependencies

**Spec Reference:** Section 9.2 (Dependencies)
**Plan Reference:** Section 10.1 (Task T-202)

**Completion Criteria:**
- [ ] `requirements.txt` exists
- [ ] All required dependencies listed
- [ ] Versions are pinned

---

### TASK-206: Create Data Directory for SQLite

**Category:** Setup
**Preconditions:** TASK-201 complete
**Depends On:** TASK-201

**Description:**
Create the data directory for SQLite database storage in development.

**Artifacts to Create:**
- `todo_api/data/` (directory)
- `todo_api/data/.gitkeep` (file to track empty directory)

**Expected Output:**
- Data directory exists for SQLite database

**Spec Reference:** Section 7.1 (Development Database)
**Plan Reference:** Section 3.1 (Database URL Resolution)

**Completion Criteria:**
- [ ] `todo_api/data/` directory exists
- [ ] `.gitkeep` file present

---

### TASK-207: Implement Database Configuration

**Category:** Infrastructure
**Preconditions:** TASK-204 complete
**Depends On:** TASK-204

**Description:**
Create the database module with URL resolution based on environment.

**Artifacts to Create:**
- `todo_api/src/infrastructure/database.py`

**Implementation Details:**
```python
import os
from sqlmodel import SQLModel, create_engine

def get_database_url() -> str:
    """Get database URL based on environment.

    Returns:
        Database connection URL string.

    Raises:
        ValueError: If DATABASE_URL not set in production.
    """
    environment = os.getenv("ENVIRONMENT", "development")
    if environment == "production":
        url = os.getenv("DATABASE_URL")
        if not url:
            raise ValueError("DATABASE_URL environment variable required in production")
        return url
    return "sqlite:///./data/todo.db"

def get_connect_args() -> dict:
    """Get connection arguments based on database type."""
    url = get_database_url()
    if url.startswith("sqlite"):
        return {"check_same_thread": False}
    return {}

# Engine singleton
_engine = None

def get_engine():
    """Get or create database engine singleton."""
    global _engine
    if _engine is None:
        _engine = create_engine(
            get_database_url(),
            connect_args=get_connect_args()
        )
    return _engine

def create_db_and_tables() -> None:
    """Create all database tables."""
    engine = get_engine()
    SQLModel.metadata.create_all(engine)
```

**Expected Output:**
- Database URL resolves correctly for dev/prod
- Engine created with proper connect args
- Tables can be created

**Spec Reference:** Section 7 (Database Configuration)
**Plan Reference:** Section 3.1 (Connection Management)

**Completion Criteria:**
- [ ] `database.py` file exists
- [ ] `get_database_url()` returns SQLite URL in dev
- [ ] `get_database_url()` returns env var in prod
- [ ] `get_engine()` creates singleton engine
- [ ] `create_db_and_tables()` function exists
- [ ] Type hints and docstrings present

---

### TASK-208: Implement Database Session Management

**Category:** Infrastructure
**Preconditions:** TASK-207 complete
**Depends On:** TASK-207

**Description:**
Add session management functions to the database module.

**Artifacts to Modify:**
- `todo_api/src/infrastructure/database.py`

**Implementation Details:**
```python
from typing import Generator
from sqlmodel import Session

def get_session() -> Generator[Session, None, None]:
    """Yield database session for request lifecycle.

    Yields:
        Database session that auto-closes after use.
    """
    engine = get_engine()
    with Session(engine) as session:
        yield session
```

**Expected Output:**
- Session generator yields valid session
- Session auto-closes after use

**Spec Reference:** Section 7.4 (Database Migrations)
**Plan Reference:** Section 3.2 (Session Management)

**Completion Criteria:**
- [ ] `get_session()` generator function exists
- [ ] Session is yielded and auto-closed
- [ ] Type hints present

---

### TASK-209: Implement Task SQLModel Entity

**Category:** Domain
**Preconditions:** TASK-207 complete
**Depends On:** TASK-207

**Description:**
Create the Task SQLModel entity with all fields and constraints.

**Artifacts to Create:**
- `todo_api/src/domain/task.py`

**Implementation Details:**
```python
from datetime import datetime
from sqlmodel import SQLModel, Field


class Task(SQLModel, table=True):
    """Task entity representing a todo item.

    Attributes:
        id: Primary key, auto-incremented.
        title: Task description, max 200 characters.
        is_complete: Completion status, defaults to False.
        created_at: Timestamp of creation.
        updated_at: Timestamp of last update.
    """
    __tablename__ = "tasks"

    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(max_length=200)
    is_complete: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

**Expected Output:**
- Task model can be instantiated
- Task model maps to "tasks" table
- All fields have correct types and defaults

**Spec Reference:** Section 4 (Data Model)
**Plan Reference:** Section 4.1 (Task Entity)

**Completion Criteria:**
- [ ] `task.py` file exists
- [ ] Task class extends SQLModel with `table=True`
- [ ] All 5 fields defined (id, title, is_complete, created_at, updated_at)
- [ ] `__tablename__` set to "tasks"
- [ ] Type hints and docstring present

---

### TASK-210: Implement TaskRepository - Create Method

**Category:** Infrastructure
**Preconditions:** TASK-209 complete
**Depends On:** TASK-209

**Description:**
Create TaskRepository class with constructor and create method.

**Artifacts to Create:**
- `todo_api/src/infrastructure/task_repository.py`

**Implementation Details:**
```python
from sqlmodel import Session
from src.domain.task import Task


class TaskRepository:
    """Repository for Task database operations."""

    def __init__(self, session: Session) -> None:
        """Initialize repository with database session.

        Args:
            session: SQLModel database session.
        """
        self._session = session

    def create(self, task: Task) -> Task:
        """Create a new task in the database.

        Args:
            task: Task entity to create.

        Returns:
            Created task with assigned ID.
        """
        self._session.add(task)
        self._session.commit()
        self._session.refresh(task)
        return task
```

**Expected Output:**
- Repository can be instantiated with session
- Create method adds task to database
- Returns task with assigned ID

**Spec Reference:** Section 3.1 (US-101: Create Task)
**Plan Reference:** Section 5.2 (Task Repository)

**Completion Criteria:**
- [ ] `task_repository.py` file exists
- [ ] `TaskRepository` class defined
- [ ] Constructor accepts Session
- [ ] `create()` method adds, commits, refreshes task
- [ ] Type hints and docstrings present

---

### TASK-211: Implement TaskRepository - Read Methods

**Category:** Infrastructure
**Preconditions:** TASK-210 complete
**Depends On:** TASK-210

**Description:**
Add get_by_id and get_all methods to TaskRepository.

**Artifacts to Modify:**
- `todo_api/src/infrastructure/task_repository.py`

**Implementation Details:**
```python
from sqlmodel import select

def get_by_id(self, task_id: int) -> Task | None:
    """Get a task by ID.

    Args:
        task_id: ID of task to retrieve.

    Returns:
        Task if found, None otherwise.
    """
    return self._session.get(Task, task_id)

def get_all(self) -> list[Task]:
    """Get all tasks ordered by ID.

    Returns:
        List of all tasks, ordered by ID ascending.
    """
    statement = select(Task).order_by(Task.id)
    return list(self._session.exec(statement).all())
```

**Expected Output:**
- get_by_id returns task or None
- get_all returns list ordered by ID

**Spec Reference:** Section 3.2 (US-102), Section 3.3 (US-103)
**Plan Reference:** Section 5.2 (Task Repository)

**Completion Criteria:**
- [ ] `get_by_id()` method exists
- [ ] `get_by_id()` returns None for non-existent ID
- [ ] `get_all()` method exists
- [ ] `get_all()` returns tasks ordered by ID
- [ ] Type hints and docstrings present

---

### TASK-212: Implement TaskRepository - Update Method

**Category:** Infrastructure
**Preconditions:** TASK-211 complete
**Depends On:** TASK-211

**Description:**
Add update method to TaskRepository.

**Artifacts to Modify:**
- `todo_api/src/infrastructure/task_repository.py`

**Implementation Details:**
```python
def update(self, task: Task) -> Task:
    """Update an existing task.

    Args:
        task: Task entity with updated values.

    Returns:
        Updated task.
    """
    self._session.add(task)
    self._session.commit()
    self._session.refresh(task)
    return task
```

**Expected Output:**
- Update method persists changes
- Returns updated task

**Spec Reference:** Section 3.4 (US-104: Update Task)
**Plan Reference:** Section 5.2 (Task Repository)

**Completion Criteria:**
- [ ] `update()` method exists
- [ ] Changes are committed to database
- [ ] Updated task is returned
- [ ] Type hints and docstring present

---

### TASK-213: Implement TaskRepository - Delete Method

**Category:** Infrastructure
**Preconditions:** TASK-211 complete
**Depends On:** TASK-211

**Description:**
Add delete method to TaskRepository.

**Artifacts to Modify:**
- `todo_api/src/infrastructure/task_repository.py`

**Implementation Details:**
```python
def delete(self, task_id: int) -> bool:
    """Delete a task by ID.

    Args:
        task_id: ID of task to delete.

    Returns:
        True if deleted, False if not found.
    """
    task = self.get_by_id(task_id)
    if task is None:
        return False
    self._session.delete(task)
    self._session.commit()
    return True
```

**Expected Output:**
- Delete removes task from database
- Returns True if deleted, False if not found

**Spec Reference:** Section 3.5 (US-105: Delete Task)
**Plan Reference:** Section 5.2 (Task Repository)

**Completion Criteria:**
- [ ] `delete()` method exists
- [ ] Returns False for non-existent task
- [ ] Task is removed from database
- [ ] Returns True on successful delete
- [ ] Type hints and docstring present

---

### TASK-214: Implement TaskService - Create Method

**Category:** Application
**Preconditions:** TASK-213 complete
**Depends On:** TASK-213

**Description:**
Create TaskService class with constructor and create_task method.

**Artifacts to Create:**
- `todo_api/src/application/task_service.py`

**Implementation Details:**
```python
from datetime import datetime
from src.domain.task import Task
from src.infrastructure.task_repository import TaskRepository


class TaskService:
    """Service layer for task business logic."""

    def __init__(self, repository: TaskRepository) -> None:
        """Initialize service with repository.

        Args:
            repository: Task repository for database operations.
        """
        self._repository = repository

    def create_task(self, title: str) -> Task:
        """Create a new task.

        Args:
            title: Task title (already validated by schema).

        Returns:
            Created task with assigned ID.
        """
        now = datetime.utcnow()
        task = Task(
            title=title,
            is_complete=False,
            created_at=now,
            updated_at=now
        )
        return self._repository.create(task)
```

**Expected Output:**
- TaskService can be instantiated with repository
- create_task creates task with correct defaults

**Spec Reference:** Section 3.1 (US-101)
**Plan Reference:** Section 6.1 (Task Service)

**Completion Criteria:**
- [ ] `task_service.py` file exists
- [ ] `TaskService` class defined
- [ ] Constructor accepts repository
- [ ] `create_task()` sets is_complete=False
- [ ] `create_task()` sets timestamps
- [ ] Type hints and docstrings present

---

### TASK-215: Implement TaskService - Read Methods

**Category:** Application
**Preconditions:** TASK-214 complete
**Depends On:** TASK-214

**Description:**
Add get_all_tasks and get_task methods to TaskService.

**Artifacts to Modify:**
- `todo_api/src/application/task_service.py`

**Implementation Details:**
```python
def get_all_tasks(self) -> list[Task]:
    """Get all tasks.

    Returns:
        List of all tasks ordered by ID.
    """
    return self._repository.get_all()

def get_task(self, task_id: int) -> Task | None:
    """Get a task by ID.

    Args:
        task_id: ID of task to retrieve.

    Returns:
        Task if found, None otherwise.
    """
    return self._repository.get_by_id(task_id)
```

**Expected Output:**
- get_all_tasks returns all tasks
- get_task returns task or None

**Spec Reference:** Section 3.2 (US-102), Section 3.3 (US-103)
**Plan Reference:** Section 6.1 (Task Service)

**Completion Criteria:**
- [ ] `get_all_tasks()` method exists
- [ ] `get_task()` method exists
- [ ] Both delegate to repository
- [ ] Type hints and docstrings present

---

### TASK-216: Implement TaskService - Update Method

**Category:** Application
**Preconditions:** TASK-215 complete
**Depends On:** TASK-215

**Description:**
Add update_task method to TaskService.

**Artifacts to Modify:**
- `todo_api/src/application/task_service.py`

**Implementation Details:**
```python
def update_task(self, task_id: int, title: str) -> Task | None:
    """Update a task's title.

    Args:
        task_id: ID of task to update.
        title: New title (already validated by schema).

    Returns:
        Updated task if found, None otherwise.
    """
    task = self._repository.get_by_id(task_id)
    if task is None:
        return None
    task.title = title
    task.updated_at = datetime.utcnow()
    return self._repository.update(task)
```

**Expected Output:**
- Updates title and updated_at
- Returns None if task not found

**Spec Reference:** Section 3.4 (US-104)
**Plan Reference:** Section 6.1 (Task Service)

**Completion Criteria:**
- [ ] `update_task()` method exists
- [ ] Returns None for non-existent task
- [ ] Updates title field
- [ ] Updates updated_at timestamp
- [ ] Type hints and docstring present

---

### TASK-217: Implement TaskService - Delete Method

**Category:** Application
**Preconditions:** TASK-215 complete
**Depends On:** TASK-215

**Description:**
Add delete_task method to TaskService.

**Artifacts to Modify:**
- `todo_api/src/application/task_service.py`

**Implementation Details:**
```python
def delete_task(self, task_id: int) -> bool:
    """Delete a task.

    Args:
        task_id: ID of task to delete.

    Returns:
        True if deleted, False if not found.
    """
    return self._repository.delete(task_id)
```

**Expected Output:**
- Delegates to repository
- Returns boolean result

**Spec Reference:** Section 3.5 (US-105)
**Plan Reference:** Section 6.1 (Task Service)

**Completion Criteria:**
- [ ] `delete_task()` method exists
- [ ] Delegates to repository
- [ ] Returns True/False correctly
- [ ] Type hints and docstring present

---

### TASK-218: Implement TaskService - Toggle Method

**Category:** Application
**Preconditions:** TASK-216 complete
**Depends On:** TASK-216

**Description:**
Add toggle_task_complete method to TaskService.

**Artifacts to Modify:**
- `todo_api/src/application/task_service.py`

**Implementation Details:**
```python
def toggle_task_complete(self, task_id: int) -> Task | None:
    """Toggle a task's completion status.

    Args:
        task_id: ID of task to toggle.

    Returns:
        Updated task if found, None otherwise.
    """
    task = self._repository.get_by_id(task_id)
    if task is None:
        return None
    task.is_complete = not task.is_complete
    task.updated_at = datetime.utcnow()
    return self._repository.update(task)
```

**Expected Output:**
- Toggles is_complete value
- Updates updated_at timestamp
- Returns None if not found

**Spec Reference:** Section 3.6 (US-106)
**Plan Reference:** Section 6.1 (Task Service)

**Completion Criteria:**
- [ ] `toggle_task_complete()` method exists
- [ ] Returns None for non-existent task
- [ ] Toggles is_complete correctly
- [ ] Updates updated_at timestamp
- [ ] Type hints and docstring present

---

### TASK-219: Implement Request/Response Schemas

**Category:** Presentation
**Preconditions:** TASK-209 complete
**Depends On:** TASK-209

**Description:**
Create Pydantic schemas for API request/response validation.

**Artifacts to Create:**
- `todo_api/src/presentation/schemas.py`

**Implementation Details:**
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
        """Validate title is not empty and within length limit."""
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
        """Validate title is not empty and within length limit."""
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

**Expected Output:**
- All schemas validate correctly
- Title validation rejects empty/long titles
- Response schemas include all fields

**Spec Reference:** Section 5.3 (Request/Response Schemas), Section 6.1 (Validation Errors)
**Plan Reference:** Section 7.1 (Request/Response Schemas)

**Completion Criteria:**
- [ ] `schemas.py` file exists
- [ ] `TaskCreate` with title validation
- [ ] `TaskUpdate` with title validation
- [ ] `TaskResponse` with all 5 fields
- [ ] `HealthResponse` with status field
- [ ] Empty title raises ValueError
- [ ] Title > 200 chars raises ValueError
- [ ] Type hints present

---

### TASK-220: Implement Dependency Injection

**Category:** Presentation
**Preconditions:** TASK-218 complete
**Depends On:** TASK-218

**Description:**
Create dependency functions for FastAPI dependency injection.

**Artifacts to Create:**
- `todo_api/src/presentation/dependencies.py`

**Implementation Details:**
```python
from typing import Generator
from fastapi import Depends
from sqlmodel import Session

from src.infrastructure.database import get_session
from src.infrastructure.task_repository import TaskRepository
from src.application.task_service import TaskService


def get_repository(
    session: Session = Depends(get_session)
) -> TaskRepository:
    """Get TaskRepository instance.

    Args:
        session: Database session from dependency.

    Returns:
        TaskRepository instance.
    """
    return TaskRepository(session)


def get_task_service(
    repository: TaskRepository = Depends(get_repository)
) -> TaskService:
    """Get TaskService instance.

    Args:
        repository: TaskRepository from dependency.

    Returns:
        TaskService instance.
    """
    return TaskService(repository)
```

**Expected Output:**
- Dependencies chain correctly
- Service receives repository with session

**Spec Reference:** Section 9.3 (Project Structure)
**Plan Reference:** Section 7.2 (Dependency Injection)

**Completion Criteria:**
- [ ] `dependencies.py` file exists
- [ ] `get_repository()` returns TaskRepository
- [ ] `get_task_service()` returns TaskService
- [ ] Dependencies use Depends() correctly
- [ ] Type hints and docstrings present

---

### TASK-221: Implement Health Route

**Category:** Presentation
**Preconditions:** TASK-219 complete
**Depends On:** TASK-219

**Description:**
Create health check endpoint.

**Artifacts to Create:**
- `todo_api/src/presentation/routes/health.py`

**Implementation Details:**
```python
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
```

**Expected Output:**
- GET /health returns 200 with status

**Spec Reference:** Section 3.7 (US-107)
**Plan Reference:** Section 7.3 (Health Route)

**Completion Criteria:**
- [ ] `health.py` file exists
- [ ] Router created with "Health" tag
- [ ] GET /health endpoint defined
- [ ] Returns HealthResponse with status="healthy"
- [ ] Type hints and docstring present

---

### TASK-222: Implement POST /tasks Route

**Category:** Presentation
**Preconditions:** TASK-220 complete
**Depends On:** TASK-220

**Description:**
Create endpoint to create a new task.

**Artifacts to Create:**
- `todo_api/src/presentation/routes/tasks.py`

**Implementation Details:**
```python
from fastapi import APIRouter, Depends, status

from src.application.task_service import TaskService
from src.presentation.dependencies import get_task_service
from src.presentation.schemas import TaskCreate, TaskResponse

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post(
    "",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED
)
def create_task(
    task_data: TaskCreate,
    service: TaskService = Depends(get_task_service)
) -> TaskResponse:
    """Create a new task.

    Args:
        task_data: Task creation data.
        service: Task service from dependency.

    Returns:
        Created task data.
    """
    task = service.create_task(task_data.title)
    return TaskResponse(
        id=task.id,
        title=task.title,
        is_complete=task.is_complete,
        created_at=task.created_at,
        updated_at=task.updated_at
    )
```

**Expected Output:**
- POST /tasks creates task
- Returns 201 with TaskResponse

**Spec Reference:** Section 3.1 (US-101)
**Plan Reference:** Section 7.3 (Task Routes)

**Completion Criteria:**
- [ ] `tasks.py` file exists
- [ ] Router with prefix="/tasks"
- [ ] POST endpoint returns 201
- [ ] Validates input via TaskCreate
- [ ] Returns TaskResponse
- [ ] Type hints and docstring present

---

### TASK-223: Implement GET /tasks Routes

**Category:** Presentation
**Preconditions:** TASK-222 complete
**Depends On:** TASK-222

**Description:**
Add endpoints to list all tasks and get single task.

**Artifacts to Modify:**
- `todo_api/src/presentation/routes/tasks.py`

**Implementation Details:**
```python
from fastapi import HTTPException

@router.get("", response_model=list[TaskResponse])
def list_tasks(
    service: TaskService = Depends(get_task_service)
) -> list[TaskResponse]:
    """Get all tasks.

    Args:
        service: Task service from dependency.

    Returns:
        List of all tasks.
    """
    tasks = service.get_all_tasks()
    return [
        TaskResponse(
            id=t.id,
            title=t.title,
            is_complete=t.is_complete,
            created_at=t.created_at,
            updated_at=t.updated_at
        )
        for t in tasks
    ]


@router.get("/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: int,
    service: TaskService = Depends(get_task_service)
) -> TaskResponse:
    """Get a task by ID.

    Args:
        task_id: ID of task to retrieve.
        service: Task service from dependency.

    Returns:
        Task data.

    Raises:
        HTTPException: 404 if task not found.
    """
    task = service.get_task(task_id)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return TaskResponse(
        id=task.id,
        title=task.title,
        is_complete=task.is_complete,
        created_at=task.created_at,
        updated_at=task.updated_at
    )
```

**Expected Output:**
- GET /tasks returns list of tasks
- GET /tasks/{id} returns single task or 404

**Spec Reference:** Section 3.2 (US-102), Section 3.3 (US-103)
**Plan Reference:** Section 7.3 (Task Routes)

**Completion Criteria:**
- [ ] GET /tasks returns list
- [ ] GET /tasks/{id} returns single task
- [ ] Returns 404 for non-existent ID
- [ ] Type hints and docstrings present

---

### TASK-224: Implement PUT /tasks/{id} Route

**Category:** Presentation
**Preconditions:** TASK-223 complete
**Depends On:** TASK-223

**Description:**
Add endpoint to update a task's title.

**Artifacts to Modify:**
- `todo_api/src/presentation/routes/tasks.py`

**Implementation Details:**
```python
from src.presentation.schemas import TaskUpdate

@router.put("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    task_data: TaskUpdate,
    service: TaskService = Depends(get_task_service)
) -> TaskResponse:
    """Update a task's title.

    Args:
        task_id: ID of task to update.
        task_data: Task update data.
        service: Task service from dependency.

    Returns:
        Updated task data.

    Raises:
        HTTPException: 404 if task not found.
    """
    task = service.update_task(task_id, task_data.title)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return TaskResponse(
        id=task.id,
        title=task.title,
        is_complete=task.is_complete,
        created_at=task.created_at,
        updated_at=task.updated_at
    )
```

**Expected Output:**
- PUT /tasks/{id} updates task
- Returns 200 with updated task or 404

**Spec Reference:** Section 3.4 (US-104)
**Plan Reference:** Section 7.3 (Task Routes)

**Completion Criteria:**
- [ ] PUT endpoint defined
- [ ] Validates input via TaskUpdate
- [ ] Returns 404 for non-existent ID
- [ ] Returns updated TaskResponse
- [ ] Type hints and docstring present

---

### TASK-225: Implement DELETE /tasks/{id} Route

**Category:** Presentation
**Preconditions:** TASK-223 complete
**Depends On:** TASK-223

**Description:**
Add endpoint to delete a task.

**Artifacts to Modify:**
- `todo_api/src/presentation/routes/tasks.py`

**Implementation Details:**
```python
from fastapi import Response

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int,
    service: TaskService = Depends(get_task_service)
) -> Response:
    """Delete a task.

    Args:
        task_id: ID of task to delete.
        service: Task service from dependency.

    Returns:
        Empty response on success.

    Raises:
        HTTPException: 404 if task not found.
    """
    deleted = service.delete_task(task_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)
```

**Expected Output:**
- DELETE /tasks/{id} removes task
- Returns 204 or 404

**Spec Reference:** Section 3.5 (US-105)
**Plan Reference:** Section 7.3 (Task Routes)

**Completion Criteria:**
- [ ] DELETE endpoint defined
- [ ] Returns 204 on success
- [ ] Returns 404 for non-existent ID
- [ ] Type hints and docstring present

---

### TASK-226: Implement PATCH /tasks/{id}/toggle Route

**Category:** Presentation
**Preconditions:** TASK-223 complete
**Depends On:** TASK-223

**Description:**
Add endpoint to toggle task completion status.

**Artifacts to Modify:**
- `todo_api/src/presentation/routes/tasks.py`

**Implementation Details:**
```python
@router.patch("/{task_id}/toggle", response_model=TaskResponse)
def toggle_task(
    task_id: int,
    service: TaskService = Depends(get_task_service)
) -> TaskResponse:
    """Toggle a task's completion status.

    Args:
        task_id: ID of task to toggle.
        service: Task service from dependency.

    Returns:
        Updated task data.

    Raises:
        HTTPException: 404 if task not found.
    """
    task = service.toggle_task_complete(task_id)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return TaskResponse(
        id=task.id,
        title=task.title,
        is_complete=task.is_complete,
        created_at=task.created_at,
        updated_at=task.updated_at
    )
```

**Expected Output:**
- PATCH /tasks/{id}/toggle toggles status
- Returns 200 with updated task or 404

**Spec Reference:** Section 3.6 (US-106)
**Plan Reference:** Section 7.3 (Task Routes)

**Completion Criteria:**
- [ ] PATCH endpoint defined
- [ ] Toggles is_complete
- [ ] Returns 404 for non-existent ID
- [ ] Returns updated TaskResponse
- [ ] Type hints and docstring present

---

### TASK-227: Implement FastAPI Application Factory

**Category:** Presentation
**Preconditions:** TASK-221, TASK-226 complete
**Depends On:** TASK-226

**Description:**
Create FastAPI application with router registration and startup event.

**Artifacts to Create:**
- `todo_api/src/presentation/api.py`

**Implementation Details:**
```python
from contextlib import asynccontextmanager
from fastapi import FastAPI

from src.infrastructure.database import create_db_and_tables
from src.presentation.routes import health, tasks


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler.

    Creates database tables on startup.
    """
    create_db_and_tables()
    yield


def create_app() -> FastAPI:
    """Create and configure FastAPI application.

    Returns:
        Configured FastAPI application instance.
    """
    app = FastAPI(
        title="Todo API",
        description="Phase II - RESTful Todo API with database persistence",
        version="1.0.0",
        lifespan=lifespan
    )

    app.include_router(health.router)
    app.include_router(tasks.router)

    return app


app = create_app()
```

**Expected Output:**
- FastAPI app created with metadata
- Routes registered
- Database tables created on startup

**Spec Reference:** Section 5.6 (OpenAPI Documentation)
**Plan Reference:** Section 7.4 (FastAPI Application)

**Completion Criteria:**
- [ ] `api.py` file exists
- [ ] `create_app()` function defined
- [ ] Health and tasks routers included
- [ ] Lifespan creates database tables
- [ ] App has title, description, version
- [ ] `app` singleton exported
- [ ] Type hints and docstrings present

---

### TASK-228: Implement main.py Entry Point

**Category:** Entry Point
**Preconditions:** TASK-227 complete
**Depends On:** TASK-227

**Description:**
Create application entry point for running with uvicorn.

**Artifacts to Create:**
- `todo_api/main.py`

**Implementation Details:**
```python
"""Todo API - Phase II Entry Point.

Run with: python main.py
Or: uvicorn main:app --reload
"""

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

**Expected Output:**
- Application runs with `python main.py`
- Listens on port 8000
- Hot reload enabled in development

**Spec Reference:** Section 9.3 (Project Structure)
**Plan Reference:** Section 11.1 (Main Module)

**Completion Criteria:**
- [ ] `main.py` file exists
- [ ] Imports app from api module
- [ ] Runs uvicorn with correct settings
- [ ] `if __name__ == "__main__"` guard present
- [ ] Docstring present

---

### TASK-229: Create Test Fixtures and Configuration

**Category:** Test
**Preconditions:** TASK-228 complete
**Depends On:** TASK-228

**Description:**
Create pytest configuration and shared test fixtures.

**Artifacts to Create:**
- `todo_api/tests/conftest.py`

**Implementation Details:**
```python
"""Pytest configuration and fixtures."""

import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, Session, create_engine
from sqlmodel.pool import StaticPool

from src.presentation.api import app
from src.infrastructure.database import get_session


@pytest.fixture(name="engine")
def engine_fixture():
    """Create in-memory SQLite engine for testing."""
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    yield engine
    SQLModel.metadata.drop_all(engine)


@pytest.fixture(name="session")
def session_fixture(engine):
    """Create database session for testing."""
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    """Create test client with overridden dependencies."""
    def get_session_override():
        yield session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()
```

**Expected Output:**
- Test fixtures provide isolated database
- Client fixture overrides session dependency

**Spec Reference:** Section 8.4 (Code Quality - Testing)
**Plan Reference:** Section 9.2 (Test Fixtures)

**Completion Criteria:**
- [ ] `conftest.py` file exists
- [ ] `engine_fixture` creates in-memory SQLite
- [ ] `session_fixture` yields session
- [ ] `client_fixture` overrides get_session
- [ ] Dependencies cleared after test
- [ ] Type hints and docstrings present

---

### TASK-230: Write Integration Tests for All Endpoints

**Category:** Test
**Preconditions:** TASK-229 complete
**Depends On:** TASK-229

**Description:**
Create comprehensive integration tests for all API endpoints.

**Artifacts to Create:**
- `todo_api/tests/integration/test_api.py`

**Test Cases:**

| Test Function | Description | Expected |
|---------------|-------------|----------|
| `test_health_check` | GET /health | 200, status="healthy" |
| `test_create_task` | POST /tasks | 201, returns task |
| `test_create_task_empty_title` | POST with "" | 422 |
| `test_create_task_whitespace_title` | POST with "   " | 422 |
| `test_create_task_long_title` | POST with 201 chars | 422 |
| `test_list_tasks_empty` | GET /tasks empty | 200, [] |
| `test_list_tasks_with_data` | GET /tasks with data | 200, list |
| `test_list_tasks_ordered` | GET /tasks order | Ordered by ID |
| `test_get_task` | GET /tasks/{id} | 200, task |
| `test_get_task_not_found` | GET /tasks/999 | 404 |
| `test_update_task` | PUT /tasks/{id} | 200, updated |
| `test_update_task_not_found` | PUT /tasks/999 | 404 |
| `test_update_task_empty_title` | PUT with "" | 422 |
| `test_delete_task` | DELETE /tasks/{id} | 204 |
| `test_delete_task_not_found` | DELETE /tasks/999 | 404 |
| `test_toggle_task_to_complete` | PATCH toggle | 200, is_complete=True |
| `test_toggle_task_to_incomplete` | PATCH toggle again | 200, is_complete=False |
| `test_toggle_task_not_found` | PATCH /tasks/999/toggle | 404 |
| `test_task_has_timestamps` | Check created_at, updated_at | Both present |
| `test_update_changes_updated_at` | PUT changes timestamp | updated_at changed |

**Expected Output:**
- All 20 tests pass
- All endpoints verified

**Spec Reference:** Section 11.1 (Feature Completion Checklist)
**Plan Reference:** Section 9.4 (Integration Tests)

**Completion Criteria:**
- [ ] `test_api.py` file exists
- [ ] All 20 test cases implemented
- [ ] All tests pass
- [ ] Tests use client fixture

---

### TASK-231: Create README Documentation

**Category:** Documentation
**Preconditions:** TASK-228 complete
**Depends On:** TASK-228

**Description:**
Create comprehensive README with setup and usage instructions.

**Artifacts to Create:**
- `todo_api/README.md`

**Content Sections:**
1. Overview
2. Requirements
3. Installation
4. Configuration (environment variables)
5. Running the Application
6. API Endpoints
7. Running Tests
8. Project Structure

**Expected Output:**
- Complete documentation for Phase II

**Spec Reference:** Section 11.3 (Phase Completion Criteria)
**Plan Reference:** Section 10.1 (Task T-216)

**Completion Criteria:**
- [ ] `README.md` file exists
- [ ] All sections complete
- [ ] Setup instructions accurate
- [ ] API endpoints documented

---

### TASK-232: Final Verification and Acceptance Testing

**Category:** Verification
**Preconditions:** TASK-230, TASK-231 complete
**Depends On:** TASK-231

**Description:**
Perform final verification of all acceptance criteria.

**Verification Steps:**

1. **Run all tests:**
   ```bash
   python -m pytest tests/ -v --cov=src --cov-report=term-missing
   ```

2. **Verify coverage >= 80%**

3. **Start application:**
   ```bash
   python main.py
   ```

4. **Verify OpenAPI docs at /docs**

5. **Manual API testing:**
   - Create task
   - List tasks
   - Get single task
   - Update task
   - Toggle task
   - Delete task
   - Verify error responses

6. **Verify database persistence:**
   - Create task
   - Restart application
   - Verify task persists

**Acceptance Criteria Checklist (40 total):**

| ID | Criterion | Status |
|----|-----------|--------|
| AC-101-1 | POST /tasks accepts JSON with title | [ ] |
| AC-101-2 | System assigns unique ID | [ ] |
| AC-101-3 | Task created with is_complete=false | [ ] |
| AC-101-4 | Returns 201 Created | [ ] |
| AC-101-5 | Response includes all fields | [ ] |
| AC-101-6 | Empty title returns 422 | [ ] |
| AC-101-7 | Whitespace title returns 422 | [ ] |
| AC-101-8 | Long title returns 422 | [ ] |
| AC-102-1 | GET /tasks returns list | [ ] |
| AC-102-2 | Response is JSON array | [ ] |
| AC-102-3 | Each task has all fields | [ ] |
| AC-102-4 | Tasks ordered by ID | [ ] |
| AC-102-5 | Empty returns [] | [ ] |
| AC-102-6 | Returns 200 OK | [ ] |
| AC-103-1 | GET /tasks/{id} returns task | [ ] |
| AC-103-2 | Response has all fields | [ ] |
| AC-103-3 | Non-existent returns 404 | [ ] |
| AC-103-4 | Invalid ID returns 422 | [ ] |
| AC-103-5 | Valid task returns 200 | [ ] |
| AC-104-1 | PUT accepts JSON with title | [ ] |
| AC-104-2 | System updates title | [ ] |
| AC-104-3 | System updates updated_at | [ ] |
| AC-104-4 | Returns 200 with task | [ ] |
| AC-104-5 | Non-existent returns 404 | [ ] |
| AC-104-6 | Empty title returns 422 | [ ] |
| AC-104-7 | Whitespace returns 422 | [ ] |
| AC-104-8 | Long title returns 422 | [ ] |
| AC-105-1 | DELETE removes task | [ ] |
| AC-105-2 | Returns 204 | [ ] |
| AC-105-3 | Non-existent returns 404 | [ ] |
| AC-105-4 | Task permanently removed | [ ] |
| AC-106-1 | PATCH toggles is_complete | [ ] |
| AC-106-2 | Incomplete becomes complete | [ ] |
| AC-106-3 | Complete becomes incomplete | [ ] |
| AC-106-4 | Updates updated_at | [ ] |
| AC-106-5 | Returns 200 with task | [ ] |
| AC-106-6 | Non-existent returns 404 | [ ] |
| AC-107-1 | GET /health returns status | [ ] |
| AC-107-2 | Status is "healthy" | [ ] |
| AC-107-3 | Returns 200 OK | [ ] |

**Spec Reference:** Section 11 (Acceptance Criteria Summary)
**Plan Reference:** Section 12 (Verification Checklist)

**Completion Criteria:**
- [ ] All tests pass
- [ ] Coverage >= 80%
- [ ] All 40 acceptance criteria verified
- [ ] Database persistence confirmed
- [ ] OpenAPI docs accessible

---

## 4. Task Execution Order

```
TASK-201 (Setup: Root Directory)
    │
    ├── TASK-202 (Setup: Source Directories)
    │       │
    │       └── TASK-204 (Setup: __init__.py) ←─┐
    │                                            │
    ├── TASK-203 (Setup: Test Directories) ─────┘
    │
    ├── TASK-205 (Setup: requirements.txt)
    │
    └── TASK-206 (Setup: data directory)
            │
            ▼
    TASK-207 (Infra: Database Config)
            │
            ▼
    TASK-208 (Infra: Session Management)
            │
            ▼
    TASK-209 (Domain: Task SQLModel)
            │
            ├───────────────────────────┐
            ▼                           ▼
    TASK-210 (Infra: Repo Create)   TASK-219 (Pres: Schemas)
            │
            ▼
    TASK-211 (Infra: Repo Read)
            │
            ├───────────────┐
            ▼               ▼
    TASK-212         TASK-213
    (Repo Update)    (Repo Delete)
            │               │
            └───────┬───────┘
                    │
                    ▼
            TASK-214 (App: Service Create)
                    │
                    ▼
            TASK-215 (App: Service Read)
                    │
            ┌───────┼───────┐
            ▼       ▼       ▼
    TASK-216  TASK-217  TASK-218
    (Update)  (Delete)  (Toggle)
            │       │       │
            └───────┴───────┘
                    │
                    ▼
            TASK-220 (Pres: Dependencies)
                    │
            ┌───────┴───────┐
            ▼               ▼
    TASK-221         TASK-222
    (Health Route)   (POST Route)
                            │
                            ▼
                    TASK-223 (GET Routes)
                            │
            ┌───────┬───────┼───────┐
            ▼       ▼       ▼       ▼
    TASK-224  TASK-225  TASK-226
    (PUT)     (DELETE)  (PATCH)
            │       │       │
            └───────┴───────┘
                    │
                    ▼
            TASK-227 (Pres: FastAPI App)
                    │
                    ▼
            TASK-228 (Entry: main.py)
                    │
                    ▼
            TASK-229 (Test: Fixtures)
                    │
                    ▼
            TASK-230 (Test: Integration)
                    │
                    ▼
            TASK-231 (Docs: README)
                    │
                    ▼
            TASK-232 (Verification)
```

---

## 5. Acceptance Criteria Traceability

| AC ID | Description | Task(s) |
|-------|-------------|---------|
| AC-101-1 | POST accepts JSON title | TASK-222 |
| AC-101-2 | Unique ID assigned | TASK-209, TASK-210 |
| AC-101-3 | Created with is_complete=false | TASK-214 |
| AC-101-4 | Returns 201 Created | TASK-222 |
| AC-101-5 | Response has all fields | TASK-219, TASK-222 |
| AC-101-6 | Empty title returns 422 | TASK-219 |
| AC-101-7 | Whitespace title returns 422 | TASK-219 |
| AC-101-8 | Long title returns 422 | TASK-219 |
| AC-102-1 | GET /tasks returns list | TASK-223 |
| AC-102-2 | Response is JSON array | TASK-223 |
| AC-102-3 | Tasks have all fields | TASK-219, TASK-223 |
| AC-102-4 | Ordered by ID | TASK-211 |
| AC-102-5 | Empty returns [] | TASK-223 |
| AC-102-6 | Returns 200 OK | TASK-223 |
| AC-103-1 | GET /tasks/{id} returns task | TASK-223 |
| AC-103-2 | Response has all fields | TASK-219, TASK-223 |
| AC-103-3 | Non-existent returns 404 | TASK-223 |
| AC-103-4 | Invalid ID returns 422 | FastAPI auto |
| AC-103-5 | Valid returns 200 | TASK-223 |
| AC-104-1 | PUT accepts JSON title | TASK-224 |
| AC-104-2 | Updates title | TASK-216 |
| AC-104-3 | Updates updated_at | TASK-216 |
| AC-104-4 | Returns 200 with task | TASK-224 |
| AC-104-5 | Non-existent returns 404 | TASK-224 |
| AC-104-6 | Empty title returns 422 | TASK-219 |
| AC-104-7 | Whitespace returns 422 | TASK-219 |
| AC-104-8 | Long title returns 422 | TASK-219 |
| AC-105-1 | DELETE removes task | TASK-225 |
| AC-105-2 | Returns 204 | TASK-225 |
| AC-105-3 | Non-existent returns 404 | TASK-225 |
| AC-105-4 | Permanently removed | TASK-213 |
| AC-106-1 | PATCH toggles is_complete | TASK-226 |
| AC-106-2 | Incomplete → complete | TASK-218 |
| AC-106-3 | Complete → incomplete | TASK-218 |
| AC-106-4 | Updates updated_at | TASK-218 |
| AC-106-5 | Returns 200 with task | TASK-226 |
| AC-106-6 | Non-existent returns 404 | TASK-226 |
| AC-107-1 | GET /health returns status | TASK-221 |
| AC-107-2 | Status is "healthy" | TASK-221 |
| AC-107-3 | Returns 200 OK | TASK-221 |

---

## 6. Document Control

### 6.1 Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2025-12-28 | Agent | Initial task breakdown |

### 6.2 Approval

| Role | Name | Date | Status |
|------|------|------|--------|
| Task Author | Agent | 2025-12-28 | Draft |
| Human Reviewer | — | — | Pending |

---

## 7. References

- [PHASE-II-PLAN.md](./PHASE-II-PLAN.md) — Phase II Technical Plan
- [PHASE-II-SPEC.md](../specs/PHASE-II-SPEC.md) — Phase II Specification
- [CONSTITUTION.md](../CONSTITUTION.md) — Global Constitution

---

*End of Phase II Implementation Tasks*
