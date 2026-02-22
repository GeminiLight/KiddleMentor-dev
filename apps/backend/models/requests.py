"""
Request models for API endpoints.

All request schemas with proper validation and documentation.
"""

from typing import Optional, Any
from pydantic import BaseModel, Field, field_validator

from .common import BaseRequest


# =============================================================================
# Session Management Requests
# =============================================================================

class InitializeSessionRequest(BaseModel):
    """Request for initializing a new learner session."""

    name: Optional[str] = Field(
        None,
        description="Learner name (optional)",
        examples=["John Doe"]
    )
    email: Optional[str] = Field(
        None,
        description="Learner email (optional)",
        examples=["john@example.com"]
    )
    metadata: Optional[dict] = Field(
        None,
        description="Additional metadata (optional)"
    )


class SetLearningGoalRequest(BaseRequest):
    """Request for setting a learning goal."""

    learning_goal: str = Field(
        ...,
        description="Learning goal to set",
        examples=["Learn web development"]
    )
    learner_id: Optional[str] = Field(
        None,
        description="Learner identifier (optional, can be in URL path or body)",
        examples=["learner_123abc"]
    )


class SessionCompleteRequest(BaseModel):
    """Request for marking a session as complete."""

    session_number: int = Field(
        ...,
        description="Session number to mark complete",
        ge=1
    )
    duration_minutes: Optional[int] = Field(
        None,
        description="Session duration in minutes",
        ge=0
    )
    quiz_score: Optional[int] = Field(
        None,
        description="Quiz score (0-100)",
        ge=0,
        le=100
    )
    learner_id: Optional[str] = Field(
        None,
        description="Learner identifier (optional, can be in URL path or body)",
        examples=["learner_123abc"]
    )


class GetDashboardRequest(BaseModel):
    """Request for getting dashboard data."""

    learner_id: str = Field(
        ...,
        description="Learner identifier",
        examples=["learner_123abc"]
    )


class GetProfileRequest(BaseModel):
    """Request for getting learner profile."""

    learner_id: str = Field(
        ...,
        description="Learner identifier",
        examples=["learner_123abc"]
    )


class GetLearnerMemoryRequest(BaseModel):
    """Request for getting learner memory."""

    learner_id: str = Field(
        ...,
        description="Learner identifier",
        examples=["learner_123abc"]
    )


class SearchHistoryRequest(BaseModel):
    """Request for searching learner history."""

    learner_id: str = Field(
        ...,
        description="Learner identifier",
        examples=["learner_123abc"]
    )
    query: str = Field(
        ...,
        description="Search query string",
        examples=["learning goal"]
    )


# =============================================================================
# Chat Endpoints
# =============================================================================
class ChatWithTutorRequest(BaseRequest):
    """Request for chatting with AI tutor."""

    messages: str = Field(
        ...,
        description="JSON string array of chat messages",
        examples=['[{"role": "user", "content": "Explain neural networks"}]']
    )
    learner_profile: str = Field(
        default="",
        description="JSON string of learner profile"
    )

    @field_validator("messages")
    @classmethod
    def validate_messages(cls, v: str) -> str:
        """Validate messages format."""
        if not v.strip():
            raise ValueError("messages cannot be empty")
        if not v.strip().startswith("["):
            raise ValueError("messages must be a JSON array string")
        return v


# Goal refinement
class LearningGoalRefinementRequest(BaseRequest):
    """Request for refining learning goals."""

    learning_goal: str = Field(
        ...,
        description="Initial learning goal to refine",
        examples=["Learn machine learning"]
    )
    learner_information: str = Field(
        default="",
        description="Additional learner information"
    )

    @field_validator("learning_goal")
    @classmethod
    def validate_goal(cls, v: str) -> str:
        """Validate learning goal."""
        if not v.strip():
            raise ValueError("learning_goal cannot be empty")
        return v.strip()


# Skill gap identification
class SkillGapIdentificationRequest(BaseRequest):
    """Request for identifying skill gaps."""

    learning_goal: str = Field(..., description="Learning goal")
    learner_information: str = Field(..., description="Learner's background and experience")
    skill_requirements: Optional[str] = Field(
        default=None,
        description="Optional pre-defined skill requirements as JSON string"
    )


# Learner profile management
class LearnerProfileInitializationWithInfoRequest(BaseRequest):
    """Request for initializing learner profile with information."""

    learning_goal: str = Field(..., description="Learning goal")
    learner_information: str = Field(..., description="Learner information")
    skill_gaps: str = Field(..., description="Identified skill gaps as JSON string")


