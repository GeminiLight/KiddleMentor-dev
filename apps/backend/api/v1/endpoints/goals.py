"""
Goals endpoints - learning goal refinement.
"""

from fastapi import APIRouter, Depends

from models import LearningGoalRefinementRequest, RefinedGoalResponse
from services.llm_service import get_llm_service, LLMService
from gen_mentor.agents.learning.goal_refiner import refine_learning_goal_with_llm
from exceptions import ValidationError, LLMError

router = APIRouter()


@router.post("/refine-learning-goal", tags=["Goals"])
async def refine_learning_goal(
    request: LearningGoalRefinementRequest,
    llm_service: LLMService = Depends(get_llm_service)
):
    """Refine learning goal.

    Helps learners define and refine their educational objectives
    based on their background and interests.

    Args:
        request: Goal refinement request
        llm_service: LLM service dependency

    Returns:
        Refined learning goal

    Raises:
        ValidationError: If request validation fails
        LLMError: If goal refinement fails
    """
    if not request.learning_goal or not request.learning_goal.strip():
        raise ValidationError(
            "learning_goal cannot be empty",
            details={"field": "learning_goal"}
        )

    # Get LLM
    llm = llm_service.get_llm(request.model)

    # Refine goal
    try:
        refined_goal = refine_learning_goal_with_llm(
            llm,
            request.learning_goal,
            request.learner_information
        )
    except Exception as e:
        raise LLMError(
            f"Goal refinement failed: {str(e)}",
            details={"error": str(e)}
        )

    return RefinedGoalResponse(
        success=True,
        message="Learning goal refined successfully",
        refined_goal=refined_goal,
        rationale=refined_goal.get("rationale", "")
    )
