"""
Assessment endpoints - quiz generation and performance evaluation.
"""

from fastapi import APIRouter, Depends

from models import (
    KnowledgeQuizGenerationRequest,
    QuizResponse,
    PerformanceEvaluationRequest,
    PerformanceEvaluationResponse,
    SkillMasteryEvaluationRequest,
    SkillMasteryEvaluationResponse,
    PerformanceReportRequest,
    PerformanceReportResponse,
    FeedbackSimulationRequest,
    FeedbackSimulationResponse,
)
from services.llm_service import get_llm_service, LLMService
from services.memory_service import get_memory_service, MemoryService
from gen_mentor.agents.assessment.quiz_generator import generate_document_quizzes_with_llm
from gen_mentor.agents.assessment.performance_evaluator import (
    evaluate_learner_performance_with_llm,
    evaluate_skill_mastery_with_llm,
    generate_performance_report_with_llm,
)
from gen_mentor.agents.content.feedback_simulator import LearnerFeedbackSimulator
from dependencies import extract_learner_id, resolve_learning_goal, parse_json_string
from exceptions import LLMError, ValidationError

router = APIRouter()


@router.post("/generate-document-quizzes", response_model=QuizResponse, tags=["Assessment"])
async def generate_document_quizzes(
    request: KnowledgeQuizGenerationRequest,
    llm_service: LLMService = Depends(get_llm_service),
    memory_service: MemoryService = Depends(get_memory_service)
):
    """Generate quizzes from learning document.

    Creates personalized assessments to test understanding of the learning material.

    Args:
        request: Quiz generation request
        llm_service: LLM service dependency
        memory_service: Memory service dependency

    Returns:
        Generated quizzes

    Raises:
        LLMError: If quiz generation fails
    """
    # Get LLM
    llm = llm_service.get_llm()

    # Resolve learning goal
    learner_id = extract_learner_id(request.learner_profile)
    learning_goal = resolve_learning_goal(memory_service, learner_id, request.goal_id)

    # Generate quizzes
    try:
        document_quiz = generate_document_quizzes_with_llm(
            llm,
            request.learner_profile,
            request.learning_document,
            request.single_choice_count,
            request.multiple_choice_count,
            request.true_false_count,
            request.short_answer_count,
            learning_goal=learning_goal,
        )
    except Exception as e:
        raise LLMError(
            f"Quiz generation failed: {str(e)}",
            details={"error": str(e)}
        )

    total_questions = (
        request.single_choice_count +
        request.multiple_choice_count +
        request.true_false_count +
        request.short_answer_count
    )

    return QuizResponse(
        success=True,
        message=f"Generated {total_questions} quiz questions successfully",
        document_quiz=document_quiz
    )


@router.post("/evaluate-performance", response_model=PerformanceEvaluationResponse, tags=["Assessment"])
async def evaluate_performance(
    request: PerformanceEvaluationRequest,
    llm_service: LLMService = Depends(get_llm_service),
    memory_service: MemoryService = Depends(get_memory_service)
):
    """Evaluate learner performance on a session.

    Args:
        request: Performance evaluation request
        llm_service: LLM service dependency
        memory_service: Memory service dependency

    Returns:
        Performance evaluation result

    Raises:
        LLMError: If evaluation fails
    """
    llm = llm_service.get_llm(request.model)

    learner_id = extract_learner_id(request.learner_profile)
    learning_goal = resolve_learning_goal(memory_service, learner_id, request.goal_id)

    learner_profile = parse_json_string(request.learner_profile, "learner_profile")
    learning_path = parse_json_string(request.learning_path, "learning_path")
    session_data = parse_json_string(request.session_data, "session_data")
    quiz_results = parse_json_string(request.quiz_results, "quiz_results") if request.quiz_results else None

    try:
        result = evaluate_learner_performance_with_llm(
            llm,
            learner_profile,
            learning_path,
            session_data,
            quiz_results,
            learning_goal=learning_goal,
        )
    except Exception as e:
        raise LLMError(
            f"Performance evaluation failed: {str(e)}",
            details={"error": str(e)}
        )

    return PerformanceEvaluationResponse(
        success=True,
        message="Performance evaluated successfully",
        evaluation=result
    )


