# Phase I Implementation Tasks

**Document ID:** TASKS-PHASE-I-001
**Version:** 1.0.0
**Status:** Draft — Pending Approval
**Plan Reference:** [PHASE-I-PLAN.md](./PHASE-I-PLAN.md)
**Specification Reference:** [../specs/PHASE-I-SPEC.md](../specs/PHASE-I-SPEC.md)
**Constitution Reference:** [../CONSTITUTION.md](../CONSTITUTION.md)

---

## 1. Overview

This document contains the atomic implementation tasks for Phase I. Each task is:

- Small and testable
- Sequential (dependencies clearly stated)
- Traceable to specification and plan sections
- Sufficient to fully implement Phase I

**Total Tasks:** 25
**Estimated Files:** 17

---

## 2. Task Index

| ID | Category | Description |
|----|----------|-------------|
| TASK-001 | Setup | Create project root directory |
| TASK-002 | Setup | Create source directory structure |
| TASK-003 | Setup | Create test directory structure |
| TASK-004 | Setup | Create all `__init__.py` files |
| TASK-005 | Domain | Implement Task dataclass |
| TASK-006 | Domain | Implement title validation |
| TASK-007 | Domain | Implement toggle_complete method |
| TASK-008 | Domain | Write Task entity unit tests |
| TASK-009 | Infrastructure | Implement TaskRepository class skeleton |
| TASK-010 | Infrastructure | Implement ID generation |
| TASK-011 | Infrastructure | Implement add method |
| TASK-012 | Infrastructure | Implement get_by_id method |
| TASK-013 | Infrastructure | Implement get_all method |
| TASK-014 | Infrastructure | Implement update method |
| TASK-015 | Infrastructure | Implement delete method |
| TASK-016 | Application | Implement TaskService class with add_task |
| TASK-017 | Application | Implement get_all_tasks and get_task |
| TASK-018 | Application | Implement update_task |
| TASK-019 | Application | Implement delete_task |
| TASK-020 | Application | Implement toggle_task_complete |
| TASK-021 | Application | Write TaskService unit tests |
| TASK-022 | Presentation | Implement TodoCLI with menu display and main loop |
| TASK-023 | Presentation | Implement all CLI handlers |
| TASK-024 | Entry Point | Implement main.py |
| TASK-025 | Verification | Final testing and documentation |

---

## 3. Detailed Task Specifications

---

### TASK-001: Create Project Root Directory

**Category:** Setup
**Preconditions:** None
**Depends On:** None

**Description:**
Create the `todo_app` root directory that will contain all project files.

**Artifacts to Create:**
- `todo_app/` (directory)

**Expected Output:**
- Empty directory `todo_app` exists at project root

**Spec Reference:** Section 8.3 (Project Structure)
**Plan Reference:** Section 2.1 (Project Layout)

**Completion Criteria:**
- [ ] Directory `todo_app/` exists

---

### TASK-002: Create Source Directory Structure

**Category:** Setup
**Preconditions:** TASK-001 complete
**Depends On:** TASK-001

**Description:**
Create the `src` directory and all layer subdirectories per clean architecture.

**Artifacts to Create:**
- `todo_app/src/` (directory)
- `todo_app/src/domain/` (directory)
- `todo_app/src/application/` (directory)
- `todo_app/src/infrastructure/` (directory)
- `todo_app/src/presentation/` (directory)

**Expected Output:**
- All source directories exist with correct nesting

**Spec Reference:** Section 8.3 (Project Structure)
**Plan Reference:** Section 2.1 (Project Layout), Section 2.2 (Layer Responsibilities)

**Completion Criteria:**
- [ ] `todo_app/src/` exists
- [ ] `todo_app/src/domain/` exists
- [ ] `todo_app/src/application/` exists
- [ ] `todo_app/src/infrastructure/` exists
- [ ] `todo_app/src/presentation/` exists

---

### TASK-003: Create Test Directory Structure

**Category:** Setup
**Preconditions:** TASK-001 complete
**Depends On:** TASK-001

**Description:**
Create the `tests` directory with `unit` and `integration` subdirectories.

**Artifacts to Create:**
- `todo_app/tests/` (directory)
- `todo_app/tests/unit/` (directory)
- `todo_app/tests/integration/` (directory)

**Expected Output:**
- All test directories exist with correct nesting

**Spec Reference:** Section 8.3 (Project Structure)
**Plan Reference:** Section 8.1 (Test Structure)

**Completion Criteria:**
- [ ] `todo_app/tests/` exists
- [ ] `todo_app/tests/unit/` exists
- [ ] `todo_app/tests/integration/` exists

---

### TASK-004: Create All `__init__.py` Files

**Category:** Setup
**Preconditions:** TASK-002, TASK-003 complete
**Depends On:** TASK-002, TASK-003

**Description:**
Create empty `__init__.py` files in all directories to make them Python packages.

**Artifacts to Create:**
- `todo_app/src/__init__.py`
- `todo_app/src/domain/__init__.py`
- `todo_app/src/application/__init__.py`
- `todo_app/src/infrastructure/__init__.py`
- `todo_app/src/presentation/__init__.py`
- `todo_app/tests/__init__.py`
- `todo_app/tests/unit/__init__.py`
- `todo_app/tests/integration/__init__.py`

