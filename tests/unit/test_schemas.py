"""Unit tests for schema validation."""

import pytest
from pydantic import ValidationError

from gen_mentor.schemas import (
    # Content schemas
    LearningPath,
    SessionItem,
    DocumentQuiz,
    SingleChoiceQuestion,
    LearningContent,

    # Learning schemas
    SkillGap,
    LearnerProfile,
    MasteredSkill,
    RefinedLearningGoal,

    # Tutoring schemas
    TutorChatPayload,
    ChatMessage,

    # Assessment schemas
    PerformanceEvaluation,
    SkillMasteryEvaluation,
    DocumentQuizPayload,
)


class TestContentSchemas:
    """Tests for content-related schemas."""

    def test_session_item_creation(self):
        """Test creating a session item."""
        session = SessionItem(
            id="Session 1",
            title="Introduction to Python",
            abstract="Learn Python basics",
            if_learned=False,
            associated_skills=["Variables", "Functions"],
            desired_outcome_when_completed=[],
        )

        assert session.id == "Session 1"
        assert session.title == "Introduction to Python"
        assert len(session.associated_skills) == 2

    def test_learning_path_creation(self, sample_learning_path):
        """Test creating a learning path."""
        path = LearningPath.model_validate(sample_learning_path)

        assert len(path.learning_path) == 2
        assert path.learning_path[0].title == "Introduction to Python Functions"

    def test_single_choice_question(self):
        """Test single choice question validation."""
        question = SingleChoiceQuestion(
            question="What is Python?",
            options=["A language", "A snake", "A tool", "A framework"],
            correct_answer=0,
            explanation="Python is a programming language.",
        )

        assert len(question.options) == 4
        assert question.correct_answer == 0

    def test_document_quiz_creation(self, sample_quiz):
        """Test creating a document quiz."""
        quiz = DocumentQuiz.model_validate(sample_quiz)

        assert len(quiz.single_choice_questions) == 1
        assert quiz.single_choice_questions[0].question == "What is a function in Python?"


class TestLearningSchemas:
    """Tests for learning-related schemas."""

    def test_skill_gap_creation(self, sample_skill_gap):
        """Test creating a skill gap."""
        gap = SkillGap.model_validate(sample_skill_gap)

        assert gap.name == "Python Functions"
        assert gap.is_gap is True
        assert gap.required_level == "intermediate"

    def test_mastered_skill_creation(self):
        """Test creating a mastered skill."""
        skill = MasteredSkill(
            skill_name="Python Basics",
            proficiency="intermediate",
        )

        assert skill.skill_name == "Python Basics"
        assert skill.proficiency == "intermediate"

    def test_learner_profile_creation(self, sample_learner_profile):
        """Test creating a learner profile."""
        profile = LearnerProfile.model_validate(sample_learner_profile)

        assert profile.name == "Test Learner"
        assert profile.learning_goal == "Learn Python programming"
        assert len(profile.mastered_skills) == 1

    def test_refined_learning_goal(self):
        """Test refined learning goal."""
        goal = RefinedLearningGoal(
            original_goal="Learn Python",
            refined_goal="Master Python fundamentals including data structures and OOP",
            key_topics=["Variables", "Functions", "Classes"],
            estimated_duration="3 months",
        )

        assert "fundamentals" in goal.refined_goal
        assert len(goal.key_topics) == 3


class TestTutoringSchemas:
    """Tests for tutoring-related schemas."""

    def test_chat_message_creation(self):
        """Test creating a chat message."""
        message = ChatMessage(
            role="user",
            content="What is Python?",
        )

        assert message.role == "user"
        assert message.content == "What is Python?"

    def test_tutor_chat_payload(self):
        """Test tutor chat payload."""
        payload = TutorChatPayload(
            learner_profile={"name": "Test"},
            messages=[{"role": "user", "content": "Hello"}],
            use_search=True,
            top_k=5,
        )

        assert payload.use_search is True
        assert payload.top_k == 5

    def test_tutor_chat_payload_validation(self):
        """Test tutor chat payload with missing required fields."""
        with pytest.raises(ValidationError):
            TutorChatPayload(learner_profile={"name": "Test"})  # Missing messages


class TestAssessmentSchemas:
    """Tests for assessment-related schemas."""

    def test_document_quiz_payload(self):
        """Test document quiz payload."""
        payload = DocumentQuizPayload(
            learner_profile={"name": "Test"},
            learning_document={"title": "Python Basics"},
            single_choice_count=3,
            multiple_choice_count=2,
        )

        assert payload.single_choice_count == 3
        assert payload.multiple_choice_count == 2

    def test_performance_evaluation_schema(self):
        """Test performance evaluation schema."""
        evaluation = PerformanceEvaluation(
            overall_score=85.0,
            performance_level="good",
            strengths=["Quick learner", "Good problem solving"],
            weaknesses=["Needs more practice with OOP"],
            progress_status={
                "current_session": 5,
                "expected_session": 5,
                "on_track": True,
                "pace": "on_pace",
            },
            skill_evaluations=[],
            recommendations=[],
            next_steps="Continue with advanced topics",
        )

        assert evaluation.overall_score == 85.0
        assert evaluation.performance_level == "good"
        assert len(evaluation.strengths) == 2

    def test_skill_mastery_evaluation(self):
        """Test skill mastery evaluation."""
        mastery = SkillMasteryEvaluation(
            skill_name="Python Functions",
            current_level="intermediate",
            confidence="high",
            understanding_score=80.0,
            proficiency_score=75.0,
            ready_to_advance=True,
            mastered_aspects=["Basic functions", "Parameters"],
            gaps=["Decorators", "Closures"],
            improvement_from_previous="improved",
            evidence="Consistently correct answers on quizzes",
            practice_recommendations=["Practice with decorators"],
            estimated_time_to_mastery="2 weeks",
        )

        assert mastery.skill_name == "Python Functions"
        assert mastery.ready_to_advance is True
        assert len(mastery.gaps) == 2


class TestSchemaValidation:
    """Tests for schema validation edge cases."""

    def test_invalid_proficiency_level(self):
        """Test invalid proficiency level."""
        with pytest.raises(ValidationError):
            MasteredSkill(
                skill_name="Test",
                proficiency="invalid_level",  # Invalid
            )

    def test_score_range_validation(self):
        """Test score validation (0-100)."""
        with pytest.raises(ValidationError):
            PerformanceEvaluation(
                overall_score=150.0,  # Invalid, > 100
                performance_level="good",
                strengths=[],
                weaknesses=[],
                progress_status={
                    "current_session": 1,
                    "expected_session": 1,
                    "on_track": True,
                    "pace": "on_pace",
                },
                skill_evaluations=[],
                recommendations=[],
                next_steps="Continue",
            )

    def test_empty_required_fields(self):
        """Test validation with empty required fields."""
        with pytest.raises(ValidationError):
            SessionItem(
                id="",  # Empty ID
                title="Test",
                abstract="Test",
                if_learned=False,
            )
