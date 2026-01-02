# Implementation Tasks: Phase II Full-Stack Todo Application

**Feature**: Phase II Full-Stack Web App
**Branch**: `1-phase-ii-fullstack`
**Created**: 2026-01-02
**Total Tasks**: 82
**Estimated Complexity**: High (full-stack with authentication)

---

## Task Summary

| Phase | Focus | Task Count | User Story | Can Start After |
|-------|-------|------------|------------|-----------------|
| Phase 1 | Setup & Infrastructure | 12 tasks | - | Immediate |
| Phase 2 | Foundational (Blocking) | 8 tasks | - | Phase 1 complete |
| Phase 3 | User Story 1 (P1) | 15 tasks | Authentication & Access | Phase 2 complete |
| Phase 4 | User Story 2 (P1) | 12 tasks | View Todo List | Phase 3 complete |
| Phase 5 | User Story 3 (P2) | 10 tasks | Create Todo | Phase 4 complete |
| Phase 6 | User Story 6 (P2) | 9 tasks | Toggle Completion | Phase 5 complete |
| Phase 7 | User Story 4 (P3) | 8 tasks | Update Todo Title | Phase 6 complete |
| Phase 8 | User Story 5 (P3) | 6 tasks | Delete Todo | Phase 7 complete |
| Phase 9 | Polish & Integration | 2 tasks | Cross-cutting | Phase 8 complete |

**Parallelization Opportunities**: Tasks marked with `[P]` can be executed in parallel within their phase when dependencies are met.

---

## User Story Mapping

### Priority 1 (P1) - Foundation
- **US1**: User Registration and Authentication (Phase 3)
- **US2**: View Personal Todo List (Phase 4)

### Priority 2 (P2) - Core Operations
- **US3**: Create New Todo (Phase 5)
- **US6**: Toggle Todo Completion Status (Phase 6)

### Priority 3 (P3) - Enhanced Operations
- **US4**: Update Todo Title (Phase 7)
- **US5**: Delete Todo (Phase 8)

---

## Implementation Strategy

**MVP Scope** (Minimum Viable Product):
- Complete Phase 1-4 (Setup + US1 + US2)
- Delivers: User can register, sign in, and view their empty todo list
- Independent Test: User authentication and data isolation verified

**Incremental Delivery**:
1. MVP (Phases 1-4): Authentication + View
2. V1 (Phases 5-6): + Create + Toggle
3. V2 (Phases 7-8): + Update + Delete
4. Polish (Phase 9): Error handling refinements

---

## Phase 1: Setup & Infrastructure

**Goal**: Initialize both backend and frontend projects with required dependencies and configuration.

**Independent Test**: Both projects can be started locally (backend at :8000, frontend at :3000) without errors.

### Backend Setup

- [ ] T001 Create backend directory structure per plan.md (backend/src/{domain,application,infrastructure,presentation})
- [ ] T002 [P] Create backend/requirements.txt with all dependencies (FastAPI, SQLModel, Uvicorn, Better Auth, Alembic, pytest, ruff, black)
- [ ] T003 [P] Create backend/.env.example with environment variable templates (DATABASE_URL, BETTER_AUTH_SECRET, CORS_ORIGINS, API_HOST, API_PORT)
- [ ] T004 [P] Create backend/.gitignore to exclude .env, data/, __pycache__, venv/
- [ ] T005 [P] Initialize Python virtual environment and install dependencies (python -m venv venv && pip install -r requirements.txt)
- [ ] T006 [P] Create backend/README.md with setup instructions from quickstart.md

### Frontend Setup

- [ ] T007 Create frontend directory and initialize Next.js project (npx create-next-app@latest --typescript --tailwind --app)
- [ ] T008 [P] Add Better Auth and testing dependencies to frontend/package.json
- [ ] T009 [P] Create frontend/.env.local.example with environment variable templates (NEXT_PUBLIC_API_URL, NEXT_PUBLIC_BETTER_AUTH_CLIENT_ID)
- [ ] T010 [P] Configure frontend/tailwind.config.ts with custom breakpoints and theme
- [ ] T011 [P] Create frontend/lib/types.ts with TypeScript interfaces (User, Todo, ApiError, AuthResponse)
- [ ] T012 [P] Create frontend/README.md with setup instructions from quickstart.md

