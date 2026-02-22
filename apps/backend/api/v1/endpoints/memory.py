"""
Memory endpoints - learner context and history management.
"""

from fastapi import APIRouter, Depends

from models import LearnerMemoryResponse, HistorySearchResponse, GetLearnerMemoryRequest, SearchHistoryRequest
from services.memory_service import get_memory_service, MemoryService
from exceptions import MemoryError

router = APIRouter()


@router.post("/learner-memory", response_model=LearnerMemoryResponse, tags=["Memory"])
async def get_learner_memory(
    request: GetLearnerMemoryRequest,
    memory_service: MemoryService = Depends(get_memory_service)
):
    """Get learner memory and context information.

    Retrieves all stored information about a learner including profile,
    goals, progress, and interaction history.

    Args:
        request: Request with learner_id
        memory_service: Memory service dependency

    Returns:
        Complete learner memory and context

    Raises:
        MemoryError: If memory retrieval fails or storage is unavailable
    """
    memory_data = memory_service.get_learner_memory(request.learner_id)

    return LearnerMemoryResponse(
        success=True,
        message="Learner memory retrieved successfully",
        **memory_data
    )


@router.post("/search-history", response_model=HistorySearchResponse, tags=["Memory"])
async def search_learner_history(
    request: SearchHistoryRequest,
    memory_service: MemoryService = Depends(get_memory_service)
):
    """Search learner interaction history.

    Searches through the learner's interaction history for entries
    matching the query string.

    Args:
        request: Request with learner_id and query
        memory_service: Memory service dependency

    Returns:
        Matching history entries

    Raises:
        MemoryError: If search fails or storage is unavailable
    """
    matches = memory_service.search_history(request.learner_id, request.query)

    return HistorySearchResponse(
        success=True,
        message=f"Found {len(matches)} matching entries",
        query=request.query,
        matches=matches,
        count=len(matches)
    )
