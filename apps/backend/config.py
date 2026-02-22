"""
Backend configuration management.

Loads configuration from environment variables and gen_mentor config system.
"""

from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path
from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings

from gen_mentor.config import load_config, AppConfig


class BackendSettings(BaseSettings):
    """Backend-specific settings."""

    # Server configuration
    host: str = Field(default="127.0.0.1", env="BACKEND_HOST")
    port: int = Field(default=5000, env="BACKEND_PORT")
    reload: bool = Field(default=False, env="BACKEND_RELOAD")
    workers: int = Field(default=1, env="BACKEND_WORKERS")

    # CORS configuration
    cors_origins: list[str] = Field(
        default=["*"],
        env="CORS_ORIGINS",
        description="Comma-separated list of allowed origins"
    )
    cors_allow_credentials: bool = Field(default=True, env="CORS_ALLOW_CREDENTIALS")

    # Storage configuration
    storage_mode: str = Field(default="local", env="STORAGE_MODE")
    upload_location: str = Field(default="/tmp/uploads/", env="UPLOAD_LOCATION")
    workspace_dir: str = Field(default="~/.gen-mentor/workspace", env="WORKSPACE_DIR")

    # Cloud storage (optional)
    cloud_bucket: Optional[str] = Field(default=None, env="CLOUD_BUCKET")
    cloud_region: Optional[str] = Field(default=None, env="CLOUD_REGION")

    # API configuration
    api_prefix: str = Field(default="/api/v1", env="API_PREFIX")
    debug: bool = Field(default=True, env="DEBUG")

    # Rate limiting (optional)
    rate_limit_enabled: bool = Field(default=False, env="RATE_LIMIT_ENABLED")
    rate_limit_requests: int = Field(default=100, env="RATE_LIMIT_REQUESTS")
    rate_limit_window: int = Field(default=60, env="RATE_LIMIT_WINDOW")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False

    @property
    def expanded_upload_location(self) -> Path:
        """Get expanded upload location path."""
        return Path(os.path.expanduser(self.upload_location))

    @property
    def expanded_workspace_dir(self) -> Path:
        """Get expanded workspace directory path."""
        return Path(os.path.expanduser(self.workspace_dir))


class Config:
    """Main configuration holder."""

    def __init__(self):
        """Initialize configuration."""
        self.backend = BackendSettings()
        self.app = load_config()

    @property
    def is_local_storage(self) -> bool:
        """Check if using local storage mode."""
        return self.backend.storage_mode.lower() == "local"

    @property
    def is_debug(self) -> bool:
        """Check if debug mode is enabled."""
        return self.backend.debug or self.app.debug

    def get_log_level(self) -> str:
        """Get logging level."""
        if self.is_debug:
            return "DEBUG"
        return self.app.log_level.upper()


@lru_cache()
def get_config() -> Config:
    """Get cached configuration instance.

    Returns:
        Config: Configuration instance
    """
    return Config()


# Convenience functions for direct access
def get_backend_settings() -> BackendSettings:
    """Get backend settings."""
    return get_config().backend


def get_app_config() -> AppConfig:
    """Get application config."""
    return get_config().app
