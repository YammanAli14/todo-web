"""Integration Tests for Todo Agent.

This module contains integration tests that verify the agent
is correctly configured with all tools.
"""

import pytest


class TestAgentInitialization:
    """Tests for agent initialization and configuration."""

    def test_agent_initialization(self):
        """Test that the agent initializes correctly."""
        from src.agent.todo_agent import todo_agent

        assert todo_agent is not None
        assert todo_agent.name == "todo_agent"

    def test_agent_has_all_tools(self):
        """Test that the agent has all 6 required tools."""
        from src.agent.todo_agent import todo_agent

        tool_names = [tool.name for tool in todo_agent.tools]

        assert "create_task" in tool_names
        assert "list_tasks" in tool_names
        assert "get_task" in tool_names
        assert "update_task" in tool_names
        assert "delete_task" in tool_names
        assert "toggle_task" in tool_names
        assert len(todo_agent.tools) == 6

    def test_agent_has_instructions(self):
        """Test that the agent has instructions configured."""
        from src.agent.todo_agent import todo_agent

        assert todo_agent.instructions is not None
        assert len(todo_agent.instructions) > 0
        assert "task" in todo_agent.instructions.lower()

    def test_agent_model_configured(self):
        """Test that the agent has a model configured."""
        from src.agent.todo_agent import todo_agent

        assert todo_agent.model is not None
        assert todo_agent.model == "gpt-4o-mini"


class TestAgentConfiguration:
    """Tests for agent configuration module."""

    def test_config_loads_defaults(self):
        """Test that config loads with defaults."""
        from src.agent.config import API_BASE_URL, AGENT_MODEL, AGENT_INSTRUCTIONS

        assert API_BASE_URL == "http://localhost:8000"
        assert AGENT_MODEL == "gpt-4o-mini"
        assert AGENT_INSTRUCTIONS is not None

    def test_config_validation_without_key(self, monkeypatch):
        """Test config validation fails without API key."""
        import src.agent.config as config_module

        # Temporarily set OPENAI_API_KEY to None
        original_key = config_module.OPENAI_API_KEY
        config_module.OPENAI_API_KEY = None

        assert config_module.validate_config() is False
        assert config_module.get_config_error() is not None
        assert "OPENAI_API_KEY" in config_module.get_config_error()

        # Restore
        config_module.OPENAI_API_KEY = original_key

    def test_config_validation_with_key(self, monkeypatch):
        """Test config validation passes with API key."""
        import src.agent.config as config_module

        # Set a test key
        original_key = config_module.OPENAI_API_KEY
        config_module.OPENAI_API_KEY = "test-key"

        assert config_module.validate_config() is True
        assert config_module.get_config_error() is None

        # Restore
        config_module.OPENAI_API_KEY = original_key


class TestToolsExport:
    """Tests for tools module exports."""

    def test_all_tools_exported(self):
        """Test that ALL_TOOLS contains all tools."""
        from src.tools.task_tools import ALL_TOOLS

        assert len(ALL_TOOLS) == 6

        tool_names = [tool.name for tool in ALL_TOOLS]
        assert "create_task" in tool_names
        assert "list_tasks" in tool_names
        assert "get_task" in tool_names
        assert "update_task" in tool_names
        assert "delete_task" in tool_names
        assert "toggle_task" in tool_names
