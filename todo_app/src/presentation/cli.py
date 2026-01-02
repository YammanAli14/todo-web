"""TodoCLI - Command-line interface for the Todo application."""

from src.application.task_service import TaskService


class TodoCLI:
    """Command-line interface for the Todo application.

    Provides a menu-driven interface for task management operations.
    """

    def __init__(self, service: TaskService) -> None:
        """Initialize CLI with task service.

        Args:
            service: The task service for business operations.
        """
        self._service = service
        self._running = True

    def run(self) -> None:
        """Run the main application loop."""
        while self._running:
            self.display_menu()
            choice = self.get_menu_choice()
            if choice is not None:
                self._handle_choice(choice)

    def display_menu(self) -> None:
        """Display the main menu."""
        print()
        print("=" * 40)
        print("          TODO APPLICATION")
        print("=" * 40)
        print()
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Update Task")
        print("4. Delete Task")
        print("5. Toggle Complete")
        print("6. Exit")
        print()

    def get_menu_choice(self) -> int | None:
        """Get and validate menu choice from user.

        Returns:
            Valid menu choice (1-6) or None if invalid.
        """
        try:
            choice_str = input("Enter your choice (1-6): ")
            choice = int(choice_str)
            if 1 <= choice <= 6:
                return choice
            print()
            print("Error: Invalid choice. Please enter a number between 1 and 6.")
            return None
        except ValueError:
            print()
            print("Error: Invalid input. Please enter a number between 1 and 6.")
            return None

    def _handle_choice(self, choice: int) -> None:
        """Route to appropriate handler based on menu choice.

        Args:
            choice: The validated menu choice (1-6).
        """
        handlers = {
            1: self.handle_add_task,
            2: self.handle_view_tasks,
            3: self.handle_update_task,
            4: self.handle_delete_task,
            5: self.handle_toggle_complete,
            6: self.handle_exit,
        }
        handlers[choice]()

    def _get_task_id(self, prompt: str) -> int | None:
        """Get and validate task ID from user.

        Args:
            prompt: The prompt message to display.

        Returns:
            Valid task ID or None if invalid format.
        """
        try:
            id_str = input(prompt)
            return int(id_str)
        except ValueError:
            print()
            print("Error: Invalid input. Please enter a numeric ID.")
            return None

    def handle_add_task(self) -> None:
        """Handle add task operation."""
        print()
        print("--- Add Task ---")
        title = input("Enter task title: ")
        try:
            task = self._service.add_task(title)
            print()
            print("Task added successfully!")
            print(f"ID: {task.id}")
            print(f"Title: {task.title}")
            print("Status: Incomplete")
        except ValueError as e:
            print()
            print(f"Error: {e}")

    def handle_view_tasks(self) -> None:
        """Handle view tasks operation."""
        print()
        print("--- Task List ---")
        tasks = self._service.get_all_tasks()
        if not tasks:
            print("No tasks found.")
            return
        complete_count = 0
        for task in tasks:
            status = "[X]" if task.is_complete else "[ ]"
            if task.is_complete:
                complete_count += 1
            print(f"{status} {task.id}. {task.title}")
        incomplete_count = len(tasks) - complete_count
        print()
        print(f"Total: {len(tasks)} tasks ({complete_count} complete, {incomplete_count} incomplete)")

    def handle_update_task(self) -> None:
        """Handle update task operation."""
        print()
        print("--- Update Task ---")
        task_id = self._get_task_id("Enter task ID: ")
        if task_id is None:
            return
        new_title = input("Enter new title: ")
        try:
            task = self._service.update_task(task_id, new_title)
            if task is None:
                print()
                print(f"Error: Task with ID {task_id} not found.")
                return
            print()
            print("Task updated successfully!")
            print(f"ID: {task.id}")
            print(f"New Title: {task.title}")
        except ValueError as e:
            print()
            print(f"Error: {e}")

    def handle_delete_task(self) -> None:
        """Handle delete task operation."""
        print()
        print("--- Delete Task ---")
        task_id = self._get_task_id("Enter task ID: ")
        if task_id is None:
            return
        task = self._service.delete_task(task_id)
        if task is None:
            print()
            print(f"Error: Task with ID {task_id} not found.")
            return
        print()
        print("Task deleted successfully!")
        print(f'Deleted: "{task.title}"')

    def handle_toggle_complete(self) -> None:
        """Handle toggle complete operation."""
        print()
        print("--- Toggle Complete ---")
        task_id = self._get_task_id("Enter task ID: ")
        if task_id is None:
            return
        task = self._service.toggle_task_complete(task_id)
        if task is None:
            print()
            print(f"Error: Task with ID {task_id} not found.")
            return
        status = "Complete" if task.is_complete else "Incomplete"
        print()
        print("Task status updated!")
        print(f"ID: {task.id}")
        print(f"Title: {task.title}")
        print(f"Status: {status}")

    def handle_exit(self) -> None:
        """Handle exit operation."""
        print()
        print("Thank you for using Todo Application. Goodbye!")
        self._running = False
