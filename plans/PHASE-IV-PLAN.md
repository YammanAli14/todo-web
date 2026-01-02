# Phase IV Technical Plan — Authentication & Frontend

**Document ID:** PLAN-PHASE-IV-001
**Version:** 1.0.0
**Status:** Draft — Pending Approval
**Specification Reference:** [../specs/PHASE-IV-SPEC.md](../specs/PHASE-IV-SPEC.md)
**Constitution Reference:** [../CONSTITUTION.md](../CONSTITUTION.md)

---

## 1. Overview

This plan defines the technical implementation approach for Phase IV of the Evolution of Todo project. Phase IV adds user authentication with JWT tokens and a Next.js web frontend.

### 1.1 Deliverables

| Deliverable | Description |
|-------------|-------------|
| User Model | SQLModel entity for users |
| Auth Service | Registration, login, JWT handling |
| Auth Routes | /auth/register, /auth/login, /auth/me |
| Auth Middleware | JWT validation dependency |
| Updated Task Model | Tasks with user_id foreign key |
| Protected Task Routes | All task endpoints require auth |
| Next.js Frontend | Web UI with auth and task management |
| Tests | Unit and integration tests |

---

## 2. Backend Implementation

### 2.1 Project Structure Updates

```
todo_api/
├── src/
│   ├── domain/
│   │   ├── task.py          # Updated with user_id
│   │   └── user.py          # NEW
│   ├── application/
│   │   ├── task_service.py  # Updated for user filtering
│   │   └── auth_service.py  # NEW
│   ├── infrastructure/
│   │   ├── database.py
│   │   ├── task_repository.py  # Updated for user filtering
│   │   └── user_repository.py  # NEW
│   └── presentation/
│       ├── api.py           # Updated with auth routes
│       ├── dependencies.py  # NEW (get_current_user)
│       ├── schemas.py       # Updated with auth schemas
│       └── routes/
│           ├── tasks.py     # Updated with auth dependency
│           └── auth.py      # NEW
```

### 2.2 New Dependencies

```
# Add to requirements.txt
python-jose[cryptography]>=3.3.0
passlib[bcrypt]>=1.7.4
```

### 2.3 User Domain Model

```python
# src/domain/user.py
from datetime import datetime
from sqlmodel import SQLModel, Field

class User(SQLModel, table=True):
    __tablename__ = "users"

    id: int | None = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True, max_length=255)
    password_hash: str = Field(max_length=255)
    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)
```

### 2.4 Task Model Update

```python
# src/domain/task.py - Add user_id field
user_id: int = Field(foreign_key="users.id", index=True)
```

### 2.5 Auth Service

```python
# src/application/auth_service.py
class AuthService:
    def register(self, email: str, password: str) -> User
    def authenticate(self, email: str, password: str) -> User | None
    def create_access_token(self, user: User) -> str
    def verify_token(self, token: str) -> dict | None
    def hash_password(self, password: str) -> str
    def verify_password(self, plain: str, hashed: str) -> bool
```

### 2.6 Auth Dependency

```python
# src/presentation/dependencies.py
async def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_session)
) -> User:
    # Validate JWT and return user
```

### 2.7 Auth Routes

```python
# src/presentation/routes/auth.py
@router.post("/register", status_code=201)
@router.post("/login")
@router.get("/me")
```

---

## 3. Frontend Implementation

### 3.1 Project Setup

```bash
npx create-next-app@14 todo_web --typescript --tailwind --app --src-dir
```

### 3.2 Directory Structure

```
todo_web/
├── src/
│   ├── app/
│   │   ├── layout.tsx
│   │   ├── page.tsx
│   │   ├── login/page.tsx
│   │   ├── register/page.tsx
│   │   └── tasks/page.tsx
│   ├── components/
│   │   ├── auth/
│   │   ├── tasks/
│   │   └── layout/
│   ├── lib/
│   │   ├── api.ts
│   │   └── auth.ts
│   └── types/
│       └── index.ts
├── package.json
└── next.config.js
```

### 3.3 Key Components

