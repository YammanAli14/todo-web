# Implementation Plan: Phase II Full-Stack Todo Application

**Branch**: `1-phase-ii-fullstack` | **Date**: 2026-01-02 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/1-phase-ii-fullstack/spec.md`

---

## Summary

Phase II transforms the Evolution of Todo project into a full-stack web application with persistent storage, multi-user authentication, and a responsive web interface. The implementation delivers all 5 basic todo operations (create, view, update, delete, toggle) with Better Auth authentication, Python FastAPI backend, Neon PostgreSQL database, and Next.js frontend.

**Primary Requirement**: Build a complete full-stack todo application where authenticated users can manage their personal task lists via a web browser.

**Technical Approach**:
- **Backend**: Python 3.11 with FastAPI for RESTful API, SQLModel for ORM, Better Auth for authentication
- **Database**: Neon Serverless PostgreSQL (production), SQLite (development)
- **Frontend**: Next.js 14 with TypeScript, React, Tailwind CSS for responsive UI
- **Architecture**: Clean architecture with separation of concerns (domain, application, infrastructure, presentation)

---

## Technical Context

**Language/Version**: Python 3.11+ (backend), Node.js 20+ (frontend), TypeScript 5.0+ (frontend)

**Primary Dependencies**:
- **Backend**: FastAPI 0.100+, SQLModel 0.0.14+, Uvicorn (ASGI server), Better Auth, Alembic (migrations)
- **Frontend**: Next.js 14+, React 18+, TypeScript 5.0+, Tailwind CSS 3+, Better Auth client

**Storage**: Neon Serverless PostgreSQL (production), SQLite (local development)

**Testing**:
- **Backend**: pytest with FastAPI TestClient, pytest-asyncio for async tests
- **Frontend**: React Testing Library, Jest for component tests

**Target Platform**: Web application (desktop and mobile browsers, 320px-1920px screen widths)

**Project Type**: Web (separate backend and frontend)

**Performance Goals**:
- Account registration < 2 minutes
- Todo operations < 2 seconds response time
- 100 concurrent authenticated users supported
- 95% operation success rate

**Constraints**:
- No AI or agent frameworks (Phase III+)
- No background job processing
- No real-time features (WebSockets)
- No advanced analytics
- No Docker/Kubernetes (Phase V)
- Must use Better Auth (Constitution requirement)
- Must use Neon PostgreSQL for production
- Must support responsive UI (320px to 1920px)

**Scale/Scope**:
- 6 user stories (3 P1, 2 P2, 1 P3)
- 39 functional requirements
- 2 entities (User, Todo)
- 9 API endpoints (4 auth, 5 todos)
- 4 frontend pages (signup, signin, todos, home)
- Minimum 80% test coverage for business logic

---

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-checked after Phase 1 design.*

### Article I: Spec-Driven Development ✅

- ✅ **Section 1.1**: Specification approved (spec.md created and validated)
- ✅ **Section 1.2**: Following development hierarchy (Constitution → Specification → Plan → Tasks → Implementation)
- ✅ **Section 1.3**: Specification includes scope, requirements, interfaces, acceptance criteria, dependencies
- ✅ **Section 1.4**: Plan references approved specification and breaks work into verifiable tasks
- ✅ **Section 1.5**: Tasks will be atomic and independently verifiable (to be created via `/sp.tasks`)

### Article III: Phase Governance ✅

- ✅ **Section 3.1**: Implements Phase II requirements (Full-Stack Web App with Python REST API, Neon PostgreSQL, Next.js, Better Auth)
- ✅ **Section 3.2**: No forward leakage to Phase III+ (no AI, agents, MCP, advanced infrastructure)
- ✅ **Section 3.3**: Completion criteria defined in spec (40 acceptance scenarios, quality checklist)
- ✅ **Section 3.4**: Architecture evolution follows specification (clean architecture with clear layers)

### Article IV: Technology Constraints ✅

- ✅ **Section 4.1**: Uses mandatory technologies:
  - Python 3.11+ (backend language)
  - Python REST API via FastAPI (backend framework - flexible choice within Constitution)
  - SQLModel (ORM/data layer)
  - Neon Serverless PostgreSQL (database)
  - Next.js with React and TypeScript (frontend framework)
  - Better Auth (authentication)

- ✅ **Section 4.2**: Respects prohibitions:
  - ✅ No alternative frontend frameworks (using Next.js as required)
  - ✅ No AI/agent frameworks before Phase III
  - ✅ No authentication systems other than Better Auth
  - ✅ No databases in Phase I (Phase II correctly uses PostgreSQL)

- ✅ **Section 4.3**: Dependencies explicitly listed in requirements.txt (backend) and package.json (frontend)
- ✅ **Section 4.4**: Meets version requirements (Python 3.11+, Next.js 14+, TypeScript 5.0+, SQLModel 0.0.14+)

### Article V: Quality Principles ✅

- ✅ **Section 5.1**: Clean architecture with separation of concerns (domain, application, infrastructure, presentation layers)
- ✅ **Section 5.2**: Project structure follows convention (backend/, frontend/, specs/, tests/)
- ✅ **Section 5.3**: Backend API is stateless (all state in database)
- ✅ **Section 5.4**: Code quality standards:
  - Type hints for all functions (Python type hints, TypeScript)
  - API documentation (FastAPI auto-generates OpenAPI)
  - Minimum 80% test coverage target
  - Linting (ruff for Python, ESLint for TypeScript)
  - Formatting (black for Python, Prettier for TypeScript)

- ✅ **Section 5.5**: Error handling with specific exceptions, actionable messages, no sensitive data leakage
- ✅ **Section 5.6**: Security requirements met (no secrets in code, input validation, parameterized queries via ORM, authentication via Better Auth, HTTPS in production)

**Gate Status**: ✅ **PASSED** - All constitutional requirements met, no violations

---

## Project Structure

### Documentation (this feature)

```text
specs/1-phase-ii-fullstack/
├── spec.md              # Feature specification (created)
├── plan.md              # This file (implementation plan)
├── research.md          # Phase 0 output (technical decisions - created)
├── data-model.md        # Phase 1 output (database schema - created)
├── quickstart.md        # Phase 1 output (developer guide - created)
├── contracts/           # Phase 1 output (API contracts - created)
│   ├── openapi.yaml     # OpenAPI specification
│   └── typescript-api-client.md  # TypeScript API client
├── checklists/
│   └── requirements.md  # Specification quality checklist (created)
└── tasks.md             # Phase 2 output (NOT created by /sp.plan - awaits /sp.tasks command)
```

### Source Code (repository root)

```text
booseai/
├── backend/                    # Python FastAPI backend
│   ├── src/
│   │   ├── __init__.py
│   │   ├── domain/             # Business entities (no external dependencies)
│   │   │   ├── __init__.py
│   │   │   ├── user.py         # User SQLModel entity
│   │   │   └── todo.py         # Todo SQLModel entity
│   │   ├── application/        # Use cases and business logic
│   │   │   ├── __init__.py
│   │   │   ├── auth_service.py # Authentication logic (signup, signin, validation)
│   │   │   └── todo_service.py # Todo CRUD business logic
│   │   ├── infrastructure/     # External dependencies
│   │   │   ├── __init__.py
│   │   │   ├── database.py     # Database connection and session management
│   │   │   ├── better_auth.py  # Better Auth integration
│   │   │   └── repositories/   # Data access layer
│   │   │       ├── __init__.py
│   │   │       ├── user_repository.py  # User database operations
│   │   │       └── todo_repository.py  # Todo database operations
│   │   └── presentation/       # API layer (HTTP interface)
│   │       ├── __init__.py
│   │       ├── main.py         # FastAPI app initialization
│   │       ├── dependencies.py # Dependency injection (DB session, current user)
│   │       ├── middleware/     # Custom middleware
│   │       │   ├── __init__.py
│   │       │   └── auth.py     # Authentication middleware
│   │       ├── routers/        # API route handlers
│   │       │   ├── __init__.py
│   │       │   ├── auth.py     # Auth endpoints (signup, signin, signout, me)
│   │       │   └── todos.py    # Todo endpoints (CRUD, toggle)
│   │       └── schemas.py      # Pydantic request/response models
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── conftest.py         # Pytest fixtures (test DB, test client, auth helpers)
│   │   ├── unit/               # Unit tests for services
│   │   │   ├── __init__.py
│   │   │   ├── test_auth_service.py    # Auth logic tests
│   │   │   └── test_todo_service.py    # Todo logic tests
│   │   └── integration/        # API integration tests
│   │       ├── __init__.py
│   │       ├── test_auth_api.py        # Auth endpoint tests
│   │       └── test_todo_api.py        # Todo endpoint tests
│   ├── alembic/                # Database migrations
│   │   ├── versions/           # Migration files
│   │   ├── env.py              # Alembic configuration
│   │   └── script.py.mako      # Migration template
│   ├── data/                   # SQLite database (local dev, gitignored)
│   ├── alembic.ini             # Alembic configuration
│   ├── requirements.txt        # Python dependencies
│   ├── .env                    # Environment variables (gitignored)
│   ├── .env.example            # Example environment variables
│   └── README.md               # Backend documentation
│
├── frontend/                   # Next.js frontend
│   ├── app/                    # Next.js App Router
│   │   ├── layout.tsx          # Root layout with auth provider
│   │   ├── page.tsx            # Home/landing page
│   │   ├── auth/
│   │   │   ├── signup/
│   │   │   │   └── page.tsx    # Signup page
│   │   │   └── signin/
│   │   │       └── page.tsx    # Signin page
│   │   └── todos/
│   │       └── page.tsx        # Todo list page (protected route)
│   ├── components/             # React components
│   │   ├── TodoList.tsx        # Todo list display component
│   │   ├── TodoItem.tsx        # Individual todo item with toggle/edit/delete
│   │   ├── TodoForm.tsx        # Create/edit todo form
│   │   ├── AuthForm.tsx        # Reusable auth form (signup/signin)
│   │   ├── EmptyState.tsx      # Empty todos message
│   │   ├── LoadingSpinner.tsx  # Loading indicator
│   │   └── ErrorMessage.tsx    # Error display component
│   ├── lib/                    # Utilities and API
│   │   ├── api/
│   │   │   ├── client.ts       # Base API client with fetch wrapper
│   │   │   ├── auth.ts         # Auth API calls (signup, signin, signout, me)
│   │   │   └── todos.ts        # Todo API calls (CRUD, toggle)
│   │   ├── better-auth.ts      # Better Auth configuration
│   │   ├── types.ts            # TypeScript types (User, Todo, API responses)
│   │   └── utils.ts            # Helper functions
│   ├── tests/
│   │   └── components/         # Component tests
│   │       ├── TodoList.test.tsx
│   │       ├── TodoItem.test.tsx
│   │       └── AuthForm.test.tsx
│   ├── public/                 # Static assets
│   ├── package.json            # Node dependencies
│   ├── tsconfig.json           # TypeScript configuration
│   ├── tailwind.config.ts      # Tailwind CSS configuration
│   ├── next.config.js          # Next.js configuration
│   ├── .env.local              # Frontend environment variables (gitignored)
│   ├── .env.example            # Example environment variables
│   └── README.md               # Frontend documentation
│
├── specs/                      # Feature specifications
│   └── 1-phase-ii-fullstack/   # This feature
│
├── CONSTITUTION.md             # Global project constitution
├── CLAUDE.md                   # Agent development guidelines
├── .gitignore                  # Git ignore patterns
└── README.md                   # Project overview
```

**Structure Decision**: **Web application** structure selected (Option 2 from template). This feature requires separate backend API and frontend UI, making the web application structure the natural choice. Backend and frontend are independent projects with their own dependency management, testing, and build processes.

---

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

*No violations detected. This section is empty because all Constitutional requirements are met.*

---

## Implementation Phases

### Phase 0: Research & Decisions ✅ COMPLETE

**Status**: Completed (research.md created)

**Decisions Made**:
1. Backend framework: FastAPI (best async Python REST framework)
2. ORM: SQLModel (FastAPI-first ORM with Pydantic integration)
3. Better Auth integration: Use Better Auth SDK for both backend and frontend
4. Database migrations: Alembic (industry standard for SQLAlchemy/SQLModel)
5. Frontend state management: React Context + Better Auth hooks (no Redux needed for Phase II)
6. API communication: Native fetch with TypeScript client module
7. Responsive UI: Tailwind CSS with mobile-first approach
8. Development setup: Separate dev servers with environment variable configuration
9. Error handling: FastAPI HTTPException + global exception handler
10. Testing: pytest (backend) + React Testing Library (frontend)

**Artifacts Created**:
- `research.md`: Comprehensive technical decisions with rationale

---

### Phase 1: Design & Contracts ✅ COMPLETE

**Status**: Completed (data-model.md, contracts/, quickstart.md created)

**Design Decisions**:

**Data Model**:
- Two entities: User and Todo
- One-to-many relationship (User → Todos)
- Foreign key with CASCADE delete for data isolation
- Timestamps (created_at, updated_at) on all entities
- Email uniqueness constraint with case-insensitive index
- Password hashing via bcrypt (managed by Better Auth)

**API Contracts**:
- RESTful API with standard HTTP verbs (GET, POST, PUT, PATCH, DELETE)
- JSON request/response format
- Bearer token authentication via Better Auth
- OpenAPI 3.1 specification for all endpoints
- Consistent error response format with detail, code, field

**API Endpoints Defined**:

**Authentication**:
- `POST /auth/signup` - Register new user
- `POST /auth/signin` - Authenticate user
- `POST /auth/signout` - End session
- `GET /auth/me` - Get current user profile

**Todos**:
- `GET /todos` - List all user's todos
- `POST /todos` - Create new todo
- `GET /todos/{id}` - Get single todo
- `PUT /todos/{id}` - Update todo title
- `DELETE /todos/{id}` - Delete todo
- `PATCH /todos/{id}/toggle` - Toggle completion status

**Frontend Design**:
- Next.js App Router for routing
- Server components for initial page loads
- Client components for interactivity
- TypeScript API client with error handling
- Tailwind CSS for responsive styling
- Better Auth React hooks for auth state

**Artifacts Created**:
- `data-model.md`: Complete database schema with ERD, SQLModel definitions, access patterns
- `contracts/openapi.yaml`: Full OpenAPI 3.1 specification for REST API
- `contracts/typescript-api-client.md`: TypeScript types and API client interfaces
- `quickstart.md`: Developer setup guide with all commands and configuration

---

### Phase 2: Task Breakdown

**Status**: PENDING (awaits `/sp.tasks` command)

**Next Steps**:
1. Run `/sp.tasks` to generate `tasks.md` with detailed implementation tasks
2. Tasks will be organized by:
   - Backend infrastructure setup
   - Database models and migrations
   - Authentication implementation
   - Todo CRUD implementation
   - Frontend setup
   - UI components
   - Integration and testing

**Expected Task Categories**:
- Infrastructure (project setup, dependencies, environment)
- Database (entities, migrations, repositories)
- Backend API (routes, services, middleware)
- Authentication (Better Auth integration, session management)
- Frontend (Next.js setup, pages, components)
- API Client (TypeScript client, error handling)
- Testing (unit tests, integration tests, E2E tests)
- Documentation (README files, API docs)

---

## Backend Implementation Strategy

### Layer 1: Domain (Business Entities)

**Purpose**: Define core business entities with no external dependencies

**Files**:
- `src/domain/user.py`: User entity with SQLModel
- `src/domain/todo.py`: Todo entity with SQLModel

**Key Design Decisions**:
- Use SQLModel `table=True` for database mapping
- Include validation in Field constraints (max_length, nullable)
- Default values for timestamps (datetime.utcnow)
- Foreign key relationship for todo.user_id

**Testing Strategy**:
- Unit tests for entity creation
- Validation tests for field constraints
- Relationship tests for foreign key cascade

---

### Layer 2: Application (Business Logic)

**Purpose**: Implement use cases and business rules

**Files**:
- `src/application/auth_service.py`: User registration, login, session validation
- `src/application/todo_service.py`: Todo CRUD operations with authorization checks

**Key Design Decisions**:
- Services receive repositories via dependency injection
- All todo operations include user_id filtering for data isolation
- Password hashing delegated to Better Auth
- Validation errors raise custom exceptions

**Authorization Pattern**:
```python
def get_user_todo(todo_id: int, user_id: int) -> Todo:
    todo = todo_repo.get_by_id(todo_id)
    if not todo:
        raise TodoNotFoundError()
    if todo.user_id != user_id:
        raise UnauthorizedError("You don't own this todo")
    return todo
