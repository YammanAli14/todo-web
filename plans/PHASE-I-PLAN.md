# Phase I Technical Plan — Foundation

**Document ID:** PLAN-PHASE-I-001
**Version:** 1.0.0
**Status:** Draft — Pending Approval
**Specification Reference:** [PHASE-I-SPEC.md](../specs/PHASE-I-SPEC.md)
**Constitution Reference:** [CONSTITUTION.md](../CONSTITUTION.md)

---

## 1. Plan Overview

### 1.1 Purpose

This plan describes HOW the Phase I specification will be implemented. It does not introduce new features or modify requirements — it only details the technical approach to fulfill the approved specification.

### 1.2 Scope

This plan covers:

- Application structure and file organization
- In-memory data storage implementation
- ID generation mechanism
- CLI control flow design
- Separation of responsibilities across layers
- Error handling implementation

### 1.3 Constitutional Compliance

Per Constitution Article I, Section 1.4, this plan:

1. References the approved specification (SPEC-PHASE-I-001)
2. Breaks work into discrete, verifiable tasks
3. Defines the order of execution
4. Identifies files to be created
5. Specifies the testing approach

---

## 2. Application Structure

### 2.1 Project Layout

Per specification Section 8.3, the following files will be created:

```
todo_app/
├── src/
│   ├── __init__.py
│   ├── domain/
│   │   ├── __init__.py
│   │   └── task.py
│   ├── application/
│   │   ├── __init__.py
│   │   └── task_service.py
│   ├── infrastructure/
│   │   ├── __init__.py
│   │   └── task_repository.py
│   └── presentation/
│       ├── __init__.py
│       └── cli.py
├── tests/
│   ├── __init__.py
│   ├── unit/
│   │   ├── __init__.py
│   │   ├── test_task.py
│   │   └── test_task_service.py
│   └── integration/
│       ├── __init__.py
│       └── test_cli.py
├── main.py
└── README.md
```

### 2.2 Layer Responsibilities

| Layer | Directory | Responsibility | Dependencies |
|-------|-----------|----------------|--------------|
| Domain | `src/domain/` | Task entity definition, validation rules | None |
| Application | `src/application/` | Business logic, use case orchestration | Domain |
| Infrastructure | `src/infrastructure/` | In-memory storage implementation | Domain |
| Presentation | `src/presentation/` | CLI menu, user input/output | Application |

### 2.3 Dependency Flow

```
Presentation (cli.py)
       │
       ▼
Application (task_service.py)
       │
       ▼
Infrastructure (task_repository.py)
       │
       ▼
Domain (task.py)
```

The domain layer has no dependencies. Each layer depends only on layers below it.

---

## 3. In-Memory Data Storage

### 3.1 Storage Design

The `TaskRepository` class in `infrastructure/task_repository.py` will manage task storage.

**Data Structures:**

| Structure | Type | Purpose |
|-----------|------|---------|
| `_tasks` | `dict[int, Task]` | Maps task ID to Task object |
| `_next_id` | `int` | Counter for ID generation, starts at 1 |

**Rationale:**

- Dictionary provides O(1) lookup by ID for get, update, delete operations
- Maintains insertion order (Python 3.7+ dict behavior) for listing
- Integer counter ensures unique, sequential IDs per spec Section 4.3

### 3.2 Repository Interface

```python
class TaskRepository:
    def add(self, task: Task) -> Task
    def get_by_id(self, task_id: int) -> Task | None
    def get_all(self) -> list[Task]
    def update(self, task: Task) -> Task | None
    def delete(self, task_id: int) -> Task | None
    def get_next_id(self) -> int
```

### 3.3 Storage Lifecycle

| Event | Behavior |
|-------|----------|
| Application Start | Empty dictionary, counter = 1 |
| Add Task | Assign next ID, store task, increment counter |
| Application Exit | All data discarded (in-memory only) |

---

## 4. Task ID Generation

### 4.1 Strategy

Per specification Section 4.3:

- Sequential integer counter starting at 1
- Counter increments after each task creation
- IDs are never reused within a session

### 4.2 Implementation

```python
class TaskRepository:
    def __init__(self) -> None:
        self._tasks: dict[int, Task] = {}
        self._next_id: int = 1

    def get_next_id(self) -> int:
        current_id = self._next_id
        self._next_id += 1
        return current_id
```

