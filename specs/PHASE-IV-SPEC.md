# Phase IV Specification — Authentication & Frontend

**Document ID:** SPEC-PHASE-IV-001
**Version:** 1.0.0
**Status:** Draft — Pending Approval
**Governing Document:** [CONSTITUTION.md](../CONSTITUTION.md)
**Phase:** IV — Frontend & Authentication
**Depends On:** Phase II (Complete), Phase III (Complete)

---

## 1. Overview

### 1.1 Purpose

This specification defines the requirements for Phase IV of the Evolution of Todo project: user authentication system with JWT tokens and a Next.js web frontend for the Todo application.

### 1.2 Scope Summary

Phase IV adds:
1. User registration and authentication (JWT-based)
2. Multi-user support with user-owned tasks
3. Next.js web frontend for task management
4. Protected API endpoints

### 1.3 Constitutional Compliance

This specification complies with:

- **Article I** — Defines scope, requirements, interfaces, acceptance criteria, and dependencies
- **Article III, Section 3.1** — Implements Phase IV: Next.js web application, user authentication
- **Article III, Section 3.2** — Contains no forward leakage to Phase V
- **Article IV** — Uses mandatory technologies: FastAPI, SQLModel, Next.js
- **Article V** — Adheres to clean architecture and quality principles

---

## 2. Scope Definition

### 2.1 In Scope

| Item | Description |
|------|-------------|
| User Model | User entity with email, password hash, timestamps |
| Registration | POST /auth/register endpoint |
| Login | POST /auth/login endpoint returning JWT |
| JWT Authentication | Bearer token authentication middleware |
| Password Hashing | bcrypt for secure password storage |
| Task Ownership | Tasks belong to authenticated users |
| Protected Endpoints | All task endpoints require authentication |
| Next.js Frontend | Web UI for registration, login, task management |
| Responsive Design | Mobile-friendly UI with Tailwind CSS |

### 2.2 Explicitly Out of Scope

The following are **prohibited** in Phase IV:

| Excluded Item | Reason |
|---------------|--------|
| OAuth/Social Login | Not in Phase IV requirements |
| Password Reset | Not in Phase IV requirements |
| Email Verification | Not in Phase IV requirements |
| Role-Based Access Control | Not in Phase IV requirements |
| Docker/Kubernetes | Phase V feature |
| Message Queues | Phase V feature |
| Multi-tenant Architecture | Phase V feature |
| Admin Panel | Not specified |

---

## 3. User Stories

### 3.1 US-401: User Registration

**As a** new user
**I want to** create an account with email and password
**So that** I can have my own private todo list

**Acceptance Criteria:**

| ID | Criterion |
|----|-----------|
| AC-401-1 | User can register with email and password |
| AC-401-2 | Email must be unique (no duplicates) |
| AC-401-3 | Password must be at least 8 characters |
| AC-401-4 | Password is stored as bcrypt hash |
| AC-401-5 | Registration returns user ID and email |
| AC-401-6 | Invalid email format returns 422 error |

### 3.2 US-402: User Login

**As a** registered user
**I want to** log in with my credentials
**So that** I can access my tasks

**Acceptance Criteria:**

| ID | Criterion |
|----|-----------|
| AC-402-1 | User can login with email and password |
| AC-402-2 | Successful login returns JWT access token |
| AC-402-3 | Token expires after 24 hours |
| AC-402-4 | Invalid credentials return 401 error |
| AC-402-5 | Non-existent email returns 401 error |

### 3.3 US-403: Protected Task Operations

**As an** authenticated user
**I want to** manage only my own tasks
**So that** my tasks are private

**Acceptance Criteria:**

| ID | Criterion |
|----|-----------|
| AC-403-1 | All task endpoints require Bearer token |
| AC-403-2 | Missing token returns 401 error |
| AC-403-3 | Invalid token returns 401 error |
| AC-403-4 | Expired token returns 401 error |
| AC-403-5 | Users can only see their own tasks |
| AC-403-6 | Users cannot access other users' tasks |

### 3.4 US-404: Frontend Registration Page

**As a** new user
**I want to** register through a web form
**So that** I can create an account easily

**Acceptance Criteria:**

| ID | Criterion |
|----|-----------|
| AC-404-1 | Registration form with email and password fields |
| AC-404-2 | Password confirmation field |
| AC-404-3 | Client-side validation messages |
| AC-404-4 | Successful registration redirects to login |
| AC-404-5 | Error messages displayed on failure |

### 3.5 US-405: Frontend Login Page

**As a** registered user
**I want to** log in through a web form
**So that** I can access my tasks

**Acceptance Criteria:**

| ID | Criterion |
|----|-----------|
| AC-405-1 | Login form with email and password fields |
| AC-405-2 | Successful login stores JWT and redirects to tasks |
| AC-405-3 | Error messages displayed on failure |
| AC-405-4 | "Register" link for new users |

### 3.6 US-406: Frontend Task Dashboard