```

**Testing Strategy**:
- Unit tests with mocked repositories
- Test authorization checks (user can only access their own todos)
- Test validation logic (empty titles, whitespace, length limits)
- Test error handling

---

### Layer 3: Infrastructure (External Dependencies)

**Purpose**: Integrate external systems (database, Better Auth)

**Files**:
- `src/infrastructure/database.py`: SQLAlchemy engine, session factory
- `src/infrastructure/better_auth.py`: Better Auth client initialization
- `src/infrastructure/repositories/user_repository.py`: User database operations
- `src/infrastructure/repositories/todo_repository.py`: Todo database operations

**Key Design Decisions**:
- Repository pattern for data access abstraction
- Connection pooling for database efficiency
- Async database operations for performance
- Repositories return domain entities, not database rows

**Database Session Management**:
```python
def get_db_session():
    with Session(engine) as session:
        yield session
```

**Testing Strategy**:
- Integration tests with test database (SQLite in-memory)
- Test repository methods (CRUD operations)
- Test query filtering by user_id
- Test foreign key constraints

---

### Layer 4: Presentation (API Layer)

**Purpose**: HTTP interface for frontend communication

**Files**:
- `src/presentation/main.py`: FastAPI app setup, CORS, middleware
- `src/presentation/dependencies.py`: Dependency injection (DB session, current user)
- `src/presentation/middleware/auth.py`: Authentication middleware
- `src/presentation/routers/auth.py`: Auth endpoints
- `src/presentation/routers/todos.py`: Todo endpoints
- `src/presentation/schemas.py`: Pydantic request/response models

**Key Design Decisions**:
- Use FastAPI dependency injection for auth and database
- Separate Pydantic schemas from SQLModel entities
- Authentication middleware extracts user from Better Auth token
- Global exception handler for consistent error responses

**Dependency Injection Pattern**:
```python
async def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_db_session)
) -> User:
    # Validate token with Better Auth
    # Return authenticated user
    pass
