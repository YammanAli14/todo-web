# Phase I Specification — Foundation

**Document ID:** SPEC-PHASE-I-001
**Version:** 1.0.0
**Status:** Draft — Pending Approval
**Governing Document:** [CONSTITUTION.md](../CONSTITUTION.md)
**Phase:** I — Foundation

---

## 1. Overview

### 1.1 Purpose

This specification defines the requirements for Phase I of the Evolution of Todo project: a minimal, in-memory, console-based task management application.

### 1.2 Scope Summary

Phase I delivers a Python console application that allows a single user to manage tasks during a single runtime session. All data exists only in memory and is lost when the application terminates.

### 1.3 Constitutional Compliance

This specification complies with:

- **Article I** — Defines scope, requirements, interfaces, acceptance criteria, and dependencies
- **Article III, Section 3.2** — Contains no forward leakage to future phases
- **Article IV** — Uses only Python 3.11+ as required
- **Article V** — Adheres to clean architecture and quality principles

---

## 2. Scope Definition

### 2.1 In Scope

| Item | Description |
|------|-------------|
| Runtime Environment | Python 3.11+ console application |
| Storage | In-memory only (Python data structures) |
| User Model | Single user, no authentication |
| Interface | Text-based menu-driven CLI |
| Features | Add, View, Update, Delete, Toggle Complete |

### 2.2 Explicitly Out of Scope

The following are **prohibited** in Phase I:

| Excluded Item | Reason |
|---------------|--------|
| Database (SQLite, PostgreSQL, etc.) | Phase II+ feature |
| File persistence (JSON, CSV, etc.) | Phase II+ feature |
| User authentication | Phase IV feature |
| Web API / REST endpoints | Phase II+ feature |
| Multiple users | Phase IV+ feature |
| Task categories/tags | Not in Phase I requirements |
| Task priorities | Not in Phase I requirements |
| Due dates | Not in Phase I requirements |
| Search/filter functionality | Not in Phase I requirements |
| Sorting options | Not in Phase I requirements |
| Subtasks | Not in Phase I requirements |
| Any external dependencies | Minimal Phase I scope |

---

## 3. User Stories

### 3.1 US-001: Add Task

**As a** user
**I want to** add a new task with a title
**So that** I can track something I need to do

**Acceptance Criteria:**

| ID | Criterion |
|----|-----------|
| AC-001-1 | User can enter a task title via the CLI |
| AC-001-2 | System assigns a unique numeric ID to the task |
| AC-001-3 | Task is created with status "incomplete" |
| AC-001-4 | System confirms task creation with ID and title |
| AC-001-5 | Empty title is rejected with error message |
| AC-001-6 | Whitespace-only title is rejected with error message |

### 3.2 US-002: View Task List

**As a** user
**I want to** see all my tasks
**So that** I can review what I need to do

**Acceptance Criteria:**

| ID | Criterion |
|----|-----------|
| AC-002-1 | User can request to view all tasks |
| AC-002-2 | System displays all tasks with ID, title, and status |
| AC-002-3 | Status shows as "[X]" for complete, "[ ]" for incomplete |
| AC-002-4 | Tasks are displayed in creation order (by ID) |
| AC-002-5 | If no tasks exist, system displays "No tasks found" message |

### 3.3 US-003: Update Task

**As a** user
**I want to** change a task's title
**So that** I can correct or clarify what needs to be done

**Acceptance Criteria:**

| ID | Criterion |
|----|-----------|
| AC-003-1 | User can specify a task ID to update |
| AC-003-2 | User can enter a new title for the task |
| AC-003-3 | System updates the task and confirms the change |
| AC-003-4 | Invalid ID (non-existent) shows error message |
| AC-003-5 | Invalid ID (non-numeric) shows error message |
| AC-003-6 | Empty new title is rejected with error message |
| AC-003-7 | Whitespace-only new title is rejected with error message |

### 3.4 US-004: Delete Task

**As a** user
**I want to** remove a task
**So that** I can clean up tasks I no longer need

**Acceptance Criteria:**

| ID | Criterion |
|----|-----------|
| AC-004-1 | User can specify a task ID to delete |
| AC-004-2 | System removes the task from memory |
| AC-004-3 | System confirms deletion with task details |
| AC-004-4 | Invalid ID (non-existent) shows error message |
| AC-004-5 | Invalid ID (non-numeric) shows error message |

### 3.5 US-005: Mark Task Complete/Incomplete

**As a** user
**I want to** toggle a task's completion status
**So that** I can track my progress

**Acceptance Criteria:**

| ID | Criterion |
|----|-----------|
| AC-005-1 | User can specify a task ID to toggle |
| AC-005-2 | If task is incomplete, it becomes complete |
| AC-005-3 | If task is complete, it becomes incomplete |
| AC-005-4 | System confirms the new status |
| AC-005-5 | Invalid ID (non-existent) shows error message |
| AC-005-6 | Invalid ID (non-numeric) shows error message |

