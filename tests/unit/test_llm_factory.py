"""Unit tests for LLM factory."""

import os
from unittest.mock import patch, MagicMock

import pytest

from gen_mentor.config import load_config_from_dict
from gen_mentor.core.llm.factory import LLMFactory


class TestLLMFactory:
    """Tests for LLM factory."""

    def test_factory_initialization(self, sample_config):
        """Test LLM factory initialization."""
        factory = LLMFactory(config=sample_config)

        assert factory.config is not None

    def test_create_llm_with_api_key(self, sample_config):
        """Test creating LLM with API key from config."""
        with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}):
            with patch('gen_mentor.core.llm.factory.ChatOpenAI') as mock_openai:
                mock_openai.return_value = MagicMock()

                factory = LLMFactory(config=sample_config)
                llm = factory.create_llm(model="gpt-4")

                mock_openai.assert_called_once()

    def test_create_llm_deepseek(self, sample_config):
        """Test creating DeepSeek LLM."""
        with patch.dict(os.environ, {"DEEPSEEK_API_KEY": "test-key"}):
            with patch('gen_mentor.core.llm.factory.ChatOpenAI') as mock_chat:
                mock_chat.return_value = MagicMock()

                factory = LLMFactory(config=sample_config)
                llm = factory.create_llm(model="deepseek-chat")

                mock_chat.assert_called_once()

    def test_provider_matching(self, sample_config):
        """Test provider matching by model name."""
        factory = LLMFactory(config=sample_config)

        provider = factory._match_provider("gpt-4")
        assert provider == "openai"

        provider = factory._match_provider("deepseek-chat")
        assert provider == "deepseek"

    def test_missing_api_key_raises_error(self, sample_config):
        """Test that missing API key raises error."""
        with patch.dict(os.environ, {}, clear=True):
            factory = LLMFactory(config=sample_config)

            with pytest.raises((ValueError, KeyError)):
                factory.create_llm(model="gpt-4")

    def test_default_model_creation(self, sample_config):
        """Test creating LLM with default model."""
        with patch.dict(os.environ, {"DEEPSEEK_API_KEY": "test-key"}):
            with patch('gen_mentor.core.llm.factory.ChatOpenAI') as mock_chat:
                mock_chat.return_value = MagicMock()

                factory = LLMFactory(config=sample_config)
                llm = factory.create_llm()  # Should use default model

                mock_chat.assert_called_once()

    def test_temperature_and_max_tokens(self, sample_config):
        """Test that temperature and max_tokens are passed correctly."""
        with patch.dict(os.environ, {"DEEPSEEK_API_KEY": "test-key"}):
            with patch('gen_mentor.core.llm.factory.ChatOpenAI') as mock_chat:
                mock_chat.return_value = MagicMock()

                factory = LLMFactory(config=sample_config)
                llm = factory.create_llm(
                    model="deepseek-chat",
                    temperature=0.7,
                    max_tokens=4096,
                )

                call_kwargs = mock_chat.call_args[1]
                assert call_kwargs.get("temperature") == 0.7
                assert call_kwargs.get("max_tokens") == 4096