### 4.3 ID Assignment Flow

1. Service requests new ID from repository
2. Repository returns current `_next_id` value
3. Repository increments `_next_id`
4. Service creates Task with assigned ID
5. Service stores Task via repository

---

## 5. CLI Control Flow

### 5.1 Main Loop Design

The CLI runs an infinite loop until the user chooses to exit.

```
┌─────────────────────────────────────┐
│           Application Start          │
└─────────────────┬───────────────────┘
                  │
                  ▼
┌─────────────────────────────────────┐
│         Display Main Menu            │
└─────────────────┬───────────────────┘
                  │
                  ▼
┌─────────────────────────────────────┐
│         Get User Choice              │
└─────────────────┬───────────────────┘
                  │
                  ▼
┌─────────────────────────────────────┐
│         Validate Choice              │
│   (numeric? in range 1-6?)          │
└─────────────────┬───────────────────┘
                  │
        ┌─────────┴─────────┐
        │ Invalid           │ Valid
        ▼                   ▼
┌───────────────┐   ┌───────────────────┐
│ Display Error │   │ Route to Handler   │
└───────┬───────┘   └─────────┬─────────┘
        │                     │
        │           ┌─────────┴─────────┐
        │           │ Choice = 6?       │
        │           │ (Exit)            │
        │           └─────────┬─────────┘
        │                     │
        │           ┌─────────┴─────────┐
        │           │ Yes               │ No
        │           ▼                   ▼
        │   ┌───────────────┐   ┌───────────────┐
        │   │ Display       │   │ Execute       │
        │   │ Farewell      │   │ Operation     │
        │   │ Exit Program  │   │ Display       │
        │   └───────────────┘   │ Result        │
        │                       └───────┬───────┘
        │                               │
        └───────────────────────────────┘
                  │
                  ▼
          (Return to Display Main Menu)
```

### 5.2 Menu Routing

| Choice | Handler Function | Spec Reference |
|--------|------------------|----------------|
| 1 | `handle_add_task()` | US-001 |
| 2 | `handle_view_tasks()` | US-002 |
| 3 | `handle_update_task()` | US-003 |
| 4 | `handle_delete_task()` | US-004 |
| 5 | `handle_toggle_complete()` | US-005 |
| 6 | `handle_exit()` | US-006 |

### 5.3 Input Handling

All user input is handled via Python's built-in `input()` function.

**Input Processing Steps:**

1. Prompt user with appropriate message
2. Read raw string input
3. Validate input format (numeric where required)
4. Validate input value (range, non-empty)
5. Return validated value or display error

### 5.4 Output Formatting

Per specification Section 5, all output follows exact formats:

| Output Type | Implementation |
|-------------|----------------|
| Menu Header | `print()` with `=` separators |
| Section Headers | `print()` with `---` prefix |
| Task Display | `[X]` or `[ ]` prefix format |
| Success Messages | Confirmation with task details |
| Error Messages | `Error:` prefix |

---

## 6. Separation of Responsibilities

### 6.1 Domain Layer (`src/domain/task.py`)

**Responsibilities:**

- Define Task dataclass with fields: id, title, is_complete
- Implement title validation logic
- Provide toggle method for completion status

**Does NOT:**

- Know about storage
- Know about CLI
- Handle user input

**Implementation:**

```python
@dataclass
class Task:
    id: int
    title: str
    is_complete: bool = False

    @staticmethod
    def validate_title(title: str) -> str:
        """Validate and return stripped title, or raise ValueError."""
        ...

    def toggle_complete(self) -> None:
        """Toggle the is_complete status."""
        ...
```

### 6.2 Infrastructure Layer (`src/infrastructure/task_repository.py`)

**Responsibilities:**

- Store tasks in memory
- Generate unique IDs
- Provide CRUD operations
- Maintain task collection

**Does NOT:**

- Validate business rules
- Format output
- Handle user interaction

**Implementation:**

