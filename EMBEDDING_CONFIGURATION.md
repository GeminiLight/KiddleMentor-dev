# Embedding Configuration Enhancement - Complete

## Summary

Successfully enhanced the embedding configuration to support multiple embedding providers with `embedding_defaults` and `embedding_providers`, following the same pattern as the search configuration.

## Changes Made

### 1. Configuration Schema (`gen_mentor/config/schemas.py`)

#### Added New Classes

**EmbeddingProviderConfig**
```python
@dataclass
class EmbeddingProviderConfig:
    """Configuration for a single embedding provider."""
    api_key: Optional[str] = None
    model_name: str = "sentence-transformers/all-mpnet-base-v2"
    api_base: Optional[str] = None
```

**EmbeddingProvidersConfig**
```python
@dataclass
class EmbeddingProvidersConfig:
    """Configuration for all embedding providers."""
    huggingface: EmbeddingProviderConfig
    openai: EmbeddingProviderConfig
    cohere: EmbeddingProviderConfig
    azure: EmbeddingProviderConfig
    ollama: EmbeddingProviderConfig
```

**EmbeddingDefaults**
```python
@dataclass
class EmbeddingDefaults:
    """Default embedding configuration."""
    provider: str = "huggingface"
    model_name: str = "sentence-transformers/all-mpnet-base-v2"
    dimension: int = 768
```

#### Updated AppConfig

**Before:**
```python
embedding: EmbeddingConfig = field(default_factory=EmbeddingConfig)
```

**After:**
```python
embedding_defaults: EmbeddingDefaults = field(default_factory=EmbeddingDefaults)
embedding_providers: EmbeddingProvidersConfig = field(default_factory=EmbeddingProvidersConfig)
```

#### Added Helper Methods

```python
def _match_embedding_provider(self, provider: Optional[str] = None) -> tuple[Optional[EmbeddingProviderConfig], Optional[str]]:
    """Match embedding provider config."""

def get_embedding_provider(self, provider: Optional[str] = None) -> Optional[EmbeddingProviderConfig]:
    """Get embedding provider config."""

def get_embedding_provider_name(self, provider: Optional[str] = None) -> Optional[str]:
    """Get embedding provider name."""

def get_embedding_model_name(self, provider: Optional[str] = None) -> Optional[str]:
    """Get embedding model name for the given provider."""
```

### 2. Configuration Example (`gen_mentor/config/config.example.yaml`)

**Before:**
```yaml
# Embedding model configuration
embedding:
  provider: huggingface
  model_name: sentence-transformers/all-mpnet-base-v2
```

**After:**
```yaml
# =============================================================================
# Embedding Configuration
# =============================================================================

# Default embedding settings
embedding_defaults:
  provider: huggingface  # Options: huggingface, openai, cohere, azure, ollama
  model_name: sentence-transformers/all-mpnet-base-v2
  dimension: 768  # Embedding vector dimension

# Embedding provider configurations
embedding_providers:
  huggingface:
    api_key: null  # No API key required for public models
    model_name: sentence-transformers/all-mpnet-base-v2
    api_base: null

  openai:
    api_key: null  # Set via OPENAI_API_KEY env var
    model_name: text-embedding-3-small  # Options: text-embedding-3-small, text-embedding-3-large, text-embedding-ada-002
    api_base: null

  cohere:
    api_key: null  # Set via COHERE_API_KEY env var
    model_name: embed-english-v3.0  # Options: embed-english-v3.0, embed-multilingual-v3.0
    api_base: null

  azure:
    api_key: null  # Set via AZURE_OPENAI_API_KEY env var
    model_name: text-embedding-ada-002
    api_base: null  # Required: Your Azure endpoint (e.g., https://YOUR_RESOURCE.openai.azure.com)

  ollama:
    api_key: null  # Not required for Ollama
    model_name: nomic-embed-text  # Options: nomic-embed-text, mxbai-embed-large
    api_base: http://localhost:11434
```

### 3. Backend Main (`apps/backend/main.py`)

