"""CLI Interface - Command-line interface for the Todo Agent.

This module provides an interactive command-line interface for
interacting with the Todo Agent.
"""

import sys
from agents import Runner
from src.agent.config import validate_config, get_config_error
from src.agent.todo_agent import todo_agent


def display_welcome() -> None:
    """Display the welcome message and usage instructions."""
    print("=" * 50)
    print("           TODO AGENT ASSISTANT")
    print("=" * 50)
    print()
    print("I can help you manage your tasks. Try:")
    print('  - "Add a task to buy groceries"')
    print('  - "Show me my tasks"')
    print('  - "Mark task 1 as complete"')
    print('  - "Delete task 2"')
    print()
    print("Type 'exit' or 'quit' to end.")
    print()


def run_cli() -> None:
    """Run the interactive CLI loop.

    This function starts an interactive session where users can
    type natural language requests to manage their tasks.
    """
    # Validate configuration
    if not validate_config():
        error = get_config_error()
        print(f"Error: {error}")
        print("Please set the required environment variables.")
        print("See .env.example for details.")
        sys.exit(1)

    # Display welcome message
    display_welcome()

    # Main interaction loop
    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n\nGoodbye!")
            break

        # Check for exit commands
        if user_input.lower() in ("exit", "quit"):
            print("\nGoodbye!")
            break

        # Skip empty input
        if not user_input:
            continue

        try:
            # Run the agent with the user's input
            result = Runner.run_sync(todo_agent, user_input)
            print(f"\nAssistant: {result.final_output}\n")
        except Exception as e:
            print(f"\nError: An unexpected error occurred. Please try again.\n")


if __name__ == "__main__":
    run_cli()
