"""Prompts for assessment agents."""

from .quiz_generation import *
from .performance_evaluation import *

__all__ = [
    "DOCUMENT_QUIZ_PROMPT",
    "PERFORMANCE_EVALUATION_PROMPT",
    "SKILL_MASTERY_EVALUATION_PROMPT",
    "PERFORMANCE_REPORT_PROMPT",
]
