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

    # Get learning goals
    learning_goals = repository.get_learning_goals(learner_id) or {}

    # Get active goal info
    active_goal_id = learning_goals.get("active_goal_id")
    active_goal = None
    for g in learning_goals.get("goals", []):
        if g.get("goal_id") == active_goal_id:
            active_goal = g
            break

    # Get learning path (try goal-scoped first, fall back to flat)
    learning_path = repository.get_learning_path(learner_id) or {}
    if active_goal_id and active_goal_id in learning_path:
        goal_path_data = learning_path[active_goal_id]
        # Use the goal-scoped learning path sessions
        sessions_list = goal_path_data.get("learning_path", [])
        learning_path_for_display = {"sessions": sessions_list}
    else:
        learning_path_for_display = learning_path

    # Get mastery data
    mastery = repository.get_mastery(learner_id) or {}

    # Get recent history
    recent_history = repository.get_history(learner_id, limit=20)

    # Calculate progress
    total_sessions = len(learning_path_for_display.get("sessions", [])) if learning_path_for_display else 0
    completed_sessions = 0
    current_session = None

    if learning_path_for_display and "sessions" in learning_path_for_display:
        for session in learning_path_for_display["sessions"]:
            if session.get("completed"):
                completed_sessions += 1
            elif not current_session and not session.get("completed"):
                current_session = session

    progress_percent = (completed_sessions / total_sessions * 100) if total_sessions > 0 else 0

    # Build learner info
    learner_info = {
        "learner_id": learner_id,
        "name": profile.get("name", "Anonymous Learner"),
        "learning_goal": active_goal.get("learning_goal") if active_goal else None,
        "refined_goal": active_goal.get("refined_goal") if active_goal else None,
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
        learning_path=learning_path_for_display,
        recent_activity=recent_activity,
        mastery=mastery
    )
