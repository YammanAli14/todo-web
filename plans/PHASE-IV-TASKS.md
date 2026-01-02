# Phase IV Implementation Tasks

**Document ID:** TASKS-PHASE-IV-001
**Version:** 1.0.0
**Status:** Draft — Pending Approval
**Plan Reference:** [PHASE-IV-PLAN.md](./PHASE-IV-PLAN.md)
**Specification Reference:** [../specs/PHASE-IV-SPEC.md](../specs/PHASE-IV-SPEC.md)

---

## 1. Overview

This document contains atomic implementation tasks for Phase IV.

**Total Tasks:** 29
**Backend Tasks:** 16
**Frontend Tasks:** 13

---

## 2. Task Index

| ID | Category | Description |
|----|----------|-------------|
| TASK-401 | Setup | Update requirements.txt with auth dependencies |
| TASK-402 | Setup | Create .env.example with auth variables |
| TASK-403 | Domain | Create User model |
| TASK-404 | Domain | Update Task model with user_id |
| TASK-405 | Infrastructure | Create User repository |
| TASK-406 | Infrastructure | Update Task repository for user filtering |
| TASK-407 | Application | Create Auth service |
| TASK-408 | Application | Update Task service for user context |
| TASK-409 | Presentation | Create auth schemas |
| TASK-410 | Presentation | Create auth dependencies |
| TASK-411 | Presentation | Create auth routes |
| TASK-412 | Presentation | Update task routes with auth |
| TASK-413 | Presentation | Configure CORS middleware |
| TASK-414 | Test | Create auth test fixtures |
| TASK-415 | Test | Write auth tests |
| TASK-416 | Test | Update task tests for auth |
| TASK-417 | Frontend | Initialize Next.js project |
| TASK-418 | Frontend | Configure Tailwind and API client |
| TASK-419 | Frontend | Create types and interfaces |
| TASK-420 | Frontend | Create AuthProvider context |
| TASK-421 | Frontend | Create LoginForm component |
| TASK-422 | Frontend | Create RegisterForm component |
| TASK-423 | Frontend | Create TaskList component |
| TASK-424 | Frontend | Create TaskItem component |
| TASK-425 | Frontend | Create TaskForm component |
| TASK-426 | Frontend | Create Navbar component |
| TASK-427 | Frontend | Create login page |
| TASK-428 | Frontend | Create register page |
| TASK-429 | Frontend | Create tasks page |

---

## 3. Detailed Task Specifications

---

### TASK-401: Update requirements.txt

**Category:** Setup
**Depends On:** None

**Description:**
Add authentication dependencies to requirements.txt.

**Add to requirements.txt:**
```
python-jose[cryptography]>=3.3.0
passlib[bcrypt]>=1.7.4
```

**Completion Criteria:**
- [ ] Dependencies added to requirements.txt

---

### TASK-402: Create .env.example

**Category:** Setup
**Depends On:** None

**Description:**
Update .env.example with JWT configuration variables.

**Add variables:**
```
JWT_SECRET_KEY=your-secret-key-at-least-32-characters-long
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440
```

**Completion Criteria:**
- [ ] .env.example updated with auth variables

---

### TASK-403: Create User Model

**Category:** Domain
**Depends On:** TASK-401

**File:** `todo_api/src/domain/user.py`

**Implementation:**
```python
class User(SQLModel, table=True):
    __tablename__ = "users"

    id: int | None = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True, max_length=255)
    password_hash: str = Field(max_length=255)
    created_at: datetime
    updated_at: datetime
```

**Completion Criteria:**
- [ ] User model with all fields
- [ ] Unique constraint on email
- [ ] Index on email

---

### TASK-404: Update Task Model

**Category:** Domain
**Depends On:** TASK-403

**File:** `todo_api/src/domain/task.py`

**Changes:**
- Add `user_id: int = Field(foreign_key="users.id", index=True)`

**Completion Criteria:**
- [ ] user_id field added
- [ ] Foreign key to users table
- [ ] Index on user_id

---

### TASK-405: Create User Repository

**Category:** Infrastructure
**Depends On:** TASK-403

**File:** `todo_api/src/infrastructure/user_repository.py`

**Methods:**
```python
class UserRepository:
    def create(self, user: User) -> User
    def get_by_id(self, user_id: int) -> User | None
    def get_by_email(self, email: str) -> User | None
    def email_exists(self, email: str) -> bool
```

**Completion Criteria:**
- [ ] All CRUD methods implemented
- [ ] get_by_email for login lookup

---

### TASK-406: Update Task Repository

**Category:** Infrastructure
**Depends On:** TASK-404

**File:** `todo_api/src/infrastructure/task_repository.py`

**Changes:**
- Update `list_all()` to accept `user_id` parameter
- Update `get_by_id()` to verify user ownership
- Create method now requires `user_id`

**Completion Criteria:**
- [ ] All methods filter by user_id
- [ ] User isolation enforced at repository level

---

### TASK-407: Create Auth Service

**Category:** Application
**Depends On:** TASK-405

