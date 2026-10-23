"""Unit tests for LLM factory."""

from unittest.mock import patch

import pytest
from omegaconf import OmegaConf
from openai import OpenAIError

from gen_mentor.core.llm.factory import LLMFactory


class TestLLMFactory:
    """Tests for LLM factory."""

    def test_factory_initialization(self):
        """Test LLM factory initialization."""
        factory = LLMFactory()
        with patch("gen_mentor.core.llm.factory.init_chat_model") as init:
            assert factory.create(model="gpt-4", model_provider="openai") is init.return_value

    def test_create_llm_with_api_key(self, sample_config):
        """Test creating LLM with API key from config."""
        with patch("gen_mentor.core.llm.factory.init_chat_model") as init:
            result = LLMFactory.create(
                model="gpt-4", model_provider="openai", api_key=sample_config.get_api_key("gpt-4")
            )
            init.assert_called_once_with(model="gpt-4", model_provider="openai", temperature=0, api_key="sk-test-key")
            assert result is init.return_value

    def test_create_llm_deepseek(self, sample_config):
        """Test creating DeepSeek LLM."""
        with patch("gen_mentor.core.llm.factory.init_chat_model") as init:
            LLMFactory.create(
                model="deepseek-chat",
                model_provider=sample_config.get_provider_name("deepseek-chat"),
                base_url=sample_config.get_api_base("deepseek-chat"),
                api_key=sample_config.get_api_key("deepseek-chat"),
            )
            init.assert_called_once_with(
                model="deepseek-chat",
                model_provider="deepseek",
                temperature=0,
                base_url="https://api.deepseek.com",
                api_key="test-deepseek-key",
            )

    def test_provider_matching(self, sample_config):
        """Test provider matching by model name."""
        assert sample_config.get_provider_name("gpt-4") == "openai"
        assert sample_config.get_provider_name("deepseek-chat") == "deepseek"

    def test_missing_api_key_raises_error(self, monkeypatch):
        """Test that missing API key raises error."""
        monkeypatch.delenv("OPENAI_API_KEY", raising=False)
        with pytest.raises(OpenAIError, match="api_key"):
            LLMFactory.create(model="gpt-4", model_provider="openai")

    def test_default_model_creation(self):
        """Test creating LLM with default model."""
        with patch("gen_mentor.core.llm.factory.init_chat_model") as init:
            LLMFactory.create()
            init.assert_called_once_with(model="claude-3-5-sonnet-20241022", model_provider="anthropic", temperature=0)

    def test_temperature_and_max_tokens(self):
        """Test that temperature and max_tokens are passed correctly."""
        with patch("gen_mentor.core.llm.factory.init_chat_model") as init:
            LLMFactory.create(model="deepseek-chat", model_provider="deepseek", temperature=0.7, max_tokens=4096)
            init.assert_called_once_with(
                model="deepseek-chat", model_provider="deepseek", temperature=0.7, max_tokens=4096
            )

    def test_openai_compatible_local_server_without_a_key(self):
        with patch("gen_mentor.core.llm.factory.init_chat_model") as init:
            LLMFactory.create(model="local", model_provider="openai", base_url="http://localhost:8000/v1")
            assert init.call_args.kwargs["api_key"] == "dummy-key-for-vllm"

    def test_workflow_configuration(self):
        config = OmegaConf.create(
            {"model_name": "custom-model", "model_provider": "openai", "base_url": "https://example.org/v1"}
        )
        with patch("gen_mentor.core.llm.factory.init_chat_model") as init:
            assert LLMFactory.from_config(config) is init.return_value
            init.assert_called_once_with(
                model="custom-model", model_provider="openai", base_url="https://example.org/v1", temperature=0
            )

    def test_provider_errors_are_not_hidden(self):
        with patch("gen_mentor.core.llm.factory.init_chat_model", side_effect=ValueError("Unsupported provider")):
            with pytest.raises(ValueError, match="Unsupported provider"):
                LLMFactory.create(model="custom", model_provider="missing")
