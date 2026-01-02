# Phase III Implementation Tasks

**Document ID:** TASKS-PHASE-III-001
**Version:** 1.0.0
**Status:** Draft — Pending Approval
**Plan Reference:** [PHASE-III-PLAN.md](./PHASE-III-PLAN.md)
**Specification Reference:** [../specs/PHASE-III-SPEC.md](../specs/PHASE-III-SPEC.md)
**Constitution Reference:** [../CONSTITUTION.md](../CONSTITUTION.md)

---

## 1. Overview

This document contains the atomic implementation tasks for Phase III. Each task is:

- Small and testable
- Sequential (dependencies clearly stated)
- Traceable to specification and plan sections
- Sufficient to fully implement Phase III

**Total Tasks:** 20
**Estimated Files:** 15

---

## 2. Task Index

| ID | Category | Description |
|----|----------|-------------|
| TASK-301 | Setup | Create project directory structure |
| TASK-302 | Setup | Create requirements.txt |
| TASK-303 | Setup | Create .env.example |
| TASK-304 | Setup | Create all `__init__.py` files |
| TASK-305 | Tools | Implement API client |
| TASK-306 | Tools | Implement create_task tool |
| TASK-307 | Tools | Implement list_tasks tool |
| TASK-308 | Tools | Implement get_task tool |
| TASK-309 | Tools | Implement update_task tool |
| TASK-310 | Tools | Implement delete_task tool |
| TASK-311 | Tools | Implement toggle_task tool |
| TASK-312 | Agent | Implement agent configuration |
| TASK-313 | Agent | Implement todo agent |
| TASK-314 | CLI | Implement CLI interface |
| TASK-315 | Entry | Implement main.py entry point |
| TASK-316 | Test | Create test fixtures |
| TASK-317 | Test | Write tool unit tests |
| TASK-318 | Test | Write agent integration tests |
| TASK-319 | Docs | Create README documentation |
| TASK-320 | Verify | Final verification |

---

## 3. Detailed Task Specifications

---

### TASK-301: Create Project Directory Structure

**Category:** Setup
**Preconditions:** None
**Depends On:** None

**Description:**
Create the `todo_agent` project directory with all subdirectories.

**Artifacts to Create:**
- `todo_agent/` (directory)
- `todo_agent/src/` (directory)
- `todo_agent/src/agent/` (directory)
- `todo_agent/src/tools/` (directory)
- `todo_agent/src/cli/` (directory)
- `todo_agent/tests/` (directory)
- `todo_agent/tests/unit/` (directory)
- `todo_agent/tests/integration/` (directory)

**Spec Reference:** Section 10.3 (Project Structure)
**Plan Reference:** Section 2.1 (Project Layout)

**Completion Criteria:**
- [ ] All directories created

---

### TASK-302: Create requirements.txt

**Category:** Setup
**Preconditions:** TASK-301 complete
**Depends On:** TASK-301

**Description:**
Create requirements.txt with Phase III dependencies.

**Artifacts to Create:**
- `todo_agent/requirements.txt`

**Content:**
```
openai-agents>=0.0.3
httpx>=0.26.0
python-dotenv>=1.0.0
pytest>=8.0.0
pytest-cov>=4.0.0
pytest-asyncio>=0.23.0
respx>=0.21.0
```

**Spec Reference:** Section 10.2 (Dependencies)
**Plan Reference:** Section 9.1 (Task T-302)

**Completion Criteria:**
- [ ] requirements.txt exists with all dependencies

---

### TASK-303: Create .env.example

**Category:** Setup
**Preconditions:** TASK-301 complete
**Depends On:** TASK-301

**Description:**
Create example environment file.

**Artifacts to Create:**
- `todo_agent/.env.example`

**Content:**
```
# OpenAI API Key (required)
OPENAI_API_KEY=your-api-key-here

# Todo API Base URL (optional, defaults to http://localhost:8000)
API_BASE_URL=http://localhost:8000
```

