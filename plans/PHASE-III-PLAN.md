# Phase III Technical Plan — Agent Integration

**Document ID:** PLAN-PHASE-III-001
**Version:** 1.0.0
**Status:** Draft — Pending Approval
**Specification Reference:** [PHASE-III-SPEC.md](../specs/PHASE-III-SPEC.md)
**Constitution Reference:** [CONSTITUTION.md](../CONSTITUTION.md)

---

## 1. Plan Overview

### 1.1 Purpose

This plan describes HOW the Phase III specification will be implemented. It adds an AI agent layer using OpenAI Agents SDK that interacts with the Phase II Todo API through MCP tools.

### 1.2 Scope

This plan covers:

- Project structure and file organization
- API client implementation for connecting to Phase II API
- MCP tool definitions for all task operations
- Agent configuration and setup
- CLI interface for agent interaction
- Testing strategy

### 1.3 Constitutional Compliance

Per Constitution Article I, Section 1.4, this plan:

1. References the approved specification (SPEC-PHASE-III-001)
2. Breaks work into discrete, verifiable tasks
3. Defines the order of execution
4. Identifies files to be created
5. Specifies the testing approach

---

## 2. Application Architecture

### 2.1 Project Layout

Per specification Section 10.3:

```
todo_agent/
├── src/
│   ├── __init__.py
│   ├── agent/
│   │   ├── __init__.py
│   │   ├── todo_agent.py       # Agent definition
│   │   └── config.py           # Agent configuration
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── task_tools.py       # MCP tool implementations
│   │   └── api_client.py       # HTTP client for API
│   └── cli/
│       ├── __init__.py
│       └── main.py             # CLI interface
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── unit/
│   │   ├── __init__.py
│   │   └── test_tools.py
│   └── integration/
│       ├── __init__.py
│       └── test_agent.py
├── main.py                     # Entry point
├── requirements.txt
├── .env.example
└── README.md
```

### 2.2 Component Responsibilities

| Component | Directory | Responsibility |
|-----------|-----------|----------------|
| Agent | `src/agent/` | Agent definition and configuration |
| Tools | `src/tools/` | MCP tools and API client |
| CLI | `src/cli/` | Command-line interface |

### 2.3 Dependency Flow

```
CLI (main.py)
    │
    ▼
Agent (todo_agent.py)
    │
    ▼
Tools (task_tools.py)
    │
    ▼
API Client (api_client.py)
    │
    ▼
Phase II API (http://localhost:8000)
```

---

## 3. API Client Implementation

### 3.1 HTTP Client Design

The API client wraps httpx for making HTTP calls to the Phase II API.

```python
class TodoAPIClient:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.client = httpx.Client(timeout=30.0)

    def create_task(self, title: str) -> dict: ...
    def list_tasks(self) -> list[dict]: ...
    def get_task(self, task_id: int) -> dict | None: ...
    def update_task(self, task_id: int, title: str) -> dict | None: ...
    def delete_task(self, task_id: int) -> bool: ...
    def toggle_task(self, task_id: int) -> dict | None: ...
```

### 3.2 Error Handling

| HTTP Status | Client Behavior |
|-------------|-----------------|
| 200, 201, 204 | Return response data |
| 404 | Return None or False |
| 422 | Raise ValueError with details |
| 5xx | Raise ConnectionError |

---

## 4. MCP Tools Implementation

### 4.1 Tool Definition Pattern

Each tool follows the OpenAI Agents SDK pattern:

```python
from agents import function_tool

@function_tool
def tool_name(param: type) -> str:
    """Tool description for the agent."""
    # Implementation
    return result_string
```

### 4.2 Tool Implementations

| Tool | Implementation |
|------|----------------|
| `create_task` | Call API, return formatted task |
| `list_tasks` | Call API, format task list |
| `get_task` | Call API, return task or error |
| `update_task` | Call API, return updated task or error |
| `delete_task` | Call API, return success or error |
| `toggle_task` | Call API, return toggled task or error |

### 4.3 Tool Response Format

Tools return human-readable strings for the agent:

