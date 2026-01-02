"""Agent Configuration - Settings and configuration for the Todo Agent.

This module loads environment variables and defines agent configuration
including instructions and model settings.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Required: OpenAI API Key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Optional: Todo API Base URL (defaults to localhost)
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")

# Agent model configuration
AGENT_MODEL = "gpt-4o-mini"

# Agent instructions
AGENT_INSTRUCTIONS = """You are a helpful task management assistant.

Your role is to help users manage their todo list by:
- Creating new tasks
- Viewing existing tasks
- Updating task titles
- Deleting tasks
- Marking tasks as complete or incomplete

Guidelines:
1. Always confirm completed actions with specific details
2. When listing tasks, format them clearly with status indicators
3. If a task is not found, explain this clearly to the user
4. Be concise but helpful in your responses
5. If the user's request is ambiguous, ask for clarification

Examples of requests you can handle:
- "Add a task to buy groceries"
- "Show me my tasks" or "List all tasks"
- "What is task 1?" or "Show me task 1"
- "Change task 1 to buy groceries and milk"
- "Delete task 3" or "Remove task 3"
- "Mark task 1 as complete"
- "Mark task 2 as incomplete"
"""


def validate_config() -> bool:
    """Validate that required configuration is present.

    Returns:
        True if configuration is valid, False otherwise.
    """
    if not OPENAI_API_KEY:
        return False
    return True


def get_config_error() -> str | None:
    """Get configuration error message if any.

    Returns:
        Error message string if configuration is invalid, None otherwise.
    """
    if not OPENAI_API_KEY:
        return "OPENAI_API_KEY environment variable is not set."
    return None