**Expected Output:**
- All `__init__.py` files exist (can be empty)

**Spec Reference:** Section 8.3 (Project Structure)
**Plan Reference:** Section 2.1 (Project Layout)

**Completion Criteria:**
- [ ] 8 `__init__.py` files created
- [ ] All directories are valid Python packages

---

### TASK-005: Implement Task Dataclass

**Category:** Domain
**Preconditions:** TASK-004 complete
**Depends On:** TASK-004

**Description:**
Create the Task entity as a Python dataclass with three fields: `id`, `title`, `is_complete`.

**Artifacts to Create:**
- `todo_app/src/domain/task.py`

**Implementation Details:**
```python
from dataclasses import dataclass

@dataclass
class Task:
    id: int
    title: str
    is_complete: bool = False
```

**Expected Output:**
- Task can be instantiated with `Task(id=1, title="Test")`
- Default `is_complete` is `False`
- All fields are accessible

**Spec Reference:** Section 4.1 (Task Entity), Section 4.2 (Field Specifications)
**Plan Reference:** Section 6.1 (Domain Layer)

**Completion Criteria:**
- [ ] `task.py` file exists
- [ ] Task dataclass defined with correct fields
- [ ] Type hints present on all fields
- [ ] Default value for `is_complete` is `False`

---

### TASK-006: Implement Title Validation

**Category:** Domain
**Preconditions:** TASK-005 complete
**Depends On:** TASK-005

**Description:**
Add static method `validate_title()` to Task class that validates title constraints.

**Artifacts to Modify:**
- `todo_app/src/domain/task.py`

**Implementation Details:**
```python
@staticmethod
def validate_title(title: str) -> str:
    """Validate and return stripped title, or raise ValueError.

    Args:
        title: The title to validate

    Returns:
        The stripped title if valid

    Raises:
        ValueError: If title is empty, whitespace-only, or > 200 chars
    """
    stripped = title.strip()
    if not stripped:
        raise ValueError("Task title cannot be empty.")
    if len(stripped) > 200:
        raise ValueError("Task title must be 200 characters or less.")
    return stripped
```

**Expected Output:**
- Valid titles return stripped string
- Empty string raises `ValueError` with message "Task title cannot be empty."
- Whitespace-only raises `ValueError` with message "Task title cannot be empty."
- >200 chars raises `ValueError` with message "Task title must be 200 characters or less."

**Spec Reference:** Section 4.2 (Field Specifications), Section 6.1 (Error Types E001, E002, E003)
**Plan Reference:** Section 6.1 (Domain Layer), Section 7.3 (Exception Strategy)

**Completion Criteria:**
- [ ] `validate_title()` method exists
- [ ] Returns stripped title for valid input
- [ ] Raises `ValueError` for empty title
- [ ] Raises `ValueError` for whitespace-only title
- [ ] Raises `ValueError` for title > 200 characters
- [ ] Error messages match specification exactly

---

### TASK-007: Implement toggle_complete Method

**Category:** Domain
**Preconditions:** TASK-005 complete
**Depends On:** TASK-005

**Description:**
Add `toggle_complete()` method to Task class that flips the `is_complete` status.

**Artifacts to Modify:**
- `todo_app/src/domain/task.py`

**Implementation Details:**
```python
def toggle_complete(self) -> None:
    """Toggle the is_complete status."""
    self.is_complete = not self.is_complete
```

**Expected Output:**
- `False` becomes `True`
- `True` becomes `False`

**Spec Reference:** Section 3.5 (US-005: AC-005-2, AC-005-3)
**Plan Reference:** Section 6.1 (Domain Layer)

**Completion Criteria:**
- [ ] `toggle_complete()` method exists
- [ ] Correctly toggles `False` to `True`
- [ ] Correctly toggles `True` to `False`
- [ ] Method has docstring

---

### TASK-008: Write Task Entity Unit Tests

**Category:** Domain
**Preconditions:** TASK-005, TASK-006, TASK-007 complete
**Depends On:** TASK-007

**Description:**
Create unit tests for the Task entity covering all functionality.

**Artifacts to Create:**
- `todo_app/tests/unit/test_task.py`

**Test Cases:**
| Test Function | Description |
|---------------|-------------|
| `test_task_creation` | Task created with correct fields |
| `test_task_default_incomplete` | New task `is_complete` = `False` |
| `test_validate_title_valid` | Valid title passes and is stripped |
| `test_validate_title_empty` | Empty title raises `ValueError` |
| `test_validate_title_whitespace` | Whitespace title raises `ValueError` |
| `test_validate_title_too_long` | 201+ chars raises `ValueError` |
| `test_validate_title_exactly_200` | 200 chars passes |
| `test_toggle_complete_to_complete` | `False` → `True` |
| `test_toggle_complete_to_incomplete` | `True` → `False` |

**Expected Output:**
- All 9 tests pass
- >= 80% coverage on `task.py`

**Spec Reference:** Section 7.4 (Code Quality - Testing)
**Plan Reference:** Section 8.2 (Domain Tests)

