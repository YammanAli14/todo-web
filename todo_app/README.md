# Todo Application - Phase I

A simple in-memory console todo application built as part of the Evolution of Todo project.

## Overview

Phase I delivers a minimal, menu-driven Python console application for task management. All data exists only in memory and is lost when the application terminates.

## Requirements

- Python 3.11 or higher

## Installation

No installation required. Clone the repository and run directly.

```bash
cd todo_app
python main.py
```

## Features

1. **Add Task** - Create a new task with a title
2. **View Tasks** - Display all tasks with their status
3. **Update Task** - Change a task's title
4. **Delete Task** - Remove a task
5. **Toggle Complete** - Mark a task as complete/incomplete
6. **Exit** - Close the application

## Usage

Run the application:

```bash
python main.py
```

You will see a menu:

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

### Adding a Task

```
Enter your choice (1-6): 1

--- Add Task ---
Enter task title: Buy groceries

Task added successfully!
ID: 1
Title: Buy groceries
Status: Incomplete
```

### Viewing Tasks

```
Enter your choice (1-6): 2

--- Task List ---
[ ] 1. Buy groceries
[X] 2. Call dentist
[ ] 3. Finish report

Total: 3 tasks (1 complete, 2 incomplete)
```

### Updating a Task

```
Enter your choice (1-6): 3

--- Update Task ---
Enter task ID: 1
Enter new title: Buy groceries and milk

Task updated successfully!
ID: 1
New Title: Buy groceries and milk
```

### Deleting a Task

```
Enter your choice (1-6): 4

--- Delete Task ---
Enter task ID: 2

Task deleted successfully!
Deleted: "Call dentist"
```

### Toggling Complete Status

```
Enter your choice (1-6): 5

--- Toggle Complete ---
Enter task ID: 1

Task status updated!
ID: 1
Title: Buy groceries
Status: Complete
```

## Project Structure

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

## Running Tests

Install pytest (if not already installed):

```bash
pip install pytest pytest-cov
```

Run all tests:

```bash
cd todo_app
python -m pytest tests/ -v
```

Run with coverage:

```bash
python -m pytest tests/ -v --cov=src --cov-report=term-missing
```

## Architecture

The application follows clean architecture principles:

- **Domain Layer** (`src/domain/`) - Task entity and validation rules
- **Application Layer** (`src/application/`) - Business logic and use case orchestration
- **Infrastructure Layer** (`src/infrastructure/`) - In-memory storage implementation
- **Presentation Layer** (`src/presentation/`) - CLI menu and user interaction

## Limitations

- In-memory storage only (data is lost on exit)
- Single user
- No persistence
- No authentication

## License

Part of the Evolution of Todo project.
