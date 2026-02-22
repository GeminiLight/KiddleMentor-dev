"""
Utility to get default model values from config.
"""

from functools import lru_cache
from config import get_app_config


@lru_cache()
def get_default_model_config() -> tuple[str, str]:
    """Get default model provider and name from config.

    Returns:
        Tuple of (provider, model_name)
    """
    config = get_app_config()
    model_full = config.agent_defaults.model

    # Split provider/model if in format "provider/model"
    if "/" in model_full:
        provider, model_name = model_full.split("/", 1)
        return provider, model_name
    else:
        # Default to openai if no provider specified
        return "openai", model_full


# Get defaults at module import time
DEFAULT_MODEL_PROVIDER, DEFAULT_MODEL_NAME = get_default_model_config()
