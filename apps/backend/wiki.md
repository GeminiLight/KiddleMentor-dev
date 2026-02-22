# GenMentor Backend Wiki

**Version**: 1.0.0
**Last Updated**: 2026-02-22

---

## Table of Contents

1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Getting Started](#getting-started)
4. [API Reference](#api-reference)
5. [Configuration](#configuration)
6. [Data Models](#data-models)
7. [Services](#services)
8. [Memory System](#memory-system)
9. [Development Guide](#development-guide)
10. [Deployment](#deployment)
11. [Troubleshooting](#troubleshooting)

---

## Overview

GenMentor is an AI-powered personalized learning platform that creates adaptive learning experiences tailored to individual learners. The backend is built with FastAPI and follows a clean, modular architecture.

### Key Features

- **🤖 AI Chatbot Tutor**: Interactive conversational learning with context-aware responses
- **🎯 Learning Goal Refinement**: Helps learners define clear, achievable educational objectives
- **📊 Skill Gap Analysis**: Identifies knowledge gaps between current skills and learning goals
- **👤 Adaptive Learner Profiling**: Creates and updates detailed learner profiles dynamically
- **📚 Personalized Content Delivery**: Generates tailored learning materials and resources
- **🗺️ Learning Path Scheduling**: Creates structured learning sequences with session planning
- **🔍 Knowledge Point Exploration**: Deep-dives into topics with multiple perspectives
- **📝 Quiz Generation**: Creates personalized assessments with various question types
- **💾 Memory Persistence**: Maintains learner context across sessions

### Technology Stack

- **Framework**: FastAPI 0.115+
- **Language**: Python 3.12+
- **Validation**: Pydantic V2
- **Configuration**: Hydra + YAML
- **LLM Orchestration**: LangChain
- **Vector Database**: ChromaDB
- **Embeddings**: Sentence Transformers / OpenAI
- **Search**: DuckDuckGo / Tavily / Serper

---

## Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        Client Layer                          │
│            (Frontend, CLI, External Services)                │
└───────────────────────┬─────────────────────────────────────┘
                        │ HTTP/REST
┌───────────────────────▼─────────────────────────────────────┐
│                      API Layer (FastAPI)                     │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  /api/v1/chat      /api/v1/goals    /api/v1/skills    │ │
│  │  /api/v1/profile   /api/v1/learning /api/v1/memory    │ │
│  └────────────────────────────────────────────────────────┘ │
└───────────────────────┬─────────────────────────────────────┘
                        │
┌───────────────────────▼─────────────────────────────────────┐
│                     Service Layer                            │
│  ┌──────────────────┐  ┌──────────────────┐                │
│  │  LLM Service     │  │  Memory Service  │                │
│  │  - Multi-provider│  │  - Context Store │                │
│  │  - Model mgmt    │  │  - History mgmt  │                │
│  └──────────────────┘  └──────────────────┘                │
└───────────────────────┬─────────────────────────────────────┘
                        │
┌───────────────────────▼─────────────────────────────────────┐
│                      Core Layer                              │
│  ┌──────────┐  ┌─────────┐  ┌──────────┐  ┌─────────────┐ │
│  │   LLM    │  │   RAG   │  │ Search   │  │  Embedding  │ │
│  │ Factory  │  │ System  │  │ Provider │  │   Models    │ │
│  └──────────┘  └─────────┐  └──────────┘  └─────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

### Directory Structure

```
apps/backend/
├── main.py                         # FastAPI application entry point
├── main_legacy.py                  # Legacy monolithic code (deprecated)
├── config.py                       # Backend-specific configuration
├── dependencies.py                 # FastAPI dependency injection
├── exceptions.py                   # Custom exception hierarchy
├── schemas.py                      # Legacy schemas (deprecated)
│
├── api/                            # API layer
│   └── v1/                         # API version 1
│       ├── router.py               # Route aggregation
│       └── endpoints/              # Endpoint modules
│           ├── system.py           # Health, storage, models list
│           ├── chat.py             # AI tutor chat
│           ├── goals.py            # Goal refinement
│           ├── skills.py           # Skill gap analysis
│           ├── profile.py          # Profile management
│           ├── learning_path.py    # Learning paths & content
│           ├── assessment.py       # Quiz generation
│           └── memory.py           # Context management
│
├── models/                         # Data models
│   ├── __init__.py                 # Model exports
│   ├── defaults.py                 # Config-driven defaults
│   ├── common.py                   # Base models (BaseRequest, BaseResponse)
│   ├── requests.py                 # Request schemas (15 models)
│   └── responses.py                # Response schemas (14 models)
│
├── services/                       # Service layer
│   ├── llm_service.py              # LLM provider management
│   └── memory_service.py           # Memory persistence service
│
├── middleware/                     # Middleware components
│   └── error_handler.py            # Global error handling
│
├── test_refactored.py              # Test suite for refactored API
├── test_integration.py             # Integration tests
│
└── docs/                           # Documentation
    ├── REFACTORING_COMPLETE.md
    ├── ENDPOINT_MIGRATION.md
    ├── MODEL_DEFAULTS_ALIGNMENT.md
    └── ENDPOINT_NAMING_IMPROVEMENT.md
```

### Core Components

#### 1. API Layer (`api/v1/endpoints/`)

Handles HTTP requests and responses. Each endpoint module focuses on a specific domain:

- **system.py**: System health, storage info, available models
- **chat.py**: AI tutor chat with context awareness
- **goals.py**: Learning goal refinement
- **skills.py**: Skill gap identification
- **profile.py**: Learner profile creation and updates
- **learning_path.py**: Learning path scheduling and content generation
- **assessment.py**: Quiz generation
- **memory.py**: Context retrieval and search

#### 2. Service Layer (`services/`)

Business logic and coordination:

- **LLMService**: Manages LLM providers (OpenAI, Anthropic, DeepSeek, etc.)
- **MemoryService**: Handles learner context persistence and retrieval

#### 3. Model Layer (`models/`)

Pydantic models for data validation:

- **BaseRequest/BaseResponse**: Common base models
- **Request Models**: Input validation for all endpoints
- **Response Models**: Output structure for all endpoints

#### 4. Core Layer (`gen_mentor/`)

Located in the parent `gen_mentor` package:

- **LLM Factory**: Multi-provider LLM instantiation
- **RAG System**: Retrieval-augmented generation
- **Memory Store**: Workspace-based context storage
- **Agents**: Specialized AI agents for different tasks

---

## Getting Started

### Prerequisites

- Python 3.12 or higher
- UV package manager (recommended) or pip
- At least one LLM provider API key (OpenAI, Anthropic, DeepSeek, etc.)

### Installation

1. **Clone the repository**:
   ```bash
   cd /path/to/gen-mentor/apps/backend
   ```

2. **Create virtual environment**:
   ```bash
   uv venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   uv pip install -r requirements.txt
   ```

4. **Set up configuration**:
   ```bash
   # Copy example config
   cp ../../gen_mentor/config/config.example.yaml ../../gen_mentor/config/config.yaml

   # Set API keys via environment variables
   export OPENAI_API_KEY="your-openai-api-key"
   export DEEPSEEK_API_KEY="your-deepseek-api-key"
   export ANTHROPIC_API_KEY="your-anthropic-api-key"
   ```

5. **Run the server**:
   ```bash
   python main.py
   # or
   uvicorn main:app --reload --host 0.0.0.0 --port 5000
   ```

6. **Access the API**:
   - API: http://localhost:5000/api/v1
   - Swagger UI: http://localhost:5000/docs
   - ReDoc: http://localhost:5000/redoc

### Quick Test

```bash
# Health check
curl http://localhost:5000/api/v1/health

# List available models
curl http://localhost:5000/api/v1/list-llm-models

# Chat with tutor
curl -X POST "http://localhost:5000/api/v1/chat/chat-with-tutor" \
  -H "Content-Type: application/json" \
  -d '{
    "messages": "[{\"role\": \"user\", \"content\": \"Hello!\"}]"
  }'
```

---

## API Reference

### Base URL

All API endpoints are prefixed with `/api/v1`:

```
http://localhost:5000/api/v1
```

### Authentication

Currently, no authentication is required. For production deployment, implement authentication middleware.

### Common Request Fields

All request models inherit from `BaseRequest` and include:

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `model_provider` | string | No | From config | LLM provider (openai, anthropic, deepseek, etc.) |
| `model_name` | string | No | From config | Model name (gpt-4o, claude-3-5-sonnet, etc.) |

**Default values** are loaded from `gen_mentor/config/config.yaml`:

```yaml
agent_defaults:
  model: "openai/gpt-4o"  # Format: provider/model_name
```

### Common Response Fields

All response models inherit from `BaseResponse` and include:

| Field | Type | Description |
|-------|------|-------------|
| `success` | boolean | Operation success status |
| `message` | string | Optional message |

### Error Response Format

All errors return a structured `ErrorResponse`:

```json
{
  "success": false,
  "error_code": "LLM_ERROR",
  "message": "Failed to generate response",
  "details": {
    "provider": "openai",
    "model": "gpt-4o",
    "error": "API rate limit exceeded"
  }
}
```

### Endpoint Categories

#### 1. System Endpoints

##### GET /api/v1/health

Health check endpoint.

**Response**:
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "timestamp": "2026-02-22T10:00:00Z"
}
```

##### GET /api/v1/storage-info

Get storage configuration information.

**Response**:
```json
{
  "storage_mode": "local",
  "upload_location": "/tmp/uploads/",
  "workspace_dir": "~/.gen-mentor/workspace",
  "cloud_bucket": null,
  "cloud_region": null
}
```

##### GET /api/v1/list-llm-models

List available LLM models.

**Response**:
```json
{
  "success": true,
  "models": ["openai/gpt-4o", "openai/gpt-5.1"]
}
```

#### 2. Chat Endpoints

##### POST /api/v1/chat/chat-with-tutor

Chat with AI tutor.

**Request**:
```json
{
  "messages": "[{\"role\": \"user\", \"content\": \"Explain recursion\"}]",
  "learner_profile": "{\"level\": \"beginner\"}",
  "model_provider": "openai",
  "model_name": "gpt-4o"
}
```

**Response**:
```json
{
  "success": true,
  "message": "Chat response generated",
  "response": "Recursion is a programming technique where..."
}
```

#### 3. Goals Endpoints

##### POST /api/v1/goals/refine-learning-goal

Refine a learning goal to make it more specific and achievable.

**Request**:
```json
{
  "learning_goal": "Learn programming",
  "learner_information": "No prior experience",
  "model_provider": "openai",
  "model_name": "gpt-4o"
}
```

**Response**:
```json
{
  "success": true,
  "message": "Learning goal refined",
  "refined_goal": {
    "original_goal": "Learn programming",
    "refined_goal": "Master Python fundamentals for web development",
    "subgoals": ["Learn Python syntax", "Build simple web apps"],
    "timeline": "3-6 months",
    "prerequisites": ["Basic computer skills"]
  }
}
```

#### 4. Skills Endpoints

##### POST /api/v1/skills/identify-skill-gap-with-info

Identify skill gaps based on learner information.

**Request**:
```json
{
  "learning_goal": "Become a data scientist",
  "learner_information": "Python developer, no ML experience",
  "skill_requirements": null,
  "model_provider": "openai",
  "model_name": "gpt-4o"
}
```

**Response**:
```json
{
  "success": true,
  "message": "Skill gaps identified",
  "skill_gaps": {
    "required_skills": ["Machine Learning", "Statistics", "Data Visualization"],
    "current_skills": ["Python", "Programming"],
    "gaps": ["Machine Learning", "Statistics", "Data Visualization"],
    "learning_priority": ["Statistics", "Machine Learning", "Data Visualization"]
  }
}
```

##### POST /api/v1/skills/identify-skill-gap

Identify skill gaps from uploaded CV file (multipart/form-data).

**Form Fields**:
- `goal`: Learning goal (string)
- `cv`: CV file (PDF)
- `model_provider`: LLM provider (optional)
- `model_name`: Model name (optional)

#### 5. Profile Endpoints

##### POST /api/v1/profile/create-learner-profile

Create learner profile from structured information.

**Request**:
```json
{
  "learning_goal": "Learn web development",
  "learner_information": "{\"experience\": \"beginner\", \"interests\": [\"frontend\"]}",
  "skill_gaps": "{\"missing\": [\"JavaScript\", \"CSS\"]}",
  "model_provider": "openai",
  "model_name": "gpt-4o"
}
```

**Response**:
```json
{
  "success": true,
  "message": "Learner profile created successfully",
  "learner_profile": {
    "learner_id": "uuid-here",
    "learning_goal": "Learn web development",
    "background": {"experience": "beginner"},
    "skill_levels": {},
    "learning_preferences": {},
    "created_at": "2026-02-22T10:00:00Z"
  }
}
```

##### POST /api/v1/profile/create-learner-profile-with-cv-pdf

Create learner profile from CV PDF file.

**Request**:
```json
{
  "learning_goal": "Data science career",
  "cv_path": "uploads/resume.pdf",
  "skill_requirements": "{}",
  "skill_gaps": "{}",
  "model_provider": "openai",
  "model_name": "gpt-4o"
}
```

##### POST /api/v1/profile/update-learner-profile

Update existing learner profile.

**Request**:
```json
{
  "learner_profile": "{\"learner_id\": \"123\"}",
  "learner_interactions": "[{\"type\": \"quiz_completed\"}]",
  "learner_information": "",
  "session_information": "",
  "model_provider": "openai",
  "model_name": "gpt-4o"
}
```

#### 6. Learning Path Endpoints

##### POST /api/v1/learning/schedule-learning-path

Create a structured learning path.

**Request**:
```json
{
  "learner_profile": "{\"skills\": [], \"goal\": \"web development\"}",
  "session_count": 10,
  "model_provider": "openai",
  "model_name": "gpt-4o"
}
```

**Response**:
```json
{
  "success": true,
  "message": "Learning path created",
  "learning_path": {
    "sessions": [
      {"session_id": 1, "topic": "HTML Basics", "duration": "2 hours"},
      {"session_id": 2, "topic": "CSS Fundamentals", "duration": "3 hours"}
    ]
  }
}
```

##### POST /api/v1/learning/reschedule-learning-path

Modify an existing learning path.

##### POST /api/v1/learning/explore-knowledge-points

Explore knowledge points for a learning session.

##### POST /api/v1/learning/draft-knowledge-point

Generate draft content for a single knowledge point.

##### POST /api/v1/learning/draft-knowledge-points

Generate draft content for multiple knowledge points.

##### POST /api/v1/learning/integrate-learning-document

Integrate knowledge drafts into a cohesive learning document.

##### POST /api/v1/learning/tailor-knowledge-content

Generate complete tailored learning content for a session.

**Request**:
```json
{
  "learner_profile": "{\"level\": \"beginner\"}",
  "learning_path": "{\"sessions\": []}",
  "learning_session": "{\"topic\": \"JavaScript Basics\"}",
  "use_search": true,
  "allow_parallel": true,
  "with_quiz": true
}
```

#### 7. Assessment Endpoints

##### POST /api/v1/assessment/generate-document-quizzes

Generate quizzes from learning document.

**Request**:
```json
{
  "learner_profile": "{\"level\": \"beginner\"}",
  "learning_document": "JavaScript is a programming language...",
  "single_choice_count": 3,
  "multiple_choice_count": 2,
  "true_false_count": 2,
  "short_answer_count": 1
}
```

**Response**:
```json
{
  "success": true,
  "quizzes": {
    "single_choice": [...],
    "multiple_choice": [...],
    "true_false": [...],
    "short_answer": [...]
  }
}
```

#### 8. Memory Endpoints

##### GET /api/v1/memory/learner-memory/{learner_id}

Retrieve learner's memory context.

**Response**:
```json
{
  "learner_id": "uuid",
  "profile": {...},
  "objectives": {...},
  "mastery": {...},
  "learning_path": {...},
  "context": "Recent learning activities...",
  "recent_history": [...]
}
```

##### POST /api/v1/memory/learner-memory/{learner_id}/search-history

Search learner's history (multipart/form-data).

**Form Fields**:
- `query`: Search query (string)

---

## Configuration

### Configuration Files

The system uses Hydra for hierarchical configuration:

1. **`gen_mentor/config/config.yaml`** - Main configuration file
2. **Environment variables** - Override config values

### Configuration Structure

```yaml
# Environment
environment: dev
debug: true
log_level: INFO

# Agent defaults
agent_defaults:
  model: openai/gpt-4o
  temperature: 0.0
  max_tokens: 8192
  workspace: ~/.gen-mentor/workspace

# LLM Providers
providers:
  openai:
    api_key: null  # Set via OPENAI_API_KEY
    api_base: null

  anthropic:
    api_key: null  # Set via ANTHROPIC_API_KEY
    api_base: null

  deepseek:
    api_key: null  # Set via DEEPSEEK_API_KEY
    api_base: null

# Search
search_defaults:
  provider: duckduckgo
  max_results: 5
  enable_search: false

# Embedding
embedding_defaults:
  provider: huggingface
  model_name: sentence-transformers/all-mpnet-base-v2
  enable_vectordb: false

# RAG
rag:
  chunk_size: 1000
  num_retrieval_results: 5
  allow_parallel: true
  max_workers: 3
```

### Environment Variables

Set these to configure the backend:

```bash
# Required: At least one LLM provider
export OPENAI_API_KEY="sk-..."
export ANTHROPIC_API_KEY="sk-ant-..."
export DEEPSEEK_API_KEY="sk-..."

# Optional: Search providers
export TAVILY_API_KEY="tvly-..."
export SERPER_API_KEY="..."

# Optional: Custom model defaults
export AGENT_DEFAULTS_MODEL="openai/gpt-4o"
export AGENT_DEFAULTS_TEMPERATURE="0.1"

# Optional: Backend settings
export BACKEND_UPLOAD_LOCATION="/tmp/uploads"
export BACKEND_WORKSPACE_DIR="~/.gen-mentor/workspace"
```

### Backend-Specific Settings

Settings in `apps/backend/config.py`:

```python
class BackendSettings(BaseSettings):
    # API Configuration
    api_prefix: str = "/api/v1"
    api_title: str = "GenMentor API"
    api_version: str = "1.0.0"

    # Storage Configuration
    upload_location: str = "/tmp/uploads/"
    storage_mode: str = "local"  # or "cloud"

    # Server Configuration
    host: str = "127.0.0.1"
    port: int = 5000
```

---

## Data Models

### Request Models

Located in `models/requests.py`:

1. **ChatWithTutorRequest** - Chat interactions
2. **LearningGoalRequest** - Goal refinement
3. **SkillGapIdentificationRequest** - Skill gap analysis (with info)
4. **SkillGapUploadRequest** - Skill gap analysis (with CV)
5. **LearnerProfileInitializationWithInfoRequest** - Profile creation (info)
6. **LearnerProfileInitializationRequest** - Profile creation (CV)
7. **LearnerProfileUpdateRequest** - Profile updates
8. **LearningPathSchedulingRequest** - Path scheduling
9. **LearningPathReschedulingRequest** - Path rescheduling
10. **KnowledgePointExplorationRequest** - Point exploration
11. **KnowledgePointDraftingRequest** - Single point drafting
12. **KnowledgePointsDraftingRequest** - Multiple points drafting
13. **LearningDocumentIntegrationRequest** - Document integration
14. **TailoredContentGenerationRequest** - Complete content generation
15. **KnowledgeQuizGenerationRequest** - Quiz generation

### Response Models

Located in `models/responses.py`:

1. **ChatResponse** - Chat output
2. **LearningGoalResponse** - Refined goal
3. **SkillGapResponse** - Skill gaps
4. **LearnerProfileResponse** - Profile data
5. **LearningPathResponse** - Learning path
6. **KnowledgePointsResponse** - Knowledge points
7. **KnowledgeDraftResponse** - Content draft
8. **KnowledgeDraftsResponse** - Multiple drafts
9. **LearningDocumentResponse** - Integrated document
10. **QuizResponse** - Generated quizzes
11. **MemoryResponse** - Memory data
12. **HistorySearchResponse** - Search results
13. **ModelsListResponse** - Available models
14. **StorageInfoResponse** - Storage info

### Common Models

Located in `models/common.py`:

- **BaseRequest** - Base for all requests
- **BaseResponse** - Base for all responses
- **ErrorResponse** - Error structure
- **HealthResponse** - Health check
- **StorageInfo** - Storage configuration

---

## Services

### LLM Service

**Location**: `services/llm_service.py`

Manages LLM providers and model instantiation.

**Key Methods**:

```python
class LLMService:
    def get_llm(self, provider: str, model_name: str) -> BaseChatModel:
        """Get an LLM instance for the specified provider and model."""

    def list_available_models(self) -> List[str]:
        """List all available models."""
```

**Usage**:

```python
from services.llm_service import get_llm_service

llm_service = get_llm_service()
llm = llm_service.get_llm("openai", "gpt-4o")
response = llm.invoke("Hello!")
```

### Memory Service

**Location**: `services/memory_service.py`

Handles learner context persistence and retrieval.

**Key Methods**:

```python
class MemoryService:
    def get_memory_store(self, learner_id: str) -> LearnerMemoryStore:
        """Get memory store for a learner."""

    def save_profile(self, learner_id: str, profile: dict):
        """Save learner profile."""

    def save_objectives(self, learner_id: str, objectives: dict):
        """Save learning objectives."""

    def append_mastery_entry(self, learner_id: str, entry: dict):
        """Append to learner mastery."""

    def log_interaction(self, learner_id: str, role: str, content: str):
        """Log an interaction."""

    def get_learner_memory(self, learner_id: str) -> dict:
        """Get all memory for a learner."""
```

**Usage**:

```python
from services.memory_service import get_memory_service

memory_service = get_memory_service()
memory_service.save_profile("user123", {"name": "John"})
memory_service.log_interaction("user123", "user", "I completed the lesson")
```

---

## Memory System

### Overview

The memory system provides persistent storage for learner context in local mode.

### Storage Structure

```
~/.gen-mentor/workspace/
└── memory/
    └── {learner_id}/
        ├── profile.json       # Learner profile
        ├── chat_history.json  # Chat interactions
        ├── objectives.json    # Learning goals
        ├── mastery.json       # Learning progress & evaluations
        ├── user_facts.md      # Long-term context
        └── learning_path.json # Curriculum
```

### Memory Store API

**Location**: `gen_mentor/core/memory/memory_store.py`

```python
class LearnerMemoryStore:
    def write_profile(self, profile: dict):
        """Write learner profile."""

    def read_profile(self) -> dict:
        """Read learner profile."""

    def write_objectives(self, objectives: dict):
        """Write learning objectives."""

    def read_objectives(self) -> dict:
        """Read learning objectives."""

    def append_mastery_entry(self, entry: dict):
        """Append to mastery."""

    def get_recent_history(self, n: int = 10) -> str:
        """Get recent history formatted string."""

    def get_learner_context(self) -> str:
        """Get formatted context for LLM."""
```

### Automatic Memory Logging

All endpoints automatically log interactions:

```python
# Example from profile.py
memory_service.log_interaction(
    learner_id,
    "system",
    f"Profile initialized - Goal: {request.learning_goal}",
    metadata={"timestamp": time.strftime('%Y-%m-%d %H:%M:%S')}
)
```

---

## Development Guide

### Adding a New Endpoint

1. **Create endpoint in appropriate module** (`api/v1/endpoints/`):

```python
# api/v1/endpoints/my_module.py
from fastapi import APIRouter, Depends
from models import MyRequest, MyResponse
from services.llm_service import get_llm_service, LLMService

router = APIRouter()

@router.post("/my-endpoint", response_model=MyResponse, tags=["MyModule"])
async def my_endpoint(
    request: MyRequest,
    llm_service: LLMService = Depends(get_llm_service)
):
    """My endpoint description."""
    llm = llm_service.get_llm(request.model_provider, request.model_name)
    # ... implementation
    return MyResponse(success=True, data=result)
```

2. **Define request/response models** (`models/`):

```python
# models/requests.py
class MyRequest(BaseRequest):
    field1: str = Field(..., description="Field description")
    field2: int = Field(default=10, description="Field description")
```

```python
# models/responses.py
class MyResponse(BaseResponse):
    data: dict = Field(..., description="Response data")
```

3. **Register router** (`api/v1/router.py`):

```python
from api.v1.endpoints import my_module

api_router.include_router(
    my_module.router,
    prefix="/my-module",
    tags=["MyModule"]
)
```

4. **Export models** (`models/__init__.py`):

```python
from .requests import MyRequest
from .responses import MyResponse

__all__ = ["MyRequest", "MyResponse", ...]
```

### Running Tests

```bash
# Run refactored API tests
python test_refactored.py

# Run integration tests
python test_integration.py

# Run with pytest (if configured)
pytest tests/ -v
```

### Code Style

- Follow PEP 8
- Use type hints throughout
- Document all public functions/classes
- Keep functions focused and small
- Use meaningful variable names

### Error Handling

Always use custom exceptions from `exceptions.py`:

```python
from exceptions import LLMError, ValidationError, MemoryError

try:
    result = llm.invoke(prompt)
except Exception as e:
    raise LLMError(
        f"LLM invocation failed: {str(e)}",
        details={"model": model_name, "error": str(e)}
    )
```

---

## Deployment

### Production Checklist

- [ ] Set `debug: false` in config
- [ ] Use environment variables for API keys
- [ ] Configure proper `log_level` (INFO or WARNING)
- [ ] Set up authentication/authorization
- [ ] Configure CORS properly
- [ ] Use a production ASGI server (Gunicorn + Uvicorn)
- [ ] Set up monitoring and logging
- [ ] Configure rate limiting
- [ ] Use HTTPS
- [ ] Set up backup for workspace data

### Production Server

```bash
# Install Gunicorn
pip install gunicorn

# Run with Gunicorn
gunicorn main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:5000 \
  --access-logfile - \
  --error-logfile -
```

### Docker Deployment

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000"]
```

### Environment Variables (Production)

```bash
# Required
OPENAI_API_KEY=sk-...
DEEPSEEK_API_KEY=sk-...

# Backend
BACKEND_UPLOAD_LOCATION=/var/uploads
BACKEND_WORKSPACE_DIR=/var/gen-mentor/workspace

# Optional
LOG_LEVEL=INFO
ENVIRONMENT=production
```

---

## Troubleshooting

### Common Issues

#### 1. Import Errors

**Problem**: `ImportError: attempted relative import beyond top-level package`

**Solution**: Use absolute imports:
```python
# Bad
from ..services import llm_service

# Good
from services import llm_service
```

#### 2. Model Default Mismatch

**Problem**: API docs show wrong default models

**Solution**: Ensure `gen_mentor/config/config.yaml` is properly configured and defaults are loaded in `models/defaults.py`.

#### 3. Memory Not Persisting

**Problem**: Learner context not saved

**Solution**: Check workspace directory exists and is writable:
```bash
mkdir -p ~/.gen-mentor/workspace
chmod 755 ~/.gen-mentor/workspace
```

#### 4. LLM API Errors

**Problem**: `LLMError: API key not found`

**Solution**: Set environment variables:
```bash
export OPENAI_API_KEY="your-key"
export DEEPSEEK_API_KEY="your-key"
```

#### 5. 404 Errors

**Problem**: Endpoints return 404

**Solution**: Ensure using `/api/v1` prefix:
```bash
# Bad
curl http://localhost:5000/health

# Good
curl http://localhost:5000/api/v1/health
```

### Debug Mode

Enable debug logging:

```yaml
# config.yaml
debug: true
log_level: DEBUG
```

### Health Checks

```bash
# Check server health
curl http://localhost:5000/api/v1/health

# Check available models
curl http://localhost:5000/api/v1/list-llm-models

# Check storage
curl http://localhost:5000/api/v1/storage-info
```

---

## Additional Resources

- [README.md](README.md) - Quick start guide
- [REFACTORING_COMPLETE.md](REFACTORING_COMPLETE.md) - Refactoring details
- [ENDPOINT_MIGRATION.md](ENDPOINT_MIGRATION.md) - Migration guide
- [MODEL_DEFAULTS_ALIGNMENT.md](MODEL_DEFAULTS_ALIGNMENT.md) - Config alignment
- [ENDPOINT_NAMING_IMPROVEMENT.md](ENDPOINT_NAMING_IMPROVEMENT.md) - Naming changes

### API Documentation

- Swagger UI: http://localhost:5000/docs
- ReDoc: http://localhost:5000/redoc
- OpenAPI JSON: http://localhost:5000/openapi.json

---

**Last Updated**: 2026-02-22
**Version**: 1.0.0
**Maintainer**: GenMentor Team