```python
class TaskRepository:
    def __init__(self) -> None:
        self._tasks: dict[int, Task] = {}
        self._next_id: int = 1

    def add(self, task: Task) -> Task: ...
    def get_by_id(self, task_id: int) -> Task | None: ...
    def get_all(self) -> list[Task]: ...
    def update(self, task: Task) -> Task | None: ...
    def delete(self, task_id: int) -> Task | None: ...
    def get_next_id(self) -> int: ...
```

### 6.3 Application Layer (`src/application/task_service.py`)

**Responsibilities:**

- Orchestrate use cases
- Coordinate between repository and domain
- Apply business logic
- Return operation results

**Does NOT:**

- Store data directly
- Handle user I/O
- Format CLI output

**Implementation:**

```python
class TaskService:
    def __init__(self, repository: TaskRepository) -> None:
        self._repository = repository

    def add_task(self, title: str) -> Task: ...
    def get_all_tasks(self) -> list[Task]: ...
    def get_task(self, task_id: int) -> Task | None: ...
    def update_task(self, task_id: int, new_title: str) -> Task | None: ...
    def delete_task(self, task_id: int) -> Task | None: ...
    def toggle_task_complete(self, task_id: int) -> Task | None: ...
```

### 6.4 Presentation Layer (`src/presentation/cli.py`)

**Responsibilities:**

- Display menus and prompts
- Read user input
- Parse and validate input format
- Format and display output
- Route to appropriate handlers

**Does NOT:**

- Store data
- Implement business logic
- Validate business rules (only input format)

**Implementation:**

```python
class TodoCLI:
    def __init__(self, service: TaskService) -> None:
        self._service = service

    def run(self) -> None: ...
    def display_menu(self) -> None: ...
    def get_menu_choice(self) -> int | None: ...
    def handle_add_task(self) -> None: ...
    def handle_view_tasks(self) -> None: ...
    def handle_update_task(self) -> None: ...
    def handle_delete_task(self) -> None: ...
    def handle_toggle_complete(self) -> None: ...
    def handle_exit(self) -> None: ...
```

### 6.5 Entry Point (`main.py`)

**Responsibilities:**

- Bootstrap the application
- Wire dependencies together
- Start the CLI loop

**Implementation:**

```python
def main() -> None:
    repository = TaskRepository()
    service = TaskService(repository)
    cli = TodoCLI(service)
    cli.run()

if __name__ == "__main__":
    main()
```

---

## 7. Error Handling Strategy

### 7.1 Error Categories

Per specification Section 6.1:

| Category | Layer Handled | Error Codes |
|----------|---------------|-------------|
| Input Format Errors | Presentation | E005, E006, E007 |
| Validation Errors | Domain | E001, E002, E003 |
| Not Found Errors | Application | E004 |

### 7.2 Error Flow

```
User Input
    │
    ▼
┌─────────────────────────────────────┐
│ Presentation Layer                   │
│ - Validates input format             │
│ - Catches ValueError for non-numeric │
│ - Returns None for invalid format    │
└─────────────────┬───────────────────┘
                  │
                  ▼
┌─────────────────────────────────────┐
│ Application Layer                    │
│ - Checks if task exists              │
│ - Returns None if not found          │
│ - Delegates validation to domain     │
└─────────────────┬───────────────────┘
                  │
                  ▼
┌─────────────────────────────────────┐
│ Domain Layer                         │
│ - Validates title constraints        │
│ - Raises ValueError with message     │
└─────────────────────────────────────┘
```

### 7.3 Exception Strategy

| Exception Type | When Used | Caught By |
|----------------|-----------|-----------|
| `ValueError` | Invalid title (empty, whitespace, too long) | Presentation |
| Return `None` | Task not found | Presentation |
| No exception | Input format errors | Handled inline in Presentation |

### 7.4 Error Messages

All error messages match specification Section 6.1 exactly:

| Code | Message |
|------|---------|
| E001/E002 | "Task title cannot be empty." |
| E003 | "Task title must be 200 characters or less." |
| E004 | "Task with ID {id} not found." |
| E005 | "Invalid input. Please enter a numeric ID." |
| E006 | "Invalid choice. Please enter a number between 1 and 6." |
| E007 | "Invalid input. Please enter a number between 1 and 6." |

### 7.5 Error Recovery

Per specification Section 6.2:

- After any error, control returns to main menu
- No partial operations occur
- Application never crashes from user input

