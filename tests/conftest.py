"""Pytest configuration and shared fixtures."""

import os
import tempfile
from pathlib import Path
from typing import Any, Dict
from unittest.mock import MagicMock

import pytest
from langchain_core.language_models.fake_chat_models import FakeChatModel
from omegaconf import OmegaConf

from gen_mentor.config import AppConfig, load_config_from_dict
from gen_mentor.schemas import (
    LearnerProfile,
    LearningPath,
    SkillGap,
    DocumentQuiz,
)


@pytest.fixture
def temp_dir():
    """Create a temporary directory for tests."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def mock_config_dir(temp_dir):
    """Mock the config directory for tests."""
    config_dir = temp_dir / ".gen-mentor"
    config_dir.mkdir(parents=True, exist_ok=True)
    return config_dir


@pytest.fixture
def sample_config_dict() -> Dict[str, Any]:
    """Sample configuration dictionary for testing."""
    return {
        "agent_defaults": {
            "model": "openai/gpt-5.1",
            "temperature": 0.0,
            "max_tokens": 8192,
        },
        "providers": {
            "openai": {
                "api_key": "sk-test-key",
                "base_url": "https://api.openai.com/v1",
                "model_patterns": ["gpt-*", "o1-*"],
            },
            "deepseek": {
                "api_key": "test-deepseek-key",
                "base_url": "https://api.deepseek.com",
                "model_patterns": ["deepseek-*"],
            },
        },
        "searches": {
            "default": "duckduckgo",
            "duckduckgo": {
                "api_key": None,
                "max_results": 10,
            },
        },
    }


@pytest.fixture
def sample_config(sample_config_dict) -> AppConfig:
    """Sample AppConfig instance for testing."""
    return load_config_from_dict(sample_config_dict)


@pytest.fixture
def mock_llm():
    """Mock LLM for testing without API calls."""
    return FakeChatModel(responses=["Test response"])


@pytest.fixture
def mock_llm_json():
    """Mock LLM that returns JSON responses."""
    return FakeChatModel(responses=['{"result": "test", "status": "success"}'])


@pytest.fixture
def sample_learner_profile() -> Dict[str, Any]:
    """Sample learner profile for testing."""
    return {
        "name": "Test Learner",
        "learning_goal": "Learn Python programming",
        "mastered_skills": [
            {"skill_name": "Basic syntax", "proficiency": "intermediate"}
        ],
        "in_progress_skills": [
            {"skill_name": "Object-oriented programming", "current_level": "beginner"}
        ],
        "cognitive_status": {
            "attention_span": "medium",
            "learning_speed": "fast",
            "preferred_difficulty": "intermediate",
        },
        "learning_preferences": {
            "preferred_content_types": ["text", "code examples"],
            "preferred_session_length": 30,
            "preferred_pace": "moderate",
        },
    }


@pytest.fixture
def sample_skill_gap() -> Dict[str, Any]:
    """Sample skill gap for testing."""
    return {
        "name": "Python Functions",
        "is_gap": True,
        "required_level": "intermediate",
        "current_level": "beginner",
        "priority": "high",
        "estimated_time": "2 weeks",
    }


@pytest.fixture
def sample_learning_path() -> Dict[str, Any]:
    """Sample learning path for testing."""
    return {
        "learning_path": [
            {
                "id": "Session 1",
                "title": "Introduction to Python Functions",
                "abstract": "Learn the basics of defining and calling functions in Python.",
                "if_learned": False,
                "associated_skills": ["Functions", "Parameters"],
                "desired_outcome_when_completed": [
                    {"name": "Functions", "level": "beginner"}
                ],
            },
            {
                "id": "Session 2",
                "title": "Advanced Function Concepts",
                "abstract": "Explore decorators, closures, and higher-order functions.",
                "if_learned": False,
                "associated_skills": ["Advanced Functions", "Decorators"],
                "desired_outcome_when_completed": [
                    {"name": "Advanced Functions", "level": "intermediate"}
                ],
            },
        ]
    }


@pytest.fixture
def sample_quiz() -> Dict[str, Any]:
    """Sample quiz for testing."""
    return {
        "single_choice_questions": [
            {
                "question": "What is a function in Python?",
                "options": [
                    "A reusable block of code",
                    "A type of variable",
                    "A loop structure",
                    "A data type",
                ],
                "correct_answer": 0,
                "explanation": "A function is a reusable block of code that performs a specific task.",
            }
        ],
        "multiple_choice_questions": [],
        "true_false_questions": [],
        "short_answer_questions": [],
    }


@pytest.fixture
def sample_session_data() -> Dict[str, Any]:
    """Sample session data for testing."""
    return {
        "session_id": "test-session-1",
        "duration": 1800,
        "completed": True,
        "engagement_score": 85.0,
        "quiz_results": [
            {
                "quiz_id": "quiz-1",
                "total_questions": 5,
                "correct_answers": 4,
                "score": 80.0,
                "time_taken": 300,
            }
        ],
    }


@pytest.fixture(autouse=True)
def suppress_warnings():
    """Suppress warnings during tests."""
    import warnings
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    warnings.filterwarnings("ignore", category=FutureWarning)


@pytest.fixture
def mock_file_tool():
    """Mock file operations tool."""
    mock = MagicMock()
    mock.run.return_value = "File content"
    return mock


@pytest.fixture
def mock_search_tool():
    """Mock search tool."""
    mock = MagicMock()
    mock.run.return_value = "Search results"
    return mock
