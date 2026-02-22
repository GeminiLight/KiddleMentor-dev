"""Unit tests for configuration management."""

import os
from pathlib import Path

import pytest
from omegaconf import OmegaConf

from gen_mentor.config import (
    AppConfig,
    load_config,
    load_config_from_dict,
    save_config,
    get_default_config_path,
    ensure_config_dir,
)


class TestConfigLoader:
    """Tests for configuration loading."""

    def test_load_config_from_dict(self, sample_config_dict):
        """Test loading config from dictionary."""
        config = load_config_from_dict(sample_config_dict)

        assert isinstance(config, AppConfig)
        assert config.agent_defaults.model == "openai/gpt-5.1"
        assert config.agent_defaults.temperature == 0.0
        assert config.providers.openai.api_key == "sk-test-key"

    def test_load_config_with_defaults(self, temp_dir, monkeypatch):
        """Test loading config with default values."""
        # Mock home directory
        monkeypatch.setenv("HOME", str(temp_dir))

        config = load_config(auto_create=False)

        assert isinstance(config, AppConfig)
        assert config.agent_defaults.model is not None

    def test_load_config_from_file(self, temp_dir, sample_config_dict):
        """Test loading config from YAML file."""
        config_path = temp_dir / "test_config.yaml"

        # Create config file
        cfg = OmegaConf.create(sample_config_dict)
        OmegaConf.save(cfg, config_path)

        # Load config
        config = load_config(config_path)

        assert config.agent_defaults.model == "openai/gpt-5.1"
        assert config.providers.deepseek.api_key == "test-deepseek-key"

    def test_load_config_with_overrides(self, temp_dir, sample_config_dict):
        """Test loading config with overrides."""
        config_path = temp_dir / "test_config.yaml"
        cfg = OmegaConf.create(sample_config_dict)
        OmegaConf.save(cfg, config_path)

        overrides = {"agent_defaults": {"temperature": 0.7}}
        config = load_config(config_path, overrides=overrides)

        assert config.agent_defaults.temperature == 0.7

    def test_save_config(self, temp_dir, sample_config):
        """Test saving config to file."""
        config_path = temp_dir / "saved_config.yaml"

        saved_path = save_config(sample_config, config_path)

        assert saved_path.exists()

        # Load and verify
        loaded_config = load_config(saved_path)
        assert loaded_config.agent_defaults.model == sample_config.agent_defaults.model

    def test_get_default_config_path(self):
        """Test getting default config path."""
        path = get_default_config_path()

        assert isinstance(path, Path)
        assert path.name == "config.yaml"
        assert ".gen-mentor" in str(path)

    def test_ensure_config_dir(self, temp_dir, monkeypatch):
        """Test ensuring config directory exists."""
        monkeypatch.setenv("HOME", str(temp_dir))

        config_dir = ensure_config_dir()

        assert config_dir.exists()
        assert config_dir.is_dir()


class TestAppConfig:
    """Tests for AppConfig schema."""

    def test_agent_defaults(self, sample_config):
        """Test agent defaults configuration."""
        assert sample_config.agent_defaults.model == "openai/gpt-5.1"
        assert sample_config.agent_defaults.temperature == 0.0
        assert sample_config.agent_defaults.max_tokens == 8192

    def test_provider_config(self, sample_config):
        """Test provider configuration."""
        assert "openai" in sample_config.providers.__dict__
        assert "deepseek" in sample_config.providers.__dict__

        openai = sample_config.providers.openai
        assert openai.api_key == "sk-test-key"
        assert "gpt-*" in openai.model_patterns

    def test_search_config(self, sample_config):
        """Test search configuration."""
        assert sample_config.searches.default == "duckduckgo"
        assert sample_config.searches.duckduckgo.max_results == 10

    def test_workspace_config(self, sample_config):
        """Test workspace configuration."""
        # Default workspace should be set
        assert sample_config.workspace is not None
