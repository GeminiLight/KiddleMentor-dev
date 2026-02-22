"""Integration tests for assessment agents."""

import pytest
from unittest.mock import MagicMock, patch

from gen_mentor.agents.assessment import (
    generate_document_quiz_with_llm,
    evaluate_learner_performance_with_llm,
    evaluate_skill_mastery_with_llm,
    generate_performance_report_with_llm,
)


class TestAssessmentAgents:
    """Integration tests for assessment agents."""

    @pytest.mark.integration
    def test_generate_document_quiz(
        self, mock_llm_json, sample_learner_profile
    ):
        """Test generating document quiz."""
        with patch('gen_mentor.agents.assessment.quiz_generator.DocumentQuizGenerator') as mock_gen:
            mock_instance = MagicMock()
            mock_instance.generate.return_value = {
                "single_choice_questions": [
                    {
                        "question": "What is Python?",
                        "options": ["Language", "Snake", "Tool", "Framework"],
                        "correct_answer": 0,
                        "explanation": "Python is a programming language",
                    }
                ],
                "multiple_choice_questions": [],
                "true_false_questions": [],
                "short_answer_questions": [],
            }
            mock_gen.return_value = mock_instance

            learning_document = {"title": "Python Intro", "content": "Python is..."}

            result = generate_document_quiz_with_llm(
                llm=mock_llm_json,
                learner_profile=sample_learner_profile,
                learning_document=learning_document,
                single_choice_count=3,
            )

            assert result is not None
            mock_instance.generate.assert_called_once()

    @pytest.mark.integration
    def test_evaluate_learner_performance(
        self, mock_llm_json, sample_learner_profile, sample_learning_path, sample_session_data
    ):
        """Test evaluating learner performance."""
        with patch('gen_mentor.agents.assessment.performance_evaluator.BaseAgent') as mock_agent_class:
            mock_agent = MagicMock()
            mock_agent.invoke.return_value = {
                "overall_score": 85.0,
                "performance_level": "good",
                "strengths": ["Quick learner"],
                "weaknesses": ["Needs more practice"],
                "progress_status": {
                    "current_session": 5,
                    "expected_session": 5,
                    "on_track": True,
                    "pace": "on_pace",
                },
                "skill_evaluations": [],
                "recommendations": [],
                "next_steps": "Continue learning",
            }
            mock_agent_class.return_value = mock_agent

            result = evaluate_learner_performance_with_llm(
                llm=mock_llm_json,
                learner_profile=sample_learner_profile,
                learning_path=sample_learning_path,
                session_data=sample_session_data,
            )

            assert result is not None
            assert "overall_score" in result
            mock_agent.invoke.assert_called_once()

    @pytest.mark.integration
    def test_evaluate_skill_mastery(self, mock_llm_json):
        """Test evaluating skill mastery."""
        with patch('gen_mentor.agents.assessment.performance_evaluator.BaseAgent') as mock_agent_class:
            mock_agent = MagicMock()
            mock_agent.invoke.return_value = {
                "skill_name": "Python Functions",
                "current_level": "intermediate",
                "confidence": "high",
                "understanding_score": 80.0,
                "proficiency_score": 75.0,
                "ready_to_advance": True,
                "mastered_aspects": ["Basic functions"],
                "gaps": ["Decorators"],
                "improvement_from_previous": "improved",
                "evidence": "Good quiz scores",
                "practice_recommendations": ["Practice decorators"],
                "estimated_time_to_mastery": "2 weeks",
            }
            mock_agent_class.return_value = mock_agent

            result = evaluate_skill_mastery_with_llm(
                llm=mock_llm_json,
                skill_name="Python Functions",
                learner_responses={"quiz_1": "correct"},
            )

            assert result is not None
            assert result["skill_name"] == "Python Functions"
            mock_agent.invoke.assert_called_once()

    @pytest.mark.integration
    def test_generate_performance_report(self, mock_llm_json, sample_learner_profile):
        """Test generating performance report."""
        with patch('gen_mentor.agents.assessment.performance_evaluator.BaseAgent') as mock_agent_class:
            mock_agent = MagicMock()
            mock_agent.invoke.return_value = "# Performance Report\n\nGreat progress!"
            mock_agent_class.return_value = mock_agent

            performance_history = [
                {"session": 1, "score": 70},
                {"session": 2, "score": 85},
            ]

            result = generate_performance_report_with_llm(
                llm=mock_llm_json,
                learner_profile=sample_learner_profile,
                performance_history=performance_history,
                time_period="2 weeks",
            )

            assert result is not None
            assert isinstance(result, str)
            mock_agent.invoke.assert_called_once()
