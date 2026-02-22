"""Centralized schemas for GenMentor.

All Pydantic models and data schemas are organized here:
- content.py: Learning content, knowledge points
- learning.py: Skills, gaps, goals, learner profiles
- tutoring.py: Chatbot interactions and tutoring
- assessment.py: Quizzes and performance evaluation
"""

from .content import (
    # Enums
    Proficiency,
    KnowledgeType,
    # Learning Path
    DesiredOutcome,
    SessionItem,
    LearningPath,
    # Knowledge
    KnowledgePoint,
    KnowledgePoints,
    KnowledgeDraft,
    DocumentStructure,
    # Quizzes
    SingleChoiceQuestion,
    MultipleChoiceQuestion,
    TrueFalseQuestion,
    ShortAnswerQuestion,
    DocumentQuiz,
    QuizPair,
    # Content
    ContentSection,
    ContentOutline,
    LearningContent,
    # Feedback
    FeedbackDetail,
    LearnerFeedback,
    # Parsers
    parse_knowledge_points,
    parse_knowledge_draft,
    parse_document_structure,
    parse_document_quiz,
)

from .learning import (
    # Enums
    LevelRequired,
    LevelCurrent,
    Confidence,
    # Skills
    SkillRequirement,
    SkillRequirements,
    SkillGap,
    SkillGaps,
    SkillGapsRoot,
    # Goals
    RefinedLearningGoal,
    # Learner Profile
    MasteredSkill,
    InProgressSkill,
    CognitiveStatus,
    LearningPreferences,
    BehavioralPatterns,
    LearnerProfile,
    # Simulation
    LearnerBehaviorLog,
    GroundTruthProfileResult,
    # Parsers
    parse_learner_behavior_log,
    parse_ground_truth_profile_result,
)

from .tutoring import (
    # Tutoring schemas
    ChatMessage,
    TutorChatPayload,
    TutorResponse,
    # Parsers
    parse_tutor_response,
)

from .assessment import (
    # Enums
    PerformanceLevel,
    ProgressPace,
    SkillLevel,
    ConfidenceLevel,
    Priority,
    ImprovementStatus,
    # Quiz schemas
    DocumentQuizPayload,
    # Performance schemas
    ProgressStatus,
    SkillEvaluation,
    Recommendation,
    PerformanceEvaluation,
    SkillMasteryEvaluation,
    QuizResult,
    SessionData,
    # Parsers
    parse_performance_evaluation,
    parse_skill_mastery_evaluation,
)

__all__ = [
    # Content schemas
    "Proficiency",
    "KnowledgeType",
    "DesiredOutcome",
    "SessionItem",
    "LearningPath",
    "KnowledgePoint",
    "KnowledgePoints",
    "KnowledgeDraft",
    "DocumentStructure",
    "SingleChoiceQuestion",
    "MultipleChoiceQuestion",
    "TrueFalseQuestion",
    "ShortAnswerQuestion",
    "DocumentQuiz",
    "QuizPair",
    "ContentSection",
    "ContentOutline",
    "LearningContent",
    "FeedbackDetail",
    "LearnerFeedback",
    "parse_knowledge_points",
    "parse_knowledge_draft",
    "parse_document_structure",
    "parse_document_quiz",
    # Learning schemas
    "LevelRequired",
    "LevelCurrent",
    "Confidence",
    "SkillRequirement",
    "SkillRequirements",
    "SkillGap",
    "SkillGaps",
    "SkillGapsRoot",
    "RefinedLearningGoal",
    "MasteredSkill",
    "InProgressSkill",
    "CognitiveStatus",
    "LearningPreferences",
    "BehavioralPatterns",
    "LearnerProfile",
    "LearnerBehaviorLog",
    "GroundTruthProfileResult",
    "parse_learner_behavior_log",
    "parse_ground_truth_profile_result",
    # Tutoring schemas
    "ChatMessage",
    "TutorChatPayload",
    "TutorResponse",
    "parse_tutor_response",
    # Assessment schemas
    "PerformanceLevel",
    "ProgressPace",
    "SkillLevel",
    "ConfidenceLevel",
    "Priority",
    "ImprovementStatus",
    "DocumentQuizPayload",
    "ProgressStatus",
    "SkillEvaluation",
    "Recommendation",
    "PerformanceEvaluation",
    "SkillMasteryEvaluation",
    "QuizResult",
    "SessionData",
    "parse_performance_evaluation",
    "parse_skill_mastery_evaluation",
]
