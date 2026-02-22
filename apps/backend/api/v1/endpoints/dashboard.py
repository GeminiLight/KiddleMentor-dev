"""
Dashboard endpoints - complete learner state.
"""

from fastapi import APIRouter, Depends, HTTPException

from models import DashboardResponse, GetDashboardRequest
from repositories.learner_repository import LearnerRepository
from dependencies import get_learner_repository

router = APIRouter()


@router.post("", response_model=DashboardResponse, tags=["Dashboard"])
async def get_dashboard(
    request: GetDashboardRequest,
    repository: LearnerRepository = Depends(get_learner_repository)
):
    """Get complete dashboard state for learner.

    Returns all information needed to display the learning dashboard:
    - Learner profile and progress
    - Current session
    - Learning path
    - Recent activity
    - Skill mastery

    Args:
        request: Dashboard request with learner_id
        repository: Learner repository dependency

    Returns:
        Complete dashboard data

    Raises:
        HTTPException: If profile not found
    """
    return await _get_dashboard_internal(request.learner_id, repository)


async def _get_dashboard_internal(
    learner_id: str,
    repository: LearnerRepository
) -> DashboardResponse:
    """Internal helper for getting dashboard data.

    Args:
        learner_id: Learner identifier
        repository: Learner repository dependency

    Returns:
        Complete dashboard data

    Raises:
        HTTPException: If profile not found
    """
    # Get profile
    profile = repository.get_profile(learner_id)
    if not profile:
        raise HTTPException(
            status_code=404,
            detail=f"Profile not found for learner {learner_id}"
        )

    # Get objectives
    objectives = repository.get_objectives(learner_id) or {}

    # Get learning path
    learning_path = repository.get_learning_path(learner_id) or {}

    # Get mastery data
    mastery = repository.get_mastery(learner_id) or {}

    # Get recent history
    recent_history = repository.get_history(learner_id, limit=20)

    # Calculate progress
    total_sessions = len(learning_path.get("sessions", [])) if learning_path else 0
    completed_sessions = 0
    current_session = None

    if learning_path and "sessions" in learning_path:
        for session in learning_path["sessions"]:
            if session.get("completed"):
                completed_sessions += 1
            elif not current_session and not session.get("completed"):
                current_session = session

    progress_percent = (completed_sessions / total_sessions * 100) if total_sessions > 0 else 0

    # Build learner info
    learner_info = {
        "learner_id": learner_id,
        "name": profile.get("name", "Anonymous Learner"),
        "learning_goal": profile.get("learning_goal") or objectives.get("learning_goal"),
        "refined_goal": profile.get("refined_goal") or objectives.get("refined_goal"),
        "progress": round(progress_percent, 1),
        "total_sessions": total_sessions,
        "completed_sessions": completed_sessions,
        "created_at": profile.get("created_at"),
        "updated_at": profile.get("updated_at")
    }

    # Build recent activity from history
    recent_activity = []
    for entry in recent_history[-10:]:  # Last 10 entries
        activity = {
            "type": entry.get("role", "system"),
            "content": entry.get("content", "")[:100],  # Truncate for dashboard
            "timestamp": entry.get("timestamp"),
            "metadata": entry.get("metadata", {})
        }
        recent_activity.append(activity)

    return DashboardResponse(
        success=True,
        message="Dashboard data retrieved successfully",
        learner=learner_info,
        current_session=current_session,
        learning_path=learning_path,
        recent_activity=recent_activity,
        mastery=mastery
    )