| Component | Responsibility |
|-----------|---------------|
| AuthProvider | Manage auth state, token storage |
| LoginForm | Handle login form submission |
| RegisterForm | Handle registration with validation |
| TaskList | Display and manage tasks |
| TaskItem | Single task with toggle/delete |
| TaskForm | Create new tasks |
| Navbar | Navigation with auth state |

### 3.4 API Client

```typescript
// src/lib/api.ts
const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL,
});

// Add auth interceptor for Bearer token
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});
```

### 3.5 Auth Context

```typescript
// src/components/auth/AuthProvider.tsx
interface AuthContextType {
  user: User | null;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
  isAuthenticated: boolean;
}
```

---

## 4. Security Implementation

### 4.1 Password Hashing

```python
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)
```

### 4.2 JWT Generation

```python
from jose import jwt
from datetime import datetime, timedelta, timezone

def create_access_token(data: dict) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=1440)
    to_encode = data.copy()
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")
```

### 4.3 JWT Validation

```python
def verify_token(token: str) -> dict | None:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except JWTError:
        return None
```

---

## 5. Database Migration

### 5.1 Schema Changes

1. Create `users` table
2. Add `user_id` column to `tasks` table
3. Create foreign key constraint
4. Create index on `tasks.user_id`

### 5.2 Migration Strategy

For SQLite (development), SQLModel's `create_all` will handle schema.
For production, use Alembic migrations (not in Phase IV scope).

---

## 6. Testing Strategy

### 6.1 Backend Tests

| Test Category | Coverage |
|---------------|----------|
| User Repository | CRUD operations |
| Auth Service | Hash, verify, token operations |
| Auth Routes | Register, login, me endpoints |
| Task Routes | Protected access, user filtering |

### 6.2 Test Fixtures

```python
@pytest.fixture
def test_user():
    return {"email": "test@example.com", "password": "testpass123"}

@pytest.fixture
def auth_headers(client, test_user):
    # Register and login, return Bearer token headers
```

### 6.3 Frontend Tests

Basic component rendering tests (optional for Phase IV).

---

## 7. Environment Configuration

### 7.1 Backend (.env)

```env
DATABASE_URL=sqlite:///./todo.db
JWT_SECRET_KEY=your-super-secret-key-at-least-32-chars
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440
```

### 7.2 Frontend (.env.local)

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

---

## 8. CORS Configuration

```python
# src/presentation/api.py
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 9. Task Breakdown Summary

| Category | Tasks |
|----------|-------|
| Setup | 3 tasks |
| Domain | 2 tasks |
| Infrastructure | 2 tasks |
| Application | 2 tasks |
| Presentation | 4 tasks |
| Frontend Setup | 2 tasks |
| Frontend Components | 6 tasks |
| Frontend Pages | 4 tasks |
| Testing | 3 tasks |
| Documentation | 1 task |
| **Total** | **29 tasks** |

---

## 10. Verification Checklist

### 10.1 Backend Verification

- [ ] User registration creates user with hashed password
- [ ] Login returns valid JWT token
- [ ] Token validates correctly
- [ ] Protected endpoints reject invalid tokens
- [ ] Users can only access their own tasks
- [ ] All tests pass with >= 80% coverage

### 10.2 Frontend Verification

- [ ] Registration form works
- [ ] Login stores token and redirects
- [ ] Task dashboard shows user's tasks
- [ ] CRUD operations work
- [ ] Logout clears session
- [ ] Unauthenticated access redirects to login

---

## 11. Document Control

### 11.1 Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2025-12-28 | Agent | Initial plan |

### 11.2 Approval

| Role | Name | Date | Status |
|------|------|------|--------|
| Plan Author | Agent | 2025-12-28 | Draft |
| Human Reviewer | — | — | Pending |

---

## 12. References

- [PHASE-IV-SPEC.md](../specs/PHASE-IV-SPEC.md) — Phase IV Specification
- [CONSTITUTION.md](../CONSTITUTION.md) — Global Constitution

---

*End of Phase IV Technical Plan*
