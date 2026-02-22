# Backend Refactoring - Complete

## Summary

Successfully refactored the backend to use the new centralized configuration system in `gen_mentor/config`.

## Changes Made

### 1. Merged Requirements

✅ **Merged** `apps/backend/requirements.txt` into root `requirements.txt`
✅ **Deleted** `apps/backend/requirements.txt`
✅ **Added** `langchain-docling` to root requirements

### 2. Fixed `apps/backend/main.py`

#### Removed Old Imports
- ❌ `from gen_mentor.llm.llm_factory import LLMFactory` (old path)
- ❌ `from gen_mentor.tools.retrieval.searcher_factory import SearchRunner` (deprecated)
- ❌ Old agent imports from nested directories

#### Added New Imports
- ✅ `from gen_mentor.config import load_config`
- ✅ `from gen_mentor.core.llm.factory import LLMFactory`
- ✅ `from gen_mentor.core.tools.retrieval.search_rag import SearchRagManager`
- ✅ New agent imports from flattened structure:
  - `gen_mentor.agents.learning.skill_gap_identifier`
  - `gen_mentor.agents.learning.learner_profiler`
  - `gen_mentor.agents.content.path_scheduler`
  - `gen_mentor.agents.content.knowledge_explorer`
  - `gen_mentor.agents.content.knowledge_drafter`
  - `gen_mentor.agents.content.document_integrator`
  - `gen_mentor.agents.content.content_creator`
  - `gen_mentor.agents.assessment.quiz_generator`
  - `gen_mentor.agents.learning.goal_refiner`
  - `gen_mentor.agents.tutoring.chatbot`

#### Removed Old Configuration System
```python
# OLD (REMOVED)
def _build_backend_runtime_config() -> dict:
    cfg = load_config()
    model_full = cfg.agent_defaults.model
    if "/" in model_full:
        provider, model_name = model_full.split("/", 1)
    else:
        provider = cfg.get_provider_name(model_full) or "deepseek"
        model_name = model_full
    return {...}

app_config = _build_backend_runtime_config()
```

#### Added New Configuration System
```python
# NEW (CLEAN)
from gen_mentor.config import load_config

# Load configuration directly
app_config = load_config()

# Initialize SearchRagManager from config
search_rag_manager = SearchRagManager.from_config({
    "search": {
        "provider": app_config.search_defaults.provider,
        "max_results": app_config.search_defaults.max_results,
        "loader_type": app_config.search_defaults.loader_type,
    },
    "embedder": {
        "provider": app_config.embedding.provider,
        "model_name": app_config.embedding.model_name,
    },
    "vectorstore": {
        "persist_directory": app_config.vectorstore.persist_directory,
        "collection_name": app_config.vectorstore.collection_name,
    },
    "rag": {
        "chunk_size": app_config.rag.chunk_size,
        "num_retrieval_results": app_config.rag.num_retrieval_results,
        "allow_parallel": app_config.rag.allow_parallel,
        "max_workers": app_config.rag.max_workers,
    },
})
```

#### Updated `get_llm()` Function

**Old Implementation:**
```python
def get_llm(model_provider: str | None = None, model_name: str | None = None, **kwargs):
    model_provider = model_provider or "deepseek"
    model_name = model_name or "deepseek-chat"
    return LLMFactory.create(model=model_name, model_provider=model_provider, **kwargs)
```

**New Implementation:**
```python
def get_llm(model_provider: str | None = None, model_name: str | None = None, **kwargs):
    """Get LLM instance using the new LLMFactory.
    
    Uses configuration from gen_mentor/config for:
    - Default model and provider
    - API base URLs
    - API keys
    - Temperature settings
    """
    # Use defaults from config if not specified
    if model_name is None:
        model_name = app_config.agent_defaults.model
        # Extract provider from model if in format "provider/model"
        if "/" in model_name:
            model_provider, model_name = model_name.split("/", 1)
    
    if model_provider is None:
        model_provider = "deepseek"
    
    # Get provider config
    provider_config = getattr(app_config.providers, model_provider, None)
    
    # Create LLM with config
    llm_kwargs = {
        "model": model_name,
        "model_provider": model_provider,
        "temperature": app_config.agent_defaults.temperature,
        **kwargs
    }
    
    # Add API base if configured
    if provider_config and provider_config.api_base:
        llm_kwargs["base_url"] = provider_config.api_base
    
    # Add API key if configured
    if provider_config and provider_config.api_key:
        llm_kwargs["api_key"] = provider_config.api_key
    
    return LLMFactory.create(**llm_kwargs)
```