```

**Testing Strategy**:
- Integration tests with FastAPI TestClient
- Test all endpoints with various inputs
- Test authentication (valid token, invalid token, missing token)
- Test authorization (user accessing their own vs others' todos)
- Test error responses (400, 401, 403, 404, 500)

---

## Frontend Implementation Strategy

### App Router (Routing & Pages)

**Purpose**: Define application routes and page components

**Files**:
- `app/layout.tsx`: Root layout with Better Auth provider
- `app/page.tsx`: Landing page (redirect to /todos if authenticated)
- `app/auth/signup/page.tsx`: User registration page
- `app/auth/signin/page.tsx`: User login page
- `app/todos/page.tsx`: Todo list page (protected route)

**Key Design Decisions**:
- Use Next.js App Router for file-based routing
- Server components for initial data fetching where possible
- Client components for forms and interactive elements
- Protected routes redirect to signin if unauthenticated

**Protected Route Pattern**:
```typescript
export default function TodosPage() {
  const { user, loading } = useAuth();

  if (loading) return <LoadingSpinner />;
  if (!user) redirect('/auth/signin');

  return <TodoList />;
}
```

**Testing Strategy**:
- Component tests for each page
- Test authentication redirects
- Test loading states
- Test error states

---

### Components (UI Elements)

**Purpose**: Reusable React components for UI

**Files**:
- `components/TodoList.tsx`: Display list of todos
- `components/TodoItem.tsx`: Single todo with actions (toggle, edit, delete)
- `components/TodoForm.tsx`: Create/edit todo form
- `components/AuthForm.tsx`: Reusable auth form (signup/signin)
- `components/EmptyState.tsx`: Message when no todos exist
- `components/LoadingSpinner.tsx`: Loading indicator
- `components/ErrorMessage.tsx`: Error display

**Key Design Decisions**:
- Components receive data via props (no direct API calls in components)
- State management in parent components or pages
- Tailwind CSS for styling (no CSS modules)
- Responsive design with mobile-first approach
- Optimistic UI updates for better UX

**Component Composition**:
```
TodosPage
  └─> TodoList
       ├─> TodoItem (for each todo)
       │    ├─> Toggle button
       │    ├─> Edit button
       │    └─> Delete button
       ├─> TodoForm (create new)
       └─> EmptyState (if no todos)