class LearnerProfileInitializationRequest(BaseRequest):
    """Request for initializing learner profile from CV file."""

    learning_goal: str = Field(..., description="Learning goal")
    skill_requirements: str = Field(..., description="Skill requirements as JSON string")
    skill_gaps: str = Field(..., description="Identified skill gaps as JSON string")
    cv_path: str = Field(..., description="Path to uploaded CV file")


class LearnerProfileUpdateRequest(BaseRequest):
    """Request for updating learner profile."""

    learner_profile: str = Field(..., description="Current learner profile as JSON string")
    learner_interactions: str = Field(..., description="Recent learner interactions as JSON string")
    learner_information: str = Field(default="", description="Additional learner information")
    session_information: str = Field(default="", description="Current session information")


# Learning path management
class LearningPathSchedulingRequest(BaseRequest):
    """Request for scheduling learning path."""

    learner_profile: str = Field(..., description="Learner profile as JSON string")
    session_count: int = Field(
        ...,
        description="Number of learning sessions to schedule",
        gt=0,
        le=100
    )


class LearningPathReschedulingRequest(BaseRequest):
    """Request for rescheduling learning path."""

    learner_profile: str = Field(..., description="Learner profile as JSON string")
    learning_path: str = Field(..., description="Current learning path as JSON string")
    session_count: int = Field(
        default=-1,
        description="New session count (-1 to keep existing)"
    )
    other_feedback: str = Field(
        default="",
        description="Additional feedback for rescheduling"
    )


# Knowledge exploration and drafting
class KnowledgePointExplorationRequest(BaseModel):
    """Request for exploring knowledge points."""

    learner_profile: str = Field(..., description="Learner profile as JSON string")
    learning_path: str = Field(..., description="Learning path as JSON string")
    learning_session: str = Field(..., description="Current learning session as JSON string")


class KnowledgePointDraftingRequest(BaseModel):
    """Request for drafting a single knowledge point."""

    learner_profile: str = Field(..., description="Learner profile as JSON string")
    learning_path: str = Field(..., description="Learning path as JSON string")
    learning_session: str = Field(..., description="Learning session as JSON string")
    knowledge_points: str = Field(..., description="All knowledge points as JSON string")
    knowledge_point: str = Field(..., description="Specific knowledge point to draft")
    use_search: bool = Field(default=True, description="Whether to use web search")


class KnowledgePointsDraftingRequest(BaseModel):
    """Request for drafting multiple knowledge points."""

    learner_profile: str = Field(..., description="Learner profile as JSON string")
    learning_path: str = Field(..., description="Learning path as JSON string")
    learning_session: str = Field(..., description="Learning session as JSON string")
    knowledge_points: str = Field(..., description="Knowledge points to draft as JSON string")
    use_search: bool = Field(default=True, description="Whether to use web search")
    allow_parallel: bool = Field(default=True, description="Allow parallel processing")


# Document integration
class LearningDocumentIntegrationRequest(BaseModel):
    """Request for integrating learning document."""

    learner_profile: str = Field(..., description="Learner profile as JSON string")
    learning_path: str = Field(..., description="Learning path as JSON string")
    learning_session: str = Field(..., description="Learning session as JSON string")
    knowledge_points: str = Field(..., description="Knowledge points as JSON string")
    knowledge_drafts: str = Field(..., description="Knowledge drafts as JSON string")
    output_markdown: bool = Field(default=False, description="Output as markdown format")


# Assessment
class KnowledgeQuizGenerationRequest(BaseModel):
    """Request for generating quizzes."""

    learner_profile: str = Field(..., description="Learner profile as JSON string")
    learning_document: str = Field(..., description="Learning document content")
    single_choice_count: int = Field(default=3, ge=0, le=20, description="Number of single-choice questions")
    multiple_choice_count: int = Field(default=0, ge=0, le=20, description="Number of multiple-choice questions")
    true_false_count: int = Field(default=0, ge=0, le=20, description="Number of true/false questions")
    short_answer_count: int = Field(default=0, ge=0, le=10, description="Number of short answer questions")


# Content generation
class TailoredContentGenerationRequest(BaseModel):
    """Request for generating tailored learning content."""

    learner_profile: str = Field(..., description="Learner profile as JSON string")
    learning_path: str = Field(..., description="Learning path as JSON string")
    learning_session: str = Field(..., description="Learning session as JSON string")
    use_search: bool = Field(default=True, description="Whether to use web search")
    allow_parallel: bool = Field(default=True, description="Allow parallel processing")
    with_quiz: bool = Field(default=True, description="Include quiz generation")


# Memory and history
class HistorySearchRequest(BaseModel):
    """Request for searching learner history."""

    query: str = Field(..., description="Search query", min_length=1)
