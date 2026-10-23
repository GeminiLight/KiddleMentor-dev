"""Exercise learning wrappers, LangGraph invocation and schema validation offline."""

import json

import pytest
from langchain_core.language_models.fake_chat_models import FakeListChatModel

from gen_mentor.agents.learning import (
    identify_skill_gap_with_llm,
    refine_learning_goal_with_llm,
    map_goal_to_skills_with_llm,
)


@pytest.mark.integration
class TestLearningAgents:
    def test_identify_skill_gap(self, sample_skill_gap):
        requirements = {"skill_requirements": [{"name": "Python Functions", "required_level": "intermediate"}]}
        expected = {
            "skill_gaps": [{k: v for k, v in sample_skill_gap.items() if k not in ("priority", "estimated_time")}]
        }
        llm = FakeListChatModel(responses=[json.dumps(expected)])
        gaps, used_requirements = identify_skill_gap_with_llm(
            llm=llm,
            learning_goal="Master Python programming",
            learner_information="Knows basic Python syntax",
            skill_requirements=requirements,
        )
        assert gaps == expected
        assert used_requirements == requirements

    def test_refine_learning_goal(self):
        expected = {"refined_goal": "Master Python fundamentals for data science"}
        llm = FakeListChatModel(responses=[json.dumps(expected)])
        result = refine_learning_goal_with_llm(
            llm=llm,
            learning_goal="Learn Python",
            learner_information="For data science",
        )
        assert result == expected

    def test_map_skill_requirements(self):
        expected = {"skill_requirements": [{"name": "Python Basics", "required_level": "intermediate"}]}
        llm = FakeListChatModel(responses=[json.dumps(expected)])
        assert map_goal_to_skills_with_llm(llm=llm, learning_goal="Become a Python developer") == expected

    def test_gap_identification_generates_requirements_when_omitted(self, sample_skill_gap):
        requirements = {"skill_requirements": [{"name": "Python Functions", "required_level": "intermediate"}]}
        expected = {
            "skill_gaps": [{k: v for k, v in sample_skill_gap.items() if k not in ("priority", "estimated_time")}]
        }
        llm = FakeListChatModel(responses=[json.dumps(requirements), json.dumps(expected)])
        gaps, used_requirements = identify_skill_gap_with_llm(llm, "Learn Python", "Knows syntax")
        assert gaps == expected
        assert used_requirements == requirements
