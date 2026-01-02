"""Todo Agent - AI agent for task management.

This module defines the Todo Agent using the OpenAI Agents SDK.
The agent can understand natural language requests and perform
task operations using MCP tools.
"""

from agents import Agent
from src.agent.config import AGENT_INSTRUCTIONS, AGENT_MODEL
from src.tools.task_tools import (
    create_task,
    list_tasks,
    get_task,
    update_task,
    delete_task,
    toggle_task,
)


# Create the Todo Agent
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
        toggle_task,
    ],
)


def get_agent() -> Agent:
    """Get the Todo Agent instance.

    Returns:
        The configured Todo Agent.
    """
    return todo_agent
