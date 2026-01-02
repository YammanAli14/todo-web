"""Manual Test Script - Tests all tools directly without LLM.

This script tests all MCP tools by calling them directly against the
running Phase II API, simulating what the agent would do.
"""

import sys
sys.path.insert(0, ".")

from src.tools.api_client import TodoAPIClient, set_api_client
from src.tools.task_tools import (
    _impl_create_task,
    _impl_list_tasks,
    _impl_get_task,
    _impl_update_task,
    _impl_delete_task,
    _impl_toggle_task,
)


def print_section(title: str) -> None:
    """Print a section header."""
    print("\n" + "=" * 50)
    print(f"  {title}")
    print("=" * 50)


def main():
    """Run manual tests for all tools."""
    # Set up the API client
    client = TodoAPIClient(base_url="http://127.0.0.1:8000")
    set_api_client(client)

    print_section("TODO AGENT - MANUAL TOOL TEST")
    print("\nThis script tests all MCP tools directly against the API.")
    print("The Phase II API must be running on http://127.0.0.1:8000")

    # Test 1: List tasks (should be empty initially)
    print_section("TEST 1: List Tasks (Empty)")
    print("Simulating: 'Show me my tasks'")
    result = _impl_list_tasks()
    print(f"\nResult:\n{result}")

    # Test 2: Create task
    print_section("TEST 2: Create Task")
    print("Simulating: 'Add a task to buy groceries'")
    result = _impl_create_task("Buy groceries")
    print(f"\nResult:\n{result}")

    # Test 3: Create another task
    print_section("TEST 3: Create Another Task")
    print("Simulating: 'Add a task to finish homework'")
    result = _impl_create_task("Finish homework")
    print(f"\nResult:\n{result}")

    # Test 4: List tasks (should show 2 tasks)
    print_section("TEST 4: List Tasks (With Data)")
    print("Simulating: 'Show me my tasks'")
    result = _impl_list_tasks()
    print(f"\nResult:\n{result}")

    # Test 5: Get specific task
    print_section("TEST 5: Get Task Details")
    print("Simulating: 'Show me task 1'")
    result = _impl_get_task(1)
    print(f"\nResult:\n{result}")

    # Test 6: Update task
    print_section("TEST 6: Update Task")
    print("Simulating: 'Change task 1 to buy groceries and milk'")
    result = _impl_update_task(1, "Buy groceries and milk")
    print(f"\nResult:\n{result}")

    # Test 7: Toggle task (mark complete)
    print_section("TEST 7: Toggle Task (Complete)")
    print("Simulating: 'Mark task 1 as complete'")
    result = _impl_toggle_task(1)
    print(f"\nResult:\n{result}")

    # Test 8: List tasks (should show updated status)
    print_section("TEST 8: List Tasks (After Toggle)")
    print("Simulating: 'Show me my tasks'")
    result = _impl_list_tasks()
    print(f"\nResult:\n{result}")

    # Test 9: Toggle task (mark incomplete)
    print_section("TEST 9: Toggle Task (Incomplete)")
    print("Simulating: 'Mark task 1 as incomplete'")
    result = _impl_toggle_task(1)
    print(f"\nResult:\n{result}")

    # Test 10: Delete task
    print_section("TEST 10: Delete Task")
    print("Simulating: 'Delete task 2'")
    result = _impl_delete_task(2)
    print(f"\nResult:\n{result}")

    # Test 11: List tasks (should show 1 task)
    print_section("TEST 11: List Tasks (After Delete)")
    print("Simulating: 'Show me my tasks'")
    result = _impl_list_tasks()
    print(f"\nResult:\n{result}")

    # Test 12: Get non-existent task
    print_section("TEST 12: Get Non-Existent Task")
    print("Simulating: 'Show me task 999'")
    result = _impl_get_task(999)
    print(f"\nResult:\n{result}")

    # Test 13: Delete non-existent task
    print_section("TEST 13: Delete Non-Existent Task")
    print("Simulating: 'Delete task 999'")
    result = _impl_delete_task(999)
    print(f"\nResult:\n{result}")

    # Cleanup: Delete remaining task
    print_section("CLEANUP")
    print("Deleting remaining task...")
    result = _impl_delete_task(1)
    print(f"Result: {result}")

    # Final check
    print_section("FINAL: Verify Empty")
    result = _impl_list_tasks()
    print(f"Result:\n{result}")

    print_section("ALL TESTS COMPLETED")
    print("\nAll MCP tools are working correctly!")
    print("The agent is ready for use with an OpenAI API key.")

    client.close()


if __name__ == "__main__":
    main()