**Completion Criteria:**
- [ ] `test_task.py` file exists
- [ ] All 9 test cases implemented
- [ ] All tests pass
- [ ] Coverage >= 80% on `task.py`

---

### TASK-009: Implement TaskRepository Class Skeleton

**Category:** Infrastructure
**Preconditions:** TASK-005 complete
**Depends On:** TASK-005

**Description:**
Create TaskRepository class with constructor initializing in-memory storage.

**Artifacts to Create:**
- `todo_app/src/infrastructure/task_repository.py`

**Implementation Details:**
```python
from src.domain.task import Task

class TaskRepository:
    """In-memory repository for Task storage."""

    def __init__(self) -> None:
        """Initialize empty task storage with ID counter starting at 1."""
        self._tasks: dict[int, Task] = {}
        self._next_id: int = 1
```

**Expected Output:**
- TaskRepository can be instantiated
- `_tasks` is empty dict
- `_next_id` is 1

**Spec Reference:** Section 4.3 (Data Storage)
**Plan Reference:** Section 3.1 (Storage Design), Section 6.2 (Infrastructure Layer)

**Completion Criteria:**
- [ ] `task_repository.py` file exists
- [ ] `TaskRepository` class defined
- [ ] `_tasks` initialized as empty `dict[int, Task]`
- [ ] `_next_id` initialized to `1`
- [ ] Type hints present
- [ ] Docstring on class and `__init__`

---

### TASK-010: Implement ID Generation

**Category:** Infrastructure
**Preconditions:** TASK-009 complete
**Depends On:** TASK-009

**Description:**
Add `get_next_id()` method that returns current ID and increments counter.

**Artifacts to Modify:**
- `todo_app/src/infrastructure/task_repository.py`

**Implementation Details:**
```python
def get_next_id(self) -> int:
    """Get the next available task ID and increment counter.

    Returns:
        The next unique task ID
    """
    current_id = self._next_id
    self._next_id += 1
    return current_id
```

**Expected Output:**
- First call returns `1`
- Second call returns `2`
- Counter increments after each call

**Spec Reference:** Section 4.3 (ID Generation - Sequential counter starting at 1)
**Plan Reference:** Section 4 (Task ID Generation)

**Completion Criteria:**
- [ ] `get_next_id()` method exists
- [ ] Returns sequential IDs starting at 1
- [ ] Increments counter after returning
- [ ] Type hint and docstring present

---

### TASK-011: Implement add Method

**Category:** Infrastructure
**Preconditions:** TASK-010 complete
**Depends On:** TASK-010

**Description:**
Add `add()` method that stores a task in the dictionary.

**Artifacts to Modify:**
- `todo_app/src/infrastructure/task_repository.py`

**Implementation Details:**
```python
def add(self, task: Task) -> Task:
    """Add a task to storage.

    Args:
        task: The task to store

    Returns:
        The stored task
    """
    self._tasks[task.id] = task
    return task
```

**Expected Output:**
- Task is stored in `_tasks` dict
- Task is retrievable by ID
- Returns the stored task

**Spec Reference:** Section 3.1 (US-001: Add Task)
**Plan Reference:** Section 3.2 (Repository Interface)

**Completion Criteria:**
- [ ] `add()` method exists
- [ ] Task stored in `_tasks` by ID
- [ ] Returns the stored task
- [ ] Type hints and docstring present

---

### TASK-012: Implement get_by_id Method

**Category:** Infrastructure
**Preconditions:** TASK-011 complete
**Depends On:** TASK-011

**Description:**
Add `get_by_id()` method that retrieves a task by ID or returns None.

**Artifacts to Modify:**
- `todo_app/src/infrastructure/task_repository.py`

**Implementation Details:**
```python
def get_by_id(self, task_id: int) -> Task | None:
    """Get a task by ID.

    Args:
        task_id: The ID of the task to retrieve

    Returns:
        The task if found, None otherwise
    """
    return self._tasks.get(task_id)
```

**Expected Output:**
- Returns task if ID exists
- Returns `None` if ID does not exist

**Spec Reference:** Section 3.3 (US-003: AC-003-4), Section 3.4 (US-004: AC-004-4)
**Plan Reference:** Section 3.2 (Repository Interface)

**Completion Criteria:**
- [ ] `get_by_id()` method exists
- [ ] Returns task for valid ID
- [ ] Returns `None` for invalid ID
- [ ] Type hints and docstring present

---

### TASK-013: Implement get_all Method

**Category:** Infrastructure
**Preconditions:** TASK-011 complete
**Depends On:** TASK-011

**Description:**
Add `get_all()` method that returns all tasks in insertion order.

**Artifacts to Modify:**
- `todo_app/src/infrastructure/task_repository.py`

**Implementation Details:**
```python
def get_all(self) -> list[Task]:
    """Get all tasks in insertion order.

    Returns:
        List of all tasks, ordered by insertion (ID order)
    """
    return list(self._tasks.values())
```

**Expected Output:**
- Returns empty list if no tasks
- Returns all tasks in insertion order
- Order matches ID order (Python 3.7+ dict behavior)

**Spec Reference:** Section 3.2 (US-002: AC-002-4 - Tasks displayed in creation order)
**Plan Reference:** Section 3.1 (Storage Design - maintains insertion order)