#### Updated All Endpoints

All API endpoints now use:
- ✅ New agent imports from flattened structure
- ✅ New `get_llm()` function with config integration
- ✅ Proper error handling and docstrings

### 3. Updated Upload Location

```python
# NEW: Safer default with environment variable override
UPLOAD_LOCATION = os.getenv("UPLOAD_LOCATION", "/tmp/uploads/")
os.makedirs(UPLOAD_LOCATION, exist_ok=True)

# OLD: Hardcoded path
# UPLOAD_LOCATION = "/mnt/datadrive/tfwang/code/llm-mentor/data/cv/"
```

## Benefits

✅ **Centralized Configuration**
- All configuration managed in `gen_mentor/config`
- Single source of truth for LLM providers, models, and settings
- Easy to update and maintain

✅ **Cleaner Code**
- Removed redundant config building logic
- Uses new flattened agent structure
- Proper imports from `gen_mentor.core` and `gen_mentor.agents`

✅ **Better Integration**
- Seamless integration with new config system
- Automatic provider detection from model name
- Supports all providers configured in config.yaml

✅ **Improved Maintainability**
- No duplicate requirements.txt files
- Single dependency list in root
- Clear separation of concerns

## Configuration Example

The backend now reads from `~/.gen-mentor/config.yaml`:

```yaml
agent_defaults:
  model: "openai/gpt-5.1"
  temperature: 0.0
  max_tokens: 8192

providers:
  openai:
    api_key: ${OPENAI_API_KEY}
    api_base: "https://api.openai.com/v1"
  
  deepseek:
    api_key: ${DEEPSEEK_API_KEY}
    api_base: "https://api.deepseek.com"
  
  anthropic:
    api_key: ${ANTHROPIC_API_KEY}

search_defaults:
  provider: "duckduckgo"
  max_results: 5
  loader_type: "web"

embedding:
  provider: "huggingface"
  model_name: "sentence-transformers/all-mpnet-base-v2"

vectorstore:
  persist_directory: "data/vectorstore"
  collection_name: "genmentor"

rag:
  chunk_size: 1000
  num_retrieval_results: 5
  allow_parallel: true
  max_workers: 3
```

## Running the Backend

```bash
# Set environment variables (optional, can use config.yaml)
export BACKEND_HOST=0.0.0.0
export BACKEND_PORT=5000
export UPLOAD_LOCATION=/tmp/uploads/

# Run the backend
cd apps/backend
python main.py

# Or with uvicorn directly
uvicorn main:app --host 0.0.0.0 --port 5000 --reload
```

## API Endpoints

All endpoints remain the same, but now use the new configuration system:

- `GET /list-llm-models` - List available models
- `POST /chat-with-tutor` - Chat with AI tutor
- `POST /refine-learning-goal` - Refine learning goals
- `POST /identify-skill-gap` - Identify skill gaps
- `POST /create-learner-profile` - Create learner profile
- `POST /schedule-learning-path` - Schedule learning path
- `POST /explore-knowledge-points` - Explore knowledge
- `POST /draft-knowledge-point` - Draft knowledge
- `POST /integrate-learning-document` - Integrate document
- `POST /generate-document-quizzes` - Generate quizzes
- `POST /tailor-knowledge-content` - Tailor content

## Summary

✅ **Merged** backend requirements into root requirements.txt
✅ **Deleted** redundant apps/backend/requirements.txt
✅ **Refactored** apps/backend/main.py to use new config system
✅ **Updated** all imports to use flattened agent structure
✅ **Simplified** LLM creation with centralized config
✅ **Improved** code maintainability and consistency

The backend is now fully integrated with the new GenMentor configuration and structure!
