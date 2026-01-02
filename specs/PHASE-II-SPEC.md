# Phase II Specification — API Layer

**Document ID:** SPEC-PHASE-II-001
**Version:** 1.0.0
**Status:** Draft — Pending Approval
**Governing Document:** [CONSTITUTION.md](../CONSTITUTION.md)
**Phase:** II — API Layer
**Depends On:** Phase I (Complete)

---

## 1. Overview

### 1.1 Purpose

This specification defines the requirements for Phase II of the Evolution of Todo project: a RESTful API backend using FastAPI with persistent database storage via Neon PostgreSQL.

### 1.2 Scope Summary

Phase II transforms the in-memory console application into a stateless HTTP API with database persistence. The CLI is replaced by REST endpoints. All task data persists across application restarts.

### 1.3 Constitutional Compliance

This specification complies with:

- **Article I** — Defines scope, requirements, interfaces, acceptance criteria, and dependencies
- **Article III, Section 3.1** — Implements Phase II: FastAPI backend, Neon PostgreSQL, REST API
- **Article III, Section 3.2** — Contains no forward leakage to future phases
- **Article IV** — Uses mandatory technologies: FastAPI, SQLModel, Neon PostgreSQL
- **Article V** — Adheres to clean architecture and quality principles

---

## 2. Scope Definition

### 2.1 In Scope

| Item | Description |
|------|-------------|
| Runtime Environment | Python 3.11+ FastAPI application |
| Storage | Neon PostgreSQL (production), SQLite (development/testing) |
| Interface | RESTful HTTP API |
| User Model | Single user, no authentication |
| Features | CRUD operations via REST endpoints |
| Documentation | Auto-generated OpenAPI/Swagger |

### 2.2 Explicitly Out of Scope

The following are **prohibited** in Phase II:

| Excluded Item | Reason |
|---------------|--------|
| User authentication | Phase IV feature |
| Multiple users/tenants | Phase IV+ feature |
| Frontend/Web UI | Phase IV feature |
| Agent integration | Phase III feature |
| MCP/Tool protocols | Phase III feature |
| Docker/Kubernetes | Phase V feature |
| Message queues | Phase V feature |
| CLI interface | Replaced by API |
| Task categories/tags | Not in Phase II requirements |
| Task priorities | Not in Phase II requirements |
| Due dates | Not in Phase II requirements |
| Search/filter functionality | Not in Phase II requirements |
| Pagination | Not in Phase II requirements |
| Rate limiting | Not in Phase II requirements |

---

## 3. User Stories

### 3.1 US-101: Create Task via API

**As an** API client
**I want to** create a new task by sending a POST request
**So that** the task is persisted in the database

**Acceptance Criteria:**

| ID | Criterion |
|----|-----------|
| AC-101-1 | POST /tasks accepts JSON body with title field |
| AC-101-2 | System assigns a unique ID to the task |
| AC-101-3 | Task is created with status "incomplete" (is_complete=false) |
| AC-101-4 | System returns 201 Created with task JSON |
| AC-101-5 | Response includes id, title, is_complete, created_at, updated_at |
| AC-101-6 | Empty title returns 422 Unprocessable Entity |
| AC-101-7 | Whitespace-only title returns 422 Unprocessable Entity |
| AC-101-8 | Title > 200 characters returns 422 Unprocessable Entity |

### 3.2 US-102: Get All Tasks via API

**As an** API client
**I want to** retrieve all tasks by sending a GET request
**So that** I can see all stored tasks

**Acceptance Criteria:**

| ID | Criterion |
|----|-----------|
| AC-102-1 | GET /tasks returns list of all tasks |
| AC-102-2 | Response is JSON array |
| AC-102-3 | Each task includes id, title, is_complete, created_at, updated_at |
| AC-102-4 | Tasks are ordered by id ascending |
| AC-102-5 | Empty database returns empty array [] |
| AC-102-6 | System returns 200 OK |

### 3.3 US-103: Get Single Task via API

**As an** API client
**I want to** retrieve a specific task by ID
**So that** I can view its details

**Acceptance Criteria:**

| ID | Criterion |
|----|-----------|
| AC-103-1 | GET /tasks/{id} returns single task |
| AC-103-2 | Response includes id, title, is_complete, created_at, updated_at |
| AC-103-3 | Non-existent ID returns 404 Not Found |
| AC-103-4 | Invalid ID format returns 422 Unprocessable Entity |
| AC-103-5 | System returns 200 OK for valid task |