**Completion Criteria:**
- [ ] `get_all()` method exists
- [ ] Returns empty list when no tasks
- [ ] Returns tasks in insertion order
- [ ] Type hints and docstring present

---

### TASK-014: Implement update Method

**Category:** Infrastructure
**Preconditions:** TASK-012 complete
**Depends On:** TASK-012

**Description:**
Add `update()` method that updates a task if it exists.

**Artifacts to Modify:**
- `todo_app/src/infrastructure/task_repository.py`

**Implementation Details:**
```python
def update(self, task: Task) -> Task | None:
    """Update an existing task.

    Args:
        task: The task with updated values

    Returns:
        The updated task if found, None if task ID doesn't exist
    """
    if task.id not in self._tasks:
        return None
    self._tasks[task.id] = task
    return task
```

**Expected Output:**
- Updates task in storage if ID exists
- Returns updated task
- Returns `None` if ID does not exist

**Spec Reference:** Section 3.3 (US-003: Update Task)
**Plan Reference:** Section 3.2 (Repository Interface)

**Completion Criteria:**
- [ ] `update()` method exists
- [ ] Updates task for valid ID
- [ ] Returns `None` for invalid ID
- [ ] Type hints and docstring present

---

### TASK-015: Implement delete Method

**Category:** Infrastructure
**Preconditions:** TASK-012 complete
**Depends On:** TASK-012

**Description:**
Add `delete()` method that removes a task if it exists.

**Artifacts to Modify:**
- `todo_app/src/infrastructure/task_repository.py`

**Implementation Details:**
```python
def delete(self, task_id: int) -> Task | None:
    """Delete a task by ID.

    Args:
        task_id: The ID of the task to delete

    Returns:
        The deleted task if found, None otherwise
    """
    return self._tasks.pop(task_id, None)
```

**Expected Output:**
- Removes task from storage if ID exists
- Returns deleted task
- Returns `None` if ID does not exist

**Spec Reference:** Section 3.4 (US-004: AC-004-2 - System removes task from memory)
**Plan Reference:** Section 3.2 (Repository Interface)

**Completion Criteria:**
- [ ] `delete()` method exists
- [ ] Removes task for valid ID
- [ ] Returns deleted task
- [ ] Returns `None` for invalid ID
- [ ] Type hints and docstring present

---

### TASK-016: Implement TaskService Class with add_task

**Category:** Application
**Preconditions:** TASK-015 complete
**Depends On:** TASK-015

**Description:**
Create TaskService class with constructor and `add_task()` method.

**Artifacts to Create:**
- `todo_app/src/application/task_service.py`

**Implementation Details:**
```python
from src.domain.task import Task
from src.infrastructure.task_repository import TaskRepository

class TaskService:
    """Service layer for task operations."""

    def __init__(self, repository: TaskRepository) -> None:
        """Initialize service with repository.

        Args:
            repository: The task repository for storage
        """
        self._repository = repository

    def add_task(self, title: str) -> Task:
        """Add a new task.

        Args:
            title: The task title (will be validated)

        Returns:
            The created task

        Raises:
            ValueError: If title is invalid
        """
        validated_title = Task.validate_title(title)
        task_id = self._repository.get_next_id()
        task = Task(id=task_id, title=validated_title)
        return self._repository.add(task)
```

**Expected Output:**
- TaskService can be instantiated with repository
- `add_task()` validates title, generates ID, creates task, stores it
- Returns created task with sequential ID
- Raises `ValueError` for invalid title

**Spec Reference:** Section 3.1 (US-001: AC-001-1 through AC-001-6)
**Plan Reference:** Section 6.3 (Application Layer)

**Completion Criteria:**
- [ ] `task_service.py` file exists
- [ ] `TaskService` class defined
- [ ] Constructor accepts repository
- [ ] `add_task()` validates title via domain
- [ ] `add_task()` generates sequential ID
- [ ] `add_task()` stores and returns task
- [ ] Type hints and docstrings present

---

### TASK-017: Implement get_all_tasks and get_task

**Category:** Application
**Preconditions:** TASK-016 complete
**Depends On:** TASK-016

**Description:**
Add `get_all_tasks()` and `get_task()` methods to TaskService.

**Artifacts to Modify:**
- `todo_app/src/application/task_service.py`

**Implementation Details:**
```python
def get_all_tasks(self) -> list[Task]:
    """Get all tasks.

    Returns:
        List of all tasks in creation order
    """
    return self._repository.get_all()

def get_task(self, task_id: int) -> Task | None:
    """Get a task by ID.

    Args:
        task_id: The ID of the task to retrieve

    Returns:
        The task if found, None otherwise
    """
    return self._repository.get_by_id(task_id)
```

**Expected Output:**
- `get_all_tasks()` returns all tasks
- `get_task()` returns task for valid ID
- `get_task()` returns `None` for invalid ID

**Spec Reference:** Section 3.2 (US-002: View Task List)
**Plan Reference:** Section 6.3 (Application Layer)

**Completion Criteria:**
- [ ] `get_all_tasks()` method exists
- [ ] `get_task()` method exists
- [ ] Both delegate to repository correctly
- [ ] Type hints and docstrings present

---

