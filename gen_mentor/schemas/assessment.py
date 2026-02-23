"""Assessment-related schemas for quizzes and performance evaluation."""

from __future__ import annotations

from enum import Enum
from typing import Any, List, Literal, Mapping, Optional

from pydantic import BaseModel, Field, field_validator


# Quiz-related schemas (moved from content.py for better organization)
class DocumentQuizPayload(BaseModel):
    """Payload for generating document quizzes."""
    learner_profile: Any = Field(..., description="Learner profile information")
    learning_document: Any = Field(..., description="Learning document to generate quiz from")
    single_choice_count: int = Field(default=0, description="Number of single choice questions")
    multiple_choice_count: int = Field(default=0, description="Number of multiple choice questions")
    true_false_count: int = Field(default=0, description="Number of true/false questions")
    short_answer_count: int = Field(default=0, description="Number of short answer questions")
    learning_goal: str = Field(default="", description="Learning goal for context")

    @field_validator("learner_profile", "learning_document")
    @classmethod
    def coerce_jsonish(cls, v: Any) -> Any:
        """Coerce inputs to appropriate format."""
        if isinstance(v, BaseModel):
            return v.model_dump()
        if isinstance(v, Mapping):
            return dict(v)
        if isinstance(v, str):
            return v.strip()
        return v


# Performance evaluation schemas
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


class ProgressStatus(BaseModel):
    """Progress tracking status."""
    current_session: int = Field(..., description="Current session number")
    expected_session: int = Field(..., description="Expected session number")
    on_track: bool = Field(..., description="Whether learner is on track")
    pace: ProgressPace = Field(..., description="Learning pace")


class SkillEvaluation(BaseModel):
    """Evaluation of a specific skill."""
    skill_name: str = Field(..., description="Name of the skill")
    current_level: SkillLevel = Field(..., description="Current proficiency level")
    confidence: ConfidenceLevel = Field(..., description="Confidence in assessment")
    ready_to_advance: bool = Field(..., description="Whether ready to advance to next level")
    notes: str = Field(default="", description="Assessment notes")


class Recommendation(BaseModel):
    """Learning recommendation."""
    priority: Priority = Field(..., description="Priority level")
    action: str = Field(..., description="Recommended action")
    rationale: str = Field(..., description="Why this is recommended")


class PerformanceEvaluation(BaseModel):
    """Overall performance evaluation."""
    overall_score: float = Field(..., ge=0, le=100, description="Overall performance score (0-100)")
    performance_level: PerformanceLevel = Field(..., description="Overall performance level")
    strengths: List[str] = Field(default_factory=list, description="Learner strengths")
    weaknesses: List[str] = Field(default_factory=list, description="Areas needing improvement")
    progress_status: ProgressStatus = Field(..., description="Progress tracking")
    skill_evaluations: List[SkillEvaluation] = Field(default_factory=list, description="Skill-specific evaluations")
    recommendations: List[Recommendation] = Field(default_factory=list, description="Actionable recommendations")
    next_steps: str = Field(..., description="Summary of next steps")


class SkillMasteryEvaluation(BaseModel):
    """Detailed mastery evaluation for a specific skill."""
    skill_name: str = Field(..., description="Name of the skill")
    current_level: SkillLevel = Field(..., description="Current proficiency level")
    confidence: ConfidenceLevel = Field(..., description="Confidence in assessment")
    understanding_score: float = Field(..., ge=0, le=100, description="Understanding score (0-100)")
    proficiency_score: float = Field(..., ge=0, le=100, description="Proficiency score (0-100)")
    ready_to_advance: bool = Field(..., description="Whether ready to advance")
    mastered_aspects: List[str] = Field(default_factory=list, description="Aspects already mastered")
    gaps: List[str] = Field(default_factory=list, description="Remaining gaps")
    improvement_from_previous: ImprovementStatus = Field(..., description="Improvement status")
    evidence: str = Field(..., description="Evidence supporting assessment")
    practice_recommendations: List[str] = Field(default_factory=list, description="Practice recommendations")
    estimated_time_to_mastery: str = Field(..., description="Time estimate to mastery")


class QuizResult(BaseModel):
    """Results from a quiz attempt."""
    quiz_id: str = Field(..., description="Quiz identifier")
    total_questions: int = Field(..., description="Total number of questions")
    correct_answers: int = Field(..., description="Number of correct answers")
    score: float = Field(..., ge=0, le=100, description="Quiz score (0-100)")
    time_taken: Optional[int] = Field(default=None, description="Time taken in seconds")
    skill_breakdown: Optional[dict] = Field(default=None, description="Performance breakdown by skill")


class SessionData(BaseModel):
    """Data from a learning session."""
    session_id: str = Field(..., description="Session identifier")
    duration: int = Field(..., description="Session duration in seconds")
    completed: bool = Field(..., description="Whether session was completed")
    quiz_results: Optional[List[QuizResult]] = Field(default=None, description="Quiz results from session")
    engagement_score: Optional[float] = Field(default=None, ge=0, le=100, description="Engagement score")
    notes: Optional[str] = Field(default=None, description="Session notes")


def parse_performance_evaluation(data: Any) -> PerformanceEvaluation:
    """Parse performance evaluation from various formats."""
    if isinstance(data, dict):
        return PerformanceEvaluation.model_validate(data)
    if isinstance(data, BaseModel):
        return PerformanceEvaluation.model_validate(data.model_dump())
    raise ValueError(f"Cannot parse performance evaluation from {type(data)}")


def parse_skill_mastery_evaluation(data: Any) -> SkillMasteryEvaluation:
    """Parse skill mastery evaluation from various formats."""
    if isinstance(data, dict):
        return SkillMasteryEvaluation.model_validate(data)
    if isinstance(data, BaseModel):
        return SkillMasteryEvaluation.model_validate(data.model_dump())
    raise ValueError(f"Cannot parse skill mastery evaluation from {type(data)}")


__all__ = [
    # Enums
    "PerformanceLevel",
    "ProgressPace",
    "SkillLevel",
    "ConfidenceLevel",
    "Priority",
    "ImprovementStatus",
    # Quiz schemas
    "DocumentQuizPayload",
    # Performance schemas
    "ProgressStatus",
    "SkillEvaluation",
    "Recommendation",
    "PerformanceEvaluation",
    "SkillMasteryEvaluation",
    "QuizResult",
    "SessionData",
    # Parsers
    "parse_performance_evaluation",
    "parse_skill_mastery_evaluation",
]
