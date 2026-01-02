# Research: Phase II Full-Stack Todo Application

**Date**: 2026-01-02
**Feature**: 1-phase-ii-fullstack
**Purpose**: Resolve technical decisions and patterns for Phase II implementation

---

## Research Areas

### 1. Backend Framework Selection

**Decision**: FastAPI

**Rationale**:
- Best Python framework for RESTful APIs with automatic OpenAPI documentation
- Native async/await support for better performance
- Excellent type hint integration with Pydantic for request/response validation
- Built-in dependency injection for clean architecture
- Wide ecosystem support and active development
- Straightforward Better Auth integration via middleware

**Alternatives Considered**:
- **Flask**: Simpler but lacks built-in async support and automatic API documentation
- **Django REST Framework**: More opinionated, heavier framework, overkill for Phase II scope
- **Litestar**: Newer framework, less mature ecosystem and documentation

**Constitution Compliance**: Article IV, Section 4.1 allows flexible "Python REST API (framework TBD)" - FastAPI is a reasonable choice.

---

### 2. ORM Selection

**Decision**: SQLModel

**Rationale**:
- Combines SQLAlchemy (mature ORM) with Pydantic models (FastAPI integration)
- Single model definition for both database and API schemas
- Type-safe with full IDE support
- Designed specifically for FastAPI by the same author (Sebastián Ramírez)
- Simplifies data validation and serialization
- Native async support for database operations

**Alternatives Considered**:
- **SQLAlchemy Core**: More verbose, requires separate Pydantic models
- **Tortoise ORM**: Async-first but less mature, different API from SQLAlchemy ecosystem
- **PonyORM**: Pythonic syntax but smaller community and limited async support

**Constitution Compliance**: Article IV, Section 4.1 specifies "SQLModel or equivalent" - SQLModel is explicitly mentioned.

---

### 3. Better Auth Integration Strategy

**Decision**: Better Auth as primary authentication library with FastAPI middleware integration

**Research Findings**:
- Better Auth provides comprehensive auth solutions for full-stack applications
- Supports both frontend (Next.js) and backend (Python) integration
- Handles session management, token generation, and user credential storage
- Provides built-in password hashing and validation

**Integration Approach**:
1. **Backend**: Use Better Auth Python SDK for user registration, login, and session validation
2. **Frontend**: Use Better Auth React hooks for auth state management
3. **Communication**: Better Auth manages session tokens/cookies between frontend and backend
4. **Middleware**: Create FastAPI middleware to validate Better Auth sessions on protected routes

**Alternatives Considered**:
- **Custom JWT implementation**: More work, security risks, violates Constitution requirement for Better Auth
- **Auth0/Firebase**: Third-party services not specified in Constitution

**Constitution Compliance**: Article IV, Section 4.1 mandates "Better Auth (signup/signin) | II–V" - this is required.

---

### 4. Database Schema Management

**Decision**: SQLModel metadata with alembic for migrations

**Rationale**:
- SQLModel inherits from SQLAlchemy, allowing use of Alembic for migrations
- Alembic is industry standard for Python database migrations
- Provides version control for database schema changes
- Supports rollback and forward migration
- Works seamlessly with SQLModel's table definitions

**Migration Strategy**:
1. Define models using SQLModel with `table=True`
2. Use Alembic to auto-generate initial migration from models
3. Apply migration to Neon PostgreSQL database
4. For schema changes, create new Alembic migrations

**Alternatives Considered**:
- **SQLModel.metadata.create_all()**: Simple but no version control or rollback capability
- **Manual SQL scripts**: Error-prone, no automatic schema diff generation

---

### 5. Frontend State Management

**Decision**: React Context API with Better Auth hooks

**Rationale**:
- Next.js 14+ App Router encourages server components and minimal client-side state
- Better Auth provides React hooks for authentication state
- React Context sufficient for simple todo app state (no complex global state needed)
- Avoids unnecessary complexity of Redux/Zustand for Phase II scope
- Server components handle data fetching, reducing client state needs

**State Management Approach**:
1. **Auth State**: Better Auth React hooks (`useAuth`, `useSession`)
2. **Todo State**: Server components fetch data, client components handle local UI state
3. **Form State**: React useState for form inputs, validation before API calls
4. **Loading/Error State**: Local component state for API call feedback

**Alternatives Considered**:
- **Redux Toolkit**: Overkill for Phase II, adds complexity without clear benefit
- **Zustand**: Lightweight but unnecessary given server component architecture
- **TanStack Query**: Excellent for data fetching/caching but adds dependency not in scope

---

### 6. API Communication Pattern

**Decision**: Native fetch with TypeScript API client module

**Rationale**:
- Native fetch API available in Next.js (Node 18+)
- Type-safe API client module encapsulates all backend calls
- Centralizes error handling and authentication token management
- No additional dependencies needed
- Supports both server and client components

