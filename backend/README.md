# Backend - Phase II Todo API

Python FastAPI backend for the Evolution of Todo Phase II project.

## Setup

### 1. Create Virtual Environment

```bash
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (macOS/Linux)
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment

```bash
cp .env.example .env
# Edit .env with your configuration
```

### 4. Initialize Database

```bash
# Run migrations
alembic upgrade head
```

### 5. Run Development Server

```bash
uvicorn src.presentation.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- API: http://localhost:8000
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Development

### Run Tests

```bash
pytest tests/ -v
```

### Run Tests with Coverage

```bash
pytest tests/ --cov=src --cov-report=term-missing
```

### Lint Code

```bash
ruff check src/
```

### Format Code

```bash
black src/ tests/
```

## Project Structure

```
backend/
├── src/
│   ├── domain/              # Business entities
│   ├── application/         # Business logic
│   ├── infrastructure/      # External dependencies
│   └── presentation/        # API layer
├── tests/
│   ├── unit/               # Unit tests
│   └── integration/        # API tests
├── alembic/                # Database migrations
└── data/                   # SQLite database (dev)
```

## API Documentation

Once the server is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