```python
# Success example
"Task created successfully:\n  ID: 1\n  Title: Buy groceries\n  Status: Incomplete"

# Error example
"Error: Task with ID 99 was not found."
```

---

## 5. Agent Configuration

### 5.1 Agent Setup

```python
from agents import Agent

agent = Agent(
    name="todo_agent",
    instructions=AGENT_INSTRUCTIONS,
    model="gpt-4o-mini",
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

### 5.2 Agent Instructions

```
You are a helpful task management assistant. You help users manage their
todo list by creating, viewing, updating, and deleting tasks.

When users ask you to:
- Add/create a task: Use the create_task tool
- Show/list tasks: Use the list_tasks tool
- View a specific task: Use the get_task tool
- Update/change/rename a task: Use the update_task tool
- Delete/remove a task: Use the delete_task tool
- Complete/mark done/toggle a task: Use the toggle_task tool

Always confirm what action you took and show the result to the user.
If something goes wrong, explain the error clearly.
```

---

## 6. CLI Implementation

### 6.1 CLI Flow

```
┌─────────────────────────────────────┐
│         Application Start            │
└─────────────────┬───────────────────┘
                  │
                  ▼
┌─────────────────────────────────────┐
│      Display Welcome Message         │
└─────────────────┬───────────────────┘
                  │
                  ▼
┌─────────────────────────────────────┐
│         Get User Input               │
└─────────────────┬───────────────────┘
                  │
        ┌─────────┴─────────┐
        │ "exit"/"quit"?    │
        ▼ Yes               ▼ No
┌───────────────┐   ┌───────────────────┐
│ Display       │   │ Send to Agent      │
│ Goodbye       │   │                   │
│ Exit          │   └─────────┬─────────┘
└───────────────┘             │
                              ▼
                    ┌───────────────────┐
                    │ Display Response   │
                    └─────────┬─────────┘
                              │
                              ▼
                    (Return to Get User Input)
```

### 6.2 CLI Interface

```
========================================
       TODO AGENT ASSISTANT
========================================

I can help you manage your tasks. Try:
  - "Add a task to buy groceries"
  - "Show me my tasks"
  - "Mark task 1 as complete"
  - "Delete task 2"

Type 'exit' or 'quit' to end.

You: _
```

---

## 7. Environment Configuration

### 7.1 Environment Variables

```bash
# .env.example
OPENAI_API_KEY=your-api-key-here
API_BASE_URL=http://localhost:8000
```

### 7.2 Configuration Loading

```python
import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
```

---

## 8. Testing Strategy

### 8.1 Test Structure

```
tests/
├── __init__.py
├── conftest.py              # Shared fixtures
├── unit/
│   ├── __init__.py
│   └── test_tools.py        # Tool unit tests
└── integration/
    ├── __init__.py
    └── test_agent.py        # Agent integration tests