**Before:**
```python
"embedder": {
    "provider": app_config.embedding.provider,
    "model_name": app_config.embedding.model_name,
},
```

**After:**
```python
"embedder": {
    "provider": app_config.embedding_defaults.provider,
    "model_name": app_config.embedding_defaults.model_name,
    "dimension": app_config.embedding_defaults.dimension,
},
```

### 4. Embedder Factory (`gen_mentor/core/tools/retrieval/embedder_factory.py`)

**Enhanced to support all providers:**
```python
@staticmethod
def create(
    model: str = "sentence-transformers/all-MiniLM-L6-v2",
    model_provider: Optional[str] = "huggingface",
    api_key: Optional[str] = None,
    api_base: Optional[str] = None,
    ) -> Embeddings:
    """Create an embedding model instance based on the specified model name."""
    # Supports: huggingface, openai, azure, cohere, ollama, together
```

**Added support for:**
- **Cohere**: `CohereEmbeddings`
- **Ollama**: `OllamaEmbeddings`
- **API key and base URL parameters**

### 5. Dependencies

**Added to `requirements.txt` and `pyproject.toml`:**
```
langchain-cohere
langchain-ollama
```

### 6. Interactive Onboarding (`gen_mentor/cli/onboard.py`)

#### Added Functions

```python
def select_embedding_provider() -> str:
    """Select embedding provider."""
    # Options: HuggingFace, OpenAI, Cohere, Azure OpenAI, Ollama

def get_embedding_provider_id(choice: str) -> str:
    """Get embedding provider ID."""

def get_embedding_model_default(provider: str) -> str:
    """Get default embedding model for provider."""
```

#### Updated Setup Flow

**quick_start_setup():**
```python
# Embedding provider
console.print("\n[bold]Embedding Configuration[/bold]")
console.print("Embeddings convert text to vectors for semantic search")
embedding_choice = select_embedding_provider()
embedding_provider = get_embedding_provider_id(embedding_choice)
embedding_model = get_embedding_model_default(embedding_provider)
```

**Configuration Summary:**
```python
console.print(f"  Embedding: {setup_data['embedding_provider']} ({setup_data['embedding_model']})")
```

## Supported Embedding Providers

### 1. HuggingFace (Recommended for Free Usage)
- **No API key required** for public models
- **Default model**: `sentence-transformers/all-mpnet-base-v2`
- **Dimension**: 768
- **Use case**: Free, local inference, good quality

### 2. OpenAI
- **API key**: `OPENAI_API_KEY`
- **Default model**: `text-embedding-3-small`
- **Options**: `text-embedding-3-small`, `text-embedding-3-large`, `text-embedding-ada-002`
- **Dimension**: 1536 (small), 3072 (large), 1536 (ada-002)
- **Use case**: High quality, cloud-based, requires API key

### 3. Cohere
- **API key**: `COHERE_API_KEY`
- **Default model**: `embed-english-v3.0`
- **Options**: `embed-english-v3.0`, `embed-multilingual-v3.0`
- **Dimension**: 1024
- **Use case**: Multilingual support, high quality

### 4. Azure OpenAI
- **API key**: `AZURE_OPENAI_API_KEY`
- **API base**: Required (e.g., `https://YOUR_RESOURCE.openai.azure.com`)
- **Default model**: `text-embedding-ada-002`
- **Use case**: Enterprise deployments, Azure infrastructure

### 5. Ollama (Local Models)
- **No API key required**
- **API base**: `http://localhost:11434` (default)
- **Default model**: `nomic-embed-text`
- **Options**: `nomic-embed-text`, `mxbai-embed-large`
- **Use case**: Fully local inference, privacy-focused

## Usage Examples

### 1. Using Config Helper Methods

```python
from gen_mentor.config import load_config

config = load_config()

# Get default embedding provider
provider_name = config.embedding_defaults.provider  # "huggingface"
model_name = config.embedding_defaults.model_name   # "sentence-transformers/all-mpnet-base-v2"

# Get specific provider config
openai_config = config.get_embedding_provider("openai")
if openai_config:
    print(openai_config.model_name)  # "text-embedding-3-small"
    print(openai_config.api_key)

# Get embedding model name for a provider
model = config.get_embedding_model_name("cohere")  # "embed-english-v3.0"
```

