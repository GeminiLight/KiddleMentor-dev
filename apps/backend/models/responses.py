"""
Response models for API endpoints.

All response schemas with proper structure and documentation.
"""

from typing import Any, Optional, Dict, List
from pydantic import BaseModel, Field

from .common import BaseResponse


# =============================================================================
# Session Management Responses
# =============================================================================

class InitializeSessionResponse(BaseResponse):
    """Response from session initialization."""

    learner_id: str = Field(..., description="Generated learner ID")
    profile: Dict[str, Any] = Field(..., description="Initial learner profile")


class DashboardResponse(BaseResponse):
    """Response containing complete dashboard state."""

    learner: Dict[str, Any] = Field(..., description="Learner information and progress")
    current_session: Optional[Dict[str, Any]] = Field(None, description="Current learning session")
    learning_path: Optional[Dict[str, Any]] = Field(None, description="Complete learning path")
    recent_activity: List[Dict[str, Any]] = Field(default_factory=list, description="Recent learning activities")
    mastery: Dict[str, Any] = Field(default_factory=dict, description="Skill mastery levels")


class SessionCompleteResponse(BaseResponse):
    """Response from marking session complete."""

    session_number: int = Field(..., description="Completed session number")
    next_session: Optional[Dict[str, Any]] = Field(None, description="Next session information")
    progress_percent: float = Field(..., description="Overall progress percentage")


# =============================================================================
# Chat Responses
# =============================================================================
class ChatResponse(BaseResponse):
    """Response from chat with tutor."""

    response: str = Field(..., description="Tutor's response")


# Goal refinement responses
class RefinedGoalResponse(BaseResponse):
    """Response from goal refinement."""

    refined_goal: Any = Field(..., description="Refined learning goal (can be string or dict)")
    rationale: Optional[str] = Field(None, description="Rationale for refinement")


# Skill gap responses
class SkillGapResponse(BaseResponse):
    """Response from skill gap identification."""

    skill_requirements: Dict[str, Any] = Field(..., description="Required skills mapped to the goal")
    skill_gaps: Dict[str, Any] = Field(..., description="Identified skill gaps")
    learning_goal: str = Field(..., description="Original learning goal")


# Profile responses
class LearnerProfileResponse(BaseResponse):
    """Response containing learner profile."""

    learner_profile: Dict[str, Any] = Field(..., description="Learner profile data")


# Learning path responses
class LearningPathResponse(BaseResponse):
    """Response containing learning path."""

    learning_path: Dict[str, Any] = Field(..., description="Learning path with sessions")
    session_count: int = Field(..., description="Number of sessions")


# Knowledge point responses
class KnowledgePointsResponse(BaseResponse):
    """Response containing explored knowledge points."""

    knowledge_points: List[Dict[str, Any]] = Field(..., description="Explored knowledge points")


class KnowledgeDraftResponse(BaseResponse):
    """Response containing knowledge point draft."""

    knowledge_draft: str = Field(..., description="Drafted knowledge point content")


class KnowledgeDraftsResponse(BaseResponse):
    """Response containing multiple knowledge drafts."""

    knowledge_drafts: List[str] = Field(..., description="List of knowledge drafts")


# Document responses
class LearningDocumentResponse(BaseResponse):
    """Response containing integrated learning document."""

    learning_document: str = Field(..., description="Integrated learning document content")


# Quiz responses
class QuizResponse(BaseResponse):
    """Response containing generated quizzes."""

    document_quiz: Dict[str, Any] = Field(..., description="Generated quizzes")


# Content generation responses
class TailoredContentResponse(BaseResponse):
    """Response containing tailored learning content."""

    tailored_content: Dict[str, Any] = Field(..., description="Tailored learning content")


# Memory responses
class LearnerMemoryResponse(BaseResponse):
    """Response containing learner memory and context."""

    learner_id: str = Field(..., description="Learner identifier")
    profile: Dict[str, Any] = Field(..., description="Learner profile")
    learning_goals: Dict[str, Any] = Field(default_factory=dict, description="Learning goals")
    skill_gaps: Dict[str, Any] = Field(default_factory=dict, description="Skill gaps keyed by goal_id")
    mastery: Dict[str, Any] = Field(default_factory=dict, description="Learning mastery and progress")
    learning_path: Dict[str, Any] = Field(default_factory=dict, description="Learning paths keyed by goal_id")
    context: str = Field(..., description="Formatted context for prompts")
    recent_history: str = Field(..., description="Recent interaction history")


class HistorySearchResponse(BaseResponse):
    """Response from history search."""

    query: str = Field(..., description="Search query")
    matches: List[str] = Field(..., description="Matching history entries")
    count: int = Field(..., description="Number of matches")


# LLM models response
class LLMModel(BaseModel):
    """LLM model information."""

    model_name: str = Field(..., description="Model name")
    model_provider: str = Field(..., description="Provider name")


class LLMModelsResponse(BaseResponse):
    """Response containing available LLM models."""

    models: List[LLMModel] = Field(..., description="List of available models")
