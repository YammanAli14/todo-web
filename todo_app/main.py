"""Todo Application - Phase I Entry Point.

A simple in-memory console todo application.
"""

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