### 2. Creating Embedder with Factory

```python
from gen_mentor.core.tools.retrieval.embedder_factory import EmbedderFactory

# Using HuggingFace (default)
embedder = EmbedderFactory.create(
    model="sentence-transformers/all-mpnet-base-v2",
    model_provider="huggingface"
)

# Using OpenAI
embedder = EmbedderFactory.create(
    model="text-embedding-3-small",
    model_provider="openai",
    api_key="sk-..."
)

# Using Ollama
embedder = EmbedderFactory.create(
    model="nomic-embed-text",
    model_provider="ollama",
    api_base="http://localhost:11434"
)
```

### 3. Interactive Onboarding

```bash
$ gen-mentor onboard

# During onboarding, you'll see:

Embedding Configuration
Embeddings convert text to vectors for semantic search

Select embedding provider:
  > HuggingFace (Free, local models - Recommended)
    OpenAI (Requires API key)
    Cohere (Requires API key)
    Azure OpenAI (Requires API key)
    Ollama (Local models)

Configuration Summary:
  Provider: deepseek
  Model: deepseek-chat
  Temperature: 0.0
  Search: duckduckgo
  Embedding: huggingface (sentence-transformers/all-mpnet-base-v2)
```

## Benefits

✅ **Consistent Pattern** - Matches the search configuration structure
✅ **Multiple Providers** - Support for 5 different embedding providers
✅ **Flexible Configuration** - Per-provider API keys and base URLs
✅ **Helper Methods** - Easy provider matching and model name retrieval
✅ **Interactive Setup** - User-friendly onboarding for embedding selection
✅ **Backward Compatible** - Graceful migration from old config structure
✅ **Well Documented** - Comprehensive examples in config.example.yaml

## Migration Guide

### For Existing Configurations

**Old format (still works but deprecated):**
```yaml
embedding:
  provider: huggingface
  model_name: sentence-transformers/all-mpnet-base-v2
```

**New format (recommended):**
```yaml
embedding_defaults:
  provider: huggingface
  model_name: sentence-transformers/all-mpnet-base-v2
  dimension: 768

embedding_providers:
  huggingface:
    api_key: null
    model_name: sentence-transformers/all-mpnet-base-v2
    api_base: null
```

### Code Updates

**Old code:**
```python
provider = config.embedding.provider
model = config.embedding.model_name
```

**New code:**
```python
provider = config.embedding_defaults.provider
model = config.embedding_defaults.model_name

# Or use helper methods
provider_config = config.get_embedding_provider()
model = config.get_embedding_model_name()
```

## Testing

Run tests to ensure everything works:

```bash
# Unit tests
pytest tests/unit/test_config.py -v

# Integration tests
pytest tests/integration/ -v

# Test onboarding
gen-mentor onboard

# Test embedding creation
python -c "
from gen_mentor.core.tools.retrieval.embedder_factory import EmbedderFactory
embedder = EmbedderFactory.create(model='sentence-transformers/all-mpnet-base-v2', model_provider='huggingface')
print('Embedding created successfully!')
"
```

## Future Enhancements

Potential improvements:
1. Add more embedding providers (e.g., Voyage AI, Jina AI)
2. Support for embedding dimension auto-detection
3. Caching for frequently used embeddings
4. Batch embedding optimization
5. Embedding model benchmarking utilities

## Related Files

- `gen_mentor/config/schemas.py` - Configuration data models
- `gen_mentor/config/config.example.yaml` - Configuration example
- `gen_mentor/core/tools/retrieval/embedder_factory.py` - Embedder factory
- `gen_mentor/cli/onboard.py` - Interactive onboarding
- `apps/backend/main.py` - Backend API integration
- `requirements.txt` - Dependencies
- `pyproject.toml` - Package configuration