```

**Testing Strategy**:
- Unit tests for each component
- Test user interactions (clicks, form submissions)
- Test conditional rendering (empty states, errors)
- Test responsive behavior

---

### API Client (Backend Communication)

**Purpose**: Type-safe API communication layer

**Files**:
- `lib/api/client.ts`: Base API client with fetch wrapper
- `lib/api/auth.ts`: Auth API methods (signup, signin, signout, getCurrentUser)
- `lib/api/todos.ts`: Todo API methods (getTodos, createTodo, updateTodo, deleteTodo, toggleTodo)
- `lib/types.ts`: TypeScript interfaces (User, Todo, ApiError)

**Key Design Decisions**:
- Single source of truth for API types
- Centralized error handling in base client
- Automatic token management (read from localStorage, send in headers)
- Redirect to signin on 401 Unauthorized

**API Client Pattern**:
```typescript
const api = createApi({
  baseUrl: process.env.NEXT_PUBLIC_API_URL,
  getToken: () => localStorage.getItem('auth_token'),
  onUnauthorized: () => router.push('/auth/signin'),
});

// Usage:
const todos = await api.todos.getTodos();
const newTodo = await api.todos.createTodo({ title: "Buy milk" });
```

**Testing Strategy**:
- Unit tests with mocked fetch
- Test error handling (network errors, API errors)
- Test token injection
- Test unauthorized redirect

---

## Integration Flow

### Authentication Flow

```
1. User visits signup page
   ↓
