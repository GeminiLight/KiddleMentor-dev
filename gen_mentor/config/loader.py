from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Dict, Optional

from omegaconf import OmegaConf, DictConfig

from .schemas import AppConfig


def get_default_config_path() -> Path:
    """Get the default configuration file path.

    Returns:
        Path to ~/.gen-mentor/config.yaml
    """
    return Path.home() / ".gen-mentor" / "config.yaml"


def ensure_config_dir() -> Path:
    """Ensure the ~/.gen-mentor directory exists.

    Returns:
        Path to ~/.gen-mentor directory
    """
    config_dir = Path.home() / ".gen-mentor"
    config_dir.mkdir(parents=True, exist_ok=True)
    return config_dir


def create_default_config_file() -> Path:
    """Create default config.yaml in ~/.gen-mentor if it doesn't exist.

    Copies the example configuration as a starting point.

    Returns:
        Path to the created/existing config file
    """
    config_path = get_default_config_path()

    if config_path.exists():
        return config_path

    # Ensure directory exists
    ensure_config_dir()

    # Get the example config from the package
    example_config_path = Path(__file__).parent / "config.example.yaml"

    if example_config_path.exists():
        # Copy example config as default
        import shutil
        shutil.copy(example_config_path, config_path)
        print(f"Created default configuration at: {config_path}")
    else:
        # Create minimal default config if example not found
        default_cfg = OmegaConf.structured(AppConfig)
        OmegaConf.save(default_cfg, config_path)
        print(f"Created minimal configuration at: {config_path}")

    return config_path


def load_config(
    config_path: Optional[str | Path] = None,
    overrides: Optional[Dict[str, Any]] = None,
    auto_create: bool = True,
) -> AppConfig:
    """Load application configuration from YAML file or use defaults.

    Args:
        config_path: Path to YAML config file. If None, uses ~/.gen-mentor/config.yaml
        overrides: Dictionary of config overrides to apply.
        auto_create: If True, automatically create ~/.gen-mentor/config.yaml if it doesn't exist

    Returns:
        AppConfig instance with loaded configuration.

    Example:
        # Use default config from ~/.gen-mentor/config.yaml
        config = load_config()

        # Load from specific YAML file
        config = load_config("path/to/config.yaml")

        # Load with overrides
        config = load_config(overrides={"llms.default": "gpt4"})
    """
    if config_path is None:
        # Use default configuration path
        config_path = get_default_config_path()

        if not config_path.exists() and auto_create:
            # Create default config file
            config_path = create_default_config_file()

    config_path = Path(config_path)

    if not config_path.exists():
        # Fall back to default schema
        print(f"Config file not found: {config_path}. Using default configuration.")
        cfg = OmegaConf.structured(AppConfig)
    else:
        # Load from YAML file
        try:
            yaml_cfg = OmegaConf.load(config_path)
            default_cfg = OmegaConf.structured(AppConfig)
            cfg = OmegaConf.merge(default_cfg, yaml_cfg)
        except Exception as e:
            print(f"Error loading config from {config_path}: {e}")
            print("Using default configuration.")
            cfg = OmegaConf.structured(AppConfig)

    # Apply overrides if provided
    if overrides:
        override_cfg = OmegaConf.create(overrides)
        cfg = OmegaConf.merge(cfg, override_cfg)

    # Convert to AppConfig dataclass instance
    return OmegaConf.to_object(cfg)


def load_config_from_dict(config_dict: Dict[str, Any]) -> AppConfig:
    """Load configuration from a dictionary.

    Args:
        config_dict: Configuration dictionary.

    Returns:
        AppConfig instance.
    """
    default_cfg = OmegaConf.structured(AppConfig)
    dict_cfg = OmegaConf.create(config_dict)
    cfg = OmegaConf.merge(default_cfg, dict_cfg)
    return OmegaConf.to_object(cfg)


def save_config(config: AppConfig, config_path: Optional[str | Path] = None) -> Path:
    """Save configuration to YAML file.

    Args:
        config: AppConfig instance to save
        config_path: Path to save to. If None, saves to ~/.gen-mentor/config.yaml

    Returns:
        Path where config was saved
    """
    if config_path is None:
        config_path = get_default_config_path()
        ensure_config_dir()

    config_path = Path(config_path)

    # Convert to OmegaConf and save
    cfg = OmegaConf.structured(config)
    OmegaConf.save(cfg, config_path)

    return config_path


# Default configuration instance (loads from ~/.gen-mentor/config.yaml)
default_config = load_config()