### 3.4 US-104: Update Task via API

**As an** API client
**I want to** update a task's title by sending a PUT request
**So that** I can modify existing tasks

**Acceptance Criteria:**

| ID | Criterion |
|----|-----------|
| AC-104-1 | PUT /tasks/{id} accepts JSON body with title field |
| AC-104-2 | System updates the task title |
| AC-104-3 | System updates the updated_at timestamp |
| AC-104-4 | System returns 200 OK with updated task JSON |
| AC-104-5 | Non-existent ID returns 404 Not Found |
| AC-104-6 | Empty title returns 422 Unprocessable Entity |
| AC-104-7 | Whitespace-only title returns 422 Unprocessable Entity |
| AC-104-8 | Title > 200 characters returns 422 Unprocessable Entity |

### 3.5 US-105: Delete Task via API

**As an** API client
**I want to** delete a task by sending a DELETE request
**So that** I can remove tasks I no longer need

**Acceptance Criteria:**

| ID | Criterion |
|----|-----------|
| AC-105-1 | DELETE /tasks/{id} removes the task |
| AC-105-2 | System returns 204 No Content on success |
| AC-105-3 | Non-existent ID returns 404 Not Found |
| AC-105-4 | Task is permanently removed from database |

### 3.6 US-106: Toggle Task Completion via API

**As an** API client
**I want to** toggle a task's completion status via PATCH request
**So that** I can mark tasks complete or incomplete

**Acceptance Criteria:**

| ID | Criterion |
|----|-----------|
| AC-106-1 | PATCH /tasks/{id}/toggle toggles is_complete |
| AC-106-2 | If task is incomplete, it becomes complete |
| AC-106-3 | If task is complete, it becomes incomplete |
| AC-106-4 | System updates the updated_at timestamp |
| AC-106-5 | System returns 200 OK with updated task JSON |
| AC-106-6 | Non-existent ID returns 404 Not Found |

### 3.7 US-107: API Health Check

**As an** API client
**I want to** check if the API is running
**So that** I can verify service availability

**Acceptance Criteria:**

| ID | Criterion |
|----|-----------|
| AC-107-1 | GET /health returns health status |
| AC-107-2 | Response includes status: "healthy" |
| AC-107-3 | System returns 200 OK |

---

## 4. Data Model

### 4.1 Task Entity

The Task entity persists to the database.

```
Task (Database Table: tasks)
├── id: int              # Primary key, auto-increment
├── title: str           # Task description, required, max 200 chars
├── is_complete: bool    # Completion status, default False
├── created_at: datetime # Timestamp of creation, auto-set
└── updated_at: datetime # Timestamp of last update, auto-updated
```

### 4.2 Field Specifications

| Field | Type | Constraints | Default | Database Column |
|-------|------|-------------|---------|-----------------|
| `id` | `int` | Primary key, auto-increment | Auto | `id SERIAL PRIMARY KEY` |
| `title` | `str` | Non-empty, max 200 chars, NOT NULL | Required | `title VARCHAR(200) NOT NULL` |
| `is_complete` | `bool` | NOT NULL | `False` | `is_complete BOOLEAN DEFAULT FALSE` |
| `created_at` | `datetime` | NOT NULL, auto-set | `now()` | `created_at TIMESTAMP DEFAULT NOW()` |
| `updated_at` | `datetime` | NOT NULL, auto-update | `now()` | `updated_at TIMESTAMP DEFAULT NOW()` |

### 4.3 SQLModel Definition

```python
class Task(SQLModel, table=True):
    __tablename__ = "tasks"

    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(max_length=200, nullable=False)
    is_complete: bool = Field(default=False, nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
```

---

## 5. API Interface Specification

### 5.1 Base URL

```
Development: http://localhost:8000
Production: https://<configured-domain>
```

### 5.2 Endpoints

| Method | Path | Description | Request Body | Response |
|--------|------|-------------|--------------|----------|
| GET | /health | Health check | None | HealthResponse |
| GET | /tasks | List all tasks | None | TaskResponse[] |
| POST | /tasks | Create task | TaskCreate | TaskResponse |
| GET | /tasks/{id} | Get single task | None | TaskResponse |
| PUT | /tasks/{id} | Update task | TaskUpdate | TaskResponse |
| DELETE | /tasks/{id} | Delete task | None | None (204) |
| PATCH | /tasks/{id}/toggle | Toggle completion | None | TaskResponse |

### 5.3 Request/Response Schemas