2. User enters email + password
   ↓
3. Frontend validates input
   ↓
4. POST /auth/signup → Backend
   ↓
5. Backend validates + creates user via Better Auth
   ↓
6. Backend returns user + token (201 Created)
   ↓
7. Frontend stores token in localStorage
   ↓
8. Frontend redirects to /todos
```

### Todo CRUD Flow

```
1. User authenticated and on /todos page
   ↓
2. Frontend: GET /todos with auth token
   ↓
3. Backend: Extract user from token, query todos filtered by user_id
   ↓
4. Backend returns JSON array of todos (200 OK)
   ↓
5. Frontend displays todos in TodoList component
   ↓
6. User clicks "Add Todo"
   ↓
7. User enters title in TodoForm
   ↓
8. Frontend: POST /todos { title: "..." } with auth token
   ↓
9. Backend: Validate, create todo with user_id from token
   ↓
10. Backend returns created todo (201 Created)
   ↓
11. Frontend adds todo to list (optimistic UI)
```

### Authorization Check Flow

```
User A tries to delete User B's todo (malicious attempt)
   ↓
Frontend: DELETE /todos/123 with User A's token
   ↓
Backend middleware: Extract User A from token
   ↓
Backend service: Query todo 123
   ↓
Backend service: Check todo.user_id == User A's ID
   ↓