**Spec Reference:** Section 8.1 (Required Environment Variables)
**Plan Reference:** Section 7.1 (Environment Variables)

**Completion Criteria:**
- [ ] .env.example exists with documented variables

---

### TASK-304: Create All `__init__.py` Files

**Category:** Setup
**Preconditions:** TASK-301 complete
**Depends On:** TASK-301

**Description:**
Create `__init__.py` files for all packages.

**Artifacts to Create:**
- `todo_agent/src/__init__.py`
- `todo_agent/src/agent/__init__.py`
- `todo_agent/src/tools/__init__.py`
- `todo_agent/src/cli/__init__.py`
- `todo_agent/tests/__init__.py`
- `todo_agent/tests/unit/__init__.py`
- `todo_agent/tests/integration/__init__.py`

**Spec Reference:** Section 10.3 (Project Structure)
**Plan Reference:** Section 2.1 (Project Layout)

**Completion Criteria:**
- [ ] 7 `__init__.py` files created

---

### TASK-305: Implement API Client

**Category:** Tools
**Preconditions:** TASK-304 complete
**Depends On:** TASK-304

**Description:**
Implement HTTP client for communicating with Phase II API.

**Artifacts to Create:**
- `todo_agent/src/tools/api_client.py`

**Implementation:**
```python
class TodoAPIClient:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url

    def create_task(self, title: str) -> dict: ...
    def list_tasks(self) -> list[dict]: ...
    def get_task(self, task_id: int) -> dict | None: ...
    def update_task(self, task_id: int, title: str) -> dict | None: ...
    def delete_task(self, task_id: int) -> bool: ...
    def toggle_task(self, task_id: int) -> dict | None: ...
```

**Spec Reference:** Section 6 (API Integration)
**Plan Reference:** Section 3 (API Client Implementation)

**Completion Criteria:**
- [ ] TodoAPIClient class implemented
- [ ] All 6 methods implemented
- [ ] Error handling for 404, 422, 5xx
- [ ] Type hints and docstrings present

---

### TASK-306: Implement create_task Tool

**Category:** Tools
**Preconditions:** TASK-305 complete
**Depends On:** TASK-305

**Description:**
Implement MCP tool for creating tasks.

**Artifacts to Create:**
- `todo_agent/src/tools/task_tools.py`

**Implementation:**
```python
from agents import function_tool

@function_tool
def create_task(title: str) -> str:
    """Create a new task with the given title."""
    client = get_api_client()
    try:
        task = client.create_task(title)
        return format_task_created(task)
    except Exception as e:
        return f"Error creating task: {e}"
```

**Spec Reference:** Section 4.2.1 (create_task)
**Plan Reference:** Section 4 (MCP Tools Implementation)

**Completion Criteria:**
- [ ] create_task function with @function_tool decorator
- [ ] Returns formatted success message
- [ ] Handles errors gracefully

---

### TASK-307: Implement list_tasks Tool

**Category:** Tools
**Preconditions:** TASK-306 complete
**Depends On:** TASK-306

**Description:**
Implement MCP tool for listing all tasks.

**Artifacts to Modify:**
- `todo_agent/src/tools/task_tools.py`

**Implementation:**
```python
@function_tool
def list_tasks() -> str:
    """List all tasks in the todo list."""
    client = get_api_client()
    tasks = client.list_tasks()
    if not tasks:
        return "No tasks found. Your todo list is empty."
    return format_task_list(tasks)
```

**Spec Reference:** Section 4.2.2 (list_tasks)
**Plan Reference:** Section 4 (MCP Tools Implementation)

**Completion Criteria:**
- [ ] list_tasks function implemented
- [ ] Handles empty list
- [ ] Formats tasks with status indicators

---

### TASK-308: Implement get_task Tool

**Category:** Tools
**Preconditions:** TASK-306 complete
**Depends On:** TASK-306

**Description:**
Implement MCP tool for getting a single task.

**Artifacts to Modify:**
- `todo_agent/src/tools/task_tools.py`

