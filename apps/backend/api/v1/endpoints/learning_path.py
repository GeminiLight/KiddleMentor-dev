"""
Learning path endpoints - path scheduling and content generation.
"""

import json
import time
from fastapi import APIRouter, Depends

from models import (
    LearningPathSchedulingRequest,
    LearningPathReschedulingRequest,
    LearningPathResponse,
    KnowledgePointExplorationRequest,
    KnowledgePointsResponse,
    KnowledgePointDraftingRequest,
    KnowledgeDraftResponse,
    KnowledgePointsDraftingRequest,
    KnowledgeDraftsResponse,
    LearningDocumentIntegrationRequest,
    LearningDocumentResponse,
    TailoredContentGenerationRequest,
    TailoredContentResponse,
)
from services.llm_service import get_llm_service, LLMService
from services.memory_service import get_memory_service, MemoryService
from gen_mentor.agents.content.path_scheduler import (
    schedule_learning_path_with_llm,
    reschedule_learning_path_with_llm
)
from gen_mentor.agents.content.knowledge_explorer import explore_knowledge_points_with_llm
from gen_mentor.agents.content.knowledge_drafter import draft_knowledge_point_with_llm
from gen_mentor.agents.content.document_integrator import integrate_learning_document_with_llm
from gen_mentor.agents.content.content_creator import create_learning_content_with_llm
from dependencies import extract_learner_id, resolve_learning_goal
from exceptions import ValidationError, LLMError

router = APIRouter()


# =============================================================================
# Learning Path Scheduling
# =============================================================================

@router.post("/schedule-learning-path", response_model=LearningPathResponse, tags=["Learning Path"])
async def schedule_learning_path(
    request: LearningPathSchedulingRequest,
    llm_service: LLMService = Depends(get_llm_service),
    memory_service: MemoryService = Depends(get_memory_service)
):
    """Schedule learning path.

    Creates a structured learning sequence with session planning based on
    the learner's profile and goals.

    Args:
        request: Learning path scheduling request
        llm_service: LLM service dependency
        memory_service: Memory service dependency

    Returns:
        Scheduled learning path

    Raises:
        ValidationError: If request validation fails
        LLMError: If path scheduling fails
    """
    # Get LLM
    llm = llm_service.get_llm(request.model)

    # Parse learner profile
    learner_profile = request.learner_profile
    if isinstance(learner_profile, str) and learner_profile.strip():
        learner_profile = json.loads(learner_profile)
    if not isinstance(learner_profile, dict):
        learner_profile = {}

    # Extract learner_id
    learner_id = learner_profile.get("learner_id")

    # Load learner profile from memory if not fully provided
    if learner_id:
        stored_profile = memory_service.load_profile_from_memory(learner_id, learner_profile)
        if stored_profile and isinstance(stored_profile, dict):
            learner_profile.update({k: v for k, v in stored_profile.items() if k not in learner_profile})

    # Get memory store for agent
    memory_store = memory_service.get_memory_store(learner_id) if learner_id else None

    # Enrich learner_profile with active goal and skill gaps from memory
    if memory_store:
        active_goal = memory_store.get_active_goal()
        if active_goal:
            goal_id = active_goal.get("goal_id")
            learner_profile["refined_goal"] = active_goal.get("refined_goal")
            if goal_id:
                skill_gaps_data = memory_store.read_skill_gaps_for_goal(goal_id)
                if skill_gaps_data:
                    learner_profile["skill_gaps"] = skill_gaps_data

    # Resolve learning goal separately
    learning_goal = resolve_learning_goal(memory_service, learner_id, request.goal_id)

    # Schedule learning path with memory context
    try:
        learning_path = schedule_learning_path_with_llm(
            llm,
            learner_profile,
            request.session_count,
            learning_goal=learning_goal,
        )
    except Exception as e:
        raise LLMError(
            f"Learning path scheduling failed: {str(e)}",
            details={"error": str(e)}
        )

    # Persist learning path (keyed by active goal_id)
    if memory_store:
        goal_id = memory_store.get_active_goal_id()
        if goal_id:
            memory_store.write_learning_path_for_goal(goal_id, {
                "learning_path": learning_path,
                "session_count": request.session_count,
            })
        else:
            memory_service.save_learning_path(learner_id, learning_path)
    else:
        memory_service.save_learning_path(learner_id, learning_path)
    memory_service.log_interaction(
        learner_id,
        "system",
        f"Learning path scheduled with {request.session_count} sessions",
        metadata={"timestamp": time.strftime('%Y-%m-%d %H:%M:%S')}
    )

    return LearningPathResponse(
        success=True,
        message="Learning path scheduled successfully",
        learning_path=learning_path,
        session_count=request.session_count
    )