---

## 8. Testing Approach

### 8.1 Test Structure

```
tests/
├── __init__.py
├── unit/
│   ├── __init__.py
│   ├── test_task.py           # Domain tests
│   └── test_task_service.py   # Application tests
└── integration/
    ├── __init__.py
    └── test_cli.py            # End-to-end tests
```

### 8.2 Unit Tests

**Domain Tests (`test_task.py`):**

| Test Case | Validates |
|-----------|-----------|
| `test_task_creation` | Task created with correct fields |
| `test_task_default_incomplete` | New task is_complete = False |
| `test_validate_title_valid` | Valid title passes |
| `test_validate_title_empty` | Empty title raises ValueError |
| `test_validate_title_whitespace` | Whitespace title raises ValueError |
| `test_validate_title_too_long` | 201+ chars raises ValueError |
| `test_toggle_complete_to_complete` | False → True |
| `test_toggle_complete_to_incomplete` | True → False |

**Application Tests (`test_task_service.py`):**

| Test Case | Validates |
|-----------|-----------|
| `test_add_task` | Task added with correct ID |
| `test_add_task_increments_id` | Sequential IDs |
| `test_get_all_tasks_empty` | Returns empty list |
| `test_get_all_tasks_with_items` | Returns all tasks in order |
| `test_get_task_exists` | Returns correct task |
| `test_get_task_not_exists` | Returns None |
| `test_update_task_exists` | Updates title |
| `test_update_task_not_exists` | Returns None |
| `test_delete_task_exists` | Removes and returns task |
| `test_delete_task_not_exists` | Returns None |
| `test_toggle_task_exists` | Toggles status |
| `test_toggle_task_not_exists` | Returns None |

### 8.3 Integration Tests

**CLI Tests (`test_cli.py`):**

| Test Case | Validates |
|-----------|-----------|
| `test_add_task_flow` | Full add operation |
| `test_view_empty_list` | "No tasks found" message |
| `test_view_with_tasks` | Correct task list display |
| `test_update_task_flow` | Full update operation |
| `test_delete_task_flow` | Full delete operation |
| `test_toggle_task_flow` | Full toggle operation |
| `test_invalid_menu_choice` | Error message displayed |
| `test_invalid_task_id` | Error message displayed |

### 8.4 Test Execution

Tests will be run using `pytest` (standard library `unittest` compatible):

```bash
python -m pytest tests/ -v --cov=src --cov-report=term-missing
```

Coverage target: >= 80% per specification Section 7.4.

---

## 9. Implementation Tasks

### 9.1 Task Breakdown

Tasks are ordered for sequential execution. Each task is atomic and independently verifiable.

| Task ID | Task | Files | Depends On |
|---------|------|-------|------------|
| T-001 | Create project directory structure | All `__init__.py` files | — |
| T-002 | Implement Task entity | `src/domain/task.py` | T-001 |
| T-003 | Write Task unit tests | `tests/unit/test_task.py` | T-002 |
| T-004 | Implement TaskRepository | `src/infrastructure/task_repository.py` | T-002 |
| T-005 | Implement TaskService | `src/application/task_service.py` | T-004 |
| T-006 | Write TaskService unit tests | `tests/unit/test_task_service.py` | T-005 |
| T-007 | Implement TodoCLI | `src/presentation/cli.py` | T-005 |
| T-008 | Implement main entry point | `main.py` | T-007 |
| T-009 | Write CLI integration tests | `tests/integration/test_cli.py` | T-008 |
| T-010 | Create README | `README.md` | T-008 |
| T-011 | Final verification and cleanup | — | T-001–T-010 |

### 9.2 Task Details

#### T-001: Create Project Directory Structure

**Files to Create:**
- `todo_app/src/__init__.py`
- `todo_app/src/domain/__init__.py`
- `todo_app/src/application/__init__.py`
- `todo_app/src/infrastructure/__init__.py`
- `todo_app/src/presentation/__init__.py`
- `todo_app/tests/__init__.py`
- `todo_app/tests/unit/__init__.py`
- `todo_app/tests/integration/__init__.py`

**Completion Criteria:**
- All directories exist
- All `__init__.py` files present (can be empty)