**As an** authenticated user
**I want to** see and manage my tasks in a web interface
**So that** I can use the app from my browser

**Acceptance Criteria:**

| ID | Criterion |
|----|-----------|
| AC-406-1 | Task list displays all user's tasks |
| AC-406-2 | Form to create new tasks |
| AC-406-3 | Checkbox to toggle task completion |
| AC-406-4 | Delete button for each task |
| AC-406-5 | Edit functionality for task titles |
| AC-406-6 | Logout button that clears session |
| AC-406-7 | Unauthenticated users redirected to login |

### 3.7 US-407: Current User Endpoint

**As an** authenticated user
**I want to** retrieve my profile information
**So that** the frontend can display my identity

**Acceptance Criteria:**

| ID | Criterion |
|----|-----------|
| AC-407-1 | GET /auth/me returns current user info |
| AC-407-2 | Returns user ID and email |
| AC-407-3 | Requires valid Bearer token |

---

## 4. Data Model

### 4.1 User Entity

```python
class User(SQLModel, table=True):
    __tablename__ = "users"

    id: int | None = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True, max_length=255)
    password_hash: str = Field(max_length=255)
    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)
```

### 4.2 Updated Task Entity

```python
class Task(SQLModel, table=True):
    __tablename__ = "tasks"

    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(max_length=200)
    is_complete: bool = Field(default=False)
    user_id: int = Field(foreign_key="users.id", index=True)  # NEW
    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)
```

### 4.3 Database Schema

```sql
-- Users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tasks table (updated)
CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    is_complete BOOLEAN DEFAULT FALSE,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_tasks_user_id ON tasks(user_id);
```

---

## 5. API Specification

### 5.1 Authentication Endpoints

#### 5.1.1 POST /auth/register

