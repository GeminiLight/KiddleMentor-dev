# GenMentor Backend Documentation

## Table of Contents

1. [Overview](#1-overview)
2. [Architecture](#2-architecture)
3. [Directory Structure](#3-directory-structure)
4. [Core Components](#4-core-components)
5. [API Endpoints](#5-api-endpoints)
6. [Data Models](#6-data-models)
7. [Services Layer](#7-services-layer)
8. [Repository Layer](#8-repository-layer)
9. [Middleware](#9-middleware)
10. [Configuration](#10-configuration)
11. [Error Handling](#11-error-handling)
12. [Dependency Injection](#12-dependency-injection)
13. [Deployment](#13-deployment)
14. [Development Guide](#14-development-guide)

---

## 1. Overview

The GenMentor Backend is a FastAPI-based REST API that powers the AI-driven personalized learning platform. It provides endpoints for:

- **Session Management**: Learner registration and session initialization
- **Profile Management**: Learner profile creation, updates, and retrieval
- **Goal Refinement**: AI-powered learning goal refinement
- **Skill Gap Analysis**: Identification of skill gaps based on learning goals
- **Learning Path Scheduling**: Personalized learning path generation
- **Content Generation**: Tailored learning content creation
- **AI Tutoring**: Interactive chat with AI tutor
- **Assessment**: Quiz generation and performance evaluation
- **Memory Management**: Learner context and history persistence

### Key Features

- **Modular Architecture**: Clean separation of concerns with services, repositories, and API layers
- **Type Safety**: Pydantic models for request/response validation
- **Dependency Injection**: FastAPI's DI system for clean, testable code
- **Structured Error Handling**: Custom exceptions with consistent error responses
- **Flexible Configuration**: Environment-based configuration with sensible defaults
- **CORS Support**: Configurable CORS for frontend integration

---

## 2. Architecture

### 2.1 System Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           GenMentor Backend                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                           API Layer                                  │   │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────────┐  │   │
│  │  │   System     │  │   Chat       │  │   Profile/Session        │  │   │
│  │  │   /health    │  │   /chat      │  │   /profile              │  │   │
│  │  └──────────────┘  └──────────────┘  └──────────────────────────┘  │   │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────────┐  │   │
│  │  │   Goals      │  │   Skills     │  │   Learning Path          │  │   │
│  │  │   /goals     │  │   /skills    │  │   /learning              │  │   │
│  │  └──────────────┘  └──────────────┘  └──────────────────────────┘  │   │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────────┐  │   │
│  │  │ Assessment   │  │   Memory     │  │   Dashboard/Progress     │  │   │
│  │  │/assessment   │  │   /memory    │  │   /dashboard, /progress  │  │   │
│  │  └──────────────┘  └──────────────┘  └──────────────────────────┘  │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                        │
│  ┌─────────────────────────────────▼───────────────────────────────────┐   │
│  │                         Services Layer                               │   │
│  │  ┌──────────────────┐  ┌──────────────────┐                        │   │
│  │  │   LLMService     │  │   MemoryService   │                        │   │
│  │  │   (llm_service)  │  │ (memory_service)  │                        │   │
│  │  └──────────────────┘  └──────────────────┘                        │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                        │
│  ┌─────────────────────────────────▼───────────────────────────────────┐   │
│  │                        Repository Layer                              │   │
│  │  ┌──────────────────────────────────────────────────────────────┐  │   │
│  │  │                  LearnerRepository                            │  │   │
│  │  │        (profile, objectives, mastery, history, path)          │  │   │
│  │  └──────────────────────────────────────────────────────────────┘  │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                        │
│  ┌─────────────────────────────────▼───────────────────────────────────┐   │
│  │                      Infrastructure Layer                            │   │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────────┐  │   │
│  │  │ gen_mentor   │  │   Config     │  │   Error Handlers         │  │   │
│  │  │   Package    │  │   System     │  │   Middleware             │  │   │
│  │  └──────────────┘  └──────────────┘  └──────────────────────────┘  │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 2.2 Request Flow

```
┌─────────┐    ┌─────────────┐    ┌─────────────┐    ┌───────────────┐
│ Client  │───▶│   FastAPI   │───▶│  Endpoint   │───▶│    Service    │
│ Request │    │   Router    │    │  Handler    │    │    Layer      │
└─────────┘    └─────────────┘    └─────────────┘    └───────────────┘
                                                              │
                                                              ▼
┌─────────┐    ┌─────────────┐    ┌─────────────┐    ┌───────────────┐
│ Client  │◀───│   Response  │◀───│   Pydantic  │◀───│  gen_mentor   │
│ Response│    │   Model     │    │   Model     │    │    Package    │
└─────────┘    └─────────────┘    └─────────────┘    └───────────────┘
```

---

## 3. Directory Structure

```
apps/backend/
├── main.py                    # Application entry point
├── config.py                  # Configuration management
├── dependencies.py            # Dependency injection
├── exceptions.py              # Custom exceptions
├── schemas.py                 # Legacy request schemas
│
├── api/                       # API layer
│   └── v1/                    # Version 1 endpoints
│       ├── router.py          # API router aggregation
│       └── endpoints/         # Individual endpoint modules
│           ├── system.py      # Health, storage info, model listing
│           ├── chat.py        # AI tutor chat
│           ├── goals.py       # Goal refinement
│           ├── skills.py      # Skill gap identification
│           ├── profile.py     # Learner profile management
│           ├── learning_path.py # Learning path & content
│           ├── assessment.py  # Quiz generation
│           ├── memory.py      # Memory/context management
│           ├── dashboard.py   # Dashboard data aggregation
│           └── progress.py    # Session progress tracking
│
├── models/                    # Data models
│   ├── __init__.py           # Model exports
│   ├── requests.py           # Request models
│   ├── responses.py          # Response models
│   ├── common.py             # Common/base models
│   └── defaults.py           # Default values
│
├── services/                  # Service layer
│   ├── llm_service.py        # LLM management
│   └── memory_service.py     # Memory/context service
│
├── repositories/              # Data access layer
│   ├── base.py               # Base repository interface
│   └── learner_repository.py # Learner data repository
│
├── middleware/                # Middleware
│   └── error_handler.py      # Global error handling
│
└── tests/                     # Test files
    └── test_integration.py
```

---

## 4. Core Components

### 4.1 Application Entry Point

**File**: `main.py`

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import get_backend_settings, get_app_config
from middleware.error_handler import setup_error_handlers
from api.v1.router import api_router

# Create FastAPI application
app = FastAPI(
    title="GenMentor API",
    description="Personalized AI-powered learning platform",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# Setup CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=backend_settings.cors_origins,
    allow_credentials=backend_settings.cors_allow_credentials,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Setup error handlers
setup_error_handlers(app)

# Include API router
app.include_router(api_router, prefix=backend_settings.api_prefix)
```

**Key Features**:
- CORS middleware configuration
- Global error handler setup
- Lifecycle events (startup/shutdown)
- Uvicorn server runner

### 4.2 Configuration

**File**: `config.py`

```python
class BackendSettings(BaseSettings):
    """Backend-specific settings."""
    
    # Server configuration
    host: str = Field(default="127.0.0.1", env="BACKEND_HOST")
    port: int = Field(default=5000, env="BACKEND_PORT")
    reload: bool = Field(default=False, env="BACKEND_RELOAD")
    workers: int = Field(default=1, env="BACKEND_WORKERS")

    # CORS configuration
    cors_origins: list[str] = Field(default=["*"])
    cors_allow_credentials: bool = Field(default=True)

    # Storage configuration
    storage_mode: str = Field(default="local")  # "local" or "cloud"
    upload_location: str = Field(default="/tmp/uploads/")
    workspace_dir: str = Field(default="~/.gen-mentor/workspace")

    # API configuration
    api_prefix: str = Field(default="/api/v1")
    debug: bool = Field(default=True)
```

---

## 5. API Endpoints

### 5.1 Endpoint Overview

| Module | Prefix | Endpoints | Description |
|--------|--------|-----------|-------------|
| System | - | `/health`, `/storage-info`, `/list-llm-models` | System status and configuration |
| Chat | `/chat` | `/chat-with-tutor` | AI tutor conversation |
| Goals | `/goals` | `/refine-learning-goal` | Goal refinement |
| Skills | `/skills` | `/identify-skill-gap-with-info`, `/identify-skill-gap` | Skill gap analysis |
| Profile | `/profile` | Multiple endpoints | Profile and session management |
| Learning | `/learning` | Multiple endpoints | Learning path and content |
| Assessment | `/assessment` | `/generate-document-quizzes` | Quiz generation |
| Memory | `/memory` | `/learner-memory/{id}`, `/search-history` | Memory management |
| Dashboard | `/dashboard` | `/{id}`, POST | Complete dashboard state |
| Progress | `/progress` | `/{id}/session-complete` | Progress tracking |

### 5.2 System Endpoints

**File**: `api/v1/endpoints/system.py`

```python
@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(
        status="healthy",
        version="1.0.0",
        timestamp=datetime.now().isoformat()
    )

@router.get("/storage-info", response_model=StorageInfo)
async def get_storage_info(settings: BackendSettings = Depends(get_backend_settings)):
    """Get storage configuration information."""
    return StorageInfo(
        storage_mode=settings.storage_mode,
        upload_location=str(settings.upload_location),
        workspace_dir=str(settings.workspace_dir),
        ...
    )

@router.get("/list-llm-models", response_model=LLMModelsResponse)
async def list_llm_models(llm_service: LLMService = Depends(get_llm_service)):
    """List available LLM models."""
    models_data = llm_service.list_available_models()
    ...
```

### 5.3 Chat Endpoint

**File**: `api/v1/endpoints/chat.py`

```python
@router.post("/chat-with-tutor", response_model=ChatResponse)
async def chat_with_tutor(
    request: ChatWithTutorRequest,
    llm_service: LLMService = Depends(get_llm_service),
    memory_service: MemoryService = Depends(get_memory_service),
    search_rag_manager: SearchRagManager = Depends(get_search_rag_manager)
):
    """Chat with AI tutor.
    
    Provides interactive conversational learning with personalized responses
    based on the learner's profile and history.
    """
    # Get LLM
    llm = llm_service.get_llm(request.model)
    
    # Extract learner_id from profile
    learner_id = extract_learner_id(request.learner_profile)
    
    # Parse messages
    converted_messages = json.loads(request.messages)
    
    # Get memory store for context-aware chat
    memory_store = memory_service.get_memory_store(learner_id)
    
    # Load learner profile from memory if not provided
    learner_profile = request.learner_profile
    if not learner_profile and learner_id:
        learner_profile = memory_service.load_profile_from_memory(learner_id)
    
    # Generate response with memory context
    response = chat_with_tutor_with_llm(
        llm,
        converted_messages,
        learner_profile,
        search_rag_manager=search_rag_manager,
        memory_store=memory_store,
        use_search=True,
    )
    
    # Log interaction to workspace memory
    memory_service.log_interaction(learner_id, "learner", last_message["content"])
    memory_service.log_interaction(learner_id, "tutor", response)
    
    return ChatResponse(success=True, response=response)
```

### 5.4 Profile Endpoints

**File**: `api/v1/endpoints/profile.py`

#### Session Management

```python
@router.post("/initialize-session", response_model=InitializeSessionResponse)
async def initialize_session(
    request: InitializeSessionRequest,
    repository: LearnerRepository = Depends(get_learner_repository)
):
    """Initialize a new learner session."""
    # Generate unique learner ID
    learner_id = f"learner_{uuid.uuid4().hex[:12]}"
    
    # Create initial profile
    profile = {
        "learner_id": learner_id,
        "name": request.name or "Anonymous Learner",
        "email": request.email,
        "created_at": datetime.now().isoformat(),
        "metadata": request.metadata or {}
    }
    
    # Save to repository
    repository.save_profile(learner_id, profile)
    
    return InitializeSessionResponse(
        success=True,
        learner_id=learner_id,
        profile=profile
    )
```

#### Goal Setting

```python
@router.post("/{learner_id}/set-goal", response_model=RefinedGoalResponse)
async def set_learning_goal(
    learner_id: str,
    request: SetLearningGoalRequest,
    llm_service: LLMService = Depends(get_llm_service),
    repository: LearnerRepository = Depends(get_learner_repository)
):
    """Set and refine learning goal for learner."""
    # Get LLM
    llm = llm_service.get_llm(request.model_provider, request.model_name)
    
    # Refine goal
    refined_goal = refine_learning_goal_with_llm(
        llm,
        request.learning_goal,
        learner_information=profile.get("metadata", {})
    )
    
    # Update profile with goal
    profile["learning_goal"] = request.learning_goal
    profile["refined_goal"] = refined_goal
    repository.save_profile(learner_id, profile)
    
    # Save objectives
    repository.save_objectives(learner_id, {
        "learning_goal": request.learning_goal,
        "refined_goal": refined_goal,
    })
    
    return RefinedGoalResponse(
        success=True,
        refined_goal=refined_goal
    )
```

#### Profile Creation

```python
@router.post("/create-learner-profile", response_model=LearnerProfileResponse)
async def create_learner_profile(
    request: LearnerProfileInitializationWithInfoRequest,
    llm_service: LLMService = Depends(get_llm_service),
    memory_service: MemoryService = Depends(get_memory_service)
):
    """Create learner profile from information."""
    # Get LLM
    llm = llm_service.get_llm(request.model_provider, request.model_name)
    
    # Initialize profile
    learner_profile = initialize_learner_profile_with_llm(
        llm,
        request.learning_goal,
        learner_information,
        skill_gaps
    )
    
    # Persist profile to workspace memory
    learner_id = learner_profile.get("learner_id")
    memory_service.save_profile(learner_id, learner_profile)
    memory_service.save_objectives(learner_id, {...})
    
    return LearnerProfileResponse(
        success=True,
        learner_profile=learner_profile
    )
```

### 5.5 Learning Path Endpoints

**File**: `api/v1/endpoints/learning_path.py`

#### Path Scheduling

```python
@router.post("/schedule-learning-path", response_model=LearningPathResponse)
async def schedule_learning_path(
    request: LearningPathSchedulingRequest,
    llm_service: LLMService = Depends(get_llm_service),
    memory_service: MemoryService = Depends(get_memory_service)
):
    """Schedule learning path."""
    # Get LLM
    llm = llm_service.get_llm(request.model_provider, request.model_name)
    
    # Parse learner profile
    learner_profile = json.loads(request.learner_profile)
    learner_id = learner_profile.get("learner_id")
    
    # Get memory store for agent
    memory_store = memory_service.get_memory_store(learner_id)
    
    # Schedule learning path
    learning_path = schedule_learning_path_with_llm(
        llm,
        learner_profile,
        request.session_count,
        memory_store=memory_store
    )
    
    # Persist learning path
    memory_service.save_learning_path(learner_id, learning_path)
    
    return LearningPathResponse(
        success=True,
        learning_path=learning_path
    )
```

#### Content Generation

```python
@router.post("/tailor-knowledge-content", response_model=TailoredContentResponse)
async def tailor_knowledge_content(
    request: TailoredContentGenerationRequest,
    llm_service: LLMService = Depends(get_llm_service),
    memory_service: MemoryService = Depends(get_memory_service)
):
    """Generate complete personalized learning content for a session."""
    # Get LLM
    llm = llm_service.get_llm()
    
    # Generate tailored content
    tailored_content = create_learning_content_with_llm(
        llm,
        request.learner_profile,
        request.learning_path,
        request.learning_session,
        allow_parallel=request.allow_parallel,
        with_quiz=request.with_quiz,
        use_search=request.use_search
    )
    
    # Log content generation
    memory_service.append_mastery_entry(learner_id, {...})
    
    return TailoredContentResponse(
        success=True,
        tailored_content=tailored_content
    )
```

### 5.6 Dashboard Endpoint

**File**: `api/v1/endpoints/dashboard.py`

```python
@router.get("/{learner_id}", response_model=DashboardResponse)
async def get_dashboard(
    learner_id: str,
    repository: LearnerRepository = Depends(get_learner_repository)
):
    """Get complete dashboard state for learner."""
    # Get all data
    profile = repository.get_profile(learner_id)
    objectives = repository.get_objectives(learner_id)
    learning_path = repository.get_learning_path(learner_id)
    mastery = repository.get_mastery(learner_id)
    recent_history = repository.get_history(learner_id, limit=20)
    
    # Calculate progress
    total_sessions = len(learning_path.get("sessions", []))
    completed_sessions = sum(1 for s in sessions if s.get("completed"))
    progress_percent = (completed_sessions / total_sessions * 100)
    
    # Find current session
    current_session = next(
        (s for s in sessions if not s.get("completed")),
        None
    )
    
    return DashboardResponse(
        success=True,
        learner=learner_info,
        current_session=current_session,
        learning_path=learning_path,
        recent_activity=recent_activity,
        mastery=mastery
    )
```

### 5.7 Progress Endpoint

**File**: `api/v1/endpoints/progress.py`

```python
@router.post("/{learner_id}/session-complete", response_model=SessionCompleteResponse)
async def mark_session_complete(
    learner_id: str,
    request: SessionCompleteRequest,
    repository: LearnerRepository = Depends(get_learner_repository)
):
    """Mark a learning session as complete."""
    # Get learning path
    learning_path = repository.get_learning_path(learner_id)
    
    # Find and mark session as complete
    for session in sessions:
        if session.get("session_number") == request.session_number:
            session["completed"] = True
            session["completed_at"] = datetime.now().isoformat()
            session["duration_minutes"] = request.duration_minutes
            session["quiz_score"] = request.quiz_score
    
    # Save updated learning path
    repository.save_learning_path(learner_id, learning_path)
    
    # Update mastery if quiz score provided
    if request.quiz_score is not None:
        mastery = repository.get_mastery(learner_id)
        session_topic = sessions[request.session_number - 1].get("topic")
        new_mastery = (current_mastery + request.quiz_score) / 2
        mastery[session_topic] = new_mastery
        repository.save_mastery(learner_id, mastery)
    
    return SessionCompleteResponse(
        success=True,
        session_number=request.session_number,
        next_session=next_session,
        progress_percent=progress_percent
    )
```

---

## 6. Data Models

### 6.1 Model Organization

```
models/
├── __init__.py        # Exports all models
├── common.py          # Base models, ErrorResponse, HealthResponse
├── requests.py        # Request models for all endpoints
├── responses.py       # Response models for all endpoints
└── defaults.py        # Default values (model provider, model name)
```

### 6.2 Base Models

**File**: `models/common.py`

```python
class BaseRequest(BaseModel):
    """Base request model with common fields.
    
    Uses unified model parameter in "provider/model" format.
    Examples: "openai/gpt-4", "anthropic/claude-3-5-sonnet", "deepseek/deepseek-chat"
    """
    model: Optional[str] = Field(
        default=f"{DEFAULT_MODEL_PROVIDER}/{DEFAULT_MODEL_NAME}",
        description="Model in 'provider/model' format (e.g., 'deepseek/deepseek-chat')"
    )

    def get_model_parts(self) -> tuple[str, str]:
        """Parse model into provider and name.
        
        Returns:
            Tuple of (provider, model_name)
        """
        if self.model and "/" in self.model:
            parts = self.model.split("/", 1)
            return parts[0], parts[1]
        # Fallback: treat as model name only, use default provider
        return DEFAULT_MODEL_PROVIDER, self.model or DEFAULT_MODEL_NAME


class BaseResponse(BaseModel):
    """Base response model with common fields."""
    success: bool = Field(default=True)
    message: Optional[str] = Field(default=None)


class ErrorResponse(BaseModel):
    """Error response model."""
    success: bool = Field(default=False)
    error_code: str = Field(...)
    message: str = Field(...)
    details: Optional[dict[str, Any]] = Field(default=None)
```

### 6.3 Request Models

**File**: `models/requests.py`

#### Session Requests

```python
class InitializeSessionRequest(BaseModel):
    """Request for initializing a new learner session."""
    name: Optional[str] = Field(None, description="Learner name")
    email: Optional[str] = Field(None, description="Learner email")
    metadata: Optional[dict] = Field(None, description="Additional metadata")


class SetLearningGoalRequest(BaseRequest):
    """Request for setting a learning goal."""
    learning_goal: str = Field(..., description="Learning goal to set")
    learner_id: Optional[str] = Field(None, description="Learner identifier")


class SessionCompleteRequest(BaseModel):
    """Request for marking a session as complete."""
    session_number: int = Field(..., ge=1)
    duration_minutes: Optional[int] = Field(None, ge=0)
    quiz_score: Optional[int] = Field(None, ge=0, le=100)
    learner_id: Optional[str] = Field(None)
```

#### Chat Request

```python
class ChatWithTutorRequest(BaseRequest):
    """Request for chatting with AI tutor."""
    messages: str = Field(..., description="JSON string array of chat messages")
    learner_profile: str = Field(default="", description="JSON string of learner profile")

    @field_validator("messages")
    @classmethod
    def validate_messages(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("messages cannot be empty")
        if not v.strip().startswith("["):
            raise ValueError("messages must be a JSON array string")
        return v
```

#### Learning Path Requests

```python
class LearningPathSchedulingRequest(BaseRequest):
    """Request for scheduling learning path."""
    learner_profile: str = Field(..., description="Learner profile as JSON string")
    session_count: int = Field(..., gt=0, le=100)


class TailoredContentGenerationRequest(BaseModel):
    """Request for generating tailored learning content."""
    learner_profile: str = Field(...)
    learning_path: str = Field(...)
    learning_session: str = Field(...)
    use_search: bool = Field(default=True)
    allow_parallel: bool = Field(default=True)
    with_quiz: bool = Field(default=True)
```

### 6.4 Response Models

**File**: `models/responses.py`

```python
class InitializeSessionResponse(BaseResponse):
    """Response from session initialization."""
    learner_id: str
    profile: Dict[str, Any]


class DashboardResponse(BaseResponse):
    """Response containing complete dashboard state."""
    learner: Dict[str, Any]
    current_session: Optional[Dict[str, Any]]
    learning_path: Optional[Dict[str, Any]]
    recent_activity: List[Dict[str, Any]]
    mastery: Dict[str, Any]


class ChatResponse(BaseResponse):
    """Response from chat with tutor."""
    response: str


class LearningPathResponse(BaseResponse):
    """Response containing learning path."""
    learning_path: Dict[str, Any]
    session_count: int


class TailoredContentResponse(BaseResponse):
    """Response containing tailored learning content."""
    tailored_content: Dict[str, Any]
```

---

## 7. Services Layer

### 7.1 LLM Service

**File**: `services/llm_service.py`

```python
class LLMService:
    """Service for managing LLM operations."""

    def __init__(self):
        self.config = get_app_config()

    def get_llm(
        self,
        model: Optional[str] = None,
        **kwargs
    ) -> BaseChatModel:
        """Get LLM instance.
        
        Args:
            model: Model in "provider/model" format (e.g., "deepseek/deepseek-chat")
                   If only model name is provided, uses default provider.
            
        Returns:
            BaseChatModel instance
        """
        # Parse model string
        if model is None:
            model = f"{self.config.agent_defaults.default_provider}/{self.config.agent_defaults.model}"
        
        if "/" in model:
            model_provider, model_name = model.split("/", 1)
        else:
            # Fallback: treat as model name only
            model_provider = self.config.agent_defaults.default_provider
            model_name = model

        # Get provider config
        provider_config = getattr(self.config.providers, model_provider, None)

        # Create LLM with config
        return LLMFactory.create(
            model=model_name,
            model_provider=model_provider,
            temperature=self.config.agent_defaults.temperature,
            base_url=provider_config.api_base,
            api_key=provider_config.api_key,
            **kwargs
        )

    def list_available_models(self) -> list[dict[str, str]]:
        """List available models from configuration.
        
        Returns models in unified "provider/model" format.
        """
        model_full = self.config.agent_defaults.model
        if "/" in model_full:
            provider, model_name = model_full.split("/", 1)
        else:
            provider = self.config.agent_defaults.default_provider
            model_name = model_full
        return [{"model": f"{provider}/{model_name}"}]
```

### 7.2 Memory Service

**File**: `services/memory_service.py`

```python
class MemoryService:
    """Service for managing learner memory and context."""

    def __init__(self):
        self.settings = get_backend_settings()

    def is_available(self) -> bool:
        """Check if memory storage is available."""
        return self.settings.storage_mode.lower() == "local"

    def get_memory_store(self, learner_id: Optional[str] = None) -> Optional[LearnerMemoryStore]:
        """Get learner memory store."""
        if not self.is_available():
            return None
        return LearnerMemoryStore(
            workspace=self.settings.workspace_dir,
            learner_id=learner_id
        )

    def get_learner_memory(self, learner_id: str) -> Dict[str, Any]:
        """Get all memory and context for a learner."""
        memory = self.get_memory_store(learner_id)
        return {
            "learner_id": learner_id,
            "profile": memory.read_profile(),
            "objectives": memory.read_objectives(),
            "mastery": memory.read_mastery(),
            "learning_path": memory.read_learning_path(),
            "context": memory.get_learner_context(),
            "recent_history": memory.get_recent_history(n=20),
        }

    def log_interaction(self, learner_id: str, role: str, content: str, metadata: Optional[dict] = None):
        """Log a learning interaction to history."""
        memory = self.get_memory_store(learner_id)
        if memory:
            memory.log_interaction(role, content, metadata)

    def save_profile(self, learner_id: str, profile: Dict[str, Any]):
        """Save learner profile to memory."""
        memory = self.get_memory_store(learner_id)
        if memory:
            memory.write_profile(profile)

    def load_profile_from_memory(self, learner_id: str, provided_profile: Optional[Any] = None) -> Any:
        """Load learner profile from memory if not provided."""
        if provided_profile:
            return provided_profile
        memory = self.get_memory_store(learner_id)
        if memory:
            return memory.read_profile() or {}
        return {}
```

---

## 8. Repository Layer

### 8.1 Learner Repository

**File**: `repositories/learner_repository.py`

```python
class LearnerRepository(BaseRepository):
    """Repository for learner data using file-based storage.
    
    Wraps LearnerMemoryStore to provide a clean, standardized interface
    for learner data access.
    """

    def __init__(self, workspace: str | Path):
        self.workspace = Path(workspace).expanduser()

    def _get_memory_store(self, learner_id: str) -> LearnerMemoryStore:
        """Get memory store instance for learner."""
        return LearnerMemoryStore(
            workspace=str(self.workspace),
            learner_id=learner_id
        )

    # Profile operations
    def get_profile(self, learner_id: str) -> Optional[dict[str, Any]]:
        """Get learner profile."""
        memory_store = self._get_memory_store(learner_id)
        return memory_store.read_profile()

    def save_profile(self, learner_id: str, profile: dict[str, Any]):
        """Save learner profile."""
        memory_store = self._get_memory_store(learner_id)
        memory_store.write_profile(profile)

    # Objectives operations
    def get_objectives(self, learner_id: str) -> Optional[dict[str, Any]]:
        """Get learning objectives."""
        memory_store = self._get_memory_store(learner_id)
        return memory_store.read_objectives()

    def save_objectives(self, learner_id: str, objectives: dict[str, Any]):
        """Save learning objectives."""
        memory_store = self._get_memory_store(learner_id)
        memory_store.write_objectives(objectives)

    # Learning path operations
    def get_learning_path(self, learner_id: str) -> Optional[dict[str, Any]]:
        """Get learning path."""
        memory_store = self._get_memory_store(learner_id)
        return memory_store.read_learning_path()

    def save_learning_path(self, learner_id: str, learning_path: dict[str, Any]):
        """Save learning path."""
        memory_store = self._get_memory_store(learner_id)
        memory_store.write_learning_path(learning_path)

    # Mastery operations
    def get_mastery(self, learner_id: str) -> Optional[dict[str, Any]]:
        """Get mastery data."""
        memory_store = self._get_memory_store(learner_id)
        return memory_store.read_mastery()

    def save_mastery(self, learner_id: str, mastery: dict[str, Any]):
        """Save mastery data."""
        memory_store = self._get_memory_store(learner_id)
        memory_store.write_mastery(mastery)

    # History operations
    def get_history(self, learner_id: str, limit: int = 100) -> list[dict[str, Any]]:
        """Get interaction history."""
        memory_store = self._get_memory_store(learner_id)
        history = memory_store.read_history()
        if limit > 0 and len(history) > limit:
            return history[-limit:]
        return history

    def log_interaction(self, learner_id: str, role: str, content: str, metadata: Optional[dict] = None):
        """Log an interaction."""
        memory_store = self._get_memory_store(learner_id)
        memory_store.log_interaction(role, content, metadata)

    # Aggregate operations
    def get_learner_context(self, learner_id: str) -> dict[str, Any]:
        """Get complete learner context for AI agents."""
        return {
            "learner_id": learner_id,
            "profile": self.get_profile(learner_id) or {},
            "objectives": self.get_objectives(learner_id) or {},
            "mastery": self.get_mastery(learner_id) or {},
            "learning_path": self.get_learning_path(learner_id) or {},
            "recent_history": self.get_history(learner_id, limit=10)
        }
```

---

## 9. Middleware

### 9.1 Error Handler Middleware

**File**: `middleware/error_handler.py`

```python
async def backend_exception_handler(request: Request, exc: BackendException) -> JSONResponse:
    """Handle custom backend exceptions."""
    error_response = ErrorResponse(
        error_code=exc.error_code,
        message=exc.message,
        details=exc.details
    )
    return JSONResponse(
        status_code=exc.status_code,
        content=error_response.model_dump()
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """Handle request validation errors."""
    errors = [{"loc": e["loc"], "msg": e["msg"], "type": e["type"]} for e in exc.errors()]
    error_response = ErrorResponse(
        error_code="VALIDATION_ERROR",
        message="Request validation failed",
        details={"errors": errors}
    )
    return JSONResponse(
        status_code=422,
        content=error_response.model_dump()
    )


async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handle unexpected exceptions."""
    error_response = ErrorResponse(
        error_code="INTERNAL_SERVER_ERROR",
        message="An unexpected error occurred",
        details={"type": type(exc).__name__, "message": str(exc)}
    )
    return JSONResponse(
        status_code=500,
        content=error_response.model_dump()
    )


def setup_error_handlers(app):
    """Setup all error handlers for the application."""
    app.add_exception_handler(BackendException, backend_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(StarletteHTTPException, http_exception_handler)
    app.add_exception_handler(Exception, general_exception_handler)
```

---

## 10. Configuration

### 10.1 Configuration Sources

1. **Environment Variables**: Loaded via Pydantic Settings
2. **gen_mentor Package Config**: YAML configuration files
3. **Default Values**: Hardcoded defaults in model classes

### 10.2 Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `BACKEND_HOST` | `127.0.0.1` | Server host |
| `BACKEND_PORT` | `5000` | Server port |
| `BACKEND_RELOAD` | `False` | Enable auto-reload |
| `BACKEND_WORKERS` | `1` | Number of workers |
| `CORS_ORIGINS` | `["*"]` | Allowed CORS origins |
| `STORAGE_MODE` | `local` | Storage mode (local/cloud) |
| `UPLOAD_LOCATION` | `/tmp/uploads/` | File upload location |
| `WORKSPACE_DIR` | `~/.gen-mentor/workspace` | Workspace directory |
| `API_PREFIX` | `/api/v1` | API URL prefix |
| `DEBUG` | `True` | Debug mode |

### 10.3 Configuration Classes

```python
class BackendSettings(BaseSettings):
    """Backend-specific settings."""
    host: str = Field(default="127.0.0.1", env="BACKEND_HOST")
    port: int = Field(default=5000, env="BACKEND_PORT")
    # ... other settings

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


class Config:
    """Main configuration holder."""
    def __init__(self):
        self.backend = BackendSettings()
        self.app = load_config()  # Load from gen_mentor config

    @property
    def is_local_storage(self) -> bool:
        return self.backend.storage_mode.lower() == "local"
```

---

## 11. Error Handling

### 11.1 Custom Exceptions

**File**: `exceptions.py`

```python
class BackendException(Exception):
    """Base exception for backend errors."""
    def __init__(self, message: str, status_code: int = 500, error_code: Optional[str] = None, details: Optional[dict] = None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.error_code = error_code or self.__class__.__name__
        self.details = details or {}


class ValidationError(BackendException):
    """Raised when input validation fails."""
    def __init__(self, message: str, details: Optional[dict] = None):
        super().__init__(message, status_code=400, error_code="VALIDATION_ERROR", details=details)


class NotFoundError(BackendException):
    """Raised when a resource is not found."""
    def __init__(self, message: str, resource_type: Optional[str] = None):
        super().__init__(message, status_code=404, error_code="NOT_FOUND", details={"resource_type": resource_type})


class LLMError(BackendException):
    """Raised when LLM operations fail."""
    def __init__(self, message: str, details: Optional[dict] = None):
        super().__init__(message, status_code=500, error_code="LLM_ERROR", details=details)


class StorageError(BackendException):
    """Raised when storage operations fail."""
    def __init__(self, message: str, details: Optional[dict] = None):
        super().__init__(message, status_code=500, error_code="STORAGE_ERROR", details=details)


class MemoryError(BackendException):
    """Raised when memory operations fail."""
    def __init__(self, message: str, details: Optional[dict] = None):
        super().__init__(message, status_code=500, error_code="MEMORY_ERROR", details=details)
```

### 11.2 Error Response Format

```json
{
    "success": false,
    "error_code": "VALIDATION_ERROR",
    "message": "learning_goal cannot be empty",
    "details": {
        "field": "learning_goal"
    }
}
```

---

## 12. Dependency Injection

**File**: `dependencies.py`

### 12.1 Configuration Dependencies

```python
def get_settings() -> BackendSettings:
    """Get backend settings dependency."""
    return get_backend_settings()


def get_config() -> AppConfig:
    """Get application config dependency."""
    return get_app_config()
```

### 12.2 Repository Dependencies

```python
_learner_repository = None

def get_learner_repository(settings: BackendSettings = Depends(get_settings)) -> LearnerRepository:
    """Get learner repository dependency (cached)."""
    global _learner_repository
    if _learner_repository is None:
        _learner_repository = LearnerRepository(workspace=settings.workspace_dir)
    return _learner_repository
```

### 12.3 Service Dependencies

```python
def get_llm_service_dep() -> LLMService:
    """Get LLM service dependency."""
    return get_llm_service()


def get_memory_service_dep() -> MemoryService:
    """Get memory service dependency."""
    return get_memory_service()
```

### 12.4 Search RAG Manager Dependency

```python
_search_rag_manager = None

def get_search_rag_manager(config: AppConfig = Depends(get_config)) -> SearchRagManager:
    """Get search RAG manager dependency (cached)."""
    global _search_rag_manager
    if _search_rag_manager is None:
        _search_rag_manager = SearchRagManager.from_config({...})
    return _search_rag_manager
```

### 12.5 Helper Dependencies

```python
def extract_learner_id(profile_data: str | Dict[str, Any]) -> Optional[str]:
    """Extract learner ID from profile data."""
    if not profile_data:
        return None
    if isinstance(profile_data, dict):
        return profile_data.get("learner_id")
    try:
        profile_dict = parse_json_string(profile_data, "learner_profile")
        return profile_dict.get("learner_id")
    except Exception:
        return None
```

---

## 13. Deployment

### 13.1 Running the Server

**Development Mode:**
```bash
cd apps/backend
python main.py
```

**With Uvicorn:**
```bash
uvicorn main:app --host 0.0.0.0 --port 5000 --reload
```

**Production:**
```bash
uvicorn main:app --host 0.0.0.0 --port 5000 --workers 4
```

### 13.2 Docker Deployment

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000"]
```

### 13.3 Environment Configuration

Create `.env` file:
```env
BACKEND_HOST=0.0.0.0
BACKEND_PORT=5000
BACKEND_RELOAD=false
STORAGE_MODE=local
WORKSPACE_DIR=/data/workspace
DEBUG=false
CORS_ORIGINS=["http://localhost:3000", "https://your-domain.com"]
```

---

## 14. Development Guide

### 14.1 Adding a New Endpoint

1. **Create Request/Response Models** in `models/requests.py` and `models/responses.py`:

```python
# models/requests.py
class MyNewRequest(BaseRequest):
    field1: str = Field(..., description="Description")

# models/responses.py
class MyNewResponse(BaseResponse):
    result: Dict[str, Any]
```

2. **Create Endpoint File** in `api/v1/endpoints/my_endpoint.py`:

```python
from fastapi import APIRouter, Depends
from models import MyNewRequest, MyNewResponse
from services.llm_service import get_llm_service, LLMService

router = APIRouter()

@router.post("/my-endpoint", response_model=MyNewResponse)
async def my_endpoint(
    request: MyNewRequest,
    llm_service: LLMService = Depends(get_llm_service)
):
    """My endpoint description."""
    # Implementation
    return MyNewResponse(success=True, result={...})
```

3. **Register Router** in `api/v1/router.py`:

```python
from api.v1.endpoints import my_endpoint

api_router.include_router(my_endpoint.router, prefix="/my-endpoint", tags=["MyTag"])
```

### 14.2 Testing

```bash
# Run tests
cd apps/backend
pytest tests/

# Run with coverage
pytest tests/ --cov=. --cov-report=html
```

### 14.3 API Documentation

- **Swagger UI**: `http://localhost:5000/docs`
- **ReDoc**: `http://localhost:5000/redoc`
- **OpenAPI JSON**: `http://localhost:5000/openapi.json`

---

## Appendix A: Complete API Reference

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/health` | Health check |
| GET | `/api/v1/storage-info` | Storage configuration |
| GET | `/api/v1/list-llm-models` | Available LLM models |
| POST | `/api/v1/chat/chat-with-tutor` | AI tutor chat |
| POST | `/api/v1/goals/refine-learning-goal` | Goal refinement |
| POST | `/api/v1/skills/identify-skill-gap-with-info` | Skill gap analysis |
| POST | `/api/v1/skills/identify-skill-gap` | Skill gap from CV |
| POST | `/api/v1/profile/initialize-session` | Initialize session |
| GET | `/api/v1/profile/{learner_id}` | Get profile |
| POST | `/api/v1/profile/{learner_id}/set-goal` | Set learning goal |
| POST | `/api/v1/profile/create-learner-profile` | Create profile |
| POST | `/api/v1/profile/update-learner-profile` | Update profile |
| POST | `/api/v1/learning/schedule-learning-path` | Schedule path |
| POST | `/api/v1/learning/reschedule-learning-path` | Reschedule path |
| POST | `/api/v1/learning/explore-knowledge-points` | Explore knowledge |
| POST | `/api/v1/learning/draft-knowledge-point` | Draft knowledge |
| POST | `/api/v1/learning/integrate-learning-document` | Integrate document |
| POST | `/api/v1/learning/tailor-knowledge-content` | Generate content |
| POST | `/api/v1/assessment/generate-document-quizzes` | Generate quizzes |
| GET | `/api/v1/memory/learner-memory/{id}` | Get learner memory |
| POST | `/api/v1/memory/learner-memory/{id}/search-history` | Search history |
| GET | `/api/v1/dashboard/{learner_id}` | Dashboard data |
| POST | `/api/v1/progress/{learner_id}/session-complete` | Mark session complete |

---

## Appendix B: Data Storage Structure

```
workspace/
└── learners/
    └── {learner_id}/
        ├── profile.json           # Learner profile
        ├── objectives.json        # Learning objectives
        ├── mastery.json           # Skill mastery levels
        ├── learning_path.json     # Learning path
        ├── user_facts.md          # Long-term memory
        └── chat_history.json      # Interaction history
```

---

*Documentation generated: 2026-02-23*
*GenMentor Backend Version: 1.0.0*