#### T-002: Implement Task Entity

**File:** `src/domain/task.py`

**Implementation:**
- `Task` dataclass with id, title, is_complete
- `validate_title()` static method
- `toggle_complete()` method
- Type hints on all signatures
- Docstrings on public methods

**Completion Criteria:**
- Task can be instantiated
- Title validation works per spec
- Toggle method works correctly

#### T-003: Write Task Unit Tests

**File:** `tests/unit/test_task.py`

**Tests:**
- All domain test cases from Section 8.2

**Completion Criteria:**
- All tests pass
- >= 80% coverage on task.py

#### T-004: Implement TaskRepository

**File:** `src/infrastructure/task_repository.py`

**Implementation:**
- `TaskRepository` class
- In-memory dict storage
- ID generation
- CRUD methods
- Type hints and docstrings

**Completion Criteria:**
- All repository methods work correctly
- IDs are sequential starting at 1

#### T-005: Implement TaskService

**File:** `src/application/task_service.py`

**Implementation:**
- `TaskService` class
- Constructor accepting repository
- All use case methods
- Proper error handling
- Type hints and docstrings

**Completion Criteria:**
- All service methods work correctly
- Proper coordination with repository

#### T-006: Write TaskService Unit Tests

**File:** `tests/unit/test_task_service.py`

**Tests:**
- All application test cases from Section 8.2

**Completion Criteria:**
- All tests pass
- >= 80% coverage on task_service.py

#### T-007: Implement TodoCLI

**File:** `src/presentation/cli.py`

**Implementation:**
- `TodoCLI` class
- Main menu display per spec Section 5.1
- All handler methods
- Input validation
- Output formatting per spec Section 5.2
- Error display per spec Section 6.1
- Type hints and docstrings

**Completion Criteria:**
- Menu displays correctly
- All operations work per specification
- Errors handled gracefully

#### T-008: Implement Main Entry Point

**File:** `main.py`

**Implementation:**
- `main()` function
- Dependency wiring
- CLI startup
- `if __name__ == "__main__"` guard

**Completion Criteria:**
- Application runs with `python main.py`
- All features accessible

#### T-009: Write CLI Integration Tests

**File:** `tests/integration/test_cli.py`

**Tests:**
- All integration test cases from Section 8.3

**Completion Criteria:**
- All tests pass
- End-to-end flows verified

#### T-010: Create README

**File:** `README.md`

**Content:**
- Project description
- Requirements (Python 3.11+)
- Installation instructions
- Usage instructions
- Running tests

**Completion Criteria:**
- README is complete and accurate

#### T-011: Final Verification

**Actions:**
- Run all tests
- Verify >= 80% coverage
- Run ruff linting
- Run black formatting
- Manual verification of all 32 acceptance criteria

**Completion Criteria:**
- All tests pass
- Coverage >= 80%
- Zero linting errors
- Zero formatting issues
- All acceptance criteria verified

---

## 10. Verification Checklist

### 10.1 Specification Compliance

| Spec Section | Plan Coverage | Status |
|--------------|---------------|--------|
| 3. User Stories | Section 5.2, 6 | Covered |
| 4. Data Model | Section 3, 6.1 | Covered |
| 5. CLI Interface | Section 5 | Covered |
| 6. Error Handling | Section 7 | Covered |
| 7. Non-Functional | Section 8 | Covered |
| 8. Technical Constraints | Section 2, 3 | Covered |

### 10.2 Constitutional Compliance

| Article | Requirement | Compliance |
|---------|-------------|------------|
| I.1.4 | References approved spec | Yes |
| I.1.4 | Discrete verifiable tasks | Yes (Section 9) |
| I.1.4 | Order of execution | Yes (Section 9.1) |
| I.1.4 | Files identified | Yes (Section 2.1) |
| I.1.4 | Testing approach | Yes (Section 8) |
| V.5.1 | Clean architecture | Yes (Section 2.2, 6) |
| V.5.4 | Code quality standards | Yes (Section 8) |

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

- [PHASE-I-SPEC.md](../specs/PHASE-I-SPEC.md) — Phase I Specification
- [CONSTITUTION.md](../CONSTITUTION.md) — Global Constitution

---

*End of Phase I Technical Plan*
