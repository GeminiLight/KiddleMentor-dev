"""Unit tests for BaseAgent."""

from unittest.mock import MagicMock, patch

import pytest
from langchain_core.language_models.fake_chat_models import FakeChatModel

from gen_mentor.agents.base_agent import BaseAgent


class TestBaseAgent:
    """Tests for BaseAgent class."""

    def test_agent_initialization(self, mock_llm):
        """Test basic agent initialization."""
        agent = BaseAgent(
            model=mock_llm,
            system_prompt="You are a helpful assistant.",
            tools=[],
        )

        assert agent._model is not None
        assert agent._system_prompt == "You are a helpful assistant."
        assert agent._tools == []

    def test_agent_with_tools(self, mock_llm, mock_file_tool):
        """Test agent initialization with tools."""
        agent = BaseAgent(
            model=mock_llm,
            system_prompt="Test",
            tools=[mock_file_tool],
        )

        assert len(agent._tools) == 1

    def test_set_prompts(self, mock_llm):
        """Test setting/updating prompts."""
        agent = BaseAgent(
            model=mock_llm,
            system_prompt="Original prompt",
            tools=[],
        )

        agent.set_prompts(system_prompt="Updated prompt")

        assert agent._system_prompt == "Updated prompt"

    def test_build_prompt(self, mock_llm):
        """Test building prompt from variables."""
        agent = BaseAgent(
            model=mock_llm,
            system_prompt="Test",
            tools=[],
        )

        task_prompt = "Hello {name}, you are {age} years old."
        variables = {"name": "Alice", "age": 25}

        prompt = agent._build_prompt(variables, task_prompt=task_prompt)

        assert "messages" in prompt
        assert len(prompt["messages"]) == 1
        assert "Alice" in prompt["messages"][0]["content"]

    def test_invoke_basic(self, mock_llm):
        """Test basic agent invocation."""
        agent = BaseAgent(
            model=mock_llm,
            system_prompt="Test",
            tools=[],
            jsonalize_output=False,
        )

        task_prompt = "Say hello to {name}."
        input_dict = {"name": "Bob"}

        with patch.object(agent, '_agent') as mock_agent:
            mock_agent.invoke.return_value = {"messages": [{"content": "Hello Bob!"}]}

            result = agent.invoke(input_dict, task_prompt=task_prompt)

            mock_agent.invoke.assert_called_once()

    def test_invoke_with_json_output(self, mock_llm_json):
        """Test agent invocation with JSON output."""
        agent = BaseAgent(
            model=mock_llm_json,
            system_prompt="Test",
            tools=[],
            jsonalize_output=True,
        )

        task_prompt = "Return JSON data."
        input_dict = {}

        with patch.object(agent, '_agent') as mock_agent:
            mock_agent.invoke.return_value = {
                "messages": [{"content": '{"result": "test"}'}]
            }

            result = agent.invoke(input_dict, task_prompt=task_prompt)

            mock_agent.invoke.assert_called_once()

    def test_agent_kwargs_filtering(self, mock_llm):
        """Test that only valid agent kwargs are passed."""
        agent = BaseAgent(
            model=mock_llm,
            system_prompt="Test",
            tools=[],
            debug=True,  # Valid
            invalid_arg="should_be_filtered",  # Invalid
        )

        assert "debug" in agent._agent_kwargs
        assert "invalid_arg" not in agent._agent_kwargs

    def test_exclude_think_option(self, mock_llm):
        """Test exclude_think option."""
        agent = BaseAgent(
            model=mock_llm,
            system_prompt="Test",
            tools=[],
            exclude_think=False,
        )

        assert agent.exclude_think is False

    def test_jsonalize_output_option(self, mock_llm):
        """Test jsonalize_output option."""
        agent = BaseAgent(
            model=mock_llm,
            system_prompt="Test",
            tools=[],
            jsonalize_output=False,
        )

        assert agent.jsonalize_output is False

    def test_missing_task_prompt_raises_error(self, mock_llm):
        """Test that missing task_prompt raises assertion error."""
        agent = BaseAgent(
            model=mock_llm,
            system_prompt="Test",
            tools=[],
        )

        with pytest.raises(AssertionError):
            agent._build_prompt({"name": "Test"}, task_prompt=None)