**Implementation:**
```python
@function_tool
def get_task(task_id: int) -> str:
    """Get details of a specific task by ID."""
    client = get_api_client()
    task = client.get_task(task_id)
    if task is None:
        return f"Error: Task with ID {task_id} was not found."
    return format_task_detail(task)
```

**Spec Reference:** Section 4.2.3 (get_task)
**Plan Reference:** Section 4 (MCP Tools Implementation)

**Completion Criteria:**
- [ ] get_task function implemented
- [ ] Handles not found case
- [ ] Returns formatted task details

---

### TASK-309: Implement update_task Tool

**Category:** Tools
**Preconditions:** TASK-306 complete
**Depends On:** TASK-306

**Description:**
Implement MCP tool for updating a task.

**Artifacts to Modify:**
- `todo_agent/src/tools/task_tools.py`

**Implementation:**
```python
@function_tool
def update_task(task_id: int, title: str) -> str:
    """Update the title of an existing task."""
    client = get_api_client()
    task = client.update_task(task_id, title)
    if task is None:
        return f"Error: Task with ID {task_id} was not found."
    return format_task_updated(task)
```

**Spec Reference:** Section 4.2.4 (update_task)
**Plan Reference:** Section 4 (MCP Tools Implementation)

**Completion Criteria:**
- [ ] update_task function implemented
- [ ] Handles not found case
- [ ] Returns formatted update confirmation

---

### TASK-310: Implement delete_task Tool

**Category:** Tools
**Preconditions:** TASK-306 complete
**Depends On:** TASK-306

**Description:**
Implement MCP tool for deleting a task.

**Artifacts to Modify:**
- `todo_agent/src/tools/task_tools.py`

**Implementation:**
```python
@function_tool
def delete_task(task_id: int) -> str:
    """Delete a task by its ID."""
    client = get_api_client()
    deleted = client.delete_task(task_id)
    if not deleted:
        return f"Error: Task with ID {task_id} was not found."
    return f"Task {task_id} has been deleted successfully."
```

**Spec Reference:** Section 4.2.5 (delete_task)
**Plan Reference:** Section 4 (MCP Tools Implementation)

**Completion Criteria:**
- [ ] delete_task function implemented
- [ ] Handles not found case
- [ ] Returns success message

---

### TASK-311: Implement toggle_task Tool

**Category:** Tools
**Preconditions:** TASK-306 complete
**Depends On:** TASK-306

**Description:**
Implement MCP tool for toggling task completion.

**Artifacts to Modify:**
- `todo_agent/src/tools/task_tools.py`

**Implementation:**
```python
@function_tool
def toggle_task(task_id: int) -> str:
    """Toggle the completion status of a task."""
    client = get_api_client()
    task = client.toggle_task(task_id)
    if task is None:
        return f"Error: Task with ID {task_id} was not found."
    status = "complete" if task["is_complete"] else "incomplete"
    return f"Task {task_id} is now marked as {status}."
```

**Spec Reference:** Section 4.2.6 (toggle_task)
**Plan Reference:** Section 4 (MCP Tools Implementation)

**Completion Criteria:**
- [ ] toggle_task function implemented
- [ ] Handles not found case
- [ ] Shows new status in response

---

### TASK-312: Implement Agent Configuration

**Category:** Agent
**Preconditions:** TASK-304 complete
**Depends On:** TASK-304

**Description:**
Implement configuration module for agent settings.

**Artifacts to Create:**
- `todo_agent/src/agent/config.py`

**Implementation:**
```python
import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
AGENT_MODEL = "gpt-4o-mini"

AGENT_INSTRUCTIONS = """
You are a helpful task management assistant...
"""
```

**Spec Reference:** Section 5 (Agent Configuration)
**Plan Reference:** Section 5 (Agent Configuration)

**Completion Criteria:**
- [ ] config.py exists
- [ ] Loads environment variables
- [ ] Defines AGENT_INSTRUCTIONS
- [ ] Defines AGENT_MODEL