Check fails → Raise UnauthorizedError
   ↓
Backend returns 403 Forbidden
   ↓
Frontend displays error message "You don't own this todo"
```

---

## Database Migration Strategy

### Initial Schema Creation

1. Define SQLModel entities (User, Todo)
2. Initialize Alembic: `alembic init alembic`
3. Configure `alembic/env.py` to import SQLModel models
4. Generate initial migration: `alembic revision --autogenerate -m "Initial schema"`
5. Review generated migration file
6. Apply to local SQLite: `alembic upgrade head`
7. Apply to Neon PostgreSQL (production): `alembic upgrade head`

### Future Schema Changes

1. Update SQLModel entity definition
2. Generate migration: `alembic revision --autogenerate -m "Description"`
3. Review migration (Alembic auto-detects changes)
4. Test on local database
5. Apply to production database

### Migration Safety

- Always review auto-generated migrations before applying
- Test migrations on development database first
- Migrations are version-controlled in git
- Rollback capability: `alembic downgrade -1`

---

## Testing Strategy

### Backend Testing

**Unit Tests** (`tests/unit/`):
- Test services with mocked repositories
- Test business logic (validation, authorization)
- Test edge cases (empty strings, null values, boundary conditions)
- Target: 80% code coverage on services

**Integration Tests** (`tests/integration/`):
- Test API endpoints with TestClient
- Test full request/response cycle
- Test database operations with test database
- Test authentication and authorization
- Test error responses

**Test Fixtures** (`tests/conftest.py`):
- Test database session (SQLite in-memory)
- Test FastAPI client
- Authenticated user fixtures
- Sample data fixtures (users, todos)

**Example Test**:
```python
def test_user_cannot_delete_others_todo(client, auth_headers_user1, user2_todo):
    response = client.delete(f"/todos/{user2_todo.id}", headers=auth_headers_user1)
    assert response.status_code == 403
    assert "don't own this todo" in response.json()["detail"]