@router.post("/reschedule-learning-path", response_model=LearningPathResponse, tags=["Learning Path"])
async def reschedule_learning_path(
    request: LearningPathReschedulingRequest,
    llm_service: LLMService = Depends(get_llm_service),
    memory_service: MemoryService = Depends(get_memory_service)
):
    """Reschedule learning path.

    Updates an existing learning path based on feedback and progress.

    Args:
        request: Learning path rescheduling request
        llm_service: LLM service dependency
        memory_service: Memory service dependency

    Returns:
        Rescheduled learning path

    Raises:
        ValidationError: If request validation fails
        LLMError: If path rescheduling fails
    """
    # Get LLM
    llm = llm_service.get_llm(request.model)

    # Parse inputs
    learner_profile = request.learner_profile
    learning_path = request.learning_path
    other_feedback = request.other_feedback

    if isinstance(learner_profile, str) and learner_profile.strip():
        learner_profile = json.loads(learner_profile)
    if not isinstance(learner_profile, dict):
        learner_profile = {}

    if isinstance(learning_path, str) and learning_path.strip():
        learning_path = json.loads(learning_path)

    # Unwrap nested learning_path structure: {learning_path: [...]} -> [...]
    if isinstance(learning_path, dict) and "learning_path" in learning_path:
        learning_path = learning_path["learning_path"]

    if isinstance(other_feedback, str) and other_feedback.strip():
        try:
            other_feedback = json.loads(other_feedback)
        except Exception:
            pass

    # Extract learner_id
    learner_id = learner_profile.get("learner_id")

    # Enrich learner_profile with active goal and skill gaps from memory
    memory_store = memory_service.get_memory_store(learner_id) if learner_id else None
    if memory_store:
        active_goal = memory_store.get_active_goal()
        if active_goal:
            goal_id = active_goal.get("goal_id")
            learner_profile.setdefault("refined_goal", active_goal.get("refined_goal"))
            if goal_id:
                skill_gaps_data = memory_store.read_skill_gaps_for_goal(goal_id)
                if skill_gaps_data:
                    learner_profile.setdefault("skill_gaps", skill_gaps_data)

    # Resolve learning goal separately
    learning_goal = resolve_learning_goal(memory_service, learner_id, request.goal_id)

    # Reschedule learning path
    try:
        new_learning_path = reschedule_learning_path_with_llm(
            llm,
            learning_path,
            learner_profile,
            request.session_count,
            other_feedback,
            learning_goal=learning_goal,
        )
    except Exception as e:
        raise LLMError(
            f"Learning path rescheduling failed: {str(e)}",
            details={"error": str(e)}
        )

    # Persist rescheduled path (keyed by active goal_id)
    if not memory_store:
        memory_store = memory_service.get_memory_store(learner_id)
    if memory_store:
        goal_id = memory_store.get_active_goal_id()
        if goal_id:
            existing_path_data = memory_store.read_learning_path_for_goal(goal_id)
            session_count = request.session_count if request.session_count > 0 else existing_path_data.get("session_count", 0)
            memory_store.write_learning_path_for_goal(goal_id, {
                "learning_path": new_learning_path,
                "session_count": session_count,
            })
        else:
            memory_service.save_learning_path(learner_id, new_learning_path)
            session_count = request.session_count
    else:
        memory_service.save_learning_path(learner_id, new_learning_path)
        session_count = request.session_count

    memory_service.log_interaction(
        learner_id,
        "system",
        f"Learning path rescheduled",
        metadata={"feedback": other_feedback}
    )

    return LearningPathResponse(
        success=True,
        message="Learning path rescheduled successfully",
        learning_path=new_learning_path,
        session_count=session_count
    )


# =============================================================================
# Knowledge Point Exploration and Drafting
# =============================================================================

