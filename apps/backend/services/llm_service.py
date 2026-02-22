"""
LLM service for managing language model operations.

Handles LLM instantiation, configuration, and model selection.
"""

from typing import Optional
from functools import lru_cache

from langchain_core.language_models import BaseChatModel

from gen_mentor.core.llm.factory import LLMFactory
from config import get_app_config
from exceptions import LLMError, ConfigurationError


class LLMService:
    """Service for managing LLM operations."""

    def __init__(self):
        """Initialize LLM service."""
        self.config = get_app_config()

    def get_llm(
        self,
        model: Optional[str] = None,
        **kwargs
    ) -> BaseChatModel:
        """Get LLM instance.

        Args:
            model: Model in 'provider/model' format (e.g., 'openai/gpt-4', 'openai/gpt-5.1')
                   or just model name (will use default provider)
            **kwargs: Additional parameters for LLM creation

        Returns:
            BaseChatModel instance

        Raises:
            LLMError: If LLM creation fails
            ConfigurationError: If configuration is invalid
        """
        try:
            # Use defaults from config if not specified
            if model is None:
                model = self.config.agent_defaults.model

            # Parse provider and model name
            if "/" in model:
                model_provider, model_name = model.split("/", 1)
            else:
                # If no provider specified, use default
                model_provider = "deepseek"
                model_name = model

            # Get provider config
            provider_config = getattr(self.config.providers, model_provider, None)

            if not provider_config:
                raise ConfigurationError(
                    f"Provider '{model_provider}' not found in configuration",
                    details={"provider": model_provider}
                )

            # Create LLM with config
            llm_kwargs = {
                "model": model_name,
                "model_provider": model_provider,
                "temperature": self.config.agent_defaults.temperature,
                **kwargs
            }

            # Add API base if configured
            if provider_config.api_base:
                llm_kwargs["base_url"] = provider_config.api_base

            # Add API key if configured
            if provider_config.api_key:
                llm_kwargs["api_key"] = provider_config.api_key

            return LLMFactory.create(**llm_kwargs)

        except Exception as e:
            if isinstance(e, (LLMError, ConfigurationError)):
                raise
            raise LLMError(
                f"Failed to create LLM: {str(e)}",
                details={
                    "provider": model_provider,
                    "model": model_name,
                    "error": str(e)
                }
            )

    def list_available_models(self) -> list[dict[str, str]]:
        """List available models from configuration.

        Returns:
            List of model information dictionaries
        """
        model_full = self.config.agent_defaults.model
        if "/" in model_full:
            provider, model_name = model_full.split("/", 1)
        else:
            provider = "deepseek"
            model_name = model_full

        return [{
            "model_name": model_name,
            "model_provider": provider,
        }]


@lru_cache()
def get_llm_service() -> LLMService:
    """Get cached LLM service instance.

    Returns:
        LLMService instance
    """
    return LLMService()
