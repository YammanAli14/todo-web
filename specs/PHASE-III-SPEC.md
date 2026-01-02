# Phase III Specification — Agent Integration

**Document ID:** SPEC-PHASE-III-001
**Version:** 1.0.0
**Status:** Draft — Pending Approval
**Governing Document:** [CONSTITUTION.md](../CONSTITUTION.md)
**Phase:** III — Agent Integration
**Depends On:** Phase II (Complete)

---

## 1. Overview

### 1.1 Purpose

This specification defines the requirements for Phase III of the Evolution of Todo project: integration of OpenAI Agents SDK with Model Context Protocol (MCP) tools to enable AI-driven task management operations.

### 1.2 Scope Summary

Phase III adds an AI agent layer that can interact with the Todo API through MCP tools. The agent can understand natural language requests and perform task operations (create, list, update, delete, toggle) on behalf of users.

### 1.3 Constitutional Compliance

This specification complies with:

- **Article I** — Defines scope, requirements, interfaces, acceptance criteria, and dependencies
- **Article III, Section 3.1** — Implements Phase III: OpenAI Agents SDK, MCP, agent-driven operations
- **Article III, Section 3.2** — Contains no forward leakage to future phases
- **Article IV** — Uses mandatory technologies: OpenAI Agents SDK, MCP
- **Article V** — Adheres to clean architecture and quality principles

---

## 2. Scope Definition

### 2.1 In Scope

| Item | Description |
|------|-------------|
| Agent Framework | OpenAI Agents SDK for agent orchestration |
| Tool Protocol | MCP (Model Context Protocol) for tool definitions |
| MCP Tools | Tools for all task CRUD operations |
| Agent Interface | CLI interface for interacting with the agent |
| Natural Language | Agent understands task requests in natural language |
| API Integration | Agent uses Phase II REST API for persistence |

### 2.2 Explicitly Out of Scope

The following are **prohibited** in Phase III:

| Excluded Item | Reason |
|---------------|--------|
| User authentication | Phase IV feature |
| Multiple users/tenants | Phase IV+ feature |
| Frontend/Web UI | Phase IV feature |
| Docker/Kubernetes | Phase V feature |
| Message queues | Phase V feature |
| Streaming responses | Not in Phase III requirements |
| Multi-agent systems | Not in Phase III requirements |
| Agent memory/persistence | Not in Phase III requirements |
| Custom LLM providers | OpenAI only per spec |

---

## 3. User Stories

### 3.1 US-301: Create Task via Agent

**As a** user
**I want to** tell the agent to create a task in natural language
**So that** I can add tasks without using the API directly

**Acceptance Criteria:**

| ID | Criterion |
|----|-----------|
| AC-301-1 | User can say "Add a task to buy groceries" |
| AC-301-2 | Agent extracts task title from natural language |
| AC-301-3 | Agent calls the create task MCP tool |
| AC-301-4 | Agent confirms task creation with details |
| AC-301-5 | Task is persisted in the database |

### 3.2 US-302: List Tasks via Agent

**As a** user
**I want to** ask the agent to show my tasks
**So that** I can see what needs to be done

**Acceptance Criteria:**

| ID | Criterion |
|----|-----------|
| AC-302-1 | User can say "Show me my tasks" or "List all tasks" |
| AC-302-2 | Agent calls the list tasks MCP tool |
| AC-302-3 | Agent formats and displays task list |
| AC-302-4 | Agent shows task ID, title, and completion status |
| AC-302-5 | Agent handles empty task list gracefully |

### 3.3 US-303: Update Task via Agent

**As a** user
**I want to** tell the agent to update a task
**So that** I can modify task titles conversationally

**Acceptance Criteria:**

| ID | Criterion |
|----|-----------|
| AC-303-1 | User can say "Change task 1 to buy groceries and milk" |
| AC-303-2 | Agent extracts task ID and new title |
| AC-303-3 | Agent calls the update task MCP tool |
| AC-303-4 | Agent confirms the update with new details |
| AC-303-5 | Agent handles non-existent task gracefully |

### 3.4 US-304: Delete Task via Agent

**As a** user
**I want to** tell the agent to delete a task
**So that** I can remove tasks conversationally

**Acceptance Criteria:**

| ID | Criterion |
|----|-----------|
| AC-304-1 | User can say "Delete task 3" or "Remove task 3" |
| AC-304-2 | Agent extracts task ID from request |
| AC-304-3 | Agent calls the delete task MCP tool |
| AC-304-4 | Agent confirms deletion |
| AC-304-5 | Agent handles non-existent task gracefully |

### 3.5 US-305: Toggle Task via Agent

**As a** user
**I want to** tell the agent to mark a task complete or incomplete
**So that** I can track progress conversationally

**Acceptance Criteria:**