---

### TASK-313: Implement Todo Agent

**Category:** Agent
**Preconditions:** TASK-311, TASK-312 complete
**Depends On:** TASK-311, TASK-312

**Description:**
Implement the main agent with all tools.

**Artifacts to Create:**
- `todo_agent/src/agent/todo_agent.py`

**Implementation:**
```python
from agents import Agent
from src.agent.config import AGENT_INSTRUCTIONS, AGENT_MODEL
from src.tools.task_tools import (
    create_task, list_tasks, get_task,
    update_task, delete_task, toggle_task
)

todo_agent = Agent(
    name="todo_agent",
    instructions=AGENT_INSTRUCTIONS,
    model=AGENT_MODEL,
    tools=[
        create_task,
        list_tasks,
        get_task,
        update_task,
        delete_task,
        toggle_task
    ]
)
```

**Spec Reference:** Section 5.1 (Agent Definition)
**Plan Reference:** Section 5.1 (Agent Setup)

**Completion Criteria:**
- [ ] todo_agent.py exists
- [ ] Agent defined with all 6 tools
- [ ] Instructions and model configured

---

### TASK-314: Implement CLI Interface

**Category:** CLI
**Preconditions:** TASK-313 complete
**Depends On:** TASK-313

**Description:**
Implement command-line interface for agent interaction.

**Artifacts to Create:**
- `todo_agent/src/cli/main.py`

**Implementation:**
```python
from agents import Runner
from src.agent.todo_agent import todo_agent

def display_welcome():
    print("=" * 40)
    print("       TODO AGENT ASSISTANT")
    print("=" * 40)
    print("\nI can help you manage your tasks. Try:")
    print('  - "Add a task to buy groceries"')
    print('  - "Show me my tasks"')
    print('  - "Mark task 1 as complete"')
    print("\nType 'exit' or 'quit' to end.\n")

def run_cli():
    display_welcome()
    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in ("exit", "quit"):
            print("\nGoodbye!")
            break
        if not user_input:
            continue
        result = Runner.run_sync(todo_agent, user_input)
        print(f"\nAssistant: {result.final_output}\n")
```

**Spec Reference:** Section 3.7 (US-307: Agent CLI Interface)
**Plan Reference:** Section 6 (CLI Implementation)

**Completion Criteria:**
- [ ] cli/main.py exists
- [ ] Welcome message displayed
- [ ] Exit on "exit" or "quit"
- [ ] Agent responses displayed

---

### TASK-315: Implement main.py Entry Point

**Category:** Entry Point
**Preconditions:** TASK-314 complete
**Depends On:** TASK-314

**Description:**
Create application entry point.

**Artifacts to Create:**
- `todo_agent/main.py`

**Implementation:**
```python
"""Todo Agent - Phase III Entry Point."""

from src.cli.main import run_cli

if __name__ == "__main__":
    run_cli()
```

**Spec Reference:** Section 10.3 (Project Structure)
**Plan Reference:** Section 9.1 (Task T-315)

**Completion Criteria:**
- [ ] main.py exists
- [ ] Imports and runs CLI

---

### TASK-316: Create Test Fixtures

**Category:** Test
**Preconditions:** TASK-305 complete
**Depends On:** TASK-305

**Description:**
Create pytest fixtures for testing.

**Artifacts to Create:**
- `todo_agent/tests/conftest.py`

**Implementation:**
```python
import pytest
from unittest.mock import MagicMock
from src.tools.api_client import TodoAPIClient

@pytest.fixture
def mock_api_client():
    return MagicMock(spec=TodoAPIClient)

@pytest.fixture
def sample_task():
    return {
        "id": 1,
        "title": "Buy groceries",
        "is_complete": False,
        "created_at": "2025-12-28T10:00:00Z",
        "updated_at": "2025-12-28T10:00:00Z"
    }
```

**Spec Reference:** Section 9.3 (Code Quality - Testing)
**Plan Reference:** Section 8 (Testing Strategy)