```

---

### Frontend Testing

**Component Tests** (`tests/components/`):
- Test component rendering
- Test user interactions (clicks, form inputs)
- Test conditional rendering (loading, errors, empty states)
- Mock API calls

**Integration Tests**:
- Test user flows (signup → create todo → toggle complete)
- Test navigation between pages
- Test protected route redirects

**Example Test**:
```typescript
test('TodoItem displays title and completion status', () => {
  const todo = { id: 1, title: 'Test', is_complete: false, ... };
  render(<TodoItem todo={todo} onToggle={jest.fn()} onDelete={jest.fn()} />);

  expect(screen.getByText('Test')).toBeInTheDocument();
  expect(screen.getByRole('checkbox')).not.toBeChecked();
});
```

---

## Error Handling Strategy

### Backend Error Handling

**Custom Exceptions**:
```python
class TodoNotFoundError(Exception): pass
class UnauthorizedError(Exception): pass
class ValidationError(Exception): pass
```

**Global Exception Handler**:
```python
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    if isinstance(exc, TodoNotFoundError):
        return JSONResponse(status_code=404, content={"detail": "Todo not found"})
    elif isinstance(exc, UnauthorizedError):
        return JSONResponse(status_code=403, content={"detail": str(exc)})
    else:
        return JSONResponse(status_code=500, content={"detail": "Internal server error"})