**File:** `todo_api/src/application/auth_service.py`

**Methods:**
```python
class AuthService:
    def hash_password(self, password: str) -> str
    def verify_password(self, plain: str, hashed: str) -> bool
    def create_access_token(self, user_id: int, email: str) -> str
    def verify_token(self, token: str) -> dict | None
    def register(self, email: str, password: str) -> User
    def authenticate(self, email: str, password: str) -> User | None
```

**Completion Criteria:**
- [ ] Password hashing with bcrypt
- [ ] JWT creation and verification
- [ ] Register and authenticate methods

---

### TASK-408: Update Task Service

**Category:** Application
**Depends On:** TASK-406

**File:** `todo_api/src/application/task_service.py`

**Changes:**
- All methods accept `user_id` parameter
- `create_task` sets `user_id` on task
- `list_tasks` filters by `user_id`
- `get_task`, `update_task`, `delete_task`, `toggle_task` verify ownership

**Completion Criteria:**
- [ ] All methods require user_id
- [ ] User isolation enforced

---

### TASK-409: Create Auth Schemas

**Category:** Presentation
**Depends On:** TASK-403

**File:** `todo_api/src/presentation/schemas.py`

**Add schemas:**
```python
class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)

class UserResponse(BaseModel):
    id: int
    email: str
    created_at: datetime

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class LoginRequest(BaseModel):
    email: EmailStr
    password: str
```

**Completion Criteria:**
- [ ] UserCreate with validation
- [ ] UserResponse without password
- [ ] Token response schema
- [ ] LoginRequest schema

---

### TASK-410: Create Auth Dependencies

**Category:** Presentation
**Depends On:** TASK-407

**File:** `todo_api/src/presentation/dependencies.py`

**Implementation:**
```python
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_session),
    auth_service: AuthService = Depends(get_auth_service)
) -> User:
    # Validate token and return user
```

**Completion Criteria:**
- [ ] OAuth2 scheme configured
- [ ] get_current_user dependency
- [ ] Returns 401 on invalid token

---

### TASK-411: Create Auth Routes

**Category:** Presentation
**Depends On:** TASK-410

**File:** `todo_api/src/presentation/routes/auth.py`

**Endpoints:**
```python
@router.post("/register", status_code=201, response_model=UserResponse)
@router.post("/login", response_model=Token)
@router.get("/me", response_model=UserResponse)
```

**Completion Criteria:**
- [ ] Register endpoint (201 on success, 409 on duplicate)
- [ ] Login endpoint (returns JWT)
- [ ] Me endpoint (returns current user)

---

### TASK-412: Update Task Routes

**Category:** Presentation
**Depends On:** TASK-411

**File:** `todo_api/src/presentation/routes/tasks.py`

**Changes:**
- Add `current_user: User = Depends(get_current_user)` to all routes
- Pass `current_user.id` to service methods

**Completion Criteria:**
- [ ] All routes require authentication
- [ ] User ID passed to service layer

---

### TASK-413: Configure CORS

**Category:** Presentation
**Depends On:** None

**File:** `todo_api/src/presentation/api.py`

**Add:**
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**Completion Criteria:**
- [ ] CORS configured for frontend origin

---

### TASK-414: Create Auth Test Fixtures

**Category:** Test
**Depends On:** TASK-411

**File:** `todo_api/tests/conftest.py`

**Add fixtures:**
```python
@pytest.fixture
def test_user_data():
    return {"email": "test@example.com", "password": "testpass123"}

@pytest.fixture
def registered_user(client, test_user_data):
    # Register user and return response

@pytest.fixture
def auth_headers(client, registered_user, test_user_data):
    # Login and return {"Authorization": "Bearer <token>"}
```

**Completion Criteria:**
- [ ] test_user_data fixture
- [ ] registered_user fixture
- [ ] auth_headers fixture

---

### TASK-415: Write Auth Tests

**Category:** Test
**Depends On:** TASK-414

**File:** `todo_api/tests/unit/test_auth.py`

**Test cases:**
- test_register_success
- test_register_duplicate_email
- test_register_invalid_email
- test_register_short_password
- test_login_success
- test_login_invalid_password
- test_login_nonexistent_user
- test_me_authenticated
- test_me_unauthenticated

**Completion Criteria:**
- [ ] All 9 test cases pass

---

### TASK-416: Update Task Tests

**Category:** Test
**Depends On:** TASK-415

**File:** `todo_api/tests/unit/test_tasks.py`

**Changes:**
- All tests use auth_headers fixture
- Add tests for unauthorized access
- Add tests for user isolation

**Completion Criteria:**
- [ ] All task tests use authentication
- [ ] Unauthorized access returns 401
- [ ] Users cannot access other users' tasks

---

### TASK-417: Initialize Next.js Project

**Category:** Frontend
**Depends On:** None

**Commands:**
```bash
npx create-next-app@14 todo_web --typescript --tailwind --app --src-dir --no-eslint
cd todo_web
npm install axios react-hook-form
```

**Completion Criteria:**
- [ ] Next.js project created
- [ ] TypeScript configured
- [ ] Tailwind CSS configured
- [ ] Dependencies installed

