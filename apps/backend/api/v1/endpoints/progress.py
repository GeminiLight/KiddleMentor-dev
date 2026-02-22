"""
Progress endpoints - track learning progress.
"""

from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException

from models import SessionCompleteRequest, SessionCompleteResponse
from repositories.learner_repository import LearnerRepository
from dependencies import get_learner_repository

router = APIRouter()


@router.post("/session-complete", response_model=SessionCompleteResponse, tags=["Progress"])
async def mark_session_complete(
    request: SessionCompleteRequest,
    repository: LearnerRepository = Depends(get_learner_repository)
):
    """Mark a learning session as complete.

    Updates progress, logs completion, and returns next session info.

    Args:
        request: Session completion request with learner_id
        repository: Learner repository dependency

    Returns:
        Session completion response with next session

    Raises:
        HTTPException: If learner_id not provided or profile/learning path not found
    """
    if not request.learner_id:
        raise HTTPException(
            status_code=400,
            detail="learner_id is required in request body"
        )

    return await _mark_session_complete_internal(request.learner_id, request, repository)


async def _mark_session_complete_internal(
    learner_id: str,
    request: SessionCompleteRequest,
    repository: LearnerRepository
) -> SessionCompleteResponse:
    """Internal helper for marking session complete.

    Args:
        learner_id: Learner identifier
        request: Session completion request
        repository: Learner repository dependency

    Returns:
        Session completion response

    Raises:
        HTTPException: If profile or learning path not found
    """
    # Check if profile exists
    profile = repository.get_profile(learner_id)
    if not profile:
        raise HTTPException(
            status_code=404,
            detail=f"Profile not found for learner {learner_id}"
        )

    # Get learning path
    learning_path = repository.get_learning_path(learner_id)
    if not learning_path:
        raise HTTPException(
            status_code=404,
            detail=f"Learning path not found for learner {learner_id}"
        )

    # Find and mark session as complete
    sessions = learning_path.get("sessions", [])
    session_found = False
    next_session = None
    completed_count = 0

    for i, session in enumerate(sessions):
        if session.get("session_number") == request.session_number:
            session["completed"] = True
            session["completed_at"] = datetime.now().isoformat()
            session["duration_minutes"] = request.duration_minutes
            session["quiz_score"] = request.quiz_score
            session_found = True

            # Get next session
            if i + 1 < len(sessions):
                next_session = sessions[i + 1]

        if session.get("completed"):
            completed_count += 1

    if not session_found:
        raise HTTPException(
            status_code=404,
            detail=f"Session {request.session_number} not found in learning path"
        )

    # Save updated learning path
    repository.save_learning_path(learner_id, learning_path)

    # Calculate progress
    total_sessions = len(sessions)
    progress_percent = (completed_count / total_sessions * 100) if total_sessions > 0 else 0

    # Update profile with progress
    profile["last_session_completed"] = request.session_number
    profile["progress_percent"] = round(progress_percent, 1)
    profile["updated_at"] = datetime.now().isoformat()
    repository.save_profile(learner_id, profile)

    # Log completion
    repository.log_interaction(
        learner_id,
        "system",
        f"Session {request.session_number} completed",
        metadata={
            "session_number": request.session_number,
            "duration_minutes": request.duration_minutes,
            "quiz_score": request.quiz_score,
            "timestamp": datetime.now().isoformat()
        }
    )

    # Update mastery if quiz score provided
    if request.quiz_score is not None:
        mastery = repository.get_mastery(learner_id) or {}
        session_topic = sessions[request.session_number - 1].get("topic", "unknown")

        # Simple mastery calculation (can be improved)
        current_mastery = mastery.get(session_topic, 0)
        new_mastery = (current_mastery + request.quiz_score) / 2

        mastery[session_topic] = round(new_mastery, 1)
        repository.save_mastery(learner_id, mastery)

        repository.append_mastery_entry(learner_id, {
            "session_number": request.session_number,
            "topic": session_topic,
            "quiz_score": request.quiz_score,
            "mastery_level": new_mastery,
            "timestamp": datetime.now().isoformat()
        })

    return SessionCompleteResponse(
        success=True,
        message=f"Session {request.session_number} marked as complete",
        session_number=request.session_number,
        next_session=next_session,
        progress_percent=round(progress_percent, 1)
    )
