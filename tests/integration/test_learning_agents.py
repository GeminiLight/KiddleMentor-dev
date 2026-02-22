"""Integration tests for learning agents."""

import pytest
from unittest.mock import MagicMock, patch

from gen_mentor.agents.learning import (
    identify_skill_gap_with_llm,
    refine_learning_goal_with_llm,
    map_skill_requirements_with_llm,
)


class TestLearningAgents:
    """Integration tests for learning assessment agents."""

    @pytest.mark.integration
    def test_identify_skill_gap(self, mock_llm_json, sample_learner_profile):
        """Test identifying skill gaps."""
        with patch('gen_mentor.agents.learning.skill_gap_identifier.BaseAgent') as mock_agent_class:
            mock_agent = MagicMock()
            mock_agent.invoke.return_value = {
                "skill_gaps": [
                    {
                        "name": "Python Functions",
                        "is_gap": True,
                        "required_level": "intermediate",
                        "current_level": "beginner",
                    }
                ]
            }
            mock_agent_class.return_value = mock_agent

            result = identify_skill_gap_with_llm(
                llm=mock_llm_json,
                learner_profile=sample_learner_profile,
                target_goal="Master Python programming",
            )

            assert result is not None
            mock_agent.invoke.assert_called_once()

    @pytest.mark.integration
    def test_refine_learning_goal(self, mock_llm_json):
        """Test refining learning goal."""
        with patch('gen_mentor.agents.learning.goal_refiner.BaseAgent') as mock_agent_class:
            mock_agent = MagicMock()
            mock_agent.invoke.return_value = {
                "original_goal": "Learn Python",
                "refined_goal": "Master Python fundamentals including data structures",
                "key_topics": ["Variables", "Functions", "Classes"],
                "estimated_duration": "3 months",
            }
            mock_agent_class.return_value = mock_agent

            result = refine_learning_goal_with_llm(
                llm=mock_llm_json,
                original_goal="Learn Python",
                context="For data science",
            )

            assert result is not None
            assert "refined_goal" in result
            mock_agent.invoke.assert_called_once()

    @pytest.mark.integration
    def test_map_skill_requirements(self, mock_llm_json):
        """Test mapping skill requirements."""
        with patch('gen_mentor.agents.learning.skill_mapper.BaseAgent') as mock_agent_class:
            mock_agent = MagicMock()
            mock_agent.invoke.return_value = {
                "skill_requirements": [
                    {
                        "skill_name": "Python Basics",
                        "required_level": "intermediate",
                        "prerequisites": ["Programming fundamentals"],
                    }
                ]
            }
            mock_agent_class.return_value = mock_agent

            result = map_skill_requirements_with_llm(
                llm=mock_llm_json,
                learning_goal="Become a Python developer",
            )

            assert result is not None
            mock_agent.invoke.assert_called_once()