### 3.6 US-006: Exit Application

**As a** user
**I want to** exit the application
**So that** I can end my session

**Acceptance Criteria:**

| ID | Criterion |
|----|-----------|
| AC-006-1 | User can choose to exit from the main menu |
| AC-006-2 | System displays a farewell message |
| AC-006-3 | Application terminates cleanly |

---

## 4. Data Model

### 4.1 Task Entity

The Task entity is the sole domain object in Phase I.

```
Task
├── id: int           # Unique identifier, auto-assigned
├── title: str        # Task description, required, non-empty
└── is_complete: bool # Completion status, default False
```

### 4.2 Field Specifications

| Field | Type | Constraints | Default |
|-------|------|-------------|---------|
| `id` | `int` | Positive integer, unique, auto-incremented | Auto-assigned |
| `title` | `str` | Non-empty, non-whitespace-only, max 200 chars | Required |
| `is_complete` | `bool` | True or False | `False` |

### 4.3 Data Storage

| Aspect | Specification |
|--------|---------------|
| Storage Type | Python list in memory |
| Persistence | None — data lost on exit |
| ID Generation | Sequential counter starting at 1 |
| Ordering | Maintained by insertion order |

---

## 5. CLI Interface Specification

### 5.1 Main Menu

The application presents a numbered menu upon startup and after each operation.

```
========================================
          TODO APPLICATION
========================================

1. Add Task
2. View Tasks
3. Update Task
4. Delete Task
5. Toggle Complete
6. Exit

Enter your choice (1-6):
```

### 5.2 Input/Output Flows

#### 5.2.1 Add Task Flow

```
Enter your choice (1-6): 1

--- Add Task ---
Enter task title: Buy groceries

Task added successfully!
ID: 1
Title: Buy groceries
Status: Incomplete
```

**Error Case — Empty Title:**
```
Enter your choice (1-6): 1

--- Add Task ---
Enter task title:

Error: Task title cannot be empty.
```

#### 5.2.2 View Tasks Flow

**With Tasks:**
```
Enter your choice (1-6): 2

--- Task List ---
[ ] 1. Buy groceries
[X] 2. Call dentist
[ ] 3. Finish report

Total: 3 tasks (1 complete, 2 incomplete)
```

**Empty List:**
```
Enter your choice (1-6): 2

--- Task List ---
No tasks found.
```

#### 5.2.3 Update Task Flow

```
Enter your choice (1-6): 3

--- Update Task ---
Enter task ID: 1
Enter new title: Buy groceries and milk

Task updated successfully!
ID: 1
New Title: Buy groceries and milk
```

**Error Case — Invalid ID:**
```
Enter your choice (1-6): 3

--- Update Task ---
Enter task ID: 99

Error: Task with ID 99 not found.
```

**Error Case — Non-Numeric ID:**
```
Enter your choice (1-6): 3

--- Update Task ---
Enter task ID: abc

Error: Invalid input. Please enter a numeric ID.
```

#### 5.2.4 Delete Task Flow

```
Enter your choice (1-6): 4

--- Delete Task ---
Enter task ID: 2

Task deleted successfully!
Deleted: "Call dentist"
```

**Error Case — Invalid ID:**
```
Enter your choice (1-6): 4

--- Delete Task ---
Enter task ID: 99

Error: Task with ID 99 not found.
```

#### 5.2.5 Toggle Complete Flow

**Marking Complete:**
```
Enter your choice (1-6): 5

--- Toggle Complete ---
Enter task ID: 1

Task status updated!
ID: 1
Title: Buy groceries
Status: Complete
```

**Marking Incomplete:**
```
Enter your choice (1-6): 5

--- Toggle Complete ---
Enter task ID: 1

Task status updated!
ID: 1
Title: Buy groceries
Status: Incomplete
```

#### 5.2.6 Exit Flow

```
Enter your choice (1-6): 6

Thank you for using Todo Application. Goodbye!
```

### 5.3 Invalid Menu Choice

```
Enter your choice (1-6): 9

Error: Invalid choice. Please enter a number between 1 and 6.
```

```
Enter your choice (1-6): hello

Error: Invalid input. Please enter a number between 1 and 6.
```

---

## 6. Error Handling Specification

### 6.1 Error Types

| Error Code | Error Type | Trigger | Message |
|------------|------------|---------|---------|
| E001 | Empty Title | Title is empty string | "Task title cannot be empty." |
| E002 | Whitespace Title | Title contains only whitespace | "Task title cannot be empty." |
| E003 | Title Too Long | Title exceeds 200 characters | "Task title must be 200 characters or less." |
| E004 | Task Not Found | ID does not exist | "Task with ID {id} not found." |
| E005 | Invalid ID Format | ID is not a valid integer | "Invalid input. Please enter a numeric ID." |
| E006 | Invalid Menu Choice | Choice outside 1-6 range | "Invalid choice. Please enter a number between 1 and 6." |
| E007 | Invalid Menu Input | Non-numeric menu input | "Invalid input. Please enter a number between 1 and 6." |

