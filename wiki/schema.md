# GenMentor Data Schema Documentation

This document describes the three data layers in the GenMentor system, providing a comprehensive reference for data protocol consistency across frontend, backend, and algorithm modules.

## Table of Contents

1. [Overview](#overview)
2. [Layer Architecture](#layer-architecture)
3. [Layer 1: Frontend Data Layer](#layer-1-frontend-data-layer)
4. [Layer 2: Backend Data Layer](#layer-2-backend-data-layer)
5. [Layer 3: Algorithm Data Layer](#layer-3-algorithm-data-layer)
6. [Multi-Goal Architecture](#multi-goal-architecture)
7. [Data Flow Mapping](#data-flow-mapping)
8. [Protocol Consistency Guidelines](#protocol-consistency-guidelines)

---

## Overview

GenMentor uses a three-tier data architecture to separate concerns and maintain clean boundaries:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           FRONTEND LAYER (TypeScript)                        │
│  Location: apps/frontend/src/lib/api.ts                                      │
│  Purpose: Client-side type definitions, API request/response interfaces      │
└─────────────────────────────────────────┬───────────────────────────────────┘
                                          │ HTTP/JSON
                                          ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                           BACKEND LAYER (Python/Pydantic)                    │
│  Location: apps/backend/models/                                              │
│  Purpose: API request/response validation, serialization                     │
└─────────────────────────────────────────┬───────────────────────────────────┘
                                          │ Python Objects
                                          ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                          ALGORITHM LAYER (Python/Pydantic)                   │
│  Location: gen_mentor/schemas/                                               │
│  Purpose: Domain models for AI/LLM processing, structured outputs            │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Layer Architecture

### Data Transformation Flow

```
┌──────────────┐    JSON     ┌──────────────┐    Python    ┌──────────────┐
│  TypeScript  │ ──────────▶ │   Pydantic   │ ───────────▶ │   Pydantic   │
│  Interface   │             │   Backend    │              │   Algorithm  │
│  (Frontend)  │ ◀────────── │   Models     │ ◀─────────── │   Schemas    │
└──────────────┘    JSON     └──────────────┘    Python    └──────────────┘
```

### Key Principles

1. **Frontend Layer**: Defines what the client sends/receives
2. **Backend Layer**: Validates and transforms API data
3. **Algorithm Layer**: Structured domain models for LLM processing

---

## Layer 1: Frontend Data Layer

**Location**: `apps/frontend/src/lib/api.ts`

### Base Types

```typescript
// Base request interface - all requests extend this
export interface BaseRequest {
  model?: string;  // Format: "provider/model" (e.g., "openai/gpt-5.1")
}
```

### Core Interfaces

#### LearnerProfile

```typescript
export interface LearnerProfile {
  learner_id: string;
  name: string;
  email?: string;
  progress_percent?: number;
  last_session_completed?: number;
  created_at: string;
  updated_at?: string;
  metadata?: Record<string, any>;
}
```

#### DashboardData

```typescript
export interface DashboardData {
  success: boolean;
  message: string;
  learner: LearnerProfile & {
    learning_goal?: string;
    refined_goal?: any;
    progress: number;
    total_sessions: number;
    completed_sessions: number;
  };
  current_session?: {
    session_number: number;
    topic: string;
    status: string;
    duration_estimate: string;
  };
  learning_path?: {
    sessions: Array<{
      session_number: number;
      topic: string;
      completed: boolean;
      quiz_score?: number;
      duration_estimate?: string;
    }>;
  };
  recent_activity: Array<{
    type: string;
    content: string;
    timestamp: string;
  }>;
  mastery: Record<string, number>;
}
```

### API Method Signatures

| Method | Request Type | Response Type | goal_id Support |
|--------|-------------|---------------|-----------------|
| `initializeSession` | `FormData (name, email, metadata, cv)` | `{ learner_id, profile }` | ❌ |
| `getProfile` | `{ learner_id: string }` | `{ success, learner_profile }` | ❌ |
| `setLearningGoal` | `{ learner_id, learning_goal, model }` | `{ success, refined_goal, rationale }` | ❌ |
| `getDashboard` | `{ learner_id: string }` | `DashboardData` | ❌ |
| `refineGoal` | `{ learning_goal, learner_information?, model? }` | `{ success, refined_goal, rationale }` | ❌ |
| `identifySkillGap` | `{ learning_goal, learner_information, skill_requirements?, model? }` | `{ success, skill_requirements, skill_gaps, learning_goal }` | ❌ |
| `identifyAndSaveSkillGap` | `{ learner_id, learning_goal, learner_information?, model? }` | `{ success, skill_requirements, skill_gaps, learning_goal }` | ❌ |
| `scheduleLearningPath` | `{ learner_profile, session_count, goal_id?, model? }` | `{ success, learning_path, session_count }` | ✅ |
| `rescheduleLearningPath` | `{ learner_profile, learning_path, session_count, other_feedback?, goal_id?, model? }` | `{ success, learning_path, session_count }` | ✅ |
| `exploreKnowledgePoints` | `{ learner_profile, learning_path, learning_session, goal_id?, model? }` | `{ success, knowledge_points }` | ✅ |
| `generateTailoredContent` | `{ learner_profile, learning_path, learning_session, with_quiz?, use_search?, allow_parallel?, goal_id?, model? }` | `{ success, tailored_content }` | ✅ |
| `completeSession` | `{ learner_id, session_number, quiz_score?, duration_minutes? }` | `{ success, session_number, next_session?, progress_percent }` | ❌ |
| `chatWithTutor` | `{ messages, learner_profile?, goal_id?, model? }` | `{ success, response }` | ✅ |
| `generateDocumentQuizzes` | `{ learning_document, quiz_count?, goal_id?, model? }` | `{ success, quizzes }` | ✅ |
| `getLearnerMemory` | `{ learner_id: string }` | `{ success, learner_id, profile, learning_goals, skill_gaps, mastery, learning_path, context, recent_history }` | ❌ |
| `listUsers` | - | `{ success, users, count }` | ❌ |
| `loginUser` | `{ learner_id: string }` | `{ success, learner_id, name, email? }` | ❌ |
| `deleteUser` | `{ learner_id: string }` | `{ success, message }` | ❌ |

---

## Layer 2: Backend Data Layer

**Location**: `apps/backend/`

### File Structure

```
apps/backend/
├── models/                    # New model structure (primary)
│   ├── __init__.py           # Model exports
│   ├── common.py             # Base models (BaseRequest, BaseResponse, ErrorResponse)
│   ├── requests.py           # Request models for all endpoints
│   ├── responses.py          # Response models for all endpoints
│   └── defaults.py           # Default values (DEFAULT_MODEL_PROVIDER, DEFAULT_MODEL_NAME)
├── schemas.py                # Legacy schemas (deprecated, kept for compatibility)
├── schemas.py                # Top-level schemas (legacy)
├── services/
│   └── memory_service.py     # Memory management service
├── repositories/
│   └── learner_repository.py # Learner data repository
├── api/v1/endpoints/         # API endpoint handlers
└── core/                     # Core utilities and dependencies
```

> **Note**: The `apps/backend/models/` directory contains the new Pydantic models using the unified `model` parameter. The legacy `schemas.py` file at the root still uses the old `model_provider`/`model_name` split and is deprecated.

### Base Models

**File**: `models/common.py`

```python
class BaseRequest(BaseModel):
    """Base request model with common fields.
    
    Uses unified model parameter in "provider/model" format.
    Examples: "openai/gpt-4", "anthropic/claude-3-5-sonnet", "deepseek/deepseek-chat"
    """
    model: Optional[str] = Field(
        default=f"{DEFAULT_MODEL_PROVIDER}/{DEFAULT_MODEL_NAME}",
        description="Model in 'provider/model' format"
    )

    def get_model_parts(self) -> tuple[str, str]:
        """Parse model into provider and name.
        
        Returns:
            Tuple of (provider, model_name)
        """
        if self.model and "/" in self.model:
            parts = self.model.split("/", 1)
            return parts[0], parts[1]
        return DEFAULT_MODEL_PROVIDER, self.model or DEFAULT_MODEL_NAME


class BaseResponse(BaseModel):
    """Base response model with common fields."""
    success: bool = Field(default=True)
    message: Optional[str] = Field(default=None)


class ErrorResponse(BaseModel):
    """Error response model."""
    success: bool = Field(default=False)
    error_code: str
    message: str
    details: Optional[dict[str, Any]] = None
```

### Request Models

**File**: `models/requests.py`

| Model | Fields | Description | goal_id |
|-------|--------|-------------|---------|
| `InitializeSessionRequest` | `name?: str, email?: str, metadata?: dict` | Initialize new learner session | ❌ |
| `SetLearningGoalRequest` | `learning_goal: str, learner_id?: str, model?: str` | Set learning goal | ❌ |
| `SessionCompleteRequest` | `session_number: int, duration_minutes?: int, quiz_score?: int, learner_id?: str` | Mark session complete | ❌ |
| `GetDashboardRequest` | `learner_id: str` | Get dashboard data | ❌ |
| `GetProfileRequest` | `learner_id: str` | Get learner profile | ❌ |
| `GetLearnerMemoryRequest` | `learner_id: str` | Get learner memory | ❌ |
| `SearchHistoryRequest` | `learner_id: str, query: str` | Search history | ❌ |
| `ChatWithTutorRequest` | `messages: str, learner_profile: str, goal_id?: str, model?: str` | Chat with AI tutor | ✅ |
| `LearningGoalRefinementRequest` | `learning_goal: str, learner_information: str, model?: str` | Refine learning goal | ❌ |
| `SkillGapIdentificationRequest` | `learning_goal: str, learner_information: str, skill_requirements?: str, model?: str` | Identify skill gaps | ❌ |
| `LearnerProfileInitializationWithInfoRequest` | `learning_goal: str, learner_information: str, skill_gaps: str, model?: str` | Initialize profile with info | ❌ |
| `LearnerProfileInitializationRequest` | `learning_goal: str, skill_requirements: str, skill_gaps: str, cv_path: str, model?: str` | Initialize profile from CV | ❌ |
| `LearnerProfileUpdateRequest` | `learner_profile: str, learner_interactions: str, learner_information?: str, session_information?: str, model?: str` | Update profile | ❌ |
| `LearningPathSchedulingRequest` | `learner_profile: str, session_count: int, goal_id?: str, model?: str` | Schedule learning path | ✅ |
| `LearningPathReschedulingRequest` | `learner_profile: str, learning_path: str, session_count: int, other_feedback?: str, goal_id?: str, model?: str` | Reschedule learning path | ✅ |
| `KnowledgePointExplorationRequest` | `learner_profile: str, learning_path: str, learning_session: str, goal_id?: str` | Explore knowledge points | ✅ |
| `KnowledgePointDraftingRequest` | `learner_profile: str, learning_path: str, learning_session: str, knowledge_points: str, knowledge_point: str, use_search?: bool, goal_id?: str` | Draft knowledge point | ✅ |
| `KnowledgePointsDraftingRequest` | `learner_profile: str, learning_path: str, learning_session: str, knowledge_points: str, use_search?: bool, allow_parallel?: bool, goal_id?: str` | Draft multiple knowledge points | ✅ |
| `LearningDocumentIntegrationRequest` | `learner_profile: str, learning_path: str, learning_session: str, knowledge_points: str, knowledge_drafts: str, output_markdown?: bool, goal_id?: str` | Integrate document | ✅ |
| `KnowledgeQuizGenerationRequest` | `learner_profile: str, learning_document: str, single_choice_count?: int, multiple_choice_count?: int, true_false_count?: int, short_answer_count?: int, goal_id?: str` | Generate quizzes | ✅ |
| `TailoredContentGenerationRequest` | `learner_profile: str, learning_path: str, learning_session: str, use_search?: bool, allow_parallel?: bool, with_quiz?: bool, goal_id?: str` | Generate tailored content | ✅ |
| `HistorySearchRequest` | `query: str` | Search history globally | ❌ |

### Response Models

**File**: `models/responses.py`

| Model | Fields | Description |
|-------|--------|-------------|
| `InitializeSessionResponse` | `success, learner_id: str, profile: Dict` | Session initialization response |
| `DashboardResponse` | `success, learner: Dict, current_session?: Dict, learning_path?: Dict, recent_activity: List, mastery: Dict` | Dashboard data response |
| `SessionCompleteResponse` | `success, session_number: int, next_session?: Dict, progress_percent: float` | Session completion response |
| `ChatResponse` | `success, response: str` | Chat response |
| `RefinedGoalResponse` | `success, refined_goal: Any, rationale?: str` | Refined goal response |
| `SkillGapResponse` | `success, skill_requirements: Dict, skill_gaps: Dict, learning_goal: str` | Skill gap response |
| `LearnerProfileResponse` | `success, learner_profile: Dict` | Learner profile response |
| `LearningPathResponse` | `success, learning_path: Dict, session_count: int` | Learning path response |
| `KnowledgePointsResponse` | `success, knowledge_points: List[Dict]` | Knowledge points response |
| `KnowledgeDraftResponse` | `success, knowledge_draft: str` | Single knowledge draft response |
| `KnowledgeDraftsResponse` | `success, knowledge_drafts: List[str]` | Multiple knowledge drafts response |
| `LearningDocumentResponse` | `success, learning_document: str` | Learning document response |
| `QuizResponse` | `success, document_quiz: Dict` | Quiz response |
| `TailoredContentResponse` | `success, tailored_content: Dict` | Tailored content response |
| `LearnerMemoryResponse` | `success, learner_id: str, profile: Dict, learning_goals: Dict, skill_gaps: Dict, mastery: Dict, learning_path: Dict, context: str, recent_history: str` | Learner memory response (multi-goal) |
| `HistorySearchResponse` | `success, query: str, matches: List[str], count: int` | History search response |
| `LLMModelsResponse` | `success, models: List[LLMModel]` | Available LLM models response |

---

## Layer 3: Algorithm Data Layer

**Location**: `gen_mentor/schemas/`

### File Structure

```
gen_mentor/schemas/
├── __init__.py        # Central exports for all schemas
├── learning.py        # Skills, gaps, goals, learner profiles
├── content.py         # Learning content, knowledge points, quizzes, feedback
├── assessment.py      # Performance evaluation, assessments
└── tutoring.py        # Chatbot interactions, tutoring
```

### Learning Schemas

**File**: `gen_mentor/schemas/learning.py`

#### Enums

```python
class LevelRequired(str, Enum):
    """Required proficiency levels."""
    beginner = "beginner"
    intermediate = "intermediate"
    advanced = "advanced"


class LevelCurrent(str, Enum):
    """Current proficiency levels including unlearned."""
    unlearned = "unlearned"
    beginner = "beginner"
    intermediate = "intermediate"
    advanced = "advanced"


class Confidence(str, Enum):
    """Confidence levels."""
    low = "low"
    medium = "medium"
    high = "high"
```

#### Skill Models

```python
class SkillRequirement(BaseModel):
    """A required skill with target level."""
    name: str
    required_level: LevelRequired


class SkillRequirements(BaseModel):
    """Collection of skill requirements (1-10 items)."""
    skill_requirements: List[SkillRequirement]


class SkillGap(BaseModel):
    """A skill gap with current and required levels."""
    name: str
    is_gap: bool
    required_level: LevelRequired
    current_level: LevelCurrent
    reason: str  # ≤20 words
    level_confidence: Confidence


class SkillGaps(BaseModel):
    """Collection of skill gaps (1-10 items)."""
    skill_gaps: List[SkillGap]


class SkillGapsRoot(RootModel):
    """Root model for skill gaps list."""
    root: List[SkillGap]
```

#### Learner Profile Models

```python
class MasteredSkill(BaseModel):
    """A mastered skill."""
    name: str
    proficiency_level: LevelRequired


class InProgressSkill(BaseModel):
    """A skill in progress."""
    name: str
    required_proficiency_level: LevelRequired
    current_proficiency_level: LevelCurrent


class CognitiveStatus(BaseModel):
    """Cognitive status of a learner."""
    overall_progress: int  # 0-100
    mastered_skills: List[MasteredSkill] = []
    in_progress_skills: List[InProgressSkill] = []


class LearningPreferences(BaseModel):
    """Learning preferences of a learner."""
    content_style: str
    activity_type: str
    additional_notes: str | None = None


class BehavioralPatterns(BaseModel):
    """Behavioral patterns of a learner."""
    system_usage_frequency: str
    session_duration_engagement: str
    motivational_triggers: str | None = None
    additional_notes: str | None = None


class LearnerProfile(BaseModel):
    """Complete learner profile.
    
    Note: learning_goal is NOT included in this schema.
    Learning goals are managed separately via goal_id in the memory system.
    """
    learner_information: str
    cognitive_status: CognitiveStatus
    learning_preferences: LearningPreferences
    behavioral_patterns: BehavioralPatterns


class RefinedLearningGoal(BaseModel):
    """A refined learning goal."""
    refined_goal: str
```

### Content Schemas

**File**: `gen_mentor/schemas/content.py`

#### Enums

```python
class Proficiency(str, Enum):
    """Proficiency levels for skills."""
    beginner = "beginner"
    intermediate = "intermediate"
    advanced = "advanced"


class KnowledgeType(str, Enum):
    """Types of knowledge points."""
    foundational = "foundational"
    practical = "practical"
    strategic = "strategic"
```

#### Learning Path Models

```python
class DesiredOutcome(BaseModel):
    """Desired skill outcome for a session."""
    name: str
    level: Proficiency


class SessionItem(BaseModel):
    """A single session in a learning path."""
    id: str  # e.g., "Session 1"
    title: str
    abstract: str
    if_learned: bool
    associated_skills: List[str] = []
    desired_outcome_when_completed: List[DesiredOutcome] = []


class LearningPath(BaseModel):
    """Complete learning path with multiple sessions (1-10)."""
    learning_path: List[SessionItem]
```

#### Knowledge Models

```python
class KnowledgePoint(BaseModel):
    """A single knowledge point."""
    name: str
    type: KnowledgeType


class KnowledgePoints(BaseModel):
    """Collection of knowledge points."""
    knowledge_points: List[KnowledgePoint]


class KnowledgeDraft(BaseModel):
    """Draft knowledge content."""
    title: str
    content: str


class DocumentStructure(BaseModel):
    """Structure of a learning document."""
    title: str
    overview: str
    summary: str
```

#### Quiz Models

```python
class SingleChoiceQuestion(BaseModel):
    """Single choice question."""
    question: str
    options: List[str]
    correct_option: int | str
    explanation: str | None = None


class MultipleChoiceQuestion(BaseModel):
    """Multiple choice question."""
    question: str
    options: List[str]
    correct_options: List[int | str]
    explanation: str | None = None


class TrueFalseQuestion(BaseModel):
    """True/False question."""
    question: str
    correct_answer: bool
    explanation: str | None = None


class ShortAnswerQuestion(BaseModel):
    """Short answer question."""
    question: str
    expected_answer: str
    explanation: str | None = None


class DocumentQuiz(BaseModel):
    """Complete quiz for a document."""
    single_choice_questions: List[SingleChoiceQuestion] = []
    multiple_choice_questions: List[MultipleChoiceQuestion] = []
    true_false_questions: List[TrueFalseQuestion] = []
    short_answer_questions: List[ShortAnswerQuestion] = []


class QuizPair(BaseModel):
    """Simple question-answer pair."""
    question: str
    answer: str
```

#### Content Models

```python
class ContentSection(BaseModel):
    """A section in learning content."""
    title: str
    summary: str


class ContentOutline(BaseModel):
    """Outline for learning content."""
    title: str
    sections: List[ContentSection] = []


class LearningContent(BaseModel):
    """Complete learning content with quizzes."""
    title: str
    overview: str
    content: str
    summary: str
    quizzes: List[QuizPair] = []
```

#### Feedback Models

```python
class FeedbackDetail(BaseModel):
    """Detailed feedback category."""
    progression: str
    engagement: str
    personalization: str


class LearnerFeedback(BaseModel):
    """Learner feedback and suggestions."""
    feedback: FeedbackDetail
    suggestions: FeedbackDetail
```

#### Search Result Model

```python
@dataclass
class SearchResult:
    """Search result from vector database or search engine."""
    title: str
    link: str
    snippet: Optional[str] = None
    content: Optional[str] = None
    document: Optional[Document] = None
```

### Assessment Schemas

**File**: `gen_mentor/schemas/assessment.py`

#### Enums

```python
class PerformanceLevel(str, Enum):
    """Overall performance level categories."""
    excellent = "excellent"
    good = "good"
    satisfactory = "satisfactory"
    needs_improvement = "needs_improvement"


class ProgressPace(str, Enum):
    """Learning progress pace."""
    ahead = "ahead"
    on_pace = "on_pace"
    behind = "behind"


class SkillLevel(str, Enum):
    """Skill proficiency levels."""
    unlearned = "unlearned"
    beginner = "beginner"
    intermediate = "intermediate"
    advanced = "advanced"


class ConfidenceLevel(str, Enum):
    """Confidence in assessment."""
    low = "low"
    medium = "medium"
    high = "high"


class Priority(str, Enum):
    """Recommendation priority."""
    high = "high"
    medium = "medium"
    low = "low"


class ImprovementStatus(str, Enum):
    """Improvement from previous attempts."""
    improved = "improved"
    same = "same"
    declined = "declined"
    no_previous_data = "no_previous_data"
```

#### Quiz Payload

```python
class DocumentQuizPayload(BaseModel):
    """Payload for generating document quizzes."""
    learner_profile: Any
    learning_document: Any
    single_choice_count: int = 0
    multiple_choice_count: int = 0
    true_false_count: int = 0
    short_answer_count: int = 0
    learning_goal: str = ""  # Added for context
```

#### Performance Models

```python
class ProgressStatus(BaseModel):
    """Progress tracking status."""
    current_session: int
    expected_session: int
    on_track: bool
    pace: ProgressPace


class SkillEvaluation(BaseModel):
    """Evaluation of a specific skill."""
    skill_name: str
    current_level: SkillLevel
    confidence: ConfidenceLevel
    ready_to_advance: bool
    notes: str = ""


class Recommendation(BaseModel):
    """Learning recommendation."""
    priority: Priority
    action: str
    rationale: str


class PerformanceEvaluation(BaseModel):
    """Overall performance evaluation."""
    overall_score: float  # 0-100
    performance_level: PerformanceLevel
    strengths: List[str] = []
    weaknesses: List[str] = []
    progress_status: ProgressStatus
    skill_evaluations: List[SkillEvaluation] = []
    recommendations: List[Recommendation] = []
    next_steps: str


class SkillMasteryEvaluation(BaseModel):
    """Detailed mastery evaluation for a specific skill."""
    skill_name: str
    current_level: SkillLevel
    confidence: ConfidenceLevel
    understanding_score: float  # 0-100
    proficiency_score: float  # 0-100
    ready_to_advance: bool
    mastered_aspects: List[str] = []
    gaps: List[str] = []
    improvement_from_previous: ImprovementStatus
    evidence: str
    practice_recommendations: List[str] = []
    estimated_time_to_mastery: str


class QuizResult(BaseModel):
    """Results from a quiz attempt."""
    quiz_id: str
    total_questions: int
    correct_answers: int
    score: float  # 0-100
    time_taken: Optional[int] = None  # seconds
    skill_breakdown: Optional[dict] = None


class SessionData(BaseModel):
    """Data from a learning session."""
    session_id: str
    duration: int  # seconds
    completed: bool
    quiz_results: Optional[List[QuizResult]] = None
    engagement_score: Optional[float] = None  # 0-100
    notes: Optional[str] = None
```

### Tutoring Schemas

**File**: `gen_mentor/schemas/tutoring.py`

```python
class ChatMessage(BaseModel):
    """A single chat message in the conversation."""
    role: Literal["user", "assistant", "system"]
    content: str


class TutorChatPayload(BaseModel):
    """Payload for tutor chatbot interactions."""
    learner_profile: Any = ""
    messages: Any  # List[ChatMessage] or JSON string
    use_search: bool = True
    top_k: int = 5
    external_resources: Optional[str] = None
    learning_goal: str = ""  # Added for context


class TutorResponse(BaseModel):
    """Response from the tutor chatbot."""
    response: str
    sources: Optional[List[str]] = None
    follow_up_questions: Optional[List[str]] = None
```

---

## Memory Service Architecture

The backend uses a **MemoryService** to manage learner context and history through the `LearnerMemoryStore` from the algorithm layer.

### Memory Service API

**File**: `apps/backend/services/memory_service.py`

```python
class MemoryService:
    """Service for managing learner memory and context."""

    def is_available(self) -> bool:
        """Check if memory storage is available (local mode only)."""
        
    def get_memory_store(self, learner_id: Optional[str]) -> Optional[LearnerMemoryStore]:
        """Get learner-specific memory store instance."""
        
    def get_learner_memory(self, learner_id: str) -> Dict[str, Any]:
        """Get all memory and context for a learner.
        
        Returns:
            {
                "learner_id": str,
                "profile": Dict,
                "learning_goals": Dict[str, Any],  # Keyed by goal_id
                "skill_gaps": Dict[str, Any],      # Keyed by goal_id
                "mastery": Dict[str, Any],
                "learning_path": Dict[str, Any],   # Keyed by goal_id
                "context": str,
                "recent_history": str
            }
        """
        
    def search_history(self, learner_id: str, query: str) -> list[dict]:
        """Search learner interaction history."""
        
    def log_interaction(self, learner_id: str, role: str, content: str, metadata?: dict):
        """Log a learning interaction to history."""
        
    def save_profile(self, learner_id: str, profile: Dict[str, Any]):
        """Save learner profile to memory."""
        
    def save_learning_goals(self, learner_id: str, learning_goals: Dict[str, Any]):
        """Save learning goals to memory."""
        
    def save_skill_gaps(self, learner_id: str, skill_gaps: Dict[str, Any]):
        """Save skill gaps to memory (keyed by goal_id)."""
        
    def save_learning_path(self, learner_id: str, learning_path: Dict[str, Any]):
        """Save learning path to memory."""
        
    def get_context_for_llm(self, learner_id: str) -> Dict[str, Any]:
        """Get all context needed for LLM prompts."""
```

### Storage Modes

| Mode | Description | Memory Available | Use Case |
|------|-------------|------------------|----------|
| `local` | Local file-based storage | ✅ Yes | Development, single-user |
| `cloud` | Cloud storage (S3, GCS) | ❌ No | Production, multi-user |

```python
# config.py
class BackendSettings:
    storage_mode: str = "local"  # or "cloud"
    workspace_dir: str = "~/.gen-mentor/workspace"
```

### Memory Store Integration

The backend memory service integrates with the algorithm layer's `LearnerMemoryStore`:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         Backend Memory Service                               │
│  Location: apps/backend/services/memory_service.py                          │
└─────────────────────────────────────────┬───────────────────────────────────┘
                                          │ uses
                                          ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                      Algorithm Memory Store                                  │
│  Location: gen_mentor/core/memory/memory_store.py                           │
│                                                                              │
│  Methods:                                                                    │
│  - read_profile() / write_profile()                                         │
│  - read_learning_goals() / write_learning_goals()                           │
│  - read_skill_gaps() / write_skill_gaps()                                   │
│  - read_mastery() / append_mastery_entry()                                  │
│  - read_learning_path() / write_learning_path()                             │
│  - get_learner_context()                                                     │
│  - get_recent_history(n)                                                     │
│  - search_history(query)                                                     │
│  - log_interaction(role, content, metadata)                                 │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Multi-Goal Architecture

GenMentor supports multiple learning goals per learner. The `goal_id` parameter is used to key data in the memory system.

### Memory Structure

```python
class LearnerMemoryResponse(BaseResponse):
    """Response containing learner memory and context."""
    learner_id: str
    profile: Dict[str, Any]                    # Learner's base profile
    learning_goals: Dict[str, Any]             # {goal_id: refined_goal}
    skill_gaps: Dict[str, Any]                 # {goal_id: skill_gaps}
    mastery: Dict[str, Any]                    # Skill mastery levels
    learning_path: Dict[str, Any]              # {goal_id: learning_path}
    context: str                               # Formatted context for prompts
    recent_history: str                        # Recent interaction history
```

### Goal ID Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ 1. setLearningGoal                                                          │
│    → Backend generates goal_id (UUID)                                       │
│    → Stores refined_goal in memory[goal_id]                                 │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ 2. identifyAndSaveSkillGap                                                  │
│    → Backend uses active goal_id or generates new one                       │
│    → Stores skill_gaps in memory[goal_id]                                   │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ 3. scheduleLearningPath (with goal_id)                                      │
│    → Backend retrieves learning_goal from memory[goal_id]                   │
│    → Stores learning_path in memory[goal_id]                                │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ 4. Subsequent operations (with goal_id)                                     │
│    → chatWithTutor, generateTailoredContent, etc.                           │
│    → Backend resolves learning_goal, skill_gaps, learning_path from goal_id │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Goal ID Resolution

When `goal_id` is provided:
1. Backend retrieves `learning_goal` from `memory.learning_goals[goal_id]`
2. Backend retrieves `skill_gaps` from `memory.skill_gaps[goal_id]`
3. Backend retrieves `learning_path` from `memory.learning_path[goal_id]`

When `goal_id` is NOT provided:
1. Backend uses active/default goal
2. Falls back to the first goal in memory

---

## Data Flow Mapping

### Request Flow: Frontend → Backend → Algorithm

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ Example: scheduleLearningPath (with goal_id)                                │
└─────────────────────────────────────────────────────────────────────────────┘

Frontend (TypeScript):
{
  learner_profile: string | Record<string, any>;
  session_count: number;
  goal_id?: string;  // Optional goal ID
  model?: string;    // "openai/gpt-5.1"
}
        │
        ▼ JSON over HTTP
Backend (Pydantic - LearningPathSchedulingRequest):
{
  learner_profile: str;
  session_count: int;
  goal_id: Optional[str];
  model: Optional[str] = "openai/gpt-5.1";
}
        │
        ▼ Backend resolves learning_goal from goal_id
        ▼ Python dict → gen_mentor agents
Algorithm (Pydantic - LearningPath):
{
  learning_path: [
    {
      id: "Session 1",
      title: "...",
      abstract: "...",
      if_learned: false,
      associated_skills: [...],
      desired_outcome_when_completed: [...]
    },
    ...
  ]
}
```

### Response Flow: Algorithm → Backend → Frontend

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ Example: LearnerMemoryResponse (multi-goal)                                 │
└─────────────────────────────────────────────────────────────────────────────┘

Backend (LearnerMemoryResponse):
{
  success: true,
  learner_id: "learner_abc123",
  profile: { name: "John", email: "john@example.com", ... },
  learning_goals: {
    "goal_001": { refined_goal: "Learn Python for data science", ... },
    "goal_002": { refined_goal: "Master web development", ... }
  },
  skill_gaps: {
    "goal_001": { skill_gaps: [...] },
    "goal_002": { skill_gaps: [...] }
  },
  mastery: { "Python": 75, "JavaScript": 40, ... },
  learning_path: {
    "goal_001": { learning_path: [...] },
    "goal_002": { learning_path: [...] }
  },
  context: "...",
  recent_history: "..."
}
        │
        ▼ JSON over HTTP
Frontend:
{
  success: boolean;
  learner_id: string;
  profile: Record<string, any>;
  learning_goals: Record<string, any>;  // Keyed by goal_id
  skill_gaps: Record<string, any>;      // Keyed by goal_id
  mastery: Record<string, any>;
  learning_path: Record<string, any>;   // Keyed by goal_id
  context: string;
  recent_history: string;
}
```

### Key Data Transformations

| Data Type | Frontend Type | Backend Type | Algorithm Type |
|-----------|---------------|--------------|----------------|
| Model | `model?: string` | `model: Optional[str]` | N/A (passed to LLM) |
| Goal ID | `goal_id?: string` | `goal_id: Optional[str]` | N/A (memory key) |
| Learner ID | `learner_id: string` | `learner_id: str` | N/A (storage key) |
| Learning Goal | `learning_goal: string` | `learning_goal: str` | `RefinedLearningGoal` |
| Skill Gaps | `skill_gaps: any` | `skill_gaps: Dict` | `SkillGaps` |
| Learning Path | `learning_path.sessions[]` | `learning_path: Dict` | `LearningPath` |
| Messages | `messages: Array<{role, content}>` | `messages: str (JSON)` | `List[ChatMessage]` |
| Profile | `LearnerProfile` | `Dict[str, Any]` | `LearnerProfile` (no learning_goal) |

---

## Protocol Consistency Guidelines

### 1. Model Parameter Format

**Standard**: `"provider/model"` format

```
✅ Correct: "openai/gpt-5.1"
✅ Correct: "anthropic/claude-3-5-sonnet"
✅ Correct: "deepseek/deepseek-chat"
❌ Incorrect: { model_provider: "openai", model_name: "gpt-5.1" }
```

### 2. Goal ID Usage

The `goal_id` parameter is used to:
- Key learning goals, skill gaps, and learning paths in memory
- Resolve context for AI operations
- Support multiple concurrent learning goals per learner

```
✅ With goal_id: Backend resolves learning_goal from memory
✅ Without goal_id: Backend uses active/default goal
```

### 3. JSON String vs Object

The backend accepts both JSON strings and objects for complex fields:

```python
# Backend request handling
learner_profile: str | Record<string, any>  # Frontend
learner_profile: str  # Backend (coerced to str)
learner_profile: LearnerProfile  # Algorithm
```

**Guideline**: Frontend sends objects, Backend serializes to JSON strings, Algorithm parses to Pydantic models.

### 4. Enum Consistency

| Category | Frontend | Backend | Algorithm |
|----------|----------|---------|-----------|
| Skill Level | `string` | `str` | `LevelRequired`, `LevelCurrent`, `SkillLevel` |
| Proficiency | `string` | `str` | `Proficiency` |
| Confidence | `string` | `str` | `Confidence`, `ConfidenceLevel` |

**Values**: `"beginner"`, `"intermediate"`, `"advanced"`, `"unlearned"`

### 5. ID Naming Convention

| Type | Format | Example |
|------|--------|---------|
| Learner ID | `learner_{uuid}` | `learner_abc123def456` |
| Goal ID | `goal_{uuid}` or UUID | `goal_xyz789`, `123e4567-e89b...` |
| Session ID | `Session {n}` or `session_{id}` | `Session 1`, `session_abc` |

### 6. Timestamp Format

**Standard**: ISO 8601 format

```
✅ "2024-01-15T10:30:00Z"
✅ "2024-01-15T10:30:00+00:00"
```

### 7. Error Handling

All layers should return consistent error responses:

```typescript
// Frontend expects
{
  success: false;
  error_code: string;
  message: string;
  details?: Record<string, any>;
}
```

### 8. Validation Rules

| Field | Rule | Enforced At |
|-------|------|-------------|
| `learning_goal` | Non-empty string | Frontend, Backend, Algorithm |
| `session_count` | 1-100 | Backend |
| `skill_requirements` | 1-10 items | Algorithm |
| `skill_gaps` | 1-10 items | Algorithm |
| `quiz_score` | 0-100 | Backend |
| `reason` (SkillGap) | ≤20 words | Algorithm |
| `overall_progress` | 0-100 | Algorithm |

### 9. Optional vs Required Fields

| Field | Frontend | Backend | Algorithm |
|-------|----------|---------|-----------|
| `model` | Optional | Optional (has default) | N/A |
| `goal_id` | Optional | Optional | N/A |
| `learner_id` | Required for most | Optional (can be in URL) | N/A |
| `email` | Optional | Optional | N/A |
| `metadata` | Optional | Optional | N/A |
| `quiz_score` | Optional | Optional | N/A |

---

## Quick Reference

### Schema Files by Layer

| Layer | Location | Key Files |
|-------|----------|-----------|
| Frontend | `apps/frontend/src/lib/api.ts` | `api.ts` |
| Backend | `apps/backend/models/` | `common.py`, `requests.py`, `responses.py`, `defaults.py` |
| Backend (Legacy) | `apps/backend/schemas.py` | `schemas.py` (deprecated) |
| Backend Services | `apps/backend/services/` | `memory_service.py`, `llm_service.py`, `user_registry.py` |
| Backend Repositories | `apps/backend/repositories/` | `learner_repository.py` |
| Algorithm | `gen_mentor/schemas/` | `learning.py`, `content.py`, `assessment.py`, `tutoring.py` |
| Algorithm Memory | `gen_mentor/core/memory/` | `memory_store.py` |

### Storage Configuration

| Setting | Location | Description |
|---------|----------|-------------|
| `storage_mode` | `apps/backend/config.py` | "local" or "cloud" |
| `workspace_dir` | `apps/backend/config.py` | Workspace directory for local storage |
| `DEFAULT_MODEL_PROVIDER` | `apps/backend/models/defaults.py` | Default LLM provider |
| `DEFAULT_MODEL_NAME` | `apps/backend/models/defaults.py` | Default model name |

### Common Enums

| Enum | Values | Location |
|------|--------|----------|
| `LevelRequired` | beginner, intermediate, advanced | `gen_mentor/schemas/learning.py` |
| `LevelCurrent` | unlearned, beginner, intermediate, advanced | `gen_mentor/schemas/learning.py` |
| `Proficiency` | beginner, intermediate, advanced | `gen_mentor/schemas/content.py` |
| `KnowledgeType` | foundational, practical, strategic | `gen_mentor/schemas/content.py` |
| `PerformanceLevel` | excellent, good, satisfactory, needs_improvement | `gen_mentor/schemas/assessment.py` |
| `ProgressPace` | ahead, on_pace, behind | `gen_mentor/schemas/assessment.py` |

### Parser Functions

The algorithm layer provides parser functions for safe validation:

```python
# Learning
parse_learner_behavior_log(data) -> LearnerBehaviorLog
parse_ground_truth_profile_result(data) -> GroundTruthProfileResult

# Content
parse_knowledge_points(data) -> KnowledgePoints
parse_knowledge_draft(data) -> KnowledgeDraft
parse_document_structure(data) -> DocumentStructure
parse_document_quiz(data) -> DocumentQuiz

# Tutoring
parse_tutor_response(data) -> TutorResponse

# Assessment
parse_performance_evaluation(data) -> PerformanceEvaluation
parse_skill_mastery_evaluation(data) -> SkillMasteryEvaluation
```

### Multi-Goal Endpoints

| Endpoint | goal_id Support | Notes |
|----------|-----------------|-------|
| `/learning/schedule-learning-path` | ✅ | Resolves learning_goal from goal_id |
| `/learning/reschedule-learning-path` | ✅ | Resolves learning_path from goal_id |
| `/learning/explore-knowledge-points` | ✅ | Resolves learning_path from goal_id |
| `/learning/tailor-knowledge-content` | ✅ | Resolves all context from goal_id |
| `/chat/chat-with-tutor` | ✅ | Resolves learning_goal for context |
| `/assessment/generate-document-quizzes` | ✅ | Resolves learning_goal for context |

---

## Legacy vs New Models

The backend has two model systems:

### Legacy Schemas (`apps/backend/schemas.py`)

**Status**: ⚠️ **Deprecated** - kept for backward compatibility

```python
# Legacy format (deprecated)
class BaseRequest(BaseModel):
    model_provider: str = DEFAULT_MODEL_PROVIDER
    model_name: str = DEFAULT_MODEL_NAME
    method_name: str = "genmentor"
    storage_mode: str = "local"
```

### New Models (`apps/backend/models/`)

**Status**: ✅ **Current** - use for all new endpoints

```python
# New format (current)
class BaseRequest(BaseModel):
    model: Optional[str] = Field(
        default=f"{DEFAULT_MODEL_PROVIDER}/{DEFAULT_MODEL_NAME}",
        description="Model in 'provider/model' format"
    )

    def get_model_parts(self) -> tuple[str, str]:
        """Parse model string into provider and model name."""
```

### Migration Guide

| Legacy Parameter | New Parameter | Format |
|------------------|---------------|--------|
| `model_provider: "openai"` | `model: "openai/gpt-4"` | Combined |
| `model_name: "gpt-4"` | (included in model) | Combined |
| `method_name: "genmentor"` | (removed) | N/A |
| `storage_mode: "local"` | (config-based) | N/A |

### Migration Example

```python
# Legacy request (deprecated)
{
    "model_provider": "openai",
    "model_name": "gpt-4",
    "method_name": "genmentor",
    "storage_mode": "local",
    "learning_goal": "Learn Python"
}

# New request (current)
{
    "model": "openai/gpt-4",
    "learning_goal": "Learn Python"
}
```

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-02-23 | Initial schema documentation |
| 1.1.0 | 2026-02-23 | Added unified model parameter format ("provider/model") |
| 1.2.0 | 2026-02-23 | Added multi-goal architecture with goal_id support |
| 1.2.1 | 2026-02-23 | Updated LearnerMemoryResponse with dict-based learning_goals/skill_gaps/learning_path |
| 1.2.2 | 2026-02-23 | Removed learning_goal from LearnerProfile schema |
| 1.3.0 | 2026-02-23 | Added new schemas: FeedbackDetail, LearnerFeedback, SearchResult, SkillGapsRoot |
| 1.3.1 | 2026-02-23 | Added learning_goal field to TutorChatPayload and DocumentQuizPayload |
| 1.4.0 | 2026-02-23 | Added new endpoints: identifyAndSaveSkillGap, rescheduleLearningPath, user management |
| 1.5.0 | 2026-02-24 | **Major update**: Added Memory Service Architecture section |
| | | - Documented MemoryService API and storage modes |
| | | - Added Memory Store integration diagram |
| | | - Updated backend file structure with correct paths |
| | | - Added LearnerProfileInitializationRequest (CV-based) |
| | | - Added Legacy vs New Models section for migration guide |
| | | - Updated request models table with accurate field types |

---

*This document serves as the authoritative reference for data protocol consistency across the GenMentor system. When making changes to any layer, ensure backward compatibility or update all three layers accordingly.*