**Request:**
```json
{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

**Response (201 Created):**
```json
{
  "id": 1,
  "email": "user@example.com",
  "created_at": "2025-12-28T10:00:00Z"
}
```

**Errors:**
- 422: Invalid email format or password too short
- 409: Email already registered

#### 5.1.2 POST /auth/login

**Request:**
```json
{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

**Response (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Errors:**
- 401: Invalid credentials

#### 5.1.3 GET /auth/me

**Headers:**
```
Authorization: Bearer <token>
```

**Response (200 OK):**
```json
{
  "id": 1,
  "email": "user@example.com",
  "created_at": "2025-12-28T10:00:00Z"
}
```

**Errors:**
- 401: Missing or invalid token

### 5.2 Updated Task Endpoints

All task endpoints now require authentication:

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /tasks | List current user's tasks |
| POST | /tasks | Create task for current user |
| GET | /tasks/{id} | Get user's task by ID |
| PUT | /tasks/{id} | Update user's task |
| DELETE | /tasks/{id} | Delete user's task |
| PATCH | /tasks/{id}/toggle | Toggle user's task |

**Authorization Header Required:**
```
Authorization: Bearer <token>
```

**Access Control:**
- Users can only access tasks where `task.user_id == current_user.id`
- Attempting to access another user's task returns 404 (not 403, for security)

---

## 6. JWT Configuration

### 6.1 Token Structure

```json
{
  "sub": "1",           // User ID as string
  "email": "user@example.com",
  "exp": 1735488000,    // Expiration timestamp
  "iat": 1735401600     // Issued at timestamp
}
```

### 6.2 Token Settings

| Setting | Value |
|---------|-------|
| Algorithm | HS256 |
| Expiration | 24 hours |
| Secret Key | Environment variable `JWT_SECRET_KEY` |

---

## 7. Frontend Specification

### 7.1 Technology Stack

| Technology | Version | Purpose |
|------------|---------|---------|
| Next.js | 14+ | React framework |
| TypeScript | 5+ | Type safety |
| Tailwind CSS | 3+ | Styling |
| React Hook Form | Latest | Form handling |
| Axios | Latest | HTTP client |

### 7.2 Pages

| Route | Page | Auth Required |
|-------|------|---------------|
| `/` | Home/Landing | No |
| `/login` | Login form | No |
| `/register` | Registration form | No |
| `/tasks` | Task dashboard | Yes |

### 7.3 Components

| Component | Description |
|-----------|-------------|
| `AuthProvider` | Context for authentication state |
| `LoginForm` | Email/password login form |
| `RegisterForm` | Registration form with confirmation |
| `TaskList` | Displays list of tasks |
| `TaskItem` | Single task with actions |
| `TaskForm` | Form to create/edit tasks |
| `Navbar` | Navigation with auth state |
| `ProtectedRoute` | Wrapper requiring authentication |

### 7.4 State Management

- JWT stored in localStorage
- Auth state in React Context
- Token included in API request headers

---

## 8. Environment Configuration

### 8.1 Backend Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `DATABASE_URL` | Yes | Database connection string |
| `JWT_SECRET_KEY` | Yes | Secret for signing JWTs |
| `JWT_ALGORITHM` | No | Algorithm (default: HS256) |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | No | Token expiry (default: 1440) |

### 8.2 Frontend Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `NEXT_PUBLIC_API_URL` | Yes | Backend API URL |

---

## 9. Security Requirements

### 9.1 Password Security

| Requirement | Implementation |
|-------------|----------------|
| Minimum length | 8 characters |
| Hashing | bcrypt with cost factor 12 |
| Storage | Only hash stored, never plaintext |

### 9.2 JWT Security

| Requirement | Implementation |
|-------------|----------------|
| Secret key | Minimum 32 characters, from environment |
| Algorithm | HS256 |
| Expiration | 24 hours max |
| Validation | Verify signature and expiration |

### 9.3 API Security

| Requirement | Implementation |
|-------------|----------------|
| CORS | Configure allowed origins |
| Rate limiting | Optional for Phase IV |
| Input validation | Pydantic schemas |

---

## 10. Project Structure

### 10.1 Backend Structure (Updated todo_api)

```
todo_api/
├── src/
│   ├── domain/
│   │   ├── task.py
│   │   └── user.py              # NEW
│   ├── application/
│   │   ├── task_service.py
│   │   └── auth_service.py      # NEW
│   ├── infrastructure/
│   │   ├── database.py
│   │   ├── task_repository.py
│   │   └── user_repository.py   # NEW
│   └── presentation/
│       ├── api.py
│       ├── dependencies.py      # NEW (auth dependencies)
│       ├── schemas.py
│       └── routes/
│           ├── tasks.py
│           └── auth.py          # NEW
├── tests/
└── requirements.txt
```

### 10.2 Frontend Structure (New todo_web)

```
todo_web/
├── src/
│   ├── app/
│   │   ├── layout.tsx
│   │   ├── page.tsx
│   │   ├── login/
│   │   │   └── page.tsx
│   │   ├── register/
│   │   │   └── page.tsx
│   │   └── tasks/
│   │       └── page.tsx
│   ├── components/
│   │   ├── auth/
│   │   │   ├── LoginForm.tsx
│   │   │   ├── RegisterForm.tsx
│   │   │   └── AuthProvider.tsx
│   │   ├── tasks/
│   │   │   ├── TaskList.tsx
│   │   │   ├── TaskItem.tsx
│   │   │   └── TaskForm.tsx
│   │   └── layout/
│   │       └── Navbar.tsx
│   ├── lib/
│   │   ├── api.ts
│   │   └── auth.ts
│   └── types/
│       └── index.ts
├── public/
├── package.json
├── tsconfig.json
├── tailwind.config.js
└── next.config.js
```

---

## 11. Non-Functional Requirements

### 11.1 Performance

| Requirement | Specification |
|-------------|---------------|
| API Response | < 200ms for auth endpoints |
| Frontend Load | < 3 seconds initial load |
| Token Validation | < 10ms |

### 11.2 Code Quality

Per Constitution Article V, Section 5.4:

| Requirement | Specification |
|-------------|---------------|
| Type Hints | All Python functions typed |
| TypeScript | Strict mode enabled |
| Testing | Minimum 80% backend coverage |
| Linting | ESLint for frontend, ruff for backend |

---

## 12. Acceptance Criteria Summary

### 12.1 Feature Completion Checklist

| Feature | Criteria Count | Required Pass |
|---------|----------------|---------------|
| User Registration | 6 | All |
| User Login | 5 | All |
| Protected Tasks | 6 | All |
| Frontend Registration | 5 | All |
| Frontend Login | 4 | All |
| Frontend Dashboard | 7 | All |
| Current User Endpoint | 3 | All |
| **Total** | **36** | **All** |

### 12.2 Quality Checklist

| Requirement | Pass Criteria |
|-------------|---------------|
| Type Hints | All functions typed |
| TypeScript | No type errors |
| Backend Tests | >= 80% coverage |
| Security | Passwords hashed, JWTs validated |

### 12.3 Phase Completion Criteria

Phase IV is complete when:

1. All 36 acceptance criteria pass
2. All quality requirements met
3. All tests pass
4. Backend and frontend integrated
5. README documentation complete
6. Human review approves deliverable

---

## 13. Glossary

| Term | Definition |
|------|------------|
| JWT | JSON Web Token for authentication |
| Bearer Token | Token passed in Authorization header |
| bcrypt | Password hashing algorithm |
| Access Token | JWT granting API access |

---

## 14. Document Control

### 14.1 Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2025-12-28 | Agent | Initial specification |

### 14.2 Approval

| Role | Name | Date | Status |
|------|------|------|--------|
| Specification Author | Agent | 2025-12-28 | Draft |
| Human Reviewer | — | — | Pending |

---

## 15. References

- [CONSTITUTION.md](../CONSTITUTION.md) — Global project constitution
- [PHASE-II-SPEC.md](./PHASE-II-SPEC.md) — Phase II specification
- [PHASE-III-SPEC.md](./PHASE-III-SPEC.md) — Phase III specification

---

*End of Phase IV Specification*
