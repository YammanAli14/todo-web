# Todo API - Phase II

A RESTful API for task management built with FastAPI and SQLModel.

## Overview

Phase II transforms the Phase I console application into a stateless HTTP API with database persistence. All task data persists across application restarts.

## Requirements

- Python 3.11 or higher

## Installation

1. Navigate to the project directory:
   ```bash
   cd todo_api
   ```

2. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

### Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `ENVIRONMENT` | No | `development` | Set to `production` for PostgreSQL |
| `DATABASE_URL` | Yes (prod) | - | PostgreSQL connection string |

### Development

By default, the application uses SQLite stored in `./data/todo.db`.

### Production

Set environment variables:
```bash
export ENVIRONMENT=production
export DATABASE_URL=postgresql://user:password@host:port/database
```

## Running the Application

### Development

```bash
python main.py
```

Or with uvicorn directly:
```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`.

### API Documentation

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- OpenAPI JSON: http://localhost:8000/openapi.json

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | /health | Health check |
| GET | /tasks | List all tasks |
| POST | /tasks | Create a task |
| GET | /tasks/{id} | Get a task |
| PUT | /tasks/{id} | Update a task |
| DELETE | /tasks/{id} | Delete a task |
| PATCH | /tasks/{id}/toggle | Toggle completion |

### Examples

**Create a task:**
```bash
curl -X POST http://localhost:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Buy groceries"}'
```

**List all tasks:**
```bash
curl http://localhost:8000/tasks
```

**Get a task:**
```bash
curl http://localhost:8000/tasks/1
```

**Update a task:**
```bash
curl -X PUT http://localhost:8000/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{"title": "Buy groceries and milk"}'
```

**Toggle completion:**
```bash
curl -X PATCH http://localhost:8000/tasks/1/toggle
```

**Delete a task:**
```bash
curl -X DELETE http://localhost:8000/tasks/1
```

## Running Tests

```bash
python -m pytest tests/ -v
```

With coverage:
```bash
python -m pytest tests/ -v --cov=src --cov-report=term-missing
```

## Project Structure

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
│   │   ├── database.py          # Database configuration
│   │   └── task_repository.py   # Database operations
│   └── presentation/
│       ├── __init__.py
│       ├── api.py               # FastAPI application
│       ├── dependencies.py      # Dependency injection
│       ├── schemas.py           # Request/Response schemas
│       └── routes/
│           ├── __init__.py
│           ├── health.py        # Health endpoint
│           └── tasks.py         # Task endpoints
├── tests/
│   ├── __init__.py
│   ├── conftest.py              # Test fixtures
│   ├── unit/
│   │   └── __init__.py
│   └── integration/
│       ├── __init__.py
│       └── test_api.py          # API tests
├── data/                        # SQLite database (dev)
├── main.py                      # Entry point
├── requirements.txt             # Dependencies
└── README.md
```

## Architecture

The application follows clean architecture principles:

- **Domain Layer** (`src/domain/`) - Task entity definition
- **Application Layer** (`src/application/`) - Business logic
- **Infrastructure Layer** (`src/infrastructure/`) - Database operations
- **Presentation Layer** (`src/presentation/`) - API routes and schemas

## License

Part of the Evolution of Todo project.