**API Client Structure**:
```typescript
// lib/api/client.ts - Centralized API client
// lib/api/auth.ts - Auth endpoints (signup, signin, signout)
// lib/api/todos.ts - Todo CRUD endpoints
```

**Error Handling Strategy**:
- Catch network errors and return user-friendly messages
- Parse backend error responses and display validation errors
- Handle 401 (unauthorized) by redirecting to signin
- Handle 403 (forbidden) with appropriate error message

**Alternatives Considered**:
- **Axios**: Additional dependency, fetch is sufficient for Phase II needs
- **SWR**: React Hooks library for data fetching, adds complexity beyond Phase II scope
- **tRPC**: Type-safe API framework but requires backend changes and is overkill

---

### 7. Responsive UI Strategy

**Decision**: Tailwind CSS with mobile-first approach

**Rationale**:
- Tailwind is industry standard for utility-first CSS in React/Next.js projects
- Built-in responsive design utilities (sm:, md:, lg:, xl: breakpoints)
- Small bundle size with purging unused styles
- Excellent DX with IntelliSense support
- No custom CSS writing needed for Phase II
- Mobile-first approach ensures usability on 320px+ screens

**Responsive Breakpoints**:
- Mobile: 320px - 640px (default, no prefix)
- Tablet: 640px - 1024px (sm:)
- Desktop: 1024px+ (lg:)

**Alternatives Considered**:
- **CSS Modules**: More verbose, requires writing custom responsive CSS
- **Styled Components**: Runtime CSS-in-JS with performance overhead
- **Material-UI**: Heavy component library, overkill for simple todo app

---

### 8. Development Environment Setup

**Decision**: Separate backend and frontend development servers with environment variables

**Backend Development**:
- FastAPI with `uvicorn --reload` for auto-reload on code changes
- SQLite for local development (same schema as PostgreSQL)
- Environment variables for database URL switching (local SQLite vs Neon PostgreSQL)

**Frontend Development**:
- Next.js dev server with hot module replacement
- Environment variables for backend API URL
- Proxy configuration for API calls to avoid CORS issues in development

**Environment Variables**:
```bash
# Backend (.env)
DATABASE_URL=postgresql://user:pass@localhost/todos  # or Neon URL
BETTER_AUTH_SECRET=your-secret-key
ENVIRONMENT=development

# Frontend (.env.local)
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_BETTER_AUTH_CLIENT_ID=your-client-id
```

**Alternatives Considered**:
- **Docker Compose**: Adds infrastructure complexity not needed for Phase II
- **Monorepo with Turborepo**: Overkill for two simple projects
- **Same port deployment**: Complicates development, requires reverse proxy

---

### 9. Error Handling Patterns

**Backend Error Handling**:
- Use FastAPI's HTTPException for structured error responses
- Create custom exception classes for domain errors (e.g., `TodoNotFoundError`, `UnauthorizedError`)
- Global exception handler middleware to catch unexpected errors and return 500
- Log errors to stdout/stderr for debugging

**Frontend Error Handling**:
- Try-catch blocks around all API calls
- Display toast notifications or inline error messages
- Handle validation errors from backend with field-specific messages
- Graceful degradation for network failures with retry prompts

**Error Response Format** (Backend):
```json
{
  "detail": "Human-readable error message",
  "code": "TODO_NOT_FOUND",
  "field": "title" // optional, for validation errors
}
```

---

### 10. Testing Strategy

**Backend Testing**:
- **Unit Tests**: pytest for business logic (todo validation, user operations)
- **Integration Tests**: pytest with test database for API endpoints
- **Test Database**: SQLite in-memory for fast test execution
- **Test Client**: FastAPI TestClient for HTTP endpoint testing
- **Fixtures**: pytest fixtures for common test data (users, todos)

**Frontend Testing**:
- **Component Tests**: React Testing Library for UI components
- **Integration Tests**: Testing user flows (signup → create todo → toggle complete)
- **E2E Tests**: Optional for Phase II, can be deferred to later phase
- **Mocking**: Mock API calls for frontend tests

**Test Coverage Goal**: 80% minimum as specified in Constitution (Article V, Section 5.4)

---

## Technology Stack Summary

| Layer | Technology | Version | Purpose |
|-------|-----------|---------|---------|
| **Backend** |
| Language | Python | 3.11+ | Backend runtime |
| Framework | FastAPI | 0.100+ | REST API framework |
| ORM | SQLModel | 0.0.14+ | Database ORM |
| ASGI Server | Uvicorn | Latest | Application server |
| Validation | Pydantic | v2 | Request/response validation |
| Migrations | Alembic | Latest | Database schema versioning |
| Testing | pytest | Latest | Test framework |
| **Frontend** |
| Runtime | Node.js | 20+ | JavaScript runtime |
| Framework | Next.js | 14+ | React framework |
| Language | TypeScript | 5.0+ | Type safety |
| Styling | Tailwind CSS | 3+ | Utility-first CSS |
| Testing | React Testing Library | Latest | Component testing |
| **Database** |
| Production | Neon PostgreSQL | Latest | Serverless PostgreSQL |
| Development | SQLite | 3+ | Local development |
| **Authentication** |
| Library | Better Auth | Latest | Auth provider |
| **Infrastructure** |
| Version Control | Git | Latest | Source control |
| Package Manager (Python) | pip/venv | Latest | Python dependencies |
| Package Manager (Node) | npm/yarn | Latest | JavaScript dependencies |

