from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional, Dict
from pathlib import Path


@dataclass
class ProviderConfig:
    """Configuration for a single LLM provider."""
    api_key: Optional[str] = None
    api_base: Optional[str] = None
    extra_headers: Optional[Dict[str, str]] = None


@dataclass
class ProvidersConfig:
    """Configuration for all LLM providers."""
    openai: ProviderConfig = field(default_factory=ProviderConfig)
    anthropic: ProviderConfig = field(default_factory=ProviderConfig)
    deepseek: ProviderConfig = field(default_factory=ProviderConfig)
    together: ProviderConfig = field(default_factory=ProviderConfig)
    groq: ProviderConfig = field(default_factory=ProviderConfig)
    openrouter: ProviderConfig = field(default_factory=ProviderConfig)
    ollama: ProviderConfig = field(default_factory=ProviderConfig)
    custom: ProviderConfig = field(default_factory=ProviderConfig)


@dataclass
class AgentDefaults:
    """Default agent configuration."""
    model: str = "openai/gpt-5.1"
    temperature: float = 0.0
    max_tokens: int = 8192
    workspace: str = "~/.gen-mentor/workspace"  # Workspace for memory and context storage
    storage_mode: str = "local"  # local | cloud


@dataclass
class EmbeddingProviderConfig:
    """Configuration for a single embedding provider."""
    api_key: Optional[str] = None
    model_name: str = "sentence-transformers/all-mpnet-base-v2"
    api_base: Optional[str] = None


@dataclass
class EmbeddingProvidersConfig:
    """Configuration for all embedding providers."""
    huggingface: EmbeddingProviderConfig = field(default_factory=lambda: EmbeddingProviderConfig(
        model_name="sentence-transformers/all-mpnet-base-v2"
    ))
    openai: EmbeddingProviderConfig = field(default_factory=lambda: EmbeddingProviderConfig(
        model_name="text-embedding-3-small"
    ))
    cohere: EmbeddingProviderConfig = field(default_factory=lambda: EmbeddingProviderConfig(
        model_name="embed-english-v3.0"
    ))
    azure: EmbeddingProviderConfig = field(default_factory=lambda: EmbeddingProviderConfig(
        model_name="text-embedding-ada-002"
    ))
    ollama: EmbeddingProviderConfig = field(default_factory=lambda: EmbeddingProviderConfig(
        model_name="nomic-embed-text",
        api_base="http://localhost:11434"
    ))


@dataclass
class EmbeddingDefaults:
    """Default embedding configuration."""
    provider: str = "huggingface"
    model_name: str = "sentence-transformers/all-mpnet-base-v2"
    dimension: int = 768
    enable_vectordb: bool = False  # Disabled by default, requires valid embedding setup


@dataclass
class SearchProviderConfig:
    """Configuration for a single search provider."""
    api_key: Optional[str] = None
    max_results: int = 5


@dataclass
class SearchProvidersConfig:
    """Configuration for all search providers."""
    duckduckgo: SearchProviderConfig = field(default_factory=SearchProviderConfig)
    tavily: SearchProviderConfig = field(default_factory=SearchProviderConfig)
    serper: SearchProviderConfig = field(default_factory=SearchProviderConfig)
    bing: SearchProviderConfig = field(default_factory=SearchProviderConfig)
    brave: SearchProviderConfig = field(default_factory=SearchProviderConfig)
    you: SearchProviderConfig = field(default_factory=SearchProviderConfig)


@dataclass
class SearchDefaults:
    """Default search configuration."""
    provider: str = "duckduckgo"
    max_results: int = 5
    loader_type: str = "web"
    enable_search: bool = False  # Disabled by default, requires search provider setup


@dataclass
class VectorstoreConfig:
    """Configuration for vector database storage."""
    persist_directory: str = "data/vectorstore"
    collection_name: str = "genmentor"


@dataclass
class StorageConfig:
    """Configuration for storage backend."""
    mode: str = "local"  # local | cloud
    local_upload_dir: str = "/tmp/uploads/"
    cloud_bucket: Optional[str] = None  # For cloud storage (e.g., S3 bucket name)
    cloud_region: Optional[str] = None  # For cloud storage region
    cloud_access_key: Optional[str] = None
    cloud_secret_key: Optional[str] = None


