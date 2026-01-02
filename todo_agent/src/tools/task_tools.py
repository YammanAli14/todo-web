"""MCP Task Tools - Function tools for task operations.

This module defines all MCP tools for task management operations.
Each tool is decorated with @function_tool from the OpenAI Agents SDK.

The implementation is split into two parts:
1. Core implementation functions (_impl_*) for business logic (testable)
2. Tool-decorated functions that wrap the implementations
"""

from agents import function_tool
from src.tools.api_client import get_api_client


def _format_task(task: dict) -> str:
    """Format a single task for display.

    Args:
        task: Task dictionary from the API.

    Returns:
        Formatted task string.
    """
    status = "[x]" if task["is_complete"] else "[ ]"
    return f"{status} Task {task['id']}: {task['title']}"


def _format_task_detail(task: dict) -> str:
    """Format a task with full details.

    Args:
        task: Task dictionary from the API.

    Returns:
        Formatted task detail string.
    """
    status = "Complete" if task["is_complete"] else "Incomplete"
    return (
        f"Task {task['id']}:\n"
        f"  Title: {task['title']}\n"
        f"  Status: {status}\n"
        f"  Created: {task['created_at']}\n"
        f"  Updated: {task['updated_at']}"
    )


# ============================================================================
# Core Implementation Functions (testable without decorator)
# ============================================================================

def _impl_create_task(title: str) -> str:
    """Implementation for create_task tool."""
    client = get_api_client()
    try:
        task = client.create_task(title)
        return (
            f"Task created successfully!\n"
            f"  ID: {task['id']}\n"
            f"  Title: {task['title']}\n"
            f"  Status: Incomplete"
        )
    except ValueError as e:
        return f"Error: {e}"
    except Exception as e:
        return f"Error creating task: Unable to connect to task service."


def _impl_list_tasks() -> str:
    """Implementation for list_tasks tool."""
    client = get_api_client()
    try:
        tasks = client.list_tasks()
        if not tasks:
            return "No tasks found. Your todo list is empty."

        lines = ["Your tasks:"]
        for task in tasks:
            lines.append(f"  {_format_task(task)}")
        return "\n".join(lines)
    except Exception as e:
        return f"Error listing tasks: Unable to connect to task service."


def _impl_get_task(task_id: int) -> str:
    """Implementation for get_task tool."""
    client = get_api_client()
    try:
        task = client.get_task(task_id)
        if task is None:
            return f"Error: Task with ID {task_id} was not found."
        return _format_task_detail(task)
    except Exception as e:
        return f"Error getting task: Unable to connect to task service."


def _impl_update_task(task_id: int, title: str) -> str:
    """Implementation for update_task tool."""
    client = get_api_client()
    try:
        task = client.update_task(task_id, title)
        if task is None:
            return f"Error: Task with ID {task_id} was not found."
        return (
            f"Task {task_id} updated successfully!\n"
            f"  New title: {task['title']}"
        )
    except ValueError as e:
        return f"Error: {e}"
    except Exception as e:
        return f"Error updating task: Unable to connect to task service."


def _impl_delete_task(task_id: int) -> str:
    """Implementation for delete_task tool."""
    client = get_api_client()
    try:
        deleted = client.delete_task(task_id)
        if not deleted:
            return f"Error: Task with ID {task_id} was not found."
        return f"Task {task_id} has been deleted successfully."
    except Exception as e:
        return f"Error deleting task: Unable to connect to task service."


def _impl_toggle_task(task_id: int) -> str:
    """Implementation for toggle_task tool."""
    client = get_api_client()
    try:
        task = client.toggle_task(task_id)
        if task is None:
            return f"Error: Task with ID {task_id} was not found."
        status = "complete" if task["is_complete"] else "incomplete"
        return f"Task {task_id} is now marked as {status}."
    except Exception as e:
        return f"Error toggling task: Unable to connect to task service."


# ============================================================================
# Tool-Decorated Functions (for agent use)
# ============================================================================

@function_tool
def create_task(title: str) -> str:
    """Create a new task with the given title.

    The task will be created as incomplete by default.

    Args:
        title: The title of the task to create (max 200 characters).

    Returns:
        A message confirming the task was created with its details.
    """
    return _impl_create_task(title)


@function_tool
def list_tasks() -> str:
    """List all tasks in the todo list, ordered by ID.

    Returns:
        A formatted list of all tasks with their status,
        or a message if the list is empty.
    """
    return _impl_list_tasks()


@function_tool
def get_task(task_id: int) -> str:
    """Get details of a specific task by its ID.

    Args:
        task_id: The ID of the task to retrieve.

    Returns:
        The task details, or an error message if not found.
    """
    return _impl_get_task(task_id)


@function_tool
def update_task(task_id: int, title: str) -> str:
    """Update the title of an existing task.

    Args:
        task_id: The ID of the task to update.
        title: The new title for the task (max 200 characters).

    Returns:
        A message confirming the update, or an error if not found.
    """
    return _impl_update_task(task_id, title)


@function_tool
def delete_task(task_id: int) -> str:
    """Delete a task by its ID.

    Args:
        task_id: The ID of the task to delete.

    Returns:
        A message confirming deletion, or an error if not found.
    """
    return _impl_delete_task(task_id)


@function_tool
def toggle_task(task_id: int) -> str:
    """Toggle the completion status of a task.

    If the task is incomplete, it will be marked as complete.
    If the task is complete, it will be marked as incomplete.

    Args:
        task_id: The ID of the task to toggle.

    Returns:
        A message with the new status, or an error if not found.
    """
    return _impl_toggle_task(task_id)


# Export all tools for easy importing
ALL_TOOLS = [
    create_task,
    list_tasks,
    get_task,
    update_task,
    delete_task,
    toggle_task,
]
