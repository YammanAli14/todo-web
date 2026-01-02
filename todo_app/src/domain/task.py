"""Task entity - Core domain object for the Todo application."""

from dataclasses import dataclass


@dataclass
class Task:
    """A task entity representing a single todo item.

    Attributes:
        id: Unique identifier, auto-assigned by repository.
        title: Task description, required, non-empty, max 200 chars.
        is_complete: Completion status, defaults to False.
    """

    id: int
    title: str
    is_complete: bool = False

    @staticmethod
    def validate_title(title: str) -> str:
        """Validate and return stripped title, or raise ValueError.

        Args:
            title: The title to validate.

        Returns:
            The stripped title if valid.

        Raises:
            ValueError: If title is empty, whitespace-only, or exceeds 200 chars.
        """
        stripped = title.strip()
        if not stripped:
            raise ValueError("Task title cannot be empty.")
        if len(stripped) > 200:
            raise ValueError("Task title must be 200 characters or less.")
        return stripped

    def toggle_complete(self) -> None:
        """Toggle the is_complete status between True and False."""
        self.is_complete = not self.is_complete
