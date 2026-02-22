"""
Profile endpoints - learner profile management.
"""

import json
import time
import uuid
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, Form
import shutil
import os

from models import (
    InitializeSessionRequest,
    InitializeSessionResponse,
    SetLearningGoalRequest,
    RefinedGoalResponse,
    LearnerProfileInitializationWithInfoRequest,
    LearnerProfileInitializationRequest,
    LearnerProfileUpdateRequest,
    LearnerProfileResponse,
    GetProfileRequest
)
from services.llm_service import get_llm_service, LLMService
from services.memory_service import get_memory_service, MemoryService
from repositories.learner_repository import LearnerRepository
from dependencies import get_learner_repository
from config import get_backend_settings, BackendSettings
from gen_mentor.agents.learning.learner_profiler import (
    initialize_learner_profile_with_llm,
    update_learner_profile_with_llm
)
from gen_mentor.agents.learning.goal_refiner import refine_learning_goal_with_llm
from gen_mentor.core.memory.memory_store import LearnerMemoryStore
from gen_mentor.utils.preprocess import extract_text_from_pdf
from dependencies import extract_learner_id
from exceptions import ValidationError, LLMError, StorageError

router = APIRouter()


# =============================================================================
# Session Management Endpoints
# =============================================================================

@router.post("/initialize-session", response_model=InitializeSessionResponse, tags=["Session"])
async def initialize_session(
    name: str = Form(None, description="Learner name (optional)"),
    email: str = Form(None, description="Learner email (optional)"),
    metadata: str = Form(None, description="JSON string of metadata (optional)"),
    cv: UploadFile = File(None, description="CV file (PDF)"),
    repository: LearnerRepository = Depends(get_learner_repository),
    settings: BackendSettings = Depends(get_backend_settings)
):
    """Initialize a new learner session.

    Creates a new learner with a unique ID and minimal initial profile.
    Frontend should save the learner_id for all subsequent requests.

    Args:
        name: Learner name
        email: Learner email
        metadata: JSON string of metadata
        cv: CV file (PDF)
        repository: Learner repository dependency
        settings: Backend settings dependency

    Returns:
        Session with learner_id and initial profile
    """
    # Generate unique learner ID
    learner_id = f"learner_{uuid.uuid4().hex[:12]}"

    # Parse metadata
    parsed_metadata = {}
    if metadata:
        try:
            parsed_metadata = json.loads(metadata)
        except Exception:
            pass

    # Handle CV upload
    cv_path = None
    if cv:
        try:
            # Create upload directory if it doesn't exist
            upload_dir = settings.expanded_upload_location
            upload_dir.mkdir(parents=True, exist_ok=True)
            
            # Generate unique filename
            file_ext = os.path.splitext(cv.filename)[1] if cv.filename else ".pdf"
            filename = f"{learner_id}_cv{file_ext}"
            file_path = upload_dir / filename
            
            # Save file
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(cv.file, buffer)
                
            cv_path = str(file_path)
            parsed_metadata["cv_path"] = cv_path
            
            # Extract text from CV and add to metadata
            try:
                cv_text = extract_text_from_pdf(str(file_path))
                parsed_metadata["cv_text"] = cv_text
            except Exception as e:
                print(f"Failed to extract text from CV: {e}")
                
        except Exception as e:
            raise StorageError(
                f"Failed to save CV file: {str(e)}",
                details={"error": str(e)}
            )

    # Create initial profile
    profile = {
        "learner_id": learner_id,
        "name": name or "Anonymous Learner",
        "email": email,
        "created_at": datetime.now().isoformat(),
        "metadata": parsed_metadata
    }

    # Save to repository
    repository.save_profile(learner_id, profile)

    # Log session initialization
    repository.log_interaction(
        learner_id,
        "system",
        "Session initialized",
        metadata={"timestamp": datetime.now().isoformat()}
    )

    return InitializeSessionResponse(
        success=True,
        message="Session initialized successfully",
        learner_id=learner_id,
        profile=profile
    )


@router.post("/get-profile", response_model=LearnerProfileResponse, tags=["Profile"])
async def get_learner_profile_with_body(
    request: GetProfileRequest,
    repository: LearnerRepository = Depends(get_learner_repository)
):
    """Get learner profile by ID.

    Args:
        request: Profile request with learner_id
        repository: Learner repository dependency

    Returns:
        Learner profile

    Raises:
        HTTPException: If profile not found
    """
    profile = repository.get_profile(request.learner_id)

    if not profile:
        raise HTTPException(
            status_code=404,
            detail=f"Profile not found for learner {request.learner_id}"
        )

    return LearnerProfileResponse(
        success=True,
        message="Profile retrieved successfully",
        learner_profile=profile
    )