**Phase 1 Complete**: Both projects initialized, dependencies installed, ready for implementation.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Goal**: Set up database connection, migrations, and core infrastructure needed by all user stories.

**Independent Test**: Backend can connect to database, migrations can be applied, FastAPI server starts successfully.

### Database Infrastructure

- [ ] T013 Create backend/src/infrastructure/database.py with SQLAlchemy engine and session factory (support both SQLite dev and Neon PostgreSQL prod)
- [ ] T014 Initialize Alembic for database migrations (alembic init alembic)
- [ ] T015 Configure backend/alembic/env.py to import SQLModel metadata and support migrations
- [ ] T016 Create backend/data/ directory for SQLite database (development only)

### FastAPI Application Setup

- [ ] T017 Create backend/src/presentation/main.py with FastAPI app initialization, CORS middleware, and health check endpoint
- [ ] T018 [P] Create backend/src/presentation/dependencies.py with get_db_session dependency function
- [ ] T019 [P] Create backend/src/presentation/schemas.py with base Pydantic response models (ErrorResponse, HealthResponse)
- [ ] T020 [P] Create backend/tests/conftest.py with pytest fixtures (test database session, test FastAPI client)

**Phase 2 Complete**: Backend infrastructure ready, database can be created, FastAPI app can start.

---

## Phase 3: User Story 1 - User Registration and Authentication (P1)

**User Story**: A new user visits the web application, creates an account using email and password through Better Auth, and gains access to their personal todo workspace.

**Why P1**: Without authentication, users cannot have personalized, persistent todo lists. This is the foundation for all other features.

**Independent Test**: Register a new user → Sign in → Verify authentication token received → Access protected route → Sign out.

**Acceptance Criteria**:
- User can register with email and password
- User can sign in with correct credentials
- Session persists across page refreshes
- Invalid credentials show error message
- Duplicate email registration is rejected

### Backend: User Entity & Auth Service

- [ ] T021 [US1] Create backend/src/domain/user.py with User SQLModel entity (id, email, password_hash, created_at, updated_at)
- [ ] T022 [US1] Create Alembic migration for users table (alembic revision --autogenerate -m "Add users table")
- [ ] T023 [US1] Apply migration to create users table (alembic upgrade head)
- [ ] T024 [P] [US1] Create backend/src/infrastructure/better_auth.py with Better Auth client initialization and password hashing functions
- [ ] T025 [P] [US1] Create backend/src/infrastructure/repositories/user_repository.py with CRUD operations (create, get_by_email, get_by_id)
- [ ] T026 [US1] Create backend/src/application/auth_service.py with signup logic (validate email, hash password, create user)
- [ ] T027 [US1] Create backend/src/application/auth_service.py signin logic (validate credentials, generate token)
- [ ] T028 [P] [US1] Create backend/src/presentation/schemas.py auth schemas (SignupRequest, SigninRequest, UserResponse, AuthResponse)

### Backend: Auth API Endpoints

- [ ] T029 [US1] Create backend/src/presentation/routers/auth.py with POST /auth/signup endpoint (calls auth_service.signup)
- [ ] T030 [US1] Create backend/src/presentation/routers/auth.py with POST /auth/signin endpoint (calls auth_service.signin)
- [ ] T031 [P] [US1] Create backend/src/presentation/routers/auth.py with POST /auth/signout endpoint (invalidate session)
- [ ] T032 [P] [US1] Create backend/src/presentation/routers/auth.py with GET /auth/me endpoint (return current user)
- [ ] T033 [US1] Create backend/src/presentation/middleware/auth.py with authentication middleware (extract user from token)
- [ ] T034 [US1] Update backend/src/presentation/dependencies.py with get_current_user dependency (uses auth middleware)
- [ ] T035 [US1] Register auth router in backend/src/presentation/main.py

