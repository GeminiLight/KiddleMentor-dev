"""Integration tests for content agents."""

import pytest
from unittest.mock import MagicMock, patch

from gen_mentor.agents.content import (
    create_learning_content_with_llm,
    schedule_learning_path_with_llm,
    explore_goal_knowledge_with_llm,
)


class TestContentAgents:
    """Integration tests for content generation agents."""

    @pytest.mark.integration
    def test_create_learning_content(self, mock_llm_json, sample_learner_profile):
        """Test creating learning content."""
        with patch('gen_mentor.agents.content.content_creator.BaseAgent') as mock_agent_class:
            mock_agent = MagicMock()
            mock_agent.invoke.return_value = {
                "title": "Introduction to Python",
                "sections": [
                    {
                        "heading": "Variables",
                        "content": "Variables store data values.",
                        "code_examples": ["x = 5"],
                    }
                ],
            }
            mock_agent_class.return_value = mock_agent

            result = create_learning_content_with_llm(
                llm=mock_llm_json,
                learner_profile=sample_learner_profile,
                topic="Python Variables",
            )

            assert result is not None
            mock_agent.invoke.assert_called_once()

    @pytest.mark.integration
    def test_schedule_learning_path(self, mock_llm_json, sample_learner_profile):
        """Test scheduling learning path."""
        with patch('gen_mentor.agents.content.path_scheduler.BaseAgent') as mock_agent_class:
            mock_agent = MagicMock()
            mock_agent.invoke.return_value = {
                "learning_path": [
                    {
                        "id": "Session 1",
                        "title": "Python Basics",
                        "abstract": "Learn Python basics",
                        "if_learned": False,
                        "associated_skills": ["Variables"],
                        "desired_outcome_when_completed": [],
                    }
                ]
            }
            mock_agent_class.return_value = mock_agent

            skill_gaps = [{"name": "Python", "is_gap": True}]

            result = schedule_learning_path_with_llm(
                llm=mock_llm_json,
                learner_profile=sample_learner_profile,
                skill_gaps=skill_gaps,
            )

            assert result is not None
            assert "learning_path" in result
            mock_agent.invoke.assert_called_once()

    @pytest.mark.integration
    def test_explore_goal_knowledge(self, mock_llm_json):
        """Test exploring goal knowledge."""
        with patch('gen_mentor.agents.content.knowledge_explorer.BaseAgent') as mock_agent_class:
            mock_agent = MagicMock()
            mock_agent.invoke.return_value = {
                "knowledge_points": [
                    {
                        "topic": "Variables",
                        "description": "Variables store values",
                        "importance": "high",
                    }
                ]
            }
            mock_agent_class.return_value = mock_agent

            result = explore_goal_knowledge_with_llm(
                llm=mock_llm_json,
                learning_goal="Learn Python",
                current_skills=["Basic syntax"],
            )

            assert result is not None
            mock_agent.invoke.assert_called_once()
