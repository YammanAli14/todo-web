# Todo Agent - Phase III

AI-powered task management assistant using OpenAI Agents SDK with MCP tools.

## Overview

Todo Agent is a conversational AI assistant that helps users manage their todo list using natural language. It connects to the Phase II Todo API and provides an interactive command-line interface.

## Features

- **Natural Language Understanding**: Describe tasks in plain English
- **Full CRUD Operations**: Create, read, update, and delete tasks
- **Task Status Management**: Mark tasks as complete or incomplete
- **Conversational Interface**: Interactive CLI for seamless task management

## Requirements

- Python 3.11+
- OpenAI API key
- Phase II Todo API running (default: http://localhost:8000)

## Installation

1. Navigate to the project directory:
   ```bash
   cd todo_agent
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv

   # Windows
   venv\Scripts\activate

   # macOS/Linux
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   ```bash
   # Copy the example file
   cp .env.example .env

   # Edit .env and add your OpenAI API key
   OPENAI_API_KEY=your-api-key-here
   ```

## Configuration

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `OPENAI_API_KEY` | Yes | - | Your OpenAI API key |
| `API_BASE_URL` | No | http://localhost:8000 | Todo API base URL |

## Running the Agent

1. Ensure the Phase II Todo API is running:
   ```bash
   # In the todo_api directory
   cd ../todo_api
   uvicorn src.presentation.api:app --reload
   ```

2. Start the Todo Agent:
   ```bash
   # In the todo_agent directory
   python main.py
   ```

## Usage Examples

Once the agent is running, you can interact with it using natural language:

### Creating Tasks
```
You: Add a task to buy groceries
Assistant: Task created successfully!
  ID: 1
  Title: buy groceries
  Status: Incomplete
```

### Listing Tasks
```
You: Show me my tasks
Assistant: Your tasks:
  [ ] Task 1: buy groceries
  [x] Task 2: finish homework
```

### Updating Tasks
```
You: Change task 1 to buy groceries and milk
Assistant: Task 1 updated successfully!
  New title: buy groceries and milk
```

### Toggling Task Status
```
You: Mark task 1 as complete
Assistant: Task 1 is now marked as complete.
```

### Deleting Tasks
```
You: Delete task 2
Assistant: Task 2 has been deleted successfully.
```

### Viewing Task Details
```
You: Show me task 1
Assistant: Task 1:
  Title: buy groceries
  Status: Complete
  Created: 2025-12-28T10:00:00Z
  Updated: 2025-12-28T11:00:00Z
```

### Exiting
```
You: exit
Goodbye!
```

## Running Tests

Run the test suite:
```bash
pytest
```

Run with coverage:
```bash
pytest --cov=src --cov-report=term-missing
```

## Project Structure

```
todo_agent/
├── src/
│   ├── __init__.py
│   ├── agent/
│   │   ├── __init__.py
│   │   ├── config.py           # Agent configuration
│   │   └── todo_agent.py       # Agent definition
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── api_client.py       # HTTP client for API
│   │   └── task_tools.py       # MCP tool definitions
│   └── cli/
│       ├── __init__.py
│       └── main.py             # CLI interface
├── tests/
│   ├── __init__.py
│   ├── conftest.py             # Test fixtures
│   ├── unit/
│   │   ├── __init__.py
│   │   ├── test_api_client.py
│   │   └── test_tools.py
│   └── integration/
│       ├── __init__.py
│       └── test_agent.py
├── main.py                     # Entry point
├── requirements.txt
├── .env.example
└── README.md
```

## MCP Tools

The agent uses the following MCP (Model Context Protocol) tools:

| Tool | Description | Parameters |
|------|-------------|------------|
| `create_task` | Create a new task | `title: str` |
| `list_tasks` | List all tasks | None |
| `get_task` | Get task details | `task_id: int` |
| `update_task` | Update task title | `task_id: int, title: str` |
| `delete_task` | Delete a task | `task_id: int` |
| `toggle_task` | Toggle completion | `task_id: int` |

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                       User                              │
│                         │                               │
│                    Natural Language                     │
│                         ▼                               │
│  ┌─────────────────────────────────────────────────┐   │
│  │                   CLI Interface                  │   │
│  │                    (main.py)                     │   │
│  └─────────────────────────────────────────────────┘   │
│                         │                               │
│                         ▼                               │
│  ┌─────────────────────────────────────────────────┐   │
│  │                  Todo Agent                      │   │
│  │            (OpenAI Agents SDK)                   │   │
│  │                                                  │   │
│  │  ┌────────────────────────────────────────────┐ │   │
│  │  │              MCP Tools                     │ │   │
│  │  │  create_task │ list_tasks │ get_task      │ │   │
│  │  │  update_task │ delete_task │ toggle_task  │ │   │
│  │  └────────────────────────────────────────────┘ │   │
│  └─────────────────────────────────────────────────┘   │
│                         │                               │
│                    HTTP (httpx)                         │
│                         ▼                               │
│  ┌─────────────────────────────────────────────────┐   │
│  │              Phase II Todo API                   │   │
│  │              (FastAPI + SQLite)                  │   │
│  └─────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

## License

This project is part of the Evolution of Todo series.