---

## Architecture Patterns

### Backend Architecture (Clean Architecture)

```
backend/
├── src/
│   ├── domain/              # Business entities (User, Todo)
│   │   ├── user.py          # User entity with SQLModel
│   │   └── todo.py          # Todo entity with SQLModel
│   ├── application/         # Business logic & use cases
│   │   ├── auth_service.py  # Authentication logic
│   │   └── todo_service.py  # Todo CRUD logic
│   ├── infrastructure/      # External dependencies
│   │   ├── database.py      # Database connection setup
│   │   ├── better_auth.py   # Better Auth integration
│   │   └── repositories/    # Data access layer
│   │       ├── user_repository.py
│   │       └── todo_repository.py
│   └── presentation/        # API layer
│       ├── main.py          # FastAPI app setup
│       ├── middleware/      # Custom middleware
│       │   └── auth.py      # Auth middleware
│       ├── routers/         # API route handlers
│       │   ├── auth.py      # Auth endpoints
│       │   └── todos.py     # Todo endpoints
│       └── schemas.py       # Request/response models
└── tests/
    ├── unit/                # Unit tests for services
    ├── integration/         # API integration tests
    └── conftest.py          # Pytest fixtures
```

### Frontend Architecture (Next.js App Router)

```
frontend/
├── app/                     # Next.js App Router
│   ├── layout.tsx           # Root layout
│   ├── page.tsx             # Home/landing page
│   ├── auth/
│   │   ├── signup/
│   │   │   └── page.tsx     # Signup page
│   │   └── signin/
│   │       └── page.tsx     # Signin page
│   └── todos/
│       └── page.tsx         # Todo list page (protected)
├── components/              # React components
│   ├── TodoList.tsx         # Todo list display
│   ├── TodoItem.tsx         # Individual todo item
│   ├── TodoForm.tsx         # Create/edit todo form
│   ├── AuthForm.tsx         # Reusable auth form
│   └── EmptyState.tsx       # Empty todos message
├── lib/                     # Utilities and API
│   ├── api/
│   │   ├── client.ts        # Base API client
│   │   ├── auth.ts          # Auth API calls
│   │   └── todos.ts         # Todo API calls
│   ├── better-auth.ts       # Better Auth config
│   └── types.ts             # TypeScript types
└── tests/
    └── components/          # Component tests
```

---

## Security Considerations

### Authentication Security
- Passwords hashed with bcrypt (minimum 8 characters)
- Session tokens stored in HTTP-only cookies
- CSRF protection via Better Auth
- No passwords or tokens logged

### Authorization Security
- Middleware validates user owns requested todo on all operations
- Database queries filtered by user_id to prevent data leakage
- 403 Forbidden returned for unauthorized access attempts

### Input Validation
- Backend validates all inputs before database operations
- Frontend provides early validation for better UX
- SQL injection prevented via SQLModel parameterized queries
- XSS prevention via React automatic escaping

### Data Privacy
- Users can only access their own data
- No user data exposed in error messages
- Audit logging for security-relevant events (failed logins, etc.)

---

## Performance Considerations

### Backend Performance
- Async/await for database operations (non-blocking I/O)
- Connection pooling for Neon PostgreSQL
- Indexes on user_id and id columns for fast queries
- Query optimization (select only needed fields)

### Frontend Performance
- Server components for initial page load (faster rendering)
- Client components only where interactivity needed
- Optimistic UI updates for better perceived performance
- Image optimization with Next.js Image component (if images added later)

### Database Performance
- Primary key indexes (automatic)
- Foreign key index on todos.user_id
- Query limit for todo list (prevent unbounded results)
- Consider pagination if user has >100 todos (future enhancement)

---

## Deployment Considerations (for future phases)

*Note: Deployment is not in scope for Phase II specification, but documenting for awareness:*

### Backend Deployment Options
- Platform: Vercel, Railway, Fly.io, or AWS Lambda
- Database: Neon PostgreSQL (already serverless)
- Environment variables: Set via platform dashboard

### Frontend Deployment
- Platform: Vercel (recommended for Next.js)
- Build: Static + server-side rendering
- Environment variables: Set via Vercel dashboard

### HTTPS
- Production must use HTTPS (handled by deployment platforms)
- Development can use HTTP for simplicity

---

*End of Research Document*