@router.post("/set-goal", response_model=RefinedGoalResponse, tags=["Profile"])
async def set_learning_goal(
    request: SetLearningGoalRequest,
    llm_service: LLMService = Depends(get_llm_service),
    repository: LearnerRepository = Depends(get_learner_repository)
):
    """Set and refine learning goal for learner.

    Automatically refines the goal using AI and saves to profile.

    Args:
        request: Learning goal request with learner_id
        llm_service: LLM service dependency
        repository: Learner repository dependency

    Returns:
        Refined learning goal

    Raises:
        HTTPException: If learner_id not provided or profile not found
        LLMError: If goal refinement fails
    """
    if not request.learner_id:
        raise HTTPException(
            status_code=400,
            detail="learner_id is required in request body"
        )

    learner_id = request.learner_id

    # Check if profile exists
    profile = repository.get_profile(learner_id)
    if not profile:
        raise HTTPException(
            status_code=404,
            detail=f"Profile not found for learner {learner_id}"
        )

    # Get LLM
    llm = llm_service.get_llm(request.model)

    # Refine goal
    try:
        # Convert metadata dict to string for the agent
        metadata = profile.get("metadata", {})
        learner_info_str = json.dumps(metadata) if metadata else ""

        refined_goal = refine_learning_goal_with_llm(
            llm,
            request.learning_goal,
            learner_information=learner_info_str
        )
    except Exception as e:
        raise LLMError(
            f"Goal refinement failed: {str(e)}",
            details={"error": str(e)}
        )

    # Update profile timestamp (no goal fields in profile)
    profile["updated_at"] = datetime.now().isoformat()
    repository.save_profile(learner_id, profile)

    # Save to learning_goal.json via memory store
    memory_store = LearnerMemoryStore(
        workspace=str(repository.workspace),
        learner_id=learner_id
    )
    goal_id = memory_store.add_goal(request.learning_goal, refined_goal)

    # Log goal setting
    repository.log_interaction(
        learner_id,
        "system",
        f"Learning goal set: {request.learning_goal}",
        metadata={"refined_goal": refined_goal, "goal_id": goal_id}
    )

    return RefinedGoalResponse(
        success=True,
        message="Learning goal set and refined successfully",
        refined_goal=refined_goal,
        rationale=refined_goal.get("rationale") if isinstance(refined_goal, dict) else None
    )


# =============================================================================
# Profile Management Endpoints
# =============================================================================


@router.post("/create-learner-profile", response_model=LearnerProfileResponse, tags=["Profile"])
async def create_learner_profile(
    request: LearnerProfileInitializationWithInfoRequest,
    llm_service: LLMService = Depends(get_llm_service),
    memory_service: MemoryService = Depends(get_memory_service)
):
    """Create learner profile from information.

    Initializes a detailed learner profile based on provided information,
    learning goals, and identified skill gaps.

    Args:
        request: Profile initialization request
        llm_service: LLM service dependency
        memory_service: Memory service dependency

    Returns:
        Created learner profile

    Raises:
        ValidationError: If request validation fails
        LLMError: If profile creation fails
    """
    # Get LLM
    llm = llm_service.get_llm(request.model)

    # Parse learner information
    learner_information = request.learner_information
    if isinstance(learner_information, str):
        try:
            learner_information = json.loads(learner_information)
        except Exception:
            learner_information = {"raw": learner_information}

    # Parse skill gaps
    skill_gaps = request.skill_gaps
    if isinstance(skill_gaps, str):
        try:
            skill_gaps = json.loads(skill_gaps)
        except Exception:
            skill_gaps = {"raw": skill_gaps}

    # Initialize profile
    try:
        learner_profile = initialize_learner_profile_with_llm(
            llm,
            request.learning_goal,
            learner_information,
            skill_gaps
        )
    except Exception as e:
        raise LLMError(
            f"Profile initialization failed: {str(e)}",
            details={"error": str(e)}
        )

    # Persist profile to workspace memory
    learner_id = learner_profile.get("learner_id") if isinstance(learner_profile, dict) else None
    memory_service.save_profile(learner_id, learner_profile)

    # Save goal to learning_goal.json and skill_gaps to skill_gaps.json
    if learner_id:
        memory_store = memory_service.get_memory_store(learner_id)
        if memory_store:
            goal_id = memory_store.add_goal(request.learning_goal)
            memory_store.write_skill_gaps_for_goal(goal_id, {"skill_gaps": skill_gaps})

    memory_service.log_interaction(
        learner_id,
        "system",
        f"Profile initialized - Goal: {request.learning_goal}",
        metadata={"timestamp": time.strftime('%Y-%m-%d %H:%M:%S')}
    )

    return LearnerProfileResponse(
        success=True,
        message="Learner profile created successfully",
        learner_profile=learner_profile
    )


