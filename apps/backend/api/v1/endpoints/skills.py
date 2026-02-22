"""
Skills endpoints - skill gap identification.
"""

import ast
import json
from pathlib import Path
from fastapi import APIRouter, Depends, File, UploadFile, Form

from models import SkillGapIdentificationRequest, SkillGapResponse
from services.llm_service import get_llm_service, LLMService
from services.memory_service import get_memory_service, MemoryService
from config import get_backend_settings, BackendSettings
from gen_mentor.agents.learning.skill_gap_identifier import identify_skill_gap_with_llm
from gen_mentor.agents.learning.skill_mapper import map_goal_to_skills_with_llm as map_skill_requirements_with_llm
from gen_mentor.utils.preprocess import extract_text_from_pdf
from exceptions import ValidationError, LLMError, StorageError

router = APIRouter()


@router.post("/identify-skill-gap-with-info", response_model=SkillGapResponse, tags=["Skills"])
async def identify_skill_gap_with_info(
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
        skill_gaps = identify_skill_gap_with_llm(
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
        skill_requirements=skill_requirements,
        skill_gaps=skill_gaps,
        learning_goal=request.learning_goal
    )


@router.post("/identify-skill-gap", response_model=SkillGapResponse, tags=["Skills"])
async def identify_skill_gap(
    goal: str = Form(..., description="Learning goal"),
    cv: UploadFile = File(..., description="CV file (PDF)"),
    model: str = Form("openai/gpt-5.1", description="Model in 'provider/model' format"),
    llm_service: LLMService = Depends(get_llm_service),
    settings: BackendSettings = Depends(get_backend_settings)
):
    """Identify skill gap from uploaded CV.

    Extracts text from CV file and identifies skill gaps relative to the learning goal.

    Args:
        goal: Learning goal
        cv: Uploaded CV file
        model: Model in 'provider/model' format
        llm_service: LLM service dependency
        settings: Backend settings dependency

    Returns:
        Identified skill gaps and requirements

    Raises:
        ValidationError: If request validation fails
        StorageError: If file operations fail
        LLMError: If skill gap identification fails
    """
    # Get LLM
    llm = llm_service.get_llm(model)

    # Validate file type
    if not cv.filename or not cv.filename.lower().endswith('.pdf'):
        raise ValidationError(
            "Only PDF files are allowed",
            details={"filename": cv.filename, "content_type": cv.content_type}
        )

    # Validate file size (10MB limit)
    content = await cv.read()
    if len(content) > 10 * 1024 * 1024:
        raise ValidationError(
            "File size exceeds 10MB limit",
            details={"filename": cv.filename, "size": len(content)}
        )

    # Sanitize filename to prevent path traversal
    safe_filename = Path(cv.filename).name

    # Save uploaded file
    try:
        import os
        os.makedirs(settings.expanded_upload_location, exist_ok=True)
        file_location = settings.expanded_upload_location / safe_filename

        with open(file_location, "wb") as f:
            f.write(content)
    except Exception as e:
        raise StorageError(
            f"Failed to save uploaded file: {str(e)}",
            details={"filename": safe_filename, "error": str(e)}
        )

    # Extract text from PDF
    try:
        cv_text = extract_text_from_pdf(str(file_location))
    except Exception as e:
        raise StorageError(
            f"Failed to extract text from PDF: {str(e)}",
            details={"filename": cv.filename, "error": str(e)}
        )

    # Map skill requirements
    try:
        skill_requirements = map_skill_requirements_with_llm(llm, goal)
    except Exception as e:
        raise LLMError(
            f"Skill requirement mapping failed: {str(e)}",
            details={"error": str(e)}
        )

    # Identify skill gaps
    try:
        skill_gaps = identify_skill_gap_with_llm(
            llm,
            goal,
            cv_text,
            skill_requirements
        )
    except Exception as e:
        raise LLMError(
            f"Skill gap identification failed: {str(e)}",
            details={"error": str(e)}
        )

    return SkillGapResponse(
        success=True,
        skill_requirements=skill_requirements,
        skill_gaps=skill_gaps,
        learning_goal=goal
    )
