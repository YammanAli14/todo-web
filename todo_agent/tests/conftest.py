"""Test Fixtures - Shared fixtures for all tests.

This module provides pytest fixtures used across unit and integration tests.
"""

import pytest
from unittest.mock import MagicMock, patch
from src.tools.api_client import TodoAPIClient


@pytest.fixture
def mock_api_client():
    """Create a mock API client.

    Returns:
        A MagicMock instance configured as a TodoAPIClient.
    """
    return MagicMock(spec=TodoAPIClient)


@pytest.fixture
def sample_task():
    """Create a sample task dictionary.

    Returns:
        A dictionary representing a sample task.
    """
    return {
        "id": 1,
        "title": "Buy groceries",
        "is_complete": False,
        "created_at": "2025-12-28T10:00:00Z",
        "updated_at": "2025-12-28T10:00:00Z"
    }


@pytest.fixture
def sample_task_complete():
    """Create a sample completed task dictionary.

    Returns:
        A dictionary representing a completed task.
    """
    return {
        "id": 2,
        "title": "Finish homework",
        "is_complete": True,
        "created_at": "2025-12-28T09:00:00Z",
        "updated_at": "2025-12-28T11:00:00Z"
    }


@pytest.fixture
def sample_task_list(sample_task, sample_task_complete):
    """Create a sample list of tasks.

    Returns:
        A list of task dictionaries.
    """
    return [sample_task, sample_task_complete]


@pytest.fixture
def patched_api_client(mock_api_client):
    """Patch the get_api_client function to return a mock.

    This fixture patches the global get_api_client function in task_tools
    to return the mock_api_client fixture.

    Yields:
        The mock API client.
    """
    with patch("src.tools.task_tools.get_api_client", return_value=mock_api_client):
        yield mock_api_client
