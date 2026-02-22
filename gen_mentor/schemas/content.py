"""Content-related schemas for learning materials, quizzes, and feedback."""

from __future__ import annotations

from enum import Enum
from typing import List

from pydantic import BaseModel, Field, field_validator


# Enums
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


# Learning Path Schemas
class DesiredOutcome(BaseModel):
    """Desired skill outcome for a session."""
    name: str = Field(..., description="Skill name")
    level: Proficiency = Field(..., description="Desired proficiency when completed")


class SessionItem(BaseModel):
    """A single session in a learning path."""
    id: str = Field(..., description="Session identifier, e.g., 'Session 1'")
    title: str
    abstract: str
    if_learned: bool
    associated_skills: List[str] = Field(default_factory=list)
    desired_outcome_when_completed: List[DesiredOutcome] = Field(default_factory=list)

    @field_validator("associated_skills")
    @classmethod
    def ensure_nonempty_strings(cls, v: List[str]) -> List[str]:
        return [s for s in (str(x).strip() for x in v) if s]


class LearningPath(BaseModel):
    """Complete learning path with multiple sessions."""
    learning_path: List[SessionItem]

    @field_validator("learning_path")
    @classmethod
    def limit_sessions(cls, v: List[SessionItem]) -> List[SessionItem]:
        if not (1 <= len(v) <= 10):
            raise ValueError("Learning path must contain between 1 and 10 sessions.")
        return v


# Knowledge Schemas
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


# Quiz Schemas
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
    single_choice_questions: List[SingleChoiceQuestion] = Field(default_factory=list)
    multiple_choice_questions: List[MultipleChoiceQuestion] = Field(default_factory=list)
    true_false_questions: List[TrueFalseQuestion] = Field(default_factory=list)
    short_answer_questions: List[ShortAnswerQuestion] = Field(default_factory=list)


class QuizPair(BaseModel):
    """Simple question-answer pair."""
    question: str
    answer: str


# Content Schemas
class ContentSection(BaseModel):
    """A section in learning content."""
    title: str
    summary: str


class ContentOutline(BaseModel):
    """Outline for learning content."""
    title: str
    sections: List[ContentSection] = Field(default_factory=list)


class LearningContent(BaseModel):
    """Complete learning content with quizzes."""
    title: str
    overview: str
    content: str
    summary: str
    quizzes: List[QuizPair] = Field(default_factory=list)


# Feedback Schemas
class FeedbackDetail(BaseModel):
    """Detailed feedback category."""
    progression: str
    engagement: str
    personalization: str


class LearnerFeedback(BaseModel):
    """Learner feedback and suggestions."""
    feedback: FeedbackDetail
    suggestions: FeedbackDetail


# Parser functions
def parse_knowledge_points(data) -> KnowledgePoints:
    """Parse knowledge points from data."""
    return KnowledgePoints.model_validate(data)


def parse_knowledge_draft(data) -> KnowledgeDraft:
    """Parse knowledge draft from data."""
    return KnowledgeDraft.model_validate(data)


def parse_document_structure(data) -> DocumentStructure:
    """Parse document structure from data."""
    return DocumentStructure.model_validate(data)


def parse_document_quiz(data) -> DocumentQuiz:
    """Parse document quiz from data."""
    return DocumentQuiz.model_validate(data)


# Search Result Schema
from dataclasses import dataclass
from typing import Optional
from langchain_core.documents import Document

@dataclass
class SearchResult:
    """Search result from vector database or search engine."""
    title: str
    link: str
    snippet: Optional[str] = None
    content: Optional[str] = None
    document: Optional[Document] = None