```

### Frontend Error Handling

**API Error Handling**:
```typescript
try {
  const todos = await api.todos.getTodos();
  setTodos(todos);
} catch (error) {
  if (error instanceof ApiException) {
    if (error.status === 401) {
      // Handled by onUnauthorized callback
    } else {
      setError(error.error.detail);
    }
  } else {
    setError('Network error: Please try again');
  }
}
```

**User-Friendly Messages**:
- Validation errors: Show field-specific messages
- Network errors: "Connection problem, please try again"
- Authorization errors: "You don't have permission"
- Server errors: "Something went wrong, please try again later"

---

## Security Measures

### Authentication Security

1. **Password Hashing**: bcrypt via Better Auth (never store plain text)
2. **Session Tokens**: JWT or session cookies managed by Better Auth
3. **Token Storage**: localStorage (frontend) with httpOnly cookies where possible
4. **Token Validation**: Every protected endpoint validates token
5. **Session Expiry**: Better Auth handles token expiration

### Authorization Security

1. **User Isolation**: All todo queries filtered by user_id
2. **Ownership Checks**: Backend verifies user owns resource before operations
3. **Fail Closed**: Default deny, explicit checks for access
4. **No Client Trust**: Backend always validates, never trusts frontend

### Input Validation

1. **Backend Validation**: Pydantic models validate all inputs
2. **Frontend Validation**: Early validation for better UX, not security
3. **SQL Injection**: Prevented via SQLModel parameterized queries
4. **XSS**: React automatically escapes strings

### Data Privacy

1. **Password Hash Never Exposed**: Response models exclude password_hash
2. **User Data Isolation**: Users see only their own data
3. **Error Messages**: No sensitive data in error responses
4. **Logging**: Sanitize logs (no passwords, tokens, or PII)

---

## Performance Optimizations

### Backend Performance

1. **Async/Await**: FastAPI supports async for non-blocking I/O
2. **Connection Pooling**: PostgreSQL connection pool for efficient database access
3. **Database Indexes**: Indexes on user_id, email for fast queries
4. **Query Optimization**: Select only needed fields, avoid N+1 queries

### Frontend Performance

1. **Server Components**: Use for non-interactive content (faster initial load)
2. **Client Components**: Only for interactive elements (smaller JS bundle)
3. **Optimistic UI**: Update UI immediately, rollback on error
4. **Code Splitting**: Next.js automatic code splitting per route
5. **Image Optimization**: Next.js Image component (if images added later)

### Database Performance

1. **Primary Key Indexes**: Automatic on id fields
2. **Foreign Key Indexes**: Index on todos.user_id for fast user filtering
3. **Query Limits**: Prevent unbounded result sets (consider pagination future)

---

## Deployment Considerations

*Note: Deployment is not in scope for Phase II implementation, but documented for future reference.*

### Backend Deployment

**Platform Options**: Vercel, Railway, Fly.io, AWS Lambda, Google Cloud Run

**Requirements**:
- Python 3.11+ runtime
- Environment variables (DATABASE_URL, BETTER_AUTH_SECRET)
- Database connection to Neon PostgreSQL
- HTTPS for production

**Steps**:
1. Set DATABASE_URL to Neon connection string
2. Run migrations: `alembic upgrade head`
3. Deploy application code
4. Configure environment variables via platform dashboard

### Frontend Deployment

**Platform**: Vercel (recommended for Next.js)

**Requirements**:
- Node.js 20+ runtime
- Environment variables (NEXT_PUBLIC_API_URL)
- Build process: `npm run build`

**Steps**:
1. Connect git repository to Vercel
2. Configure environment variables
3. Deploy (automatic on git push)

### Database

**Neon PostgreSQL**:
- Already serverless (no deployment needed)
- Connection string provided by Neon
- Automatic backups and scaling

---

## Risk Mitigation

### Technical Risks

| Risk | Impact | Mitigation |
|------|--------|-----------|
| Better Auth integration complexity | High | Follow official documentation, allocate time for learning curve |
| Database connection issues with Neon | Medium | Use SQLite for development, test Neon connection early |
| CORS issues between frontend/backend | Low | Configure CORS in FastAPI main.py with frontend URL |
| Authentication token expiry handling | Medium | Implement automatic refresh or clear error messages |
| User data isolation bugs | High | Comprehensive testing of authorization checks, code review |

### Quality Risks

| Risk | Impact | Mitigation |
|------|--------|-----------|
| Insufficient test coverage | Medium | Write tests alongside implementation, aim for 80% coverage |
| UI not responsive on mobile | Medium | Test on multiple screen sizes (320px, 768px, 1920px) |
| API errors not user-friendly | Low | User-friendly error messages, comprehensive error handling |

---

## Definition of Done

Phase II implementation is complete when:

1. ✅ **All Functional Requirements Met** (39 requirements from spec.md)
2. ✅ **All User Stories Delivered** (6 stories with acceptance scenarios)
3. ✅ **Backend API Functional**:
   - All 9 endpoints working (4 auth, 5 todos)
   - OpenAPI docs accessible at /docs
   - Authentication via Better Auth working
   - User data isolation verified
4. ✅ **Frontend UI Functional**:
   - All 4 pages working (home, signup, signin, todos)
   - Responsive design (320px to 1920px)
   - Authentication flow working
   - All todo operations working
5. ✅ **Database Persistence**:
   - Migrations applied to Neon PostgreSQL
   - Data persists across application restarts
6. ✅ **Testing Complete**:
   - Minimum 80% backend test coverage
   - All integration tests passing
   - Frontend component tests passing
7. ✅ **Code Quality**:
   - Backend linting (ruff) passes
   - Backend formatting (black) passes
   - Frontend linting (ESLint) passes
   - Type hints on all backend functions
   - No TypeScript errors in frontend
8. ✅ **Documentation**:
   - Backend README with setup instructions
   - Frontend README with setup instructions
   - API documentation (auto-generated by FastAPI)
9. ✅ **Success Criteria Met** (10 criteria from spec.md)
10. ✅ **Human Review Approval**

---

## Next Steps

1. ✅ Complete Phase 0 (Research) - DONE
2. ✅ Complete Phase 1 (Design & Contracts) - DONE
3. 📋 **Run `/sp.tasks`** to generate detailed task breakdown
4. 🚀 Begin implementation following task sequence
5. ✅ Verify each task completion against acceptance criteria
6. 🧪 Run tests continuously during implementation
7. 📝 Update documentation as needed
8. 🎯 Human review and approval

---

## Related Documents

- [spec.md](./spec.md) - Feature specification (requirements, user stories)
- [research.md](./research.md) - Technical decisions and rationale
- [data-model.md](./data-model.md) - Database schema and entities
- [quickstart.md](./quickstart.md) - Developer setup guide
- [contracts/openapi.yaml](./contracts/openapi.yaml) - REST API specification
- [contracts/typescript-api-client.md](./contracts/typescript-api-client.md) - Frontend API types
- [../../CONSTITUTION.md](../../CONSTITUTION.md) - Project constitution
- [../../CLAUDE.md](../../CLAUDE.md) - Agent development guidelines

---

*End of Implementation Plan*