### TASK-018: Implement update_task

**Category:** Application
**Preconditions:** TASK-017 complete
**Depends On:** TASK-017

**Description:**
Add `update_task()` method to TaskService.

**Artifacts to Modify:**
- `todo_app/src/application/task_service.py`

**Implementation Details:**
```python
def update_task(self, task_id: int, new_title: str) -> Task | None:
    """Update a task's title.

    Args:
        task_id: The ID of the task to update
        new_title: The new title (will be validated)

    Returns:
        The updated task if found, None otherwise

    Raises:
        ValueError: If new_title is invalid
    """
    validated_title = Task.validate_title(new_title)
    task = self._repository.get_by_id(task_id)
    if task is None:
        return None
    task.title = validated_title
    return self._repository.update(task)
```

**Expected Output:**
- Validates new title first
- Returns `None` if task not found
- Updates title and returns task if found
- Raises `ValueError` for invalid title

**Spec Reference:** Section 3.3 (US-003: AC-003-1 through AC-003-7)
**Plan Reference:** Section 6.3 (Application Layer)

**Completion Criteria:**
- [ ] `update_task()` method exists
- [ ] Validates title before checking existence
- [ ] Returns `None` for non-existent task
- [ ] Updates and returns task for valid ID
- [ ] Type hints and docstring present

---

### TASK-019: Implement delete_task

**Category:** Application
**Preconditions:** TASK-017 complete
**Depends On:** TASK-017

**Description:**
Add `delete_task()` method to TaskService.

**Artifacts to Modify:**
- `todo_app/src/application/task_service.py`

**Implementation Details:**
```python
def delete_task(self, task_id: int) -> Task | None:
    """Delete a task.

    Args:
        task_id: The ID of the task to delete

    Returns:
        The deleted task if found, None otherwise
    """
    return self._repository.delete(task_id)
```

**Expected Output:**
- Deletes task if ID exists
- Returns deleted task
- Returns `None` if ID does not exist

**Spec Reference:** Section 3.4 (US-004: AC-004-1 through AC-004-5)
**Plan Reference:** Section 6.3 (Application Layer)

**Completion Criteria:**
- [ ] `delete_task()` method exists
- [ ] Delegates to repository
- [ ] Returns deleted task or `None`
- [ ] Type hints and docstring present

---

### TASK-020: Implement toggle_task_complete

**Category:** Application
**Preconditions:** TASK-017 complete
**Depends On:** TASK-017

**Description:**
Add `toggle_task_complete()` method to TaskService.

**Artifacts to Modify:**
- `todo_app/src/application/task_service.py`

**Implementation Details:**
```python
def toggle_task_complete(self, task_id: int) -> Task | None:
    """Toggle a task's completion status.

    Args:
        task_id: The ID of the task to toggle

    Returns:
        The updated task if found, None otherwise
    """
    task = self._repository.get_by_id(task_id)
    if task is None:
        return None
    task.toggle_complete()
    return self._repository.update(task)
```

**Expected Output:**
- Returns `None` if task not found
- Toggles status and returns task if found

**Spec Reference:** Section 3.5 (US-005: AC-005-1 through AC-005-6)
**Plan Reference:** Section 6.3 (Application Layer)

**Completion Criteria:**
- [ ] `toggle_task_complete()` method exists
- [ ] Returns `None` for non-existent task
- [ ] Toggles status via domain method
- [ ] Updates via repository
- [ ] Type hints and docstring present

---

### TASK-021: Write TaskService Unit Tests

**Category:** Application
**Preconditions:** TASK-020 complete
**Depends On:** TASK-020

**Description:**
Create unit tests for TaskService covering all methods.

**Artifacts to Create:**
- `todo_app/tests/unit/test_task_service.py`

**Test Cases:**
| Test Function | Description |
|---------------|-------------|
| `test_add_task` | Task added with correct ID and title |
| `test_add_task_increments_id` | Sequential IDs for multiple adds |
| `test_add_task_invalid_title` | Raises `ValueError` |
| `test_get_all_tasks_empty` | Returns empty list |
| `test_get_all_tasks_with_items` | Returns all tasks in order |
| `test_get_task_exists` | Returns correct task |
| `test_get_task_not_exists` | Returns `None` |
| `test_update_task_exists` | Updates title correctly |
| `test_update_task_not_exists` | Returns `None` |
| `test_update_task_invalid_title` | Raises `ValueError` |
| `test_delete_task_exists` | Removes and returns task |
| `test_delete_task_not_exists` | Returns `None` |
| `test_toggle_task_exists_to_complete` | Toggles `False` → `True` |
| `test_toggle_task_exists_to_incomplete` | Toggles `True` → `False` |
| `test_toggle_task_not_exists` | Returns `None` |

**Expected Output:**
- All 15 tests pass
- >= 80% coverage on `task_service.py`

**Spec Reference:** Section 7.4 (Code Quality - Testing)
**Plan Reference:** Section 8.2 (Application Tests)

**Completion Criteria:**
- [ ] `test_task_service.py` file exists
- [ ] All 15 test cases implemented
- [ ] All tests pass
- [ ] Coverage >= 80% on `task_service.py`

---

