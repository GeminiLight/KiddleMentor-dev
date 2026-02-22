"""
Assessment endpoints - quiz generation.
"""

from fastapi import APIRouter, Depends

from models import KnowledgeQuizGenerationRequest, QuizResponse
from services.llm_service import get_llm_service, LLMService
from gen_mentor.agents.assessment.quiz_generator import generate_document_quizzes_with_llm
from exceptions import LLMError

router = APIRouter()


@router.post("/generate-document-quizzes", response_model=QuizResponse, tags=["Assessment"])
async def generate_document_quizzes(
    request: KnowledgeQuizGenerationRequest,
    llm_service: LLMService = Depends(get_llm_service)
):
    """Generate quizzes from learning document.

    Creates personalized assessments to test understanding of the learning material.

    Args:
        request: Quiz generation request
        llm_service: LLM service dependency

    Returns:
        Generated quizzes

    Raises:
        LLMError: If quiz generation fails
    """
    # Get LLM
    llm = llm_service.get_llm()

    # Generate quizzes
    try:
        document_quiz = generate_document_quizzes_with_llm(
            llm,
            request.learner_profile,
            request.learning_document,
            request.single_choice_count,
            request.multiple_choice_count,
            request.true_false_count,
            request.short_answer_count
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