**Backend Auth Complete**: Auth endpoints functional, users can register and sign in via API.

### Frontend: Auth UI & State

- [ ] T036 [US1] Create frontend/lib/better-auth.ts with Better Auth client configuration
- [ ] T037 [P] [US1] Create frontend/lib/api/client.ts with base API client (fetch wrapper, error handling, token management)
- [ ] T038 [P] [US1] Create frontend/lib/api/auth.ts with auth API methods (signup, signin, signout, getCurrentUser)
- [ ] T039 [US1] Create frontend/app/auth/signup/page.tsx with signup form (email, password inputs, validation, API call)
- [ ] T040 [US1] Create frontend/app/auth/signin/page.tsx with signin form (email, password inputs, API call, redirect on success)
- [ ] T041 [P] [US1] Create frontend/components/AuthForm.tsx reusable auth form component (handles both signup and signin)
- [ ] T042 [P] [US1] Create frontend/components/ErrorMessage.tsx to display API errors
- [ ] T043 [US1] Update frontend/app/layout.tsx to include Better Auth provider and auth state management
- [ ] T044 [US1] Create frontend/app/page.tsx landing page with links to signup/signin (redirect to /todos if authenticated)
- [ ] T045 [US1] Implement protected route logic in frontend/app/todos/page.tsx (redirect to signin if not authenticated)

**Phase 3 Complete**: Users can register, sign in, and authentication state is managed. Protected routes redirect unauthenticated users.

---

## Phase 4: User Story 2 - View Personal Todo List (P1)

**User Story**: An authenticated user views their complete list of todos in the web interface, seeing title and completion status for each item.

**Why P1**: Viewing todos is the most fundamental read operation. Proves full stack works end-to-end with data isolation.

**Independent Test**: Sign in as User A with todos → Verify only their todos displayed → Sign in as User B → Verify User B doesn't see User A's todos → Sign in as new user → Verify empty state shown.

**Acceptance Criteria**:
- Authenticated user with no todos sees empty state message
- Authenticated user with todos sees all their todos with title and completion status
- User A cannot see User B's todos (data isolation)
- Unauthenticated user is redirected to signin page

### Backend: Todo Entity & Service

- [ ] T046 [US2] Create backend/src/domain/todo.py with Todo SQLModel entity (id, user_id FK, title, is_complete, created_at, updated_at)
- [ ] T047 [US2] Create Alembic migration for todos table with foreign key to users (alembic revision --autogenerate -m "Add todos table")
- [ ] T048 [US2] Apply migration to create todos table (alembic upgrade head)
- [ ] T049 [P] [US2] Create backend/src/infrastructure/repositories/todo_repository.py with get_all_by_user_id method (filters by user_id)
- [ ] T050 [US2] Create backend/src/application/todo_service.py with get_user_todos method (calls repository, enforces data isolation)
- [ ] T051 [P] [US2] Create backend/src/presentation/schemas.py todo schemas (TodoResponse)

### Backend: Todo API Endpoint (Read)

