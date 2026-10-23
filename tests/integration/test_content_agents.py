"""Exercise current content wrappers with deterministic local model responses."""

import json

import pytest
from langchain_core.language_models.fake_chat_models import FakeListChatModel

from gen_mentor.agents.content import (
    create_learning_content_with_llm,
    schedule_learning_path_with_llm,
    explore_knowledge_points_with_llm,
)


@pytest.mark.integration
class TestContentAgents:
    def test_create_learning_content(self, sample_learner_profile, sample_learning_path, sample_quiz):
        outputs = [
            {"knowledge_points": [{"name": "Variables", "type": "foundational"}]},
            {"title": "Variables", "content": "Variables store data values. Example: x = 5."},
            {"title": "Introduction to Python", "overview": "Learn variables", "summary": "Practice assigning values"},
            sample_quiz,
        ]
        llm = FakeListChatModel(responses=[json.dumps(output) for output in outputs])
        result = create_learning_content_with_llm(
            llm=llm,
            learner_profile=sample_learner_profile,
            learning_path=sample_learning_path,
            learning_session=sample_learning_path["learning_path"][0],
            allow_parallel=False,
            use_search=False,
        )
        assert "Introduction to Python" in result["document"]
        assert "Variables store data values" in result["document"]
        assert result["quizzes"] == sample_quiz

    def test_schedule_learning_path(self, sample_learner_profile, sample_learning_path):
        llm = FakeListChatModel(responses=[json.dumps(sample_learning_path)])
        result = schedule_learning_path_with_llm(
            llm=llm,
            learner_profile=sample_learner_profile,
            session_count=2,
            learning_goal="Learn Python",
        )
        assert result == sample_learning_path

    def test_explore_goal_knowledge(self, sample_learner_profile, sample_learning_path):
        expected = {"knowledge_points": [{"name": "Variables", "type": "foundational"}]}
        llm = FakeListChatModel(responses=[json.dumps(expected)])
        result = explore_knowledge_points_with_llm(
            llm=llm,
            learner_profile=sample_learner_profile,
            learning_path=sample_learning_path,
            learning_session=sample_learning_path["learning_path"][0],
            learning_goal="Learn Python",
        )
        assert result == expected
