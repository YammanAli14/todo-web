# Data Model: Phase II Full-Stack Todo Application

**Date**: 2026-01-02
**Feature**: 1-phase-ii-fullstack
**Database**: Neon Serverless PostgreSQL (Production), SQLite (Development)

---

## Entity Relationship Diagram

```
┌─────────────────────┐
│       User          │
├─────────────────────┤
│ id (PK)             │
│ email (UNIQUE)      │
│ password_hash       │
│ created_at          │
│ updated_at          │
└─────────────────────┘
           │
           │ 1:N
           │
           ▼
┌─────────────────────┐
│       Todo          │
├─────────────────────┤
│ id (PK)             │
│ user_id (FK)        │
│ title               │
│ is_complete         │
│ created_at          │
│ updated_at          │
└─────────────────────┘
```

**Relationship**: One User has many Todos. Each Todo belongs to exactly one User.

---

## Entity: User

### Purpose
Represents a registered user account. Users authenticate via Better Auth and own a collection of todos.

### Fields

| Field | Type | Constraints | Default | Description |
|-------|------|-------------|---------|-------------|
| `id` | `int` | PRIMARY KEY, AUTO INCREMENT | Auto | Unique user identifier |
| `email` | `str` | UNIQUE, NOT NULL, max 255 chars | Required | User's email address (used for login) |
| `password_hash` | `str` | NOT NULL, max 255 chars | Required | Bcrypt hashed password (never store plain text) |
| `created_at` | `datetime` | NOT NULL | `now()` | Timestamp when user account was created |
| `updated_at` | `datetime` | NOT NULL | `now()` | Timestamp of last update to user record |

### Validation Rules

- **Email**:
  - Must be valid email format (e.g., user@example.com)
  - Must be unique across all users
  - Case-insensitive comparison (store as lowercase)
  - Maximum 255 characters

- **Password** (before hashing):
  - Minimum 8 characters
  - Must not be empty or whitespace-only
  - Hashed with bcrypt before storage (managed by Better Auth)

### Indexes

```sql
CREATE UNIQUE INDEX idx_user_email ON users(LOWER(email));
```

### SQLModel Definition (Backend)

```python
from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

class User(SQLModel, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(max_length=255, nullable=False, unique=True, index=True)
    password_hash: str = Field(max_length=255, nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
```

### TypeScript Type (Frontend)

```typescript
export interface User {
  id: number;
  email: string;
  created_at: string;  // ISO 8601 datetime string
  updated_at: string;  // ISO 8601 datetime string
}
// Note: password_hash is NEVER sent to frontend
```

### State Transitions

Users have no explicit state field, but conceptually:
1. **Unregistered** → Register → **Registered**
2. **Registered** → Sign In → **Authenticated** (session-based, not stored in DB)
3. **Authenticated** → Sign Out → **Unauthenticated**

---

## Entity: Todo

### Purpose
Represents a single task in a user's todo list. Each todo has a title, completion status, and belongs to exactly one user.

### Fields

| Field | Type | Constraints | Default | Description |
|-------|------|-------------|---------|-------------|
| `id` | `int` | PRIMARY KEY, AUTO INCREMENT | Auto | Unique todo identifier |
| `user_id` | `int` | FOREIGN KEY (users.id), NOT NULL, ON DELETE CASCADE | Required | Owner of this todo |
| `title` | `str` | NOT NULL, max 200 chars | Required | Todo task description |
| `is_complete` | `bool` | NOT NULL | `False` | Completion status (true = complete, false = incomplete) |
| `created_at` | `datetime` | NOT NULL | `now()` | Timestamp when todo was created |
| `updated_at` | `datetime` | NOT NULL | `now()` | Timestamp of last update (title change or toggle) |

### Validation Rules

- **Title**:
  - Must not be empty string
  - Must not be whitespace-only (e.g., "   ")
  - Maximum 200 characters
  - Trimmed of leading/trailing whitespace before storage

- **User ID**:
  - Must reference an existing user
  - Cannot be null or changed after creation

- **Is Complete**:
  - Boolean only (no null values)
  - Defaults to false (incomplete) on creation

### Indexes

```sql
CREATE INDEX idx_todo_user_id ON todos(user_id);
CREATE INDEX idx_todo_created_at ON todos(created_at);
```

*Rationale*: `user_id` index for fast filtering of todos by user. `created_at` index for ordering todos (if sorting by creation time).

### Constraints

```sql
ALTER TABLE todos
ADD CONSTRAINT fk_todo_user
FOREIGN KEY (user_id) REFERENCES users(id)
ON DELETE CASCADE;
```

*ON DELETE CASCADE*: When a user is deleted, all their todos are automatically deleted (data isolation).

### SQLModel Definition (Backend)

```python
from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

class Todo(SQLModel, table=True):
    __tablename__ = "todos"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", nullable=False, index=True)
    title: str = Field(max_length=200, nullable=False)
    is_complete: bool = Field(default=False, nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
```

### TypeScript Type (Frontend)

```typescript
export interface Todo {
  id: number;
  user_id: number;  // Often omitted in frontend since user sees only their todos
  title: string;
  is_complete: boolean;
  created_at: string;  // ISO 8601 datetime string
  updated_at: string;  // ISO 8601 datetime string
}
```

### State Transitions

Todos have explicit state via `is_complete`:

```
[Created]
   │
   ├─> is_complete = false (Incomplete)
   │        │
   │        ├─> Toggle ─> is_complete = true (Complete)
   │        │                    │
   │        │                    └─> Toggle ─> is_complete = false
   │        │
   │        └─> Delete ─> [Deleted]
   │
   └─> Delete ─> [Deleted]
```