### TASK-022: Implement TodoCLI with Menu Display and Main Loop

**Category:** Presentation
**Preconditions:** TASK-020 complete
**Depends On:** TASK-020

**Description:**
Create TodoCLI class with menu display and main application loop.

**Artifacts to Create:**
- `todo_app/src/presentation/cli.py`

**Implementation Details:**
```python
from src.application.task_service import TaskService

class TodoCLI:
    """Command-line interface for the Todo application."""

    def __init__(self, service: TaskService) -> None:
        """Initialize CLI with task service."""
        self._service = service
        self._running = True

    def run(self) -> None:
        """Run the main application loop."""
        while self._running:
            self.display_menu()
            choice = self.get_menu_choice()
            if choice is not None:
                self._handle_choice(choice)

    def display_menu(self) -> None:
        """Display the main menu."""
        print()
        print("=" * 40)
        print("          TODO APPLICATION")
        print("=" * 40)
        print()
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Update Task")
        print("4. Delete Task")
        print("5. Toggle Complete")
        print("6. Exit")
        print()

    def get_menu_choice(self) -> int | None:
        """Get and validate menu choice from user."""
        try:
            choice_str = input("Enter your choice (1-6): ")
            choice = int(choice_str)
            if 1 <= choice <= 6:
                return choice
            print()
            print("Error: Invalid choice. Please enter a number between 1 and 6.")
            return None
        except ValueError:
            print()
            print("Error: Invalid input. Please enter a number between 1 and 6.")
            return None

    def _handle_choice(self, choice: int) -> None:
        """Route to appropriate handler."""
        handlers = {
            1: self.handle_add_task,
            2: self.handle_view_tasks,
            3: self.handle_update_task,
            4: self.handle_delete_task,
            5: self.handle_toggle_complete,
            6: self.handle_exit,
        }
        handlers[choice]()
```

**Expected Output:**
- Menu displays per spec Section 5.1
- Loop continues until exit chosen
- Invalid choices show correct error messages
- Valid choices route to handlers

**Spec Reference:** Section 5.1 (Main Menu), Section 5.3 (Invalid Menu Choice), Section 6.1 (E006, E007)
**Plan Reference:** Section 5 (CLI Control Flow), Section 6.4 (Presentation Layer)

**Completion Criteria:**
- [ ] `cli.py` file exists
- [ ] `TodoCLI` class defined
- [ ] `display_menu()` matches spec exactly
- [ ] `get_menu_choice()` validates numeric input
- [ ] `get_menu_choice()` validates range 1-6
- [ ] Error messages match spec exactly
- [ ] Main loop runs until exit
- [ ] Type hints and docstrings present

---

### TASK-023: Implement All CLI Handlers

**Category:** Presentation
**Preconditions:** TASK-022 complete
**Depends On:** TASK-022

**Description:**
Implement all handler methods for CLI operations.

**Artifacts to Modify:**
- `todo_app/src/presentation/cli.py`

**Implementation Details:**

```python
def _get_task_id(self, prompt: str) -> int | None:
    """Get and validate task ID from user."""
    try:
        id_str = input(prompt)
        return int(id_str)
    except ValueError:
        print()
        print("Error: Invalid input. Please enter a numeric ID.")
        return None

def handle_add_task(self) -> None:
    """Handle add task operation."""
    print()
    print("--- Add Task ---")
    title = input("Enter task title: ")
    try:
        task = self._service.add_task(title)
        print()
        print("Task added successfully!")
        print(f"ID: {task.id}")
        print(f"Title: {task.title}")
        print("Status: Incomplete")
    except ValueError as e:
        print()
        print(f"Error: {e}")

def handle_view_tasks(self) -> None:
    """Handle view tasks operation."""
    print()
    print("--- Task List ---")
    tasks = self._service.get_all_tasks()
    if not tasks:
        print("No tasks found.")
        return
    complete_count = 0
    for task in tasks:
        status = "[X]" if task.is_complete else "[ ]"
        if task.is_complete:
            complete_count += 1
        print(f"{status} {task.id}. {task.title}")
    incomplete_count = len(tasks) - complete_count
    print()
    print(f"Total: {len(tasks)} tasks ({complete_count} complete, {incomplete_count} incomplete)")

def handle_update_task(self) -> None:
    """Handle update task operation."""
    print()
    print("--- Update Task ---")
    task_id = self._get_task_id("Enter task ID: ")
    if task_id is None:
        return
    new_title = input("Enter new title: ")
    try:
        task = self._service.update_task(task_id, new_title)
        if task is None:
            print()
            print(f"Error: Task with ID {task_id} not found.")
            return
        print()
        print("Task updated successfully!")
        print(f"ID: {task.id}")
        print(f"New Title: {task.title}")
    except ValueError as e:
        print()
        print(f"Error: {e}")

def handle_delete_task(self) -> None:
    """Handle delete task operation."""
    print()
    print("--- Delete Task ---")
    task_id = self._get_task_id("Enter task ID: ")
    if task_id is None:
        return
    task = self._service.delete_task(task_id)
    if task is None:
        print()
        print(f"Error: Task with ID {task_id} not found.")
        return
    print()
    print("Task deleted successfully!")
    print(f'Deleted: "{task.title}"')

def handle_toggle_complete(self) -> None:
    """Handle toggle complete operation."""
    print()
    print("--- Toggle Complete ---")
    task_id = self._get_task_id("Enter task ID: ")
    if task_id is None:
        return
    task = self._service.toggle_task_complete(task_id)
    if task is None:
        print()
        print(f"Error: Task with ID {task_id} not found.")
        return
    status = "Complete" if task.is_complete else "Incomplete"
    print()
    print("Task status updated!")
    print(f"ID: {task.id}")
    print(f"Title: {task.title}")
    print(f"Status: {status}")

def handle_exit(self) -> None:
    """Handle exit operation."""
    print()
    print("Thank you for using Todo Application. Goodbye!")
    self._running = False
```

