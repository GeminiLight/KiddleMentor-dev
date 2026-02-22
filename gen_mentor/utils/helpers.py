"""Utility functions for nanobot."""

from pathlib import Path
from datetime import datetime


def ensure_dir(path: Path) -> Path:
    """Ensure a directory exists, creating it if necessary."""
    path.mkdir(parents=True, exist_ok=True)
    return path