#### 5.3.1 TaskCreate (Request)

```json
{
  "title": "string (required, 1-200 chars)"
}
```

#### 5.3.2 TaskUpdate (Request)

```json
{
  "title": "string (required, 1-200 chars)"
}
```

#### 5.3.3 TaskResponse (Response)

```json
{
  "id": 1,
  "title": "Buy groceries",
  "is_complete": false,
  "created_at": "2025-12-28T10:30:00Z",
  "updated_at": "2025-12-28T10:30:00Z"
}
```

#### 5.3.4 HealthResponse (Response)

```json
{
  "status": "healthy"
}
```

#### 5.3.5 ErrorResponse (Response)

```json
{
  "detail": "Error message"
}
```

### 5.4 HTTP Status Codes

| Code | Meaning | When Used |
|------|---------|-----------|
| 200 | OK | Successful GET, PUT, PATCH |
| 201 | Created | Successful POST |
| 204 | No Content | Successful DELETE |
| 404 | Not Found | Task ID does not exist |
| 422 | Unprocessable Entity | Validation error |
| 500 | Internal Server Error | Unexpected server error |

### 5.5 Content Type

All requests and responses use `application/json`.

### 5.6 OpenAPI Documentation

- Swagger UI available at `/docs`
- ReDoc available at `/redoc`
- OpenAPI JSON at `/openapi.json`

---

## 6. Error Handling Specification

### 6.1 Validation Errors (422)

| Error | Trigger | Response Detail |
|-------|---------|-----------------|
| Empty title | title is "" | "Title cannot be empty" |
| Whitespace title | title is "   " | "Title cannot be empty" |
| Title too long | len(title) > 200 | "Title must be 200 characters or less" |
| Invalid ID | ID is not integer | FastAPI auto-validation |
| Missing field | Required field missing | FastAPI auto-validation |

### 6.2 Not Found Errors (404)

| Error | Trigger | Response Detail |
|-------|---------|-----------------|
| Task not found | ID does not exist | "Task not found" |

### 6.3 Error Response Format

All errors follow the standard FastAPI format:

```json
{
  "detail": "Error message here"
}
```

---

## 7. Database Configuration

### 7.1 Development Database

| Setting | Value |
|---------|-------|
| Database | SQLite |
| File | `./data/todo.db` |
| Connection | `sqlite:///./data/todo.db` |

### 7.2 Production Database

| Setting | Value |
|---------|-------|
| Provider | Neon PostgreSQL |
| Connection | Environment variable `DATABASE_URL` |
| SSL | Required |

### 7.3 Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `DATABASE_URL` | Yes (prod) | PostgreSQL connection string |
| `ENVIRONMENT` | No | "development" or "production" (default: development) |

### 7.4 Database Migrations

- SQLModel handles table creation
- `SQLModel.metadata.create_all()` creates tables on startup
- No complex migrations required for Phase II

---

## 8. Non-Functional Requirements

### 8.1 Performance

| Requirement | Specification |
|-------------|---------------|
| Response Time | All operations complete in < 500ms |
| Concurrent Requests | Handle 100 concurrent connections |
| Startup Time | Application starts in < 5 seconds |

### 8.2 Reliability

| Requirement | Specification |
|-------------|---------------|
| Availability | Service remains available during normal operation |
| Error Recovery | Invalid requests do not crash the service |
| Data Integrity | All operations are atomic via database transactions |

### 8.3 Statelessness

| Requirement | Specification |
|-------------|---------------|
| No Session State | No server-side session storage |
| Database State | All state persisted to database |
| Scalability | Service can be horizontally scaled |

### 8.4 Code Quality

Per Constitution Article V, Section 5.4:

| Requirement | Specification |
|-------------|---------------|
| Type Hints | All function signatures typed |
| Documentation | All endpoints documented via OpenAPI |
| Testing | Minimum 80% code coverage |
| Linting | Must pass ruff |
| Formatting | Must pass black |

---

## 9. Technical Constraints

### 9.1 Required Technologies

| Technology | Version | Purpose |
|------------|---------|---------|
| Python | 3.11+ | Runtime |
| FastAPI | 0.100+ | Web framework |
| SQLModel | 0.0.14+ | ORM |
| Uvicorn | Latest | ASGI server |
| Pydantic | v2 | Validation (via FastAPI) |
| httpx | Latest | Testing HTTP client |
| pytest | Latest | Testing framework |

### 9.2 Dependencies