**Expected Output:**
- All handlers match spec Section 5.2 output formats exactly
- Error handling per spec Section 6.1
- ID validation shows E005 message for non-numeric
- Not found shows E004 message with ID
- Title validation shows E001/E002/E003 messages

**Spec Reference:** Section 5.2 (Input/Output Flows), Section 6.1 (Error Types)
**Plan Reference:** Section 5.2 (Menu Routing), Section 7 (Error Handling Strategy)

**Completion Criteria:**
- [ ] `handle_add_task()` implemented per spec
- [ ] `handle_view_tasks()` implemented per spec
- [ ] `handle_update_task()` implemented per spec
- [ ] `handle_delete_task()` implemented per spec
- [ ] `handle_toggle_complete()` implemented per spec
- [ ] `handle_exit()` implemented per spec
- [ ] All output formats match specification exactly
- [ ] All error messages match specification exactly
- [ ] Type hints and docstrings present

---

### TASK-024: Implement main.py

**Category:** Entry Point
**Preconditions:** TASK-023 complete
**Depends On:** TASK-023

**Description:**
Create the application entry point that wires dependencies and starts CLI.

**Artifacts to Create:**
- `todo_app/main.py`

**Implementation Details:**
```python
"""Todo Application - Phase I Entry Point."""

from src.infrastructure.task_repository import TaskRepository
from src.application.task_service import TaskService
from src.presentation.cli import TodoCLI


def main() -> None:
    """Bootstrap and run the Todo application."""
    repository = TaskRepository()
    service = TaskService(repository)
    cli = TodoCLI(service)
    cli.run()


if __name__ == "__main__":
    main()
```

**Expected Output:**
- Application runs with `python main.py`
- Dependencies wired correctly
- CLI loop starts
- All features accessible

**Spec Reference:** Section 8.3 (Project Structure - main.py)
**Plan Reference:** Section 6.5 (Entry Point)

**Completion Criteria:**
- [ ] `main.py` file exists
- [ ] `main()` function defined
- [ ] Dependencies wired: Repository → Service → CLI
- [ ] `if __name__ == "__main__"` guard present
- [ ] Application runs successfully
- [ ] Type hints and docstring present

---

### TASK-025: Final Testing and Documentation

**Category:** Verification
**Preconditions:** TASK-024 complete
**Depends On:** TASK-024

**Description:**
Create integration tests, README, and perform final verification.

**Artifacts to Create:**
- `todo_app/tests/integration/test_cli.py`
- `todo_app/README.md`

**Sub-tasks:**

#### 25a: Create Integration Tests

**Test Cases:**
| Test Function | Description |
|---------------|-------------|
| `test_add_task_flow` | Full add operation with valid input |
| `test_add_task_empty_title` | Error for empty title |
| `test_view_empty_list` | "No tasks found" message |
| `test_view_with_tasks` | Correct task list display |
| `test_update_task_flow` | Full update operation |
| `test_update_task_not_found` | Error for invalid ID |
| `test_delete_task_flow` | Full delete operation |
| `test_delete_task_not_found` | Error for invalid ID |
| `test_toggle_task_flow` | Full toggle operation |
| `test_invalid_menu_choice_out_of_range` | Error for choice outside 1-6 |
| `test_invalid_menu_choice_non_numeric` | Error for non-numeric input |
| `test_invalid_task_id_non_numeric` | Error for non-numeric task ID |

#### 25b: Create README

**Content:**
```markdown
# Todo Application - Phase I

A simple in-memory console todo application.

## Requirements

- Python 3.11 or higher

## Installation

No installation required. Clone and run.

## Usage

python main.py

## Features

- Add Task
- View Tasks
- Update Task
- Delete Task
- Toggle Complete/Incomplete

## Running Tests

python -m pytest tests/ -v

## Project Structure

[Include structure from spec Section 8.3]
```

#### 25c: Final Verification Checklist

- [ ] All unit tests pass
- [ ] All integration tests pass
- [ ] Coverage >= 80% on business logic
- [ ] Run ruff linting (zero errors)
- [ ] Run black formatting (zero changes)
- [ ] Manual test all 6 menu options
- [ ] Verify all 32 acceptance criteria from spec Section 10.1

**Spec Reference:** Section 7.4 (Code Quality), Section 10 (Acceptance Criteria Summary)
**Plan Reference:** Section 8 (Testing Approach), Section 9.2 (T-009, T-010, T-011)

