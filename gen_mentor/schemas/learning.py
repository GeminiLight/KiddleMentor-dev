"""Learning-related schemas for skills, gaps, goals, and learner profiles."""

from __future__ import annotations

from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, RootModel, field_validator


# Enums
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


# Skill Requirement Schemas
class SkillRequirement(BaseModel):
    """A required skill with target level."""
    name: str = Field(..., description="Actionable, concise skill name.")
    required_level: LevelRequired


class SkillRequirements(BaseModel):
    """Collection of skill requirements."""
    skill_requirements: List[SkillRequirement]

    @field_validator("skill_requirements")
    @classmethod
    def validate_length_and_uniqueness(cls, v: List[SkillRequirement]):
        if not (1 <= len(v) <= 10):
            raise ValueError("Number of skill requirements must be within 1 to 10.")
        seen = set()
        for item in v:
            key = item.name.strip().lower()
            if key in seen:
                raise ValueError(f'Duplicate skill name detected: "{item.name}".')
            seen.add(key)
        return v


# Skill Gap Schemas
class SkillGap(BaseModel):
    """A skill gap with current and required levels."""
    name: str
    is_gap: bool
    required_level: LevelRequired
    current_level: LevelCurrent
    reason: str = Field(..., description="≤20 words concise rationale for current level.")
    level_confidence: Confidence

    @field_validator("reason")
    @classmethod
    def limit_reason_words(cls, v: str) -> str:
        words = v.split()
        if len(words) > 20:
            raise ValueError("Reason must be 20 words or fewer.")
        return v

    @field_validator("is_gap")
    @classmethod
    def check_gap_consistency(cls, is_gap_value, info):
        data = info.data
        required = data.get("required_level")
        current = data.get("current_level")
        if required is None or current is None:
            return is_gap_value
        order = {"unlearned": 0, "beginner": 1, "intermediate": 2, "advanced": 3}
        gap_should_be = order[current.value] < order[required.value]
        if is_gap_value != gap_should_be:
            raise ValueError(
                f'is_gap inconsistency: required="{required.value}", current="{current.value}" implies is_gap={gap_should_be}.'
            )
        return is_gap_value


class SkillGaps(BaseModel):
    """Collection of skill gaps."""
    skill_gaps: List[SkillGap]

    @field_validator("skill_gaps")
    @classmethod
    def limit_length_and_names(cls, v: List[SkillGap]):
        if not (1 <= len(v) <= 10):
            raise ValueError("Number of skill gaps must be within 1 to 10.")
        seen = set()
        for item in v:
            key = item.name.strip().lower()
            if key in seen:
                raise ValueError(f'Duplicate skill name detected: "{item.name}".')
            seen.add(key)
        return v


class SkillGapsRoot(RootModel):
    """Root model for skill gaps list."""
    root: List[SkillGap]


# Learning Goal Schemas
class RefinedLearningGoal(BaseModel):
    """A refined learning goal."""
    refined_goal: str


# Learner Profile Schemas
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
    overall_progress: int = Field(..., ge=0, le=100)
    mastered_skills: List[MasteredSkill] = Field(default_factory=list)
    in_progress_skills: List[InProgressSkill] = Field(default_factory=list)


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
    """Complete learner profile."""
    learner_information: str
    cognitive_status: CognitiveStatus
    learning_preferences: LearningPreferences
    behavioral_patterns: BehavioralPatterns


# Learner Simulation Schemas
class LearnerBehaviorLog(BaseModel):
    """Schema for a single session's learner interaction log."""
    session_number: int = Field(..., ge=1)
    interactions: List[Dict[str, Any]] = Field(default_factory=list)
    notes: Optional[str] = None


class GroundTruthProfileResult(BaseModel):
    """Schema for ground-truth profile generation/progression output."""
    learner_profile: Dict[str, Any]


# Parser functions
def parse_learner_behavior_log(data: Any) -> LearnerBehaviorLog:
    """Validate arbitrary LLM output as a LearnerBehaviorLog."""
    return LearnerBehaviorLog.model_validate(data)


def parse_ground_truth_profile_result(data: Any) -> GroundTruthProfileResult:
    """Validate LLM output of ground-truth profile creation/progression."""
    return GroundTruthProfileResult.model_validate(data)