@router.post("/create-learner-profile-with-cv-pdf", response_model=LearnerProfileResponse, tags=["Profile"])
async def create_learner_profile_with_cv_pdf(
    request: LearnerProfileInitializationRequest,
    llm_service: LLMService = Depends(get_llm_service),
    memory_service: MemoryService = Depends(get_memory_service),
    settings: BackendSettings = Depends(get_backend_settings)
):
    """Create learner profile from CV PDF file.

    Initializes a learner profile by extracting information from an uploaded CV PDF file.

    Args:
        request: Profile initialization request with CV path
        llm_service: LLM service dependency
        memory_service: Memory service dependency
        settings: Backend settings dependency

    Returns:
        Created learner profile

    Raises:
        ValidationError: If request validation fails
        StorageError: If file operations fail
        LLMError: If profile creation fails
    """
    # Get LLM
    llm = llm_service.get_llm(request.model)

    # Get file location
    file_location = settings.expanded_upload_location / request.cv_path

    # Extract text from PDF
    try:
        learner_information = extract_text_from_pdf(str(file_location))
    except Exception as e:
        raise StorageError(
            f"Failed to extract text from CV: {str(e)}",
            details={"cv_path": request.cv_path, "error": str(e)}
        )

    # Parse skill gaps
    skill_gaps = request.skill_gaps
    if isinstance(skill_gaps, str):
        try:
            skill_gaps = json.loads(skill_gaps)
        except Exception:
            skill_gaps = {"raw": skill_gaps}

    # Initialize profile
    try:
        learner_profile = initialize_learner_profile_with_llm(
            llm,
            request.learning_goal,
            {"raw": learner_information},
            skill_gaps
        )
    except Exception as e:
        raise LLMError(
            f"Profile initialization failed: {str(e)}",
            details={"error": str(e)}
        )

    # Persist profile to workspace memory
    learner_id = learner_profile.get("learner_id") if isinstance(learner_profile, dict) else None
    memory_service.save_profile(learner_id, learner_profile)

    # Save goal to learning_goal.json and skill_gaps to skill_gaps.json
    if learner_id:
        memory_store = memory_service.get_memory_store(learner_id)
        if memory_store:
            goal_id = memory_store.add_goal(request.learning_goal)
            memory_store.write_skill_gaps_for_goal(goal_id, {"skill_gaps": skill_gaps})

    memory_service.log_interaction(
        learner_id,
        "system",
        f"Profile initialized from CV - Goal: {request.learning_goal}",
        metadata={"cv_path": request.cv_path, "timestamp": time.strftime('%Y-%m-%d %H:%M:%S')}
    )

    return LearnerProfileResponse(
        success=True,
        message="Learner profile created from CV successfully",
        learner_profile=learner_profile
    )


@router.post("/update-learner-profile", response_model=LearnerProfileResponse, tags=["Profile"])
async def update_learner_profile(
    request: LearnerProfileUpdateRequest,
    llm_service: LLMService = Depends(get_llm_service),
    memory_service: MemoryService = Depends(get_memory_service)
):
    """Update learner profile.

    Updates an existing learner profile based on new interactions and information.

    Args:
        request: Profile update request
        llm_service: LLM service dependency
        memory_service: Memory service dependency

    Returns:
        Updated learner profile

    Raises:
        ValidationError: If request validation fails
        LLMError: If profile update fails
    """
    # Get LLM
    llm = llm_service.get_llm(request.model)

    # Parse all inputs
    learner_profile = request.learner_profile
    learner_interactions = request.learner_interactions
    learner_information = request.learner_information
    session_information = request.session_information

    for name, val in [
        ("learner_profile", learner_profile),
        ("learner_interactions", learner_interactions),
        ("learner_information", learner_information),
        ("session_information", session_information)
    ]:
        if isinstance(val, str) and val.strip():
            try:
                locals()[name] = json.loads(val)
            except Exception:
                if name != "session_information":
                    locals()[name] = {"raw": val}

    # Extract learner_id before update
    learner_id = None
    if isinstance(locals()["learner_profile"], dict):
        learner_id = locals()["learner_profile"].get("learner_id")

    # Load existing profile from memory if not fully provided
    if learner_id and not locals()["learner_profile"]:
        stored_profile = memory_service.load_profile_from_memory(learner_id)
        if stored_profile:
            locals()["learner_profile"] = stored_profile

    # Get memory store for agent
    memory_store = memory_service.get_memory_store(learner_id) if learner_id else None

    # Update profile
    try:
        updated_profile = update_learner_profile_with_llm(
            llm,
            locals()["learner_profile"],
            locals()["learner_interactions"],
            locals()["learner_information"],
            locals()["session_information"]
        )
    except Exception as e:
        raise LLMError(
            f"Profile update failed: {str(e)}",
            details={"error": str(e)}
        )

    # Persist updated profile
    memory_service.save_profile(learner_id, updated_profile)
    memory_service.log_interaction(
        learner_id,
        "system",
        f"Profile updated",
        metadata={"session": locals()["session_information"]}
    )

    return LearnerProfileResponse(
        success=True,
        message="Learner profile updated successfully",
        learner_profile=updated_profile
    )