---

### TASK-418: Configure API Client

**Category:** Frontend
**Depends On:** TASK-417

**Files:**
- `todo_web/src/lib/api.ts`
- `todo_web/.env.local`

**Implementation:**
```typescript
// api.ts
import axios from 'axios';

const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL,
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default api;
```

**Completion Criteria:**
- [ ] Axios client configured
- [ ] Auth interceptor adds Bearer token
- [ ] Environment variable for API URL

---

### TASK-419: Create Types

**Category:** Frontend
**Depends On:** TASK-417

**File:** `todo_web/src/types/index.ts`

**Types:**
```typescript
export interface User {
  id: number;
  email: string;
  created_at: string;
}

export interface Task {
  id: number;
  title: string;
  is_complete: boolean;
  created_at: string;
  updated_at: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
}
```

**Completion Criteria:**
- [ ] User interface
- [ ] Task interface
- [ ] AuthResponse interface

---

### TASK-420: Create AuthProvider

**Category:** Frontend
**Depends On:** TASK-418, TASK-419

**File:** `todo_web/src/components/auth/AuthProvider.tsx`

**Implementation:**
- AuthContext with user state
- login, logout, checkAuth methods
- Token storage in localStorage
- Wrap app in provider

**Completion Criteria:**
- [ ] Auth context created
- [ ] login/logout methods
- [ ] Token persistence

---

### TASK-421: Create LoginForm

**Category:** Frontend
**Depends On:** TASK-420

**File:** `todo_web/src/components/auth/LoginForm.tsx`

**Features:**
- Email and password inputs
- Form validation
- Error display
- Submit handler calling login

**Completion Criteria:**
- [ ] Form with validation
- [ ] Error handling
- [ ] Calls auth context login

---

### TASK-422: Create RegisterForm

**Category:** Frontend
**Depends On:** TASK-420

**File:** `todo_web/src/components/auth/RegisterForm.tsx`

**Features:**
- Email, password, confirm password inputs
- Password match validation
- Error display
- Success redirects to login

**Completion Criteria:**
- [ ] Form with validation
- [ ] Password confirmation
- [ ] Success redirect

---

### TASK-423: Create TaskList

**Category:** Frontend
**Depends On:** TASK-419

**File:** `todo_web/src/components/tasks/TaskList.tsx`

**Features:**
- Fetch and display tasks
- Loading state
- Empty state message
- Render TaskItem components

**Completion Criteria:**
- [ ] Displays list of tasks
- [ ] Loading indicator
- [ ] Empty state

---

### TASK-424: Create TaskItem

**Category:** Frontend
**Depends On:** TASK-423

**File:** `todo_web/src/components/tasks/TaskItem.tsx`

**Features:**
- Display task title and status
- Checkbox to toggle completion
- Delete button
- Edit button (optional inline edit)

**Completion Criteria:**
- [ ] Shows task info
- [ ] Toggle completion
- [ ] Delete functionality

---

### TASK-425: Create TaskForm

**Category:** Frontend
**Depends On:** TASK-419

**File:** `todo_web/src/components/tasks/TaskForm.tsx`

**Features:**
- Input for task title
- Submit button
- Calls API to create task
- Clears input on success

**Completion Criteria:**
- [ ] Form to create task
- [ ] Validation
- [ ] Clears on success

---

### TASK-426: Create Navbar

**Category:** Frontend
**Depends On:** TASK-420

**File:** `todo_web/src/components/layout/Navbar.tsx`

**Features:**
- Logo/title
- Auth state display (email or Login/Register)
- Logout button when authenticated
- Navigation links

**Completion Criteria:**
- [ ] Shows auth state
- [ ] Logout button
- [ ] Navigation links

---

### TASK-427: Create Login Page

**Category:** Frontend
**Depends On:** TASK-421

**File:** `todo_web/src/app/login/page.tsx`

**Features:**
- Render LoginForm
- Link to register page
- Redirect to /tasks on success

**Completion Criteria:**
- [ ] Login form displayed
- [ ] Register link
- [ ] Redirect on success

---

### TASK-428: Create Register Page

**Category:** Frontend
**Depends On:** TASK-422

**File:** `todo_web/src/app/register/page.tsx`

**Features:**
- Render RegisterForm
- Link to login page
- Redirect to login on success

**Completion Criteria:**
- [ ] Register form displayed
- [ ] Login link
- [ ] Redirect on success

---

### TASK-429: Create Tasks Page

**Category:** Frontend
**Depends On:** TASK-423, TASK-425

**File:** `todo_web/src/app/tasks/page.tsx`

**Features:**
- Protected route (redirect if not authenticated)
- TaskForm to add tasks
- TaskList to display tasks
- Refresh list on create/update/delete

**Completion Criteria:**
- [ ] Protected route
- [ ] Create and list tasks
- [ ] Updates on changes

---

## 4. Document Control

### 4.1 Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2025-12-28 | Agent | Initial task breakdown |

---

*End of Phase IV Implementation Tasks*