@router.post("/evaluate-skill-mastery", response_model=SkillMasteryEvaluationResponse, tags=["Assessment"])
async def evaluate_skill_mastery(
    request: SkillMasteryEvaluationRequest,
    llm_service: LLMService = Depends(get_llm_service),
):
    """Evaluate mastery level of a specific skill.

    Args:
        request: Skill mastery evaluation request
        llm_service: LLM service dependency

    Returns:
        Skill mastery evaluation result

    Raises:
        LLMError: If evaluation fails
    """
    llm = llm_service.get_llm(request.model)

    learner_responses = parse_json_string(request.learner_responses, "learner_responses")
    quiz_results = parse_json_string(request.quiz_results, "quiz_results") if request.quiz_results else None
    previous_attempts = parse_json_string(request.previous_attempts, "previous_attempts") if request.previous_attempts else None

    try:
        result = evaluate_skill_mastery_with_llm(
            llm,
            request.skill_name,
            learner_responses,
            quiz_results,
            previous_attempts,
        )
    except Exception as e:
        raise LLMError(
            f"Skill mastery evaluation failed: {str(e)}",
            details={"error": str(e)}
        )

    return SkillMasteryEvaluationResponse(
        success=True,
        message="Skill mastery evaluated successfully",
        evaluation=result
    )


@router.post("/generate-performance-report", response_model=PerformanceReportResponse, tags=["Assessment"])
async def generate_performance_report(
    request: PerformanceReportRequest,
    llm_service: LLMService = Depends(get_llm_service),
    memory_service: MemoryService = Depends(get_memory_service)
):
    """Generate a performance report for a learner.

    Args:
        request: Performance report request
        llm_service: LLM service dependency
        memory_service: Memory service dependency

    Returns:
        Performance report

    Raises:
        LLMError: If report generation fails
    """
    llm = llm_service.get_llm(request.model)

    learner_id = extract_learner_id(request.learner_profile)
    learning_goal = resolve_learning_goal(memory_service, learner_id, request.goal_id)

    learner_profile = parse_json_string(request.learner_profile, "learner_profile")
    performance_history = parse_json_string(request.performance_history, "performance_history")

    # performance_history should be a list; wrap if dict
    if isinstance(performance_history, dict):
        performance_history = performance_history.get("history", [performance_history])

    try:
        result = generate_performance_report_with_llm(
            llm,
            learner_profile,
            performance_history,
            request.time_period,
            learning_goal=learning_goal,
        )
    except Exception as e:
        raise LLMError(
            f"Performance report generation failed: {str(e)}",
            details={"error": str(e)}
        )

    return PerformanceReportResponse(
        success=True,
        message="Performance report generated successfully",
        report=result
    )


@router.post("/simulate-feedback", response_model=FeedbackSimulationResponse, tags=["Assessment"])
async def simulate_feedback(
    request: FeedbackSimulationRequest,
    llm_service: LLMService = Depends(get_llm_service),
    memory_service: MemoryService = Depends(get_memory_service)
):
    """Simulate learner feedback on a learning path or content.

    Args:
        request: Feedback simulation request
        llm_service: LLM service dependency
        memory_service: Memory service dependency

    Returns:
        Simulated feedback

    Raises:
        ValidationError: If feedback_type is invalid
        LLMError: If simulation fails
    """
    if request.feedback_type not in ("path", "content"):
        raise ValidationError(
            "feedback_type must be 'path' or 'content'",
            details={"feedback_type": request.feedback_type}
        )

    llm = llm_service.get_llm(request.model)

    learner_id = extract_learner_id(request.learner_profile)
    learning_goal = resolve_learning_goal(memory_service, learner_id, request.goal_id)

    learner_profile = parse_json_string(request.learner_profile, "learner_profile")
    data = parse_json_string(request.data, "data")

    simulator = LearnerFeedbackSimulator(model=llm)

    try:
        if request.feedback_type == "path":
            payload = {
                "learner_profile": learner_profile,
                "learning_path": data,
                "learning_goal": learning_goal,
            }
            result = simulator.feedback_path(payload)
        else:
            payload = {
                "learner_profile": learner_profile,
                "learning_content": data,
                "learning_goal": learning_goal,
            }
            result = simulator.feedback_content(payload)
    except Exception as e:
        raise LLMError(
            f"Feedback simulation failed: {str(e)}",
            details={"error": str(e)}
        )

    return FeedbackSimulationResponse(
        success=True,
        message="Feedback simulated successfully",
        feedback=result
    )