```

### 8.2 Unit Tests (test_tools.py)

| Test Case | Description |
|-----------|-------------|
| `test_create_task_success` | Tool creates task correctly |
| `test_create_task_empty_title` | Tool handles empty title |
| `test_list_tasks_empty` | Tool handles empty list |
| `test_list_tasks_with_data` | Tool formats list correctly |
| `test_get_task_success` | Tool returns task |
| `test_get_task_not_found` | Tool handles 404 |
| `test_update_task_success` | Tool updates task |
| `test_update_task_not_found` | Tool handles 404 |
| `test_delete_task_success` | Tool deletes task |
| `test_delete_task_not_found` | Tool handles 404 |
| `test_toggle_task_success` | Tool toggles task |
| `test_toggle_task_not_found` | Tool handles 404 |

### 8.3 Integration Tests (test_agent.py)

| Test Case | Description |
|-----------|-------------|
| `test_agent_create_task` | Agent creates task from NL |
| `test_agent_list_tasks` | Agent lists tasks from NL |
| `test_agent_update_task` | Agent updates task from NL |
| `test_agent_delete_task` | Agent deletes task from NL |
| `test_agent_toggle_task` | Agent toggles task from NL |

### 8.4 Mocking Strategy

- Mock httpx client for unit tests
- Mock OpenAI API for agent tests (or use real API with test key)

---

## 9. Implementation Tasks

### 9.1 Task Summary

| Task ID | Category | Description | Files |
|---------|----------|-------------|-------|
| T-301 | Setup | Create project structure | Directories |
| T-302 | Setup | Create requirements.txt | `requirements.txt` |
| T-303 | Setup | Create .env.example | `.env.example` |
| T-304 | Setup | Create all `__init__.py` | `__init__.py` files |
| T-305 | Tools | Implement API client | `api_client.py` |
| T-306 | Tools | Implement create_task tool | `task_tools.py` |
| T-307 | Tools | Implement list_tasks tool | `task_tools.py` |
| T-308 | Tools | Implement get_task tool | `task_tools.py` |
| T-309 | Tools | Implement update_task tool | `task_tools.py` |
| T-310 | Tools | Implement delete_task tool | `task_tools.py` |
| T-311 | Tools | Implement toggle_task tool | `task_tools.py` |
| T-312 | Agent | Implement agent config | `config.py` |
| T-313 | Agent | Implement todo agent | `todo_agent.py` |
| T-314 | CLI | Implement CLI interface | `cli/main.py` |
| T-315 | Entry | Implement main.py | `main.py` |
| T-316 | Test | Create test fixtures | `conftest.py` |
| T-317 | Test | Write tool unit tests | `test_tools.py` |
| T-318 | Test | Write agent integration tests | `test_agent.py` |
| T-319 | Docs | Create README | `README.md` |
| T-320 | Verify | Final verification | — |

### 9.2 Task Execution Order

```
T-301 (Setup: Structure)
    │
    ├── T-302 (requirements.txt)
    ├── T-303 (.env.example)
    └── T-304 (__init__.py files)
            │
            ▼
    T-305 (API Client)
            │
    ┌───────┴───────┬───────┬───────┬───────┬───────┐
    ▼       ▼       ▼       ▼       ▼       ▼
T-306   T-307   T-308   T-309   T-310   T-311
(create) (list)  (get)  (update)(delete)(toggle)
    │       │       │       │       │       │
    └───────┴───────┴───────┴───────┴───────┘
                    │
                    ▼
            T-312 (Agent Config)
                    │
                    ▼
            T-313 (Todo Agent)
                    │
                    ▼
            T-314 (CLI)
                    │
                    ▼
            T-315 (main.py)
                    │
                    ▼
            T-316 (Test Fixtures)
                    │
            ┌───────┴───────┐
            ▼               ▼
        T-317           T-318
        (Unit)       (Integration)
            │               │
            └───────┬───────┘
                    │
                    ▼
            T-319 (README)
                    │
                    ▼
            T-320 (Verification)
```

---

## 10. Verification Checklist

### 10.1 Specification Compliance

| Spec Section | Plan Coverage | Status |
|--------------|---------------|--------|
| 3. User Stories | Section 4, 5, 6 | Covered |
| 4. MCP Tools | Section 4 | Covered |
| 5. Agent Config | Section 5 | Covered |
| 6. API Integration | Section 3 | Covered |
| 7. Error Handling | Section 3.2 | Covered |
| 8. Environment | Section 7 | Covered |

### 10.2 Constitutional Compliance

| Article | Requirement | Compliance |
|---------|-------------|------------|
| I.1.4 | References approved spec | Yes |
| I.1.4 | Discrete verifiable tasks | Yes |
| I.1.4 | Order of execution | Yes |
| I.1.4 | Files identified | Yes |
| I.1.4 | Testing approach | Yes |
| IV.4.1 | OpenAI Agents SDK, MCP | Yes |
| V.5.1 | Clean architecture | Yes |

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

- [PHASE-III-SPEC.md](../specs/PHASE-III-SPEC.md) — Phase III Specification
- [CONSTITUTION.md](../CONSTITUTION.md) — Global Constitution
- [OpenAI Agents SDK](https://github.com/openai/openai-agents-python)

---

*End of Phase III Technical Plan*