### 6.2 Error Behavior

1. All errors are displayed to the user immediately
2. After an error, the user returns to the main menu
3. No operation is partially completed — operations are atomic
4. Errors do not crash the application

---

## 7. Non-Functional Requirements

### 7.1 Performance

| Requirement | Specification |
|-------------|---------------|
| Response Time | All operations complete in < 100ms |
| Memory | Application uses < 50MB for up to 1000 tasks |
| Startup Time | Application starts in < 1 second |

### 7.2 Usability

| Requirement | Specification |
|-------------|---------------|
| Menu Clarity | All options clearly numbered and labeled |
| Feedback | Every action provides confirmation or error |
| Navigation | User always returns to main menu after operation |

### 7.3 Reliability

| Requirement | Specification |
|-------------|---------------|
| Crash Recovery | Invalid input does not crash application |
| Data Integrity | Operations are atomic — no partial states |

### 7.4 Code Quality

Per Constitution Article V, Section 5.4:

| Requirement | Specification |
|-------------|---------------|
| Type Hints | All function signatures must be typed |
| Documentation | Public functions must have docstrings |
| Testing | Minimum 80% code coverage |
| Linting | Must pass ruff |
| Formatting | Must pass black |

---

## 8. Technical Constraints

### 8.1 Language and Runtime

| Constraint | Value |
|------------|-------|
| Language | Python |
| Minimum Version | 3.11 |
| External Dependencies | None (standard library only) |

### 8.2 Prohibited Technologies

The following are explicitly prohibited in Phase I:

- SQLite or any database
- File I/O for data persistence
- JSON/YAML/CSV serialization for storage
- HTTP/networking libraries
- External packages (pip dependencies)
- Async/await patterns
- Threading/multiprocessing

### 8.3 Project Structure

Per Constitution Article V, Section 5.2, adapted for Phase I:

```
todo_app/
├── src/
│   ├── __init__.py
│   ├── domain/
│   │   ├── __init__.py
│   │   └── task.py          # Task entity
│   ├── application/
│   │   ├── __init__.py
│   │   └── task_service.py  # Business logic
│   ├── infrastructure/
│   │   ├── __init__.py
│   │   └── task_repository.py  # In-memory storage
│   └── presentation/
│       ├── __init__.py
│       └── cli.py           # Menu and user interaction
├── tests/
│   ├── __init__.py
│   ├── unit/
│   │   ├── __init__.py
│   │   ├── test_task.py
│   │   └── test_task_service.py
│   └── integration/
│       ├── __init__.py
│       └── test_cli.py
├── main.py                  # Application entry point
└── README.md
```

---

## 9. Dependencies

### 9.1 Prerequisites

| Dependency | Requirement |
|------------|-------------|
| Python | 3.11 or higher installed |
| Terminal | Any terminal/console that supports text I/O |

### 9.2 External Dependencies

**None.** Phase I uses only Python standard library.

---

## 10. Acceptance Criteria Summary

### 10.1 Feature Completion Checklist

| Feature | Criteria Count | Required Pass |
|---------|----------------|---------------|
| Add Task | 6 | All |
| View Tasks | 5 | All |
| Update Task | 7 | All |
| Delete Task | 5 | All |
| Toggle Complete | 6 | All |
| Exit | 3 | All |
| **Total** | **32** | **All** |

### 10.2 Quality Checklist

| Quality Requirement | Pass Criteria |
|---------------------|---------------|
| Type Hints | All functions typed |
| Documentation | All public APIs documented |
| Test Coverage | >= 80% on business logic |
| Linting | Zero ruff errors |
| Formatting | Zero black changes |

### 10.3 Phase Completion Criteria

Phase I is complete when:

1. All 32 acceptance criteria pass
2. All quality requirements met
3. All tests pass
4. README documentation complete
5. Human review approves deliverable

---

## 11. Glossary

| Term | Definition |
|------|------------|
| Task | A single item to be done, with ID, title, and completion status |
| Complete | A task marked as finished |
| Incomplete | A task not yet finished |
| Toggle | Switch a boolean value to its opposite |
| CLI | Command Line Interface |
| In-memory | Data stored in RAM, not persisted to disk |

---

## 12. Document Control

### 12.1 Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2025-12-28 | Agent | Initial specification |

### 12.2 Approval

| Role | Name | Date | Status |
|------|------|------|--------|
| Specification Author | Agent | 2025-12-28 | Draft |
| Human Reviewer | — | — | Pending |

---

## 13. References

- [CONSTITUTION.md](../CONSTITUTION.md) — Global project constitution

---

*End of Phase I Specification*