@router.post("/explore-knowledge-points", response_model=KnowledgePointsResponse, tags=["Content"])
async def explore_knowledge_points(
    request: KnowledgePointExplorationRequest,
    llm_service: LLMService = Depends(get_llm_service),
    memory_service: MemoryService = Depends(get_memory_service)
):
    """Explore knowledge points.

    Deep-dives into specific topics with multiple perspectives for a learning session.

    Args:
        request: Knowledge point exploration request
        llm_service: LLM service dependency
        memory_service: Memory service dependency

    Returns:
        Explored knowledge points

    Raises:
        ValidationError: If request validation fails
        LLMError: If exploration fails
    """
    # Get LLM
    llm = llm_service.get_llm()

    # Parse inputs
    learner_profile = json.loads(request.learner_profile) if isinstance(request.learner_profile, str) else request.learner_profile
    learning_path = json.loads(request.learning_path) if isinstance(request.learning_path, str) else request.learning_path
    learning_session = json.loads(request.learning_session) if isinstance(request.learning_session, str) else request.learning_session

    # Resolve learning goal
    learner_id = extract_learner_id(request.learner_profile)
    learning_goal = resolve_learning_goal(memory_service, learner_id, request.goal_id)

    # Explore knowledge points
    try:
        knowledge_points = explore_knowledge_points_with_llm(
            llm,
            learner_profile,
            learning_path,
            learning_session,
            learning_goal=learning_goal,
        )
    except Exception as e:
        raise LLMError(
            f"Knowledge point exploration failed: {str(e)}",
            details={"error": str(e)}
        )

    return KnowledgePointsResponse(
        success=True,
        message="Knowledge points explored successfully",
        knowledge_points=knowledge_points
    )


@router.post("/draft-knowledge-point", response_model=KnowledgeDraftResponse, tags=["Content"])
async def draft_knowledge_point(
    request: KnowledgePointDraftingRequest,
    llm_service: LLMService = Depends(get_llm_service),
    memory_service: MemoryService = Depends(get_memory_service)
):
    """Draft a single knowledge point.

    Creates detailed content for a specific knowledge point.

    Args:
        request: Knowledge point drafting request
        llm_service: LLM service dependency
        memory_service: Memory service dependency

    Returns:
        Drafted knowledge point

    Raises:
        ValidationError: If request validation fails
        LLMError: If drafting fails
    """
    # Get LLM
    llm = llm_service.get_llm()

    # Resolve learning goal
    learner_id = extract_learner_id(request.learner_profile)
    learning_goal = resolve_learning_goal(memory_service, learner_id, request.goal_id)

    # Draft knowledge point
    try:
        knowledge_draft = draft_knowledge_point_with_llm(
            llm,
            request.learner_profile,
            request.learning_path,
            request.learning_session,
            request.knowledge_points,
            request.knowledge_point,
            request.use_search,
            learning_goal=learning_goal,
        )
    except Exception as e:
        raise LLMError(
            f"Knowledge point drafting failed: {str(e)}",
            details={"error": str(e)}
        )

    return KnowledgeDraftResponse(
        success=True,
        message="Knowledge point drafted successfully",
        knowledge_draft=knowledge_draft
    )


@router.post("/draft-knowledge-points", response_model=KnowledgeDraftsResponse, tags=["Content"])
async def draft_knowledge_points(
    request: KnowledgePointsDraftingRequest,
    llm_service: LLMService = Depends(get_llm_service),
    memory_service: MemoryService = Depends(get_memory_service)
):
    """Draft multiple knowledge points.

    Creates detailed content for multiple knowledge points.

    Args:
        request: Knowledge points drafting request
        llm_service: LLM service dependency
        memory_service: Memory service dependency

    Returns:
        Drafted knowledge points

    Raises:
        ValidationError: If request validation fails
        LLMError: If drafting fails
    """
    # Get LLM
    llm = llm_service.get_llm()

    # Parse knowledge points
    knowledge_points = json.loads(request.knowledge_points) if isinstance(request.knowledge_points, str) else request.knowledge_points

    # Resolve learning goal
    learner_id = extract_learner_id(request.learner_profile)
    learning_goal = resolve_learning_goal(memory_service, learner_id, request.goal_id)

    # Draft all knowledge points
    try:
        knowledge_drafts = []
        for kp in knowledge_points:
            draft = draft_knowledge_point_with_llm(
                llm,
                request.learner_profile,
                request.learning_path,
                request.learning_session,
                knowledge_points,
                kp,
                request.use_search,
                learning_goal=learning_goal,
            )
            knowledge_drafts.append(draft)
    except Exception as e:
        raise LLMError(
            f"Knowledge points drafting failed: {str(e)}",
            details={"error": str(e)}
        )

    return KnowledgeDraftsResponse(
        success=True,
        message=f"{len(knowledge_drafts)} knowledge points drafted successfully",
        knowledge_drafts=knowledge_drafts
    )


