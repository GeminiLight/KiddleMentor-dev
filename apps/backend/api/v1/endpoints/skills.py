"""
Skills endpoints - skill gap identification.
"""

import json
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from models import SkillGapIdentificationRequest, SkillGapResponse
from services.llm_service import get_llm_service, LLMService
from services.memory_service import get_memory_service, MemoryService
from gen_mentor.agents.learning.skill_gap_identifier import identify_skill_gap_with_llm
from gen_mentor.agents.learning.skill_mapper import map_goal_to_skills_with_llm as map_skill_requirements_with_llm
from exceptions import LLMError

router = APIRouter()


class IdentifyAndSaveSkillGapRequest(BaseModel):
    """Request for identifying skill gaps and saving to learner memory."""
    learner_id: str = Field(..., description="Learner identifier")
    learning_goal: str = Field(..., description="Learning goal")
    learner_information: str = Field(default="", description="Learner's background and experience")
    model: Optional[str] = Field(default=None, description="LLM model to use")


@router.post("/identify-skill-gap", response_model=SkillGapResponse, tags=["Skills"])
async def identify_skill_gap(
    request: SkillGapIdentificationRequest,
    llm_service: LLMService = Depends(get_llm_service)
):
    """Identify skill gaps from learner information.

    Analyzes learner profiles and identifies knowledge gaps relative
    to their learning goals.

    Args:
        request: Skill gap identification request
        llm_service: LLM service dependency

    Returns:
        Identified skill gaps and requirements

    Raises:
        ValidationError: If request validation fails
        LLMError: If skill gap identification fails
    """
    # Get LLM
    llm = llm_service.get_llm(request.model)

    # Parse skill requirements if provided
    skill_requirements = None
    if request.skill_requirements and request.skill_requirements.strip():
        try:
            skill_requirements = json.loads(request.skill_requirements)
            if not isinstance(skill_requirements, dict):
                skill_requirements = None
        except Exception:
            pass

    # Map skill requirements if not provided
    if skill_requirements is None:
        try:
            skill_requirements = map_skill_requirements_with_llm(llm, request.learning_goal)
        except Exception as e:
            raise LLMError(
                f"Skill requirement mapping failed: {str(e)}",
                details={"error": str(e)}
            )

    # Identify skill gaps
    try:
        skill_gaps, effective_requirements = identify_skill_gap_with_llm(
            llm,
            request.learning_goal,
            request.learner_information,
            skill_requirements
        )
    except Exception as e:
        raise LLMError(
            f"Skill gap identification failed: {str(e)}",
            details={"error": str(e)}
        )

    return SkillGapResponse(
        success=True,
        skill_requirements=effective_requirements,
        skill_gaps=skill_gaps,
        learning_goal=request.learning_goal
    )


@router.post("/identify-and-save-skill-gap", response_model=SkillGapResponse, tags=["Skills"])
async def identify_and_save_skill_gap(
    request: IdentifyAndSaveSkillGapRequest,
    llm_service: LLMService = Depends(get_llm_service),
    memory_service: MemoryService = Depends(get_memory_service),
):
    """Identify skill gaps and persist them to the learner's memory.

    Same as identify-skill-gap but also saves the result to memory
    keyed by the learner's active goal_id.

    Args:
        request: Request with learner_id, learning_goal, learner_information
        llm_service: LLM service dependency
        memory_service: Memory service dependency

    Returns:
        Identified skill gaps and requirements
    """
    llm = llm_service.get_llm(request.model)

    # Map skill requirements
    try:
        skill_requirements = map_skill_requirements_with_llm(llm, request.learning_goal)
    except Exception as e:
        raise LLMError(
            f"Skill requirement mapping failed: {str(e)}",
            details={"error": str(e)}
        )

    # Identify skill gaps
    try:
        skill_gaps, effective_requirements = identify_skill_gap_with_llm(
            llm,
            request.learning_goal,
            request.learner_information or "",
            skill_requirements
        )
    except Exception as e:
        raise LLMError(
            f"Skill gap identification failed: {str(e)}",
            details={"error": str(e)}
        )

    # Persist to memory keyed by active goal_id
    memory_store = memory_service.get_memory_store(request.learner_id)
    if memory_store:
        goal_id = memory_store.get_active_goal_id()
        if goal_id:
            memory_store.write_skill_gaps_for_goal(goal_id, {
                "skill_gaps": skill_gaps,
                "skill_requirements": effective_requirements,
            })

    return SkillGapResponse(
        success=True,
        skill_requirements=effective_requirements,
        skill_gaps=skill_gaps,
        learning_goal=request.learning_goal
    )