@dataclass
class RAGConfig:
    """Configuration for Retrieval-Augmented Generation."""
    chunk_size: int = 1000
    num_retrieval_results: int = 5
    allow_parallel: bool = True
    max_workers: int = 3


@dataclass
class AppConfig:
    """Main application configuration."""
    environment: str = "dev"  # dev | staging | prod
    debug: bool = True
    log_level: str = "INFO"

    # Agent/LLM configuration
    agent_defaults: AgentDefaults = field(default_factory=AgentDefaults)
    providers: ProvidersConfig = field(default_factory=ProvidersConfig)

    # Search configuration
    search_defaults: SearchDefaults = field(default_factory=SearchDefaults)
    search_providers: SearchProvidersConfig = field(default_factory=SearchProvidersConfig)

    # Embedding configuration
    embedding_defaults: EmbeddingDefaults = field(default_factory=EmbeddingDefaults)
    embedding_providers: EmbeddingProvidersConfig = field(default_factory=EmbeddingProvidersConfig)

    # Other configurations
    vectorstore: VectorstoreConfig = field(default_factory=VectorstoreConfig)
    storage: StorageConfig = field(default_factory=StorageConfig)
    rag: RAGConfig = field(default_factory=RAGConfig)

    def _match_provider(self, model: Optional[str] = None) -> tuple[Optional[ProviderConfig], Optional[str]]:
        """Match provider config based on model name.

        Args:
            model: Model name (e.g., "gpt-4", "openai/gpt-5.1")

        Returns:
            Tuple of (ProviderConfig, provider_name) or (None, None)
        """
        model_str = model or self.agent_defaults.model
        model_lower = model_str.lower()
        model_prefix = model_lower.split("/")[0] if "/" in model_lower else ""

        # Provider keywords mapping
        provider_keywords = {
            "openai": ["gpt", "openai"],
            "anthropic": ["claude", "anthropic"],
            "deepseek": ["deepseek"],
            "together": ["together", "llama", "mistral", "qwen"],
            "groq": ["groq"],
            "openrouter": ["openrouter"],
            "ollama": ["ollama"],
        }

        # First, try exact prefix match
        if model_prefix:
            for provider_name, keywords in provider_keywords.items():
                if model_prefix in keywords:
                    provider = getattr(self.providers, provider_name, None)
                    if provider and provider.api_key:
                        return provider, provider_name

        # Then try keyword matching
        for provider_name, keywords in provider_keywords.items():
            if any(kw in model_lower for kw in keywords):
                provider = getattr(self.providers, provider_name, None)
                if provider and provider.api_key:
                    return provider, provider_name

        # Fallback: first provider with an API key
        for provider_name in ["deepseek", "openai", "anthropic", "together", "groq", "openrouter", "custom"]:
            provider = getattr(self.providers, provider_name, None)
            if provider and provider.api_key:
                return provider, provider_name

        return None, None

    def get_provider(self, model: Optional[str] = None) -> Optional[ProviderConfig]:
        """Get provider config for the given model.

        Args:
            model: Model name. If None, uses default model.

        Returns:
            ProviderConfig or None
        """
        provider, _ = self._match_provider(model)
        return provider

    def get_provider_name(self, model: Optional[str] = None) -> Optional[str]:
        """Get provider name for the given model.

        Args:
            model: Model name. If None, uses default model.

        Returns:
            Provider name (e.g., "openai", "deepseek") or None
        """
        _, name = self._match_provider(model)
        return name

    def get_api_key(self, model: Optional[str] = None) -> Optional[str]:
        """Get API key for the given model.

        Args:
            model: Model name. If None, uses default model.

        Returns:
            API key or None
        """
        provider = self.get_provider(model)
        return provider.api_key if provider else None

    def get_api_base(self, model: Optional[str] = None) -> Optional[str]:
        """Get API base URL for the given model.

        Args:
            model: Model name. If None, uses default model.

        Returns:
            API base URL or None
        """
        provider = self.get_provider(model)
        return provider.api_base if provider else None

    def _match_search_provider(self, provider: Optional[str] = None) -> tuple[Optional[SearchProviderConfig], Optional[str]]:
        """Match search provider config.

        Args:
            provider: Provider name (e.g., "tavily", "serper")

        Returns:
            Tuple of (SearchProviderConfig, provider_name) or (None, None)
        """
        provider_name = provider or self.search_defaults.provider
        provider_lower = provider_name.lower()

        # Try exact match first
        search_provider = getattr(self.search_providers, provider_lower, None)
        if search_provider:
            return search_provider, provider_lower

        # Fallback to default
        default_provider = getattr(self.search_providers, self.search_defaults.provider, None)
        if default_provider:
            return default_provider, self.search_defaults.provider

        return None, None

    def get_search_provider(self, provider: Optional[str] = None) -> Optional[SearchProviderConfig]:
        """Get search provider config.

        Args:
            provider: Provider name. If None, uses default provider.

        Returns:
            SearchProviderConfig or None
        """
        search_provider, _ = self._match_search_provider(provider)
        return search_provider

    def get_search_provider_name(self, provider: Optional[str] = None) -> Optional[str]:
        """Get search provider name.

        Args:
            provider: Provider name. If None, uses default provider.

        Returns:
            Provider name or None
        """
        _, name = self._match_search_provider(provider)
        return name

    def is_search_enabled(self) -> bool:
        """Check if web search is enabled.

        Web search is enabled only if:
        1. enable_search flag is True
        2. A valid search provider is configured

        Returns:
            True if search is enabled, False otherwise
        """
        if not self.search_defaults.enable_search:
            return False

        # Check if we have a valid search provider
        search_provider = self.get_search_provider()
        if not search_provider:
            return False

        return True

    def _match_embedding_provider(self, provider: Optional[str] = None) -> tuple[Optional[EmbeddingProviderConfig], Optional[str]]:
        """Match embedding provider config.

        Args:
            provider: Provider name (e.g., "huggingface", "openai")

        Returns:
            Tuple of (EmbeddingProviderConfig, provider_name) or (None, None)
        """
        provider_name = provider or self.embedding_defaults.provider
        provider_lower = provider_name.lower()

        # Try exact match first
        embedding_provider = getattr(self.embedding_providers, provider_lower, None)
        if embedding_provider:
            return embedding_provider, provider_lower

        # Fallback to default
        default_provider = getattr(self.embedding_providers, self.embedding_defaults.provider, None)
        if default_provider:
            return default_provider, self.embedding_defaults.provider

        return None, None

    def get_embedding_provider(self, provider: Optional[str] = None) -> Optional[EmbeddingProviderConfig]:
        """Get embedding provider config.

        Args:
            provider: Provider name. If None, uses default provider.

        Returns:
            EmbeddingProviderConfig or None
        """
        embedding_provider, _ = self._match_embedding_provider(provider)
        return embedding_provider

    def get_embedding_provider_name(self, provider: Optional[str] = None) -> Optional[str]:
        """Get embedding provider name.

        Args:
            provider: Provider name. If None, uses default provider.

        Returns:
            Provider name or None
        """
        _, name = self._match_embedding_provider(provider)
        return name

    def get_embedding_model_name(self, provider: Optional[str] = None) -> Optional[str]:
        """Get embedding model name for the given provider.

        Args:
            provider: Provider name. If None, uses default provider.

        Returns:
            Model name or None
        """
        embedding_provider = self.get_embedding_provider(provider)
        return embedding_provider.model_name if embedding_provider else None

    def is_vectordb_enabled(self) -> bool:
        """Check if vector database is enabled.

        Vector database is enabled only if:
        1. enable_vectordb flag is True
        2. A valid embedding provider is configured
        3. The embedding model is accessible

        Returns:
            True if vectordb is enabled and ready to use, False otherwise
        """
        if not self.embedding_defaults.enable_vectordb:
            return False

        # Check if we have a valid embedding provider
        embedding_provider = self.get_embedding_provider()
        if not embedding_provider:
            return False

        # For providers that need API keys, verify they're set
        provider_name = self.get_embedding_provider_name()
        if provider_name in ["openai", "cohere", "azure"]:
            if not embedding_provider.api_key:
                return False

        return True