- [ ] T052 [US2] Create backend/src/presentation/routers/todos.py with GET /todos endpoint (protected, returns user's todos filtered by user_id)
- [ ] T053 [US2] Register todos router in backend/src/presentation/main.py

**Backend View Complete**: GET /todos endpoint returns user-specific todos with proper authorization.

### Frontend: Todo List UI

- [ ] T054 [US2] Create frontend/lib/api/todos.ts with getTodos API method (GET /todos with auth token)
- [ ] T055 [US2] Create frontend/components/TodoList.tsx to display list of todos (map over todos array)
- [ ] T056 [P] [US2] Create frontend/components/TodoItem.tsx to display single todo (title, completion checkbox, placeholder action buttons)
- [ ] T057 [P] [US2] Create frontend/components/EmptyState.tsx with message for users with no todos
- [ ] T058 [P] [US2] Create frontend/components/LoadingSpinner.tsx for loading state during API calls
- [ ] T059 [US2] Update frontend/app/todos/page.tsx to fetch and display todos (call getTodos, show TodoList or EmptyState)

**Phase 4 Complete**: Authenticated users can view their todo list. Data isolation verified (users only see their own todos).

---

## Phase 5: User Story 3 - Create New Todo (P2)

**User Story**: An authenticated user creates a new todo by entering a title in the web interface, and the todo is immediately added to their list.

**Why P2**: Creating todos is the primary write operation. Without this, users cannot add tasks.

**Independent Test**: Sign in → Create todo with title "Buy groceries" → Verify it appears in list → Refresh page → Verify it persists.

**Acceptance Criteria**:
- User can create todo with valid title (1-200 characters)
- Empty title is rejected with validation error
- Whitespace-only title is rejected
- Created todo appears immediately in list
- Created todo persists after page refresh

### Backend: Create Todo

- [ ] T060 [US3] Add create method to backend/src/infrastructure/repositories/todo_repository.py (create todo with user_id)
- [ ] T061 [US3] Add create_todo method to backend/src/application/todo_service.py (validate title, associate with user, call repository)
- [ ] T062 [P] [US3] Add TodoCreateRequest schema to backend/src/presentation/schemas.py (title field with validation)
- [ ] T063 [US3] Add POST /todos endpoint to backend/src/presentation/routers/todos.py (protected, calls todo_service.create_todo)

**Backend Create Complete**: POST /todos endpoint creates todo associated with authenticated user.

### Frontend: Create Todo UI

- [ ] T064 [US3] Create frontend/components/TodoForm.tsx with form to create new todo (title input, submit button, validation)
- [ ] T065 [US3] Add createTodo method to frontend/lib/api/todos.ts (POST /todos with title)
- [ ] T066 [US3] Update frontend/app/todos/page.tsx to include TodoForm and refresh list after creation (optimistic UI update)
- [ ] T067 [P] [US3] Handle validation errors in TodoForm (empty title, title too long)
- [ ] T068 [P] [US3] Implement loading state in TodoForm during API call
- [ ] T069 [US3] Clear form input after successful todo creation

**Phase 5 Complete**: Users can create new todos via web UI. Todos persist and appear in list immediately.

---

## Phase 6: User Story 6 - Toggle Todo Completion Status (P2)

**User Story**: An authenticated user marks a todo as complete or incomplete by toggling its status in the web interface, and the change is saved to the database.

**Why P2**: Marking tasks complete is a core todo app function. Provides sense of accomplishment and tracks progress.

**Independent Test**: Create todo → Toggle to complete → Verify checkbox checked → Refresh page → Verify still complete → Toggle back to incomplete → Verify state updated.

**Acceptance Criteria**:
- Incomplete todo can be toggled to complete
- Complete todo can be toggled to incomplete
- Completion status persists after page refresh
- User A cannot toggle User B's todo (authorization check)

### Backend: Toggle Todo

- [ ] T070 [US6] Add get_by_id_and_user method to backend/src/infrastructure/repositories/todo_repository.py (get todo with ownership check)
- [ ] T071 [US6] Add update method to backend/src/infrastructure/repositories/todo_repository.py (update todo fields and updated_at timestamp)
- [ ] T072 [US6] Add toggle_todo method to backend/src/application/todo_service.py (get todo, verify ownership, flip is_complete, update)
- [ ] T073 [US6] Add PATCH /todos/{id}/toggle endpoint to backend/src/presentation/routers/todos.py (protected, calls todo_service.toggle_todo)

**Backend Toggle Complete**: PATCH /todos/{id}/toggle endpoint toggles completion status with authorization.

### Frontend: Toggle Todo UI

- [ ] T074 [US6] Add toggleTodo method to frontend/lib/api/todos.ts (PATCH /todos/{id}/toggle)
- [ ] T075 [US6] Update frontend/components/TodoItem.tsx to make checkbox functional (call toggleTodo on click, optimistic UI update)
- [ ] T076 [P] [US6] Handle toggle errors in TodoItem (show error message, revert UI on failure)
- [ ] T077 [P] [US6] Add visual distinction for completed todos (strikethrough text, different color)
- [ ] T078 [US6] Implement loading state for individual todo during toggle operation

**Phase 6 Complete**: Users can toggle todo completion status. Status persists across page refreshes.

---

## Phase 7: User Story 4 - Update Todo Title (P3)

**User Story**: An authenticated user edits the title of an existing todo in the web interface, and the change is saved to the database.

**Why P3**: Users need to correct typos or update task descriptions. Enhances usability.

**Independent Test**: Create todo "Buy milk" → Edit to "Buy almond milk" → Verify title updated → Refresh page → Verify change persisted.

**Acceptance Criteria**:
- User can edit existing todo title
- Empty title is rejected with validation error
- Title change persists after page refresh
- User A cannot edit User B's todo (authorization check)

### Backend: Update Todo

- [ ] T079 [US4] Add update_title method to backend/src/application/todo_service.py (get todo, verify ownership, validate title, update)
- [ ] T080 [P] [US4] Add TodoUpdateRequest schema to backend/src/presentation/schemas.py (title field with validation)
- [ ] T081 [US4] Add PUT /todos/{id} endpoint to backend/src/presentation/routers/todos.py (protected, calls todo_service.update_title)

**Backend Update Complete**: PUT /todos/{id} endpoint updates todo title with authorization.

### Frontend: Update Todo UI

- [ ] T082 [US4] Add updateTodo method to frontend/lib/api/todos.ts (PUT /todos/{id} with new title)
- [ ] T083 [US4] Update frontend/components/TodoItem.tsx with inline edit mode (double-click to edit, Enter to save, Escape to cancel)
- [ ] T084 [P] [US4] Handle update validation errors in TodoItem (empty title, title too long)
- [ ] T085 [P] [US4] Implement optimistic UI update for title change (update immediately, revert on error)
- [ ] T086 [US4] Add loading state during title update API call

**Phase 7 Complete**: Users can edit todo titles. Changes persist and validation prevents empty titles.

---

## Phase 8: User Story 5 - Delete Todo (P3)

**User Story**: An authenticated user deletes a todo from their list in the web interface, and it is permanently removed from the database.

**Why P3**: Users need to remove completed or irrelevant tasks. Helps maintain clean todo list.

**Independent Test**: Create todo → Delete todo → Verify it disappears from list → Refresh page → Verify deletion persisted.

**Acceptance Criteria**:
- User can delete their own todo
- Deleted todo is permanently removed from database
- Deleted todo does not reappear after page refresh
- User A cannot delete User B's todo (authorization check)

### Backend: Delete Todo

- [ ] T087 [US5] Add delete method to backend/src/infrastructure/repositories/todo_repository.py (delete todo from database)
- [ ] T088 [US5] Add delete_todo method to backend/src/application/todo_service.py (get todo, verify ownership, delete)
- [ ] T089 [US5] Add DELETE /todos/{id} endpoint to backend/src/presentation/routers/todos.py (protected, calls todo_service.delete_todo, returns 204)

**Backend Delete Complete**: DELETE /todos/{id} endpoint removes todo with authorization.

### Frontend: Delete Todo UI

- [ ] T090 [US5] Add deleteTodo method to frontend/lib/api/todos.ts (DELETE /todos/{id})
- [ ] T091 [US5] Update frontend/components/TodoItem.tsx with delete button (calls deleteTodo, removes from list on success)
- [ ] T092 [P] [US5] Add confirmation dialog before deleting todo ("Are you sure?")
- [ ] T093 [P] [US5] Implement optimistic UI update for delete (remove from list immediately, restore on error)
- [ ] T094 [US5] Handle delete errors (show error message, keep todo in list if API call fails)

**Phase 8 Complete**: Users can delete todos. Deletions are permanent and persist across page refreshes.

---

## Phase 9: Polish & Cross-Cutting Concerns

**Goal**: Final integration, error handling improvements, and responsive design validation.

**Independent Test**: Test all user stories end-to-end on multiple devices (desktop, tablet, mobile). Verify error handling for network failures and authorization errors.

### Final Integration & Polish

- [ ] T095 Validate responsive design on all pages (test 320px, 768px, 1920px screen widths) and adjust Tailwind classes if needed
- [ ] T096 Add global error handling for network failures in frontend/lib/api/client.ts (retry logic, user-friendly messages)

**Phase 9 Complete**: Application polished, responsive, and production-ready.

---

## Dependency Graph

### User Story Dependencies

```
Setup (Phase 1)
    ↓
Foundational (Phase 2)
    ↓
US1: Authentication (Phase 3) [P1]
    ↓
US2: View Todos (Phase 4) [P1]
    ↓
US3: Create Todo (Phase 5) [P2]
    ↓
US6: Toggle Complete (Phase 6) [P2]
    ↓
US4: Update Title (Phase 7) [P3]
    ↓
US5: Delete Todo (Phase 8) [P3]
    ↓
Polish (Phase 9)
```

**Critical Path**: Setup → Foundational → US1 → US2 → US3 → US6 → US4 → US5 → Polish

**Parallelization**: Within each phase, tasks marked `[P]` can be executed in parallel.

---

## Parallel Execution Examples

### Phase 1 (Setup) Parallelization
```
Start: T001 (backend directory)
Then parallel:
  - T002 (requirements.txt)
  - T003 (.env.example)
  - T004 (.gitignore)
  - T006 (README.md)
Then: T005 (install dependencies)

Separately parallel:
  - T007 (Next.js init)
  Then parallel:
    - T008 (add dependencies)
    - T009 (.env.local.example)
    - T010 (Tailwind config)
    - T011 (types.ts)
    - T012 (README.md)
```

### Phase 3 (US1) Parallelization
```
Sequential: T021-T023 (User entity + migration)
Then parallel:
  - T024 (Better Auth setup)
  - T025 (User repository)
Then sequential: T026-T027 (Auth service)
Then parallel:
  - T028 (Auth schemas)
  - T029-T032 (Auth endpoints - can be done in parallel if schema done)
  - T033-T034 (Auth middleware & dependency)
Then: T035 (Register router)

Frontend (after backend auth endpoints ready):
Sequential: T036-T038 (Auth API client)
Then parallel:
  - T039 (Signup page)
  - T040 (Signin page)
  - T041 (AuthForm component)
  - T042 (ErrorMessage component)
Then: T043-T045 (Layout and routing)
```

---

## Testing Notes

**Test Coverage Target**: 80% minimum on backend business logic (services and repositories).

**Testing Approach**:
- Backend: Unit tests for services, integration tests for API endpoints
- Frontend: Component tests for UI elements, integration tests for user flows
- E2E: Manual testing of complete user journeys per acceptance scenarios

**Test Execution**:
- Backend: `pytest tests/ -v --cov=src`
- Frontend: `npm test`

**Note**: This task breakdown focuses on implementation tasks. Comprehensive test tasks can be added based on specific testing requirements or TDD approach.

---

## Definition of Done (Per Phase)

Each phase is complete when:
1. ✅ All tasks in phase completed
2. ✅ Independent test criteria met (documented at phase level)
3. ✅ Acceptance scenarios from spec.md verified
4. ✅ Code linted and formatted (ruff/black for backend, ESLint for frontend)
5. ✅ No TypeScript or Python type errors
6. ✅ Manual testing on localhost successful

**Final Done** (All Phases):
- All 6 user stories implemented and tested
- All 39 functional requirements from spec.md met
- Application deployable (migrations applied, environment configured)
- README documentation updated

---

## References

- **Specification**: [spec.md](./spec.md) - User stories, acceptance criteria, functional requirements
- **Implementation Plan**: [plan.md](./plan.md) - Architecture, tech stack, design decisions
- **Data Model**: [data-model.md](./data-model.md) - Database schema, entities, relationships
- **API Contracts**: [contracts/openapi.yaml](./contracts/openapi.yaml) - REST API specification
- **Quickstart Guide**: [quickstart.md](./quickstart.md) - Development setup instructions

---

*End of Task Breakdown*