| ID | Criterion |
|----|-----------|
| AC-305-1 | User can say "Mark task 1 as complete" |
| AC-305-2 | User can say "Mark task 2 as incomplete" |
| AC-305-3 | Agent calls the toggle task MCP tool |
| AC-305-4 | Agent confirms the new status |
| AC-305-5 | Agent handles non-existent task gracefully |

### 3.6 US-306: Get Single Task via Agent

**As a** user
**I want to** ask the agent about a specific task
**So that** I can see task details

**Acceptance Criteria:**

| ID | Criterion |
|----|-----------|
| AC-306-1 | User can say "Show me task 1" or "What is task 1?" |
| AC-306-2 | Agent calls the get task MCP tool |
| AC-306-3 | Agent displays task details |
| AC-306-4 | Agent handles non-existent task gracefully |

### 3.7 US-307: Agent CLI Interface

**As a** user
**I want to** interact with the agent via command line
**So that** I can have a conversation about my tasks

**Acceptance Criteria:**

| ID | Criterion |
|----|-----------|
| AC-307-1 | Agent CLI starts with a welcome message |
| AC-307-2 | User can type natural language requests |
| AC-307-3 | Agent responds with results |
| AC-307-4 | User can type "exit" or "quit" to end |
| AC-307-5 | Agent handles invalid requests gracefully |

---

## 4. MCP Tools Specification

### 4.1 Tool Overview

| Tool Name | Description | Parameters |
|-----------|-------------|------------|
| `create_task` | Create a new task | `title: str` |
| `list_tasks` | List all tasks | None |
| `get_task` | Get a specific task | `task_id: int` |
| `update_task` | Update a task's title | `task_id: int, title: str` |
| `delete_task` | Delete a task | `task_id: int` |
| `toggle_task` | Toggle task completion | `task_id: int` |

### 4.2 Tool Definitions

#### 4.2.1 create_task

```json
{
  "name": "create_task",
  "description": "Create a new task with the given title. The task will be created as incomplete.",
  "parameters": {
    "type": "object",
    "properties": {
      "title": {
        "type": "string",
        "description": "The title of the task to create (max 200 characters)"
      }
    },
    "required": ["title"]
  }
}
```

**Returns:** Task object with id, title, is_complete, created_at, updated_at

#### 4.2.2 list_tasks

```json
{
  "name": "list_tasks",
  "description": "List all tasks in the todo list, ordered by ID.",
  "parameters": {
    "type": "object",
    "properties": {}
  }
}
```

**Returns:** Array of task objects

#### 4.2.3 get_task

```json
{
  "name": "get_task",
  "description": "Get details of a specific task by its ID.",
  "parameters": {
    "type": "object",
    "properties": {
      "task_id": {
        "type": "integer",
        "description": "The ID of the task to retrieve"
      }
    },
    "required": ["task_id"]
  }
}
```

**Returns:** Task object or error if not found

#### 4.2.4 update_task

```json
{
  "name": "update_task",
  "description": "Update the title of an existing task.",
  "parameters": {
    "type": "object",
    "properties": {
      "task_id": {
        "type": "integer",
        "description": "The ID of the task to update"
      },
      "title": {
        "type": "string",
        "description": "The new title for the task (max 200 characters)"
      }
    },
    "required": ["task_id", "title"]
  }
}
```

**Returns:** Updated task object or error if not found

#### 4.2.5 delete_task

```json
{
  "name": "delete_task",
  "description": "Delete a task by its ID.",
  "parameters": {
    "type": "object",
    "properties": {
      "task_id": {
        "type": "integer",
        "description": "The ID of the task to delete"
      }
    },
    "required": ["task_id"]
  }
}
```

**Returns:** Success message or error if not found

#### 4.2.6 toggle_task

```json
{
  "name": "toggle_task",
  "description": "Toggle the completion status of a task. If incomplete, marks as complete. If complete, marks as incomplete.",
  "parameters": {
    "type": "object",
    "properties": {
      "task_id": {
        "type": "integer",
        "description": "The ID of the task to toggle"
      }
    },
    "required": ["task_id"]
  }
}
```

**Returns:** Updated task object or error if not found

---

## 5. Agent Configuration

### 5.1 Agent Definition

```python
Agent(
    name="todo_agent",
    instructions="""You are a helpful task management assistant.
    You help users manage their todo list by creating, viewing,
    updating, and deleting tasks. Always confirm actions with
    the user and provide clear feedback about what was done.""",
    model="gpt-4o-mini",
    tools=[create_task, list_tasks, get_task, update_task, delete_task, toggle_task]
)
```

### 5.2 Agent Behavior

| Behavior | Specification |
|----------|---------------|
| Responses | Concise and helpful |
| Confirmations | Always confirm completed actions |
| Errors | Explain errors clearly to user |
| Ambiguity | Ask for clarification when needed |

---

## 6. API Integration

### 6.1 API Base URL

The agent connects to the Phase II API:

