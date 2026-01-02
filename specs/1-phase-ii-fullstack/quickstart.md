# Quickstart: Phase II Full-Stack Todo Application

**Date**: 2026-01-02
**Feature**: 1-phase-ii-fullstack
**Purpose**: Developer setup guide for local development

---

## Prerequisites

### Required Software

- **Python 3.11+**: Backend runtime
- **Node.js 20+**: Frontend runtime
- **Git**: Version control
- **Code Editor**: VS Code (recommended) or any editor with Python/TypeScript support

### Required Accounts

- **Neon PostgreSQL**: Create a free account at [neon.tech](https://neon.tech) for database hosting
- **Better Auth**: Account setup (if required by Better Auth provider)

---

## Project Structure

```
booseai/
├── backend/                 # Python FastAPI backend
│   ├── src/
│   │   ├── domain/          # Entities (User, Todo)
│   │   ├── application/     # Business logic
│   │   ├── infrastructure/  # Database, Better Auth
│   │   └── presentation/    # API routes
│   ├── tests/
│   ├── requirements.txt
│   └── .env                 # Backend environment variables
│
├── frontend/                # Next.js frontend
│   ├── app/                 # App Router pages
│   ├── components/          # React components
│   ├── lib/                 # API client, utilities
│   ├── tests/
│   ├── package.json
│   └── .env.local           # Frontend environment variables
│
└── specs/                   # Feature specifications
    └── 1-phase-ii-fullstack/
        ├── spec.md
        ├── plan.md
        ├── research.md
        ├── data-model.md
        ├── quickstart.md (this file)
        └── contracts/
```

---

## Backend Setup

### Step 1: Create Backend Directory

```bash
cd booseai
mkdir -p backend/src/{domain,application,infrastructure,presentation}
cd backend
```

### Step 2: Set Up Python Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies

Create `requirements.txt`:

```txt
# Web framework
fastapi>=0.100.0
uvicorn[standard]>=0.23.0

# Database & ORM
sqlmodel>=0.0.14
psycopg2-binary>=2.9.0
alembic>=1.12.0

# Validation
pydantic>=2.0.0
pydantic-settings>=2.0.0

# Authentication
better-auth>=1.0.0  # Check for actual package name
passlib[bcrypt]>=1.7.4
python-jose[cryptography]>=3.3.0

# Testing
pytest>=7.0.0
pytest-asyncio>=0.21.0
httpx>=0.24.0

# Code quality
ruff>=0.1.0
black>=23.0.0
```

Install:

```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables

Create `.env`:

```bash
# Database
DATABASE_URL=sqlite:///./data/todo_dev.db  # Local development
# DATABASE_URL=postgresql://user:pass@ep-xxx.neon.tech/neondb  # Production

# Better Auth
BETTER_AUTH_SECRET=your-secret-key-here-change-in-production
BETTER_AUTH_DATABASE_URL=${DATABASE_URL}

# Environment
ENVIRONMENT=development

# API
API_HOST=0.0.0.0
API_PORT=8000

# CORS
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

### Step 5: Create Database Tables

```bash
# Initialize Alembic (first time only)
alembic init alembic

# Edit alembic/env.py to import SQLModel models
# Then generate initial migration
alembic revision --autogenerate -m "Initial schema: users and todos"

# Apply migration
alembic upgrade head
```

### Step 6: Run Backend Server

```bash
uvicorn src.presentation.main:app --reload --host 0.0.0.0 --port 8000
```

Backend will be available at `http://localhost:8000`

API documentation at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

---

## Frontend Setup

### Step 1: Create Frontend Directory

```bash
cd booseai
npx create-next-app@latest frontend --typescript --tailwind --app --no-src-dir
cd frontend
```

Answer prompts:
- ✅ TypeScript: Yes
- ✅ ESLint: Yes
- ✅ Tailwind CSS: Yes
- ✅ App Router: Yes
- ❌ `src/` directory: No
- ✅ import alias (@/*): Yes

### Step 2: Install Additional Dependencies

```bash
npm install better-auth  # Check for actual package name
npm install --save-dev @testing-library/react @testing-library/jest-dom jest
```

### Step 3: Configure Environment Variables

Create `.env.local`:

```bash
# Backend API
NEXT_PUBLIC_API_URL=http://localhost:8000

# Better Auth
NEXT_PUBLIC_BETTER_AUTH_CLIENT_ID=your-client-id
```

### Step 4: Run Frontend Development Server

```bash
npm run dev
```

Frontend will be available at `http://localhost:3000`

---

## Development Workflow

### Start Both Servers

**Terminal 1 (Backend)**:
```bash
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
uvicorn src.presentation.main:app --reload
```

**Terminal 2 (Frontend)**:
```bash
cd frontend
npm run dev
```

### Typical Development Flow

1. **Make Backend Changes**:
   - Edit Python files in `backend/src/`
   - Uvicorn auto-reloads on file save
   - Test at `http://localhost:8000/docs`

2. **Make Frontend Changes**:
   - Edit TypeScript/React files in `frontend/`
   - Next.js hot-reloads automatically
   - View at `http://localhost:3000`

3. **Database Changes**:
   - Update SQLModel models
   - Generate migration: `alembic revision --autogenerate -m "Description"`
   - Apply migration: `alembic upgrade head`

---

## Testing

### Backend Tests

```bash
cd backend
pytest tests/ -v
```

Run with coverage:

```bash
pytest tests/ --cov=src --cov-report=term-missing
```

### Frontend Tests

```bash
cd frontend
npm test
```

---

## Common Tasks

### Create a New Backend Endpoint

1. Add route function in `backend/src/presentation/routers/`
2. Add business logic in `backend/src/application/`
3. Update OpenAPI docs automatically (FastAPI handles this)
4. Test at `/docs`

### Create a New Frontend Page

1. Create page component in `frontend/app/path/page.tsx`
2. Add API calls using `lib/api/` clients
3. Add components in `frontend/components/`

### Add a New Database Table

1. Create SQLModel entity in `backend/src/domain/`
2. Generate migration: `alembic revision --autogenerate -m "Add table"`
3. Review migration file
4. Apply: `alembic upgrade head`

---

## Switching to Production Database

### Step 1: Create Neon PostgreSQL Database

1. Sign up at [neon.tech](https://neon.tech)
2. Create a new project
3. Copy the connection string

### Step 2: Update Backend `.env`

```bash
# Comment out SQLite, use Neon
# DATABASE_URL=sqlite:///./data/todo_dev.db
DATABASE_URL=postgresql://user:pass@ep-xxx.us-east-2.aws.neon.tech/neondb?sslmode=require

BETTER_AUTH_DATABASE_URL=${DATABASE_URL}
```

### Step 3: Run Migrations on Neon

```bash
cd backend
alembic upgrade head
```

### Step 4: Restart Backend

```bash
uvicorn src.presentation.main:app --reload
```

Backend now uses Neon PostgreSQL instead of SQLite.

---

## Troubleshooting

### Backend Issues

**Issue**: `ModuleNotFoundError: No module named 'fastapi'`
- **Solution**: Activate virtual environment and run `pip install -r requirements.txt`

**Issue**: `sqlalchemy.exc.OperationalError: unable to open database file`
- **Solution**: Create `data/` directory: `mkdir data`

**Issue**: `CORS error when calling from frontend`
- **Solution**: Add frontend URL to `CORS_ORIGINS` in `.env`

### Frontend Issues

**Issue**: `Error: Cannot find module 'better-auth'`
- **Solution**: Run `npm install` to install dependencies

**Issue**: `API calls return 404`
- **Solution**: Verify `NEXT_PUBLIC_API_URL` in `.env.local` matches backend URL

**Issue**: `Unauthorized error on protected routes`
- **Solution**: Check that auth token is being sent in API client headers

### Database Issues

**Issue**: `alembic.util.exc.CommandError: Can't locate revision`
- **Solution**: Delete `alembic/versions/` contents and regenerate initial migration

**Issue**: `Connection to Neon fails`
- **Solution**: Check connection string includes `?sslmode=require`

---

## Code Quality Checks

### Backend Linting & Formatting

```bash
cd backend

# Run ruff linter
ruff check src/

# Run black formatter
black src/ tests/

# Type checking (if using mypy)
mypy src/
```

### Frontend Linting & Formatting

```bash
cd frontend

# Run ESLint
npm run lint

# Format with Prettier (if configured)
npm run format
```

---

## Next Steps

1. ✅ Set up development environment (this guide)
2. 📝 Review [spec.md](./spec.md) for requirements
3. 🏗️ Review [plan.md](./plan.md) for implementation plan
4. ✅ Run `/sp.tasks` to generate task breakdown
5. 🚀 Begin implementation following tasks

---

## Useful Commands Reference

### Backend

| Command | Purpose |
|---------|---------|
| `uvicorn src.presentation.main:app --reload` | Start dev server |
| `pytest tests/ -v` | Run tests |
| `alembic upgrade head` | Apply migrations |
| `alembic revision --autogenerate -m "msg"` | Create migration |
| `ruff check src/` | Lint code |
| `black src/` | Format code |

### Frontend

| Command | Purpose |
|---------|---------|
| `npm run dev` | Start dev server |
| `npm test` | Run tests |
| `npm run lint` | Lint code |
| `npm run build` | Production build |

---

## Resources

### Documentation

- **FastAPI**: https://fastapi.tiangolo.com/
- **SQLModel**: https://sqlmodel.tiangolo.com/
- **Next.js**: https://nextjs.org/docs
- **Better Auth**: https://www.better-auth.com/docs  (verify URL)
- **Neon PostgreSQL**: https://neon.tech/docs

### Project Documents

- [spec.md](./spec.md) - Feature specification
- [plan.md](./plan.md) - Implementation plan
- [research.md](./research.md) - Technical decisions
- [data-model.md](./data-model.md) - Database schema
- [contracts/openapi.yaml](./contracts/openapi.yaml) - API contract

---

*End of Quickstart Guide*