```
fastapi>=0.100.0
sqlmodel>=0.0.14
uvicorn[standard]>=0.23.0
pydantic>=2.0.0
pydantic-settings>=2.0.0
psycopg2-binary>=2.9.0
httpx>=0.24.0
pytest>=7.0.0
pytest-asyncio>=0.21.0
```

### 9.3 Project Structure

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
│   │   ├── database.py          # Database connection
│   │   └── task_repository.py   # Database operations
│   └── presentation/
│       ├── __init__.py
│       ├── api.py               # FastAPI app setup
│       ├── routes/
│       │   ├── __init__.py
│       │   ├── health.py        # Health endpoint
│       │   └── tasks.py         # Task endpoints
│       └── schemas.py           # Request/Response schemas
├── tests/
│   ├── __init__.py
│   ├── conftest.py              # Test fixtures
│   ├── unit/
│   │   ├── __init__.py
│   │   └── test_task_service.py
│   └── integration/
│       ├── __init__.py
│       └── test_api.py          # API endpoint tests
├── data/                        # SQLite database (dev)
├── main.py                      # Application entry point
├── requirements.txt             # Dependencies
└── README.md
```

### 9.4 Prohibited Technologies

The following are explicitly prohibited in Phase II:

- Authentication/authorization systems
- JWT tokens
- Session management
- Frontend frameworks
- WebSockets
- Background task queues
- Caching layers (Redis, etc.)
- Docker/containerization

---

## 10. Migration from Phase I

### 10.1 Changes from Phase I

| Component | Phase I | Phase II |
|-----------|---------|----------|
| Interface | CLI menu | REST API |
| Storage | In-memory dict | PostgreSQL/SQLite |
| Framework | None | FastAPI |
| ORM | None | SQLModel |
| Data Model | Dataclass | SQLModel table |
| ID Generation | Sequential counter | Database auto-increment |

### 10.2 Retained Concepts

| Concept | Description |
|---------|-------------|
| Clean Architecture | Same layer structure |
| Task Entity | Same fields (plus timestamps) |
| Title Validation | Same rules (empty, whitespace, length) |
| Toggle Logic | Same behavior |

### 10.3 Deprecated Components

| Component | Reason |
|-----------|--------|
| `presentation/cli.py` | Replaced by REST API |
| In-memory repository | Replaced by database repository |

---

## 11. Acceptance Criteria Summary

### 11.1 Feature Completion Checklist

| Feature | Criteria Count | Required Pass |
|---------|----------------|---------------|
| Create Task (POST) | 8 | All |
| List Tasks (GET) | 6 | All |
| Get Task (GET) | 5 | All |
| Update Task (PUT) | 8 | All |
| Delete Task (DELETE) | 4 | All |
| Toggle Complete (PATCH) | 6 | All |
| Health Check | 3 | All |
| **Total** | **40** | **All** |

### 11.2 Quality Checklist

| Requirement | Pass Criteria |
|-------------|---------------|
| Type Hints | All functions typed |
| Documentation | OpenAPI auto-generated |
| Test Coverage | >= 80% on business logic |
| Linting | Zero ruff errors |
| Formatting | Zero black changes |
| Database | Tables created successfully |

### 11.3 Phase Completion Criteria

Phase II is complete when:

1. All 40 acceptance criteria pass
2. All quality requirements met
3. All tests pass
4. API documentation accessible at /docs
5. Database persistence verified
6. README documentation complete
7. Human review approves deliverable

---

## 12. Glossary

| Term | Definition |
|------|------------|
| REST | Representational State Transfer |
| CRUD | Create, Read, Update, Delete |
| Endpoint | URL path that accepts HTTP requests |
| SQLModel | Python ORM combining SQLAlchemy and Pydantic |
| FastAPI | Modern Python web framework for APIs |
| Neon | Serverless PostgreSQL platform |
| OpenAPI | API specification standard (Swagger) |

---

## 13. Document Control

### 13.1 Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2025-12-28 | Agent | Initial specification |

### 13.2 Approval

| Role | Name | Date | Status |
|------|------|------|--------|
| Specification Author | Agent | 2025-12-28 | Draft |
| Human Reviewer | — | — | Pending |

---

## 14. References

- [CONSTITUTION.md](../CONSTITUTION.md) — Global project constitution
- [PHASE-I-SPEC.md](./PHASE-I-SPEC.md) — Phase I specification
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLModel Documentation](https://sqlmodel.tiangolo.com/)
- [Neon Documentation](https://neon.tech/docs)

---

*End of Phase II Specification*
