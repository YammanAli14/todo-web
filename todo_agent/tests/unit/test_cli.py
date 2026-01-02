"""Unit Tests for CLI Interface.

This module contains unit tests for the CLI interface.
"""

import pytest
from unittest.mock import patch, MagicMock
from io import StringIO


class TestCLIFunctions:
    """Tests for CLI helper functions."""

    def test_display_welcome(self, capsys):
        """Test that welcome message is displayed correctly."""
        from src.cli.main import display_welcome

        display_welcome()

        captured = capsys.readouterr()
        assert "TODO AGENT ASSISTANT" in captured.out
        assert "Add a task" in captured.out
        assert "Show me my tasks" in captured.out
        assert "exit" in captured.out or "quit" in captured.out


class TestCLIRun:
    """Tests for CLI run_cli function."""

    def test_cli_exits_on_missing_config(self, capsys):
        """Test that CLI exits when config is invalid."""
        from src.cli.main import run_cli
        import src.agent.config as config_module

        # Save original value
        original_key = config_module.OPENAI_API_KEY
        config_module.OPENAI_API_KEY = None

        with pytest.raises(SystemExit) as exc_info:
            run_cli()

        assert exc_info.value.code == 1

        # Restore
        config_module.OPENAI_API_KEY = original_key

    def test_cli_exit_command(self, monkeypatch, capsys):
        """Test that 'exit' command exits the CLI."""
        from src.cli.main import run_cli
        import src.agent.config as config_module

        # Set a test API key
        original_key = config_module.OPENAI_API_KEY
        config_module.OPENAI_API_KEY = "test-key"

        # Mock input to return 'exit'
        inputs = iter(["exit"])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))

        run_cli()

        captured = capsys.readouterr()
        assert "Goodbye" in captured.out

        # Restore
        config_module.OPENAI_API_KEY = original_key

    def test_cli_quit_command(self, monkeypatch, capsys):
        """Test that 'quit' command exits the CLI."""
        from src.cli.main import run_cli
        import src.agent.config as config_module

        # Set a test API key
        original_key = config_module.OPENAI_API_KEY
        config_module.OPENAI_API_KEY = "test-key"

        # Mock input to return 'quit'
        inputs = iter(["quit"])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))

        run_cli()

        captured = capsys.readouterr()
        assert "Goodbye" in captured.out

        # Restore
        config_module.OPENAI_API_KEY = original_key

    def test_cli_empty_input_continues(self, monkeypatch, capsys):
        """Test that empty input continues the loop."""
        from src.cli.main import run_cli
        import src.agent.config as config_module

        # Set a test API key
        original_key = config_module.OPENAI_API_KEY
        config_module.OPENAI_API_KEY = "test-key"

        # Mock input: empty, then exit
        inputs = iter(["", "  ", "exit"])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))

        run_cli()

        captured = capsys.readouterr()
        assert "Goodbye" in captured.out

        # Restore
        config_module.OPENAI_API_KEY = original_key

    def test_cli_keyboard_interrupt(self, monkeypatch, capsys):
        """Test that KeyboardInterrupt exits gracefully."""
        from src.cli.main import run_cli
        import src.agent.config as config_module

        # Set a test API key
        original_key = config_module.OPENAI_API_KEY
        config_module.OPENAI_API_KEY = "test-key"

        # Mock input to raise KeyboardInterrupt
        def raise_interrupt(_):
            raise KeyboardInterrupt()

        monkeypatch.setattr("builtins.input", raise_interrupt)

        run_cli()

        captured = capsys.readouterr()
        assert "Goodbye" in captured.out

        # Restore
        config_module.OPENAI_API_KEY = original_key

    def test_cli_eof_error(self, monkeypatch, capsys):
        """Test that EOFError exits gracefully."""
        from src.cli.main import run_cli
        import src.agent.config as config_module

        # Set a test API key
        original_key = config_module.OPENAI_API_KEY
        config_module.OPENAI_API_KEY = "test-key"

        # Mock input to raise EOFError
        def raise_eof(_):
            raise EOFError()

        monkeypatch.setattr("builtins.input", raise_eof)

        run_cli()

        captured = capsys.readouterr()
        assert "Goodbye" in captured.out

        # Restore
        config_module.OPENAI_API_KEY = original_key

    def test_cli_agent_interaction(self, monkeypatch, capsys):
        """Test that agent processes user input."""
        from src.cli.main import run_cli
        import src.agent.config as config_module

        # Set a test API key
        original_key = config_module.OPENAI_API_KEY
        config_module.OPENAI_API_KEY = "test-key"

        # Mock input: a command, then exit
        inputs = iter(["list my tasks", "exit"])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))

        # Mock the Runner to avoid actual API calls
        mock_result = MagicMock()
        mock_result.final_output = "No tasks found. Your todo list is empty."

        with patch("src.cli.main.Runner") as mock_runner:
            mock_runner.run_sync.return_value = mock_result
            run_cli()

        captured = capsys.readouterr()
        assert "Assistant:" in captured.out
        assert "No tasks found" in captured.out or "empty" in captured.out

        # Restore
        config_module.OPENAI_API_KEY = original_key

    def test_cli_handles_agent_error(self, monkeypatch, capsys):
        """Test that agent errors are handled gracefully."""
        from src.cli.main import run_cli
        import src.agent.config as config_module

        # Set a test API key
        original_key = config_module.OPENAI_API_KEY
        config_module.OPENAI_API_KEY = "test-key"

        # Mock input: a command, then exit
        inputs = iter(["list my tasks", "exit"])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))

        # Mock the Runner to raise an exception
        with patch("src.cli.main.Runner") as mock_runner:
            mock_runner.run_sync.side_effect = Exception("API Error")
            run_cli()

        captured = capsys.readouterr()
        assert "Error" in captured.out

        # Restore
        config_module.OPENAI_API_KEY = original_key