| Environment | URL |
|-------------|-----|
| Development | `http://localhost:8000` |
| Production | Configurable via `API_BASE_URL` |

### 6.2 Tool-to-API Mapping

| MCP Tool | HTTP Method | API Endpoint |
|----------|-------------|--------------|
| `create_task` | POST | /tasks |
| `list_tasks` | GET | /tasks |
| `get_task` | GET | /tasks/{id} |
| `update_task` | PUT | /tasks/{id} |
| `delete_task` | DELETE | /tasks/{id} |
| `toggle_task` | PATCH | /tasks/{id}/toggle |

---

## 7. Error Handling

### 7.1 Tool Error Responses

| Error Case | Response |
|------------|----------|
| Task not found | "Task with ID {id} was not found." |
| Validation error | "Invalid input: {details}" |
| API unavailable | "Unable to connect to task service." |
| Unknown error | "An unexpected error occurred." |

### 7.2 Agent Error Behavior

1. Agent explains errors in natural language
2. Agent suggests corrective action if possible
3. Agent does not expose technical details to user

---

## 8. Environment Configuration

### 8.1 Required Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `OPENAI_API_KEY` | Yes | OpenAI API key for agent |
| `API_BASE_URL` | No | Todo API URL (default: http://localhost:8000) |

### 8.2 Configuration File

No additional configuration files required. All configuration via environment variables.

---

## 9. Non-Functional Requirements

### 9.1 Performance

| Requirement | Specification |
|-------------|---------------|
| Response Time | Agent responds within 10 seconds |
| API Calls | Minimal API calls per request |

### 9.2 Reliability

| Requirement | Specification |
|-------------|---------------|
| Error Recovery | Agent handles API failures gracefully |
| Validation | Agent validates parameters before API calls |

### 9.3 Code Quality

Per Constitution Article V, Section 5.4:

| Requirement | Specification |
|-------------|---------------|
| Type Hints | All function signatures typed |
| Documentation | All tools documented |
| Testing | Minimum 80% code coverage |
| Linting | Must pass ruff |
| Formatting | Must pass black |

---

## 10. Technical Constraints

### 10.1 Required Technologies

| Technology | Version | Purpose |
|------------|---------|---------|
| Python | 3.11+ | Runtime |
| OpenAI Agents SDK | Latest | Agent framework |
| httpx | Latest | HTTP client for API calls |
| FastAPI | 0.100+ | Phase II API (dependency) |

### 10.2 Dependencies

```
openai-agents>=0.1.0
httpx>=0.26.0
python-dotenv>=1.0.0
```

### 10.3 Project Structure

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
│   │   ├── task_tools.py       # MCP tool definitions
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

### 10.4 Prohibited Technologies

The following are explicitly prohibited in Phase III:

- Authentication/authorization systems
- Multiple LLM providers
- Agent memory/state persistence
- Streaming responses
- WebSockets
- Docker/containerization

---

## 11. Acceptance Criteria Summary

### 11.1 Feature Completion Checklist

| Feature | Criteria Count | Required Pass |
|---------|----------------|---------------|
| Create Task via Agent | 5 | All |
| List Tasks via Agent | 5 | All |
| Update Task via Agent | 5 | All |
| Delete Task via Agent | 5 | All |
| Toggle Task via Agent | 5 | All |
| Get Task via Agent | 4 | All |
| Agent CLI | 5 | All |
| **Total** | **34** | **All** |

### 11.2 Quality Checklist

| Requirement | Pass Criteria |
|-------------|---------------|
| Type Hints | All functions typed |
| Documentation | All tools documented |
| Test Coverage | >= 80% on business logic |
| Linting | Zero ruff errors |
| Formatting | Zero black changes |

### 11.3 Phase Completion Criteria

Phase III is complete when:

1. All 34 acceptance criteria pass
2. All quality requirements met
3. All tests pass
4. Agent can perform all CRUD operations
5. README documentation complete
6. Human review approves deliverable

---

## 12. Glossary

| Term | Definition |
|------|------------|
| Agent | AI system that can understand and execute tasks |
| MCP | Model Context Protocol - standard for tool definitions |
| Tool | Function that an agent can call |
| OpenAI Agents SDK | Framework for building AI agents |

---

## 13. Document Control

### 13.1 Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2025-12-28 | Agent | Initial specification |

### 13.2 Approval

| Role | Name | Date | Status |
|------|------|------|--------|
| Specification Author | Agent | 2025-12-28 | Draft |
| Human Reviewer | — | — | Pending |

---

## 14. References

- [CONSTITUTION.md](../CONSTITUTION.md) — Global project constitution
- [PHASE-II-SPEC.md](./PHASE-II-SPEC.md) — Phase II specification
- [OpenAI Agents SDK Documentation](https://github.com/openai/openai-agents-python)

---

*End of Phase III Specification*