@router.post("/integrate-learning-document", response_model=LearningDocumentResponse, tags=["Content"])
async def integrate_learning_document(
    request: LearningDocumentIntegrationRequest,
    llm_service: LLMService = Depends(get_llm_service),
    memory_service: MemoryService = Depends(get_memory_service)
):
    """Integrate learning document.

    Combines various knowledge sources into cohesive learning materials.

    Args:
        request: Learning document integration request
        llm_service: LLM service dependency
        memory_service: Memory service dependency

    Returns:
        Integrated learning document

    Raises:
        ValidationError: If request validation fails
        LLMError: If integration fails
    """
    # Get LLM
    llm = llm_service.get_llm()

    # Resolve learning goal
    learner_id = extract_learner_id(request.learner_profile)
    learning_goal = resolve_learning_goal(memory_service, learner_id, request.goal_id)

    # Integrate learning document
    try:
        learning_document = integrate_learning_document_with_llm(
            llm,
            request.learner_profile,
            request.learning_path,
            request.learning_session,
            request.knowledge_points,
            request.knowledge_drafts,
            request.output_markdown,
            learning_goal=learning_goal,
        )
    except Exception as e:
        raise LLMError(
            f"Learning document integration failed: {str(e)}",
            details={"error": str(e)}
        )

    return LearningDocumentResponse(
        success=True,
        message="Learning document integrated successfully",
        learning_document=learning_document
    )


@router.post("/tailor-knowledge-content", response_model=TailoredContentResponse, tags=["Content"])
async def tailor_knowledge_content(
    request: TailoredContentGenerationRequest,
    llm_service: LLMService = Depends(get_llm_service),
    memory_service: MemoryService = Depends(get_memory_service)
):
    """Tailor knowledge content.

    Generates complete personalized learning content for a session.

    Args:
        request: Tailored content generation request
        llm_service: LLM service dependency
        memory_service: Memory service dependency

    Returns:
        Tailored learning content

    Raises:
        ValidationError: If request validation fails
        LLMError: If content generation fails
    """
    # Get LLM
    llm = llm_service.get_llm()

    # Extract learner_id
    learner_id = extract_learner_id(request.learner_profile)

    # Parse string inputs to dicts/lists for the agent
    learner_profile = request.learner_profile
    learning_path = request.learning_path
    learning_session = request.learning_session
    if isinstance(learner_profile, str) and learner_profile.strip():
        learner_profile = json.loads(learner_profile)
    if isinstance(learning_path, str) and learning_path.strip():
        learning_path = json.loads(learning_path)
    if isinstance(learning_session, str) and learning_session.strip():
        learning_session = json.loads(learning_session)

    # Resolve learning goal
    learning_goal = resolve_learning_goal(memory_service, learner_id, request.goal_id)

    # Generate tailored content
    try:
        tailored_content = create_learning_content_with_llm(
            llm,
            learner_profile,
            learning_path,
            learning_session,
            allow_parallel=request.allow_parallel,
            with_quiz=request.with_quiz,
            use_search=request.use_search,
            learning_goal=learning_goal,
        )
    except Exception as e:
        raise LLMError(
            f"Tailored content generation failed: {str(e)}",
            details={"error": str(e)}
        )

    # Log content generation
    session_info = learning_session if isinstance(learning_session, dict) else {}
    session_title = session_info.get("title", "Unknown Session")

    memory_service.append_mastery_entry(learner_id, {
        "type": "content_generated",
        "session": session_title,
        "with_quiz": request.with_quiz,
        "content_summary": str(tailored_content)[:200] + "..." if len(str(tailored_content)) > 200 else str(tailored_content)
    })
    memory_service.log_interaction(
        learner_id,
        "system",
        f"Generated tailored content for session: {session_title}"
    )

    return TailoredContentResponse(
        success=True,
        message="Tailored content generated successfully",
        tailored_content=tailored_content
    )