**Lifecycle**:
1. **Create**: Todo created with `is_complete = false`
2. **Update**: Title can be modified (updates `updated_at`)
3. **Toggle**: `is_complete` flips between true/false (updates `updated_at`)
4. **Delete**: Todo permanently removed from database

---

## Database Schema (SQL)

### Complete Schema

```sql
-- Users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE UNIQUE INDEX idx_user_email ON users(LOWER(email));

-- Todos table
CREATE TABLE todos (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    title VARCHAR(200) NOT NULL,
    is_complete BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    CONSTRAINT fk_todo_user FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE
);

CREATE INDEX idx_todo_user_id ON todos(user_id);
CREATE INDEX idx_todo_created_at ON todos(created_at);
```

### Migration Strategy

**Tool**: Alembic (Python database migration tool)

**Initial Migration**:
1. Initialize Alembic in backend project: `alembic init alembic`
2. Configure `alembic.ini` with database URL (Neon PostgreSQL)
3. Auto-generate initial migration from SQLModel definitions:
   ```bash
   alembic revision --autogenerate -m "Initial schema: users and todos"
   ```
4. Review generated migration file
5. Apply migration to database:
   ```bash
   alembic upgrade head
   ```

**Future Migrations** (if schema changes):
1. Update SQLModel entity definitions
2. Generate migration: `alembic revision --autogenerate -m "Description"`
3. Review and apply: `alembic upgrade head`

**Rollback** (if needed):
```bash
alembic downgrade -1  # Roll back one migration
```

---

## Data Access Patterns

### User Operations

**Create User** (Registration):
```python
# Create new user with hashed password
user = User(email="user@example.com", password_hash=hashed_password)
session.add(user)
session.commit()
```

**Find User by Email** (Login):
```python
user = session.exec(
    select(User).where(User.email == email.lower())
).first()
```

**Update User** (if password change):
```python
user.password_hash = new_hashed_password
user.updated_at = datetime.utcnow()
session.add(user)
session.commit()
```

### Todo Operations

**Create Todo**:
```python
todo = Todo(user_id=current_user.id, title="Buy groceries", is_complete=False)
session.add(todo)
session.commit()
```

**Get All Todos for User**:
```python
todos = session.exec(
    select(Todo)
    .where(Todo.user_id == current_user.id)
    .order_by(Todo.created_at)
).all()
```

**Get Single Todo (with ownership check)**:
```python
todo = session.exec(
    select(Todo)
    .where(Todo.id == todo_id, Todo.user_id == current_user.id)
).first()
if not todo:
    raise HTTPException(status_code=404, detail="Todo not found")
```

**Update Todo Title**:
```python
todo.title = new_title.strip()
todo.updated_at = datetime.utcnow()
session.add(todo)
session.commit()
```

**Toggle Todo Completion**:
```python
todo.is_complete = not todo.is_complete
todo.updated_at = datetime.utcnow()
session.add(todo)
session.commit()
```

**Delete Todo**:
```python
session.delete(todo)
session.commit()
```

---

## Data Isolation & Security

### User Data Isolation

**Rule**: Users can ONLY access their own todos.

**Implementation**:
- All todo queries MUST include `WHERE user_id = current_user.id`
- Backend middleware extracts `current_user` from Better Auth session
- Frontend never stores or displays other users' data

**Example** (Correct):
```python
# ✅ CORRECT - Filtered by user_id
todos = session.exec(
    select(Todo).where(Todo.user_id == current_user.id)
).all()
```

**Example** (INCORRECT - Security Violation):
```python
# ❌ WRONG - Returns ALL todos from ALL users
todos = session.exec(select(Todo)).all()
```

### Authorization Checks

All todo operations MUST verify ownership:

```python
def get_todo_or_403(todo_id: int, user_id: int, session: Session) -> Todo:
    todo = session.get(Todo, todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    if todo.user_id != user_id:
        raise HTTPException(status_code=403, detail="Forbidden: You don't own this todo")
    return todo
```

### Sensitive Data Handling

**Password Hash**:
- NEVER return password_hash in API responses
- Use Pydantic response models that exclude password_hash
- Log sanitization: never log passwords or hashes

**User IDs**:
- Frontend doesn't need to send user_id in requests (extracted from session)
- Backend automatically filters by authenticated user's ID

---

## Sample Data (for testing)

### User Seed Data
```python
users = [
    User(email="alice@example.com", password_hash="$2b$12$..."),
    User(email="bob@example.com", password_hash="$2b$12$..."),
]
```

### Todo Seed Data
```python
todos = [
    Todo(user_id=1, title="Buy groceries", is_complete=False),
    Todo(user_id=1, title="Walk the dog", is_complete=True),
    Todo(user_id=1, title="Read a book", is_complete=False),
    Todo(user_id=2, title="Finish project", is_complete=False),
    Todo(user_id=2, title="Call mom", is_complete=True),
]
```

**Expected Behavior**:
- Alice (user_id=1) sees 3 todos
- Bob (user_id=2) sees 2 todos
- Neither user sees the other's todos

---

## Database Connection Configuration

### Development (SQLite)
```python
DATABASE_URL = "sqlite:///./data/todo_dev.db"
```

### Production (Neon PostgreSQL)
```python
DATABASE_URL = os.getenv("DATABASE_URL")
# Example: postgresql://user:pass@ep-xxx.us-east-2.aws.neon.tech/neondb
```

### Connection Pool Settings (Production)
```python
engine = create_engine(
    DATABASE_URL,
    pool_size=10,         # Max connections in pool
    max_overflow=20,      # Max additional connections
    pool_pre_ping=True,   # Verify connection before use
    echo=False            # Set True to log SQL queries
)
```

---

*End of Data Model Document*