**Completion Criteria:**
- [ ] conftest.py exists
- [ ] Mock API client fixture
- [ ] Sample task fixture

---

### TASK-317: Write Tool Unit Tests

**Category:** Test
**Preconditions:** TASK-316 complete
**Depends On:** TASK-316

**Description:**
Write unit tests for all MCP tools.

**Artifacts to Create:**
- `todo_agent/tests/unit/test_tools.py`

**Test Cases:**
- test_create_task_success
- test_list_tasks_empty
- test_list_tasks_with_data
- test_get_task_success
- test_get_task_not_found
- test_update_task_success
- test_update_task_not_found
- test_delete_task_success
- test_delete_task_not_found
- test_toggle_task_success
- test_toggle_task_not_found

**Spec Reference:** Section 9.3 (Code Quality - Testing)
**Plan Reference:** Section 8.2 (Unit Tests)

**Completion Criteria:**
- [ ] All 11 test cases implemented
- [ ] All tests pass

---

### TASK-318: Write Agent Integration Tests

**Category:** Test
**Preconditions:** TASK-317 complete
**Depends On:** TASK-317

**Description:**
Write integration tests for agent behavior.

**Artifacts to Create:**
- `todo_agent/tests/integration/test_agent.py`

**Test Cases:**
- test_agent_initialization
- test_agent_has_all_tools

**Spec Reference:** Section 9.3 (Code Quality - Testing)
**Plan Reference:** Section 8.3 (Integration Tests)

**Completion Criteria:**
- [ ] Integration tests implemented
- [ ] Tests verify agent configuration

---

### TASK-319: Create README Documentation

**Category:** Documentation
**Preconditions:** TASK-315 complete
**Depends On:** TASK-315

**Description:**
Create comprehensive README.

**Artifacts to Create:**
- `todo_agent/README.md`

**Sections:**
1. Overview
2. Requirements
3. Installation
4. Configuration
5. Running the Agent
6. Usage Examples
7. Running Tests
8. Project Structure

**Spec Reference:** Section 11.3 (Phase Completion Criteria)
**Plan Reference:** Section 9.1 (Task T-319)

**Completion Criteria:**
- [ ] README.md exists
- [ ] All sections complete

---

### TASK-320: Final Verification

**Category:** Verification
**Preconditions:** TASK-318, TASK-319 complete
**Depends On:** TASK-319

**Description:**
Perform final verification of all acceptance criteria.

**Verification Steps:**
1. Run all tests
2. Verify coverage >= 80%
3. Start Phase II API
4. Run agent CLI
5. Test all operations manually

**Acceptance Criteria Checklist (34 total):**
- US-301: Create Task via Agent (5 criteria)
- US-302: List Tasks via Agent (5 criteria)
- US-303: Update Task via Agent (5 criteria)
- US-304: Delete Task via Agent (5 criteria)
- US-305: Toggle Task via Agent (5 criteria)
- US-306: Get Task via Agent (4 criteria)
- US-307: Agent CLI (5 criteria)

**Spec Reference:** Section 11 (Acceptance Criteria Summary)
**Plan Reference:** Section 10 (Verification Checklist)

**Completion Criteria:**
- [ ] All tests pass
- [ ] All 34 acceptance criteria verified
- [ ] Agent works end-to-end

---

## 4. Document Control

### 4.1 Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2025-12-28 | Agent | Initial task breakdown |

### 4.2 Approval

| Role | Name | Date | Status |
|------|------|------|--------|
| Task Author | Agent | 2025-12-28 | Draft |
| Human Reviewer | — | — | Pending |

---

## 5. References

- [PHASE-III-PLAN.md](./PHASE-III-PLAN.md) — Phase III Technical Plan
- [PHASE-III-SPEC.md](../specs/PHASE-III-SPEC.md) — Phase III Specification
- [CONSTITUTION.md](../CONSTITUTION.md) — Global Constitution

---

*End of Phase III Implementation Tasks*