**Completion Criteria:**
- [ ] `test_cli.py` file exists with 12 test cases
- [ ] All integration tests pass
- [ ] `README.md` exists and is complete
- [ ] All 32 acceptance criteria verified
- [ ] Coverage >= 80%
- [ ] Zero linting errors
- [ ] Zero formatting issues

---

## 4. Task Execution Order

```
TASK-001 (Setup: Root Directory)
    │
    ├── TASK-002 (Setup: Source Directories)
    │       │
    │       └── TASK-004 (Setup: __init__.py files) ←─┐
    │                                                  │
    └── TASK-003 (Setup: Test Directories) ───────────┘
                │
                ▼
        TASK-005 (Domain: Task Dataclass)
                │
        ┌───────┴───────┐
        │               │
        ▼               ▼
TASK-006          TASK-007
(Title Validation) (Toggle Method)
        │               │
        └───────┬───────┘
                │
                ▼
        TASK-008 (Domain: Unit Tests)
                │
                ▼
        TASK-009 (Infra: Repository Skeleton)
                │
                ▼
        TASK-010 (Infra: ID Generation)
                │
                ▼
        TASK-011 (Infra: add Method)
                │
        ┌───────┴───────┐
        │               │
        ▼               ▼
TASK-012          TASK-013
(get_by_id)       (get_all)
        │               │
        ├───────┬───────┤
        │       │       │
        ▼       ▼       ▼
TASK-014  TASK-015  (continue)
(update)  (delete)
        │       │
        └───────┴───────┐
                        │
                        ▼
                TASK-016 (App: TaskService + add_task)
                        │
                        ▼
                TASK-017 (App: get_all_tasks, get_task)
                        │
                ┌───────┼───────┐
                │       │       │
                ▼       ▼       ▼
        TASK-018  TASK-019  TASK-020
        (update)  (delete)  (toggle)
                │       │       │
                └───────┴───────┘
                        │
                        ▼
                TASK-021 (App: Unit Tests)
                        │
                        ▼
                TASK-022 (Pres: CLI Menu + Loop)
                        │
                        ▼
                TASK-023 (Pres: All Handlers)
                        │
                        ▼
                TASK-024 (Entry: main.py)
                        │
                        ▼
                TASK-025 (Verification)
```

---

## 5. Acceptance Criteria Traceability

| AC ID | Description | Task(s) |
|-------|-------------|---------|
| AC-001-1 | User can enter task title | TASK-023 |
| AC-001-2 | System assigns unique ID | TASK-010, TASK-016 |
| AC-001-3 | Task created incomplete | TASK-005 |
| AC-001-4 | System confirms creation | TASK-023 |
| AC-001-5 | Empty title rejected | TASK-006, TASK-023 |
| AC-001-6 | Whitespace title rejected | TASK-006, TASK-023 |
| AC-002-1 | User can view all tasks | TASK-023 |
| AC-002-2 | Display ID, title, status | TASK-023 |
| AC-002-3 | Status format [X]/[ ] | TASK-023 |
| AC-002-4 | Creation order | TASK-013 |
| AC-002-5 | Empty list message | TASK-023 |
| AC-003-1 | User specifies ID | TASK-023 |
| AC-003-2 | User enters new title | TASK-023 |
| AC-003-3 | System confirms update | TASK-023 |
| AC-003-4 | Invalid ID error | TASK-018, TASK-023 |
| AC-003-5 | Non-numeric ID error | TASK-023 |
| AC-003-6 | Empty title rejected | TASK-006, TASK-023 |
| AC-003-7 | Whitespace title rejected | TASK-006, TASK-023 |
| AC-004-1 | User specifies ID | TASK-023 |
| AC-004-2 | System removes task | TASK-015, TASK-019 |
| AC-004-3 | System confirms deletion | TASK-023 |
| AC-004-4 | Invalid ID error | TASK-019, TASK-023 |
| AC-004-5 | Non-numeric ID error | TASK-023 |
| AC-005-1 | User specifies ID | TASK-023 |
| AC-005-2 | Incomplete → Complete | TASK-007, TASK-020 |
| AC-005-3 | Complete → Incomplete | TASK-007, TASK-020 |
| AC-005-4 | System confirms status | TASK-023 |
| AC-005-5 | Invalid ID error | TASK-020, TASK-023 |
| AC-005-6 | Non-numeric ID error | TASK-023 |
| AC-006-1 | Exit from menu | TASK-022, TASK-023 |
| AC-006-2 | Farewell message | TASK-023 |
| AC-006-3 | Clean termination | TASK-022, TASK-023 |

---

## 6. Document Control

### 6.1 Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2025-12-28 | Agent | Initial task breakdown |

### 6.2 Approval

| Role | Name | Date | Status |
|------|------|------|--------|
| Task Author | Agent | 2025-12-28 | Draft |
| Human Reviewer | — | — | Pending |

---

## 7. References

- [PHASE-I-PLAN.md](./PHASE-I-PLAN.md) — Phase I Technical Plan
- [PHASE-I-SPEC.md](../specs/PHASE-I-SPEC.md) — Phase I Specification
- [CONSTITUTION.md](../CONSTITUTION.md) — Global Constitution

---

*End of Phase I Implementation Tasks*
