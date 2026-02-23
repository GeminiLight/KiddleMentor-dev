"""
Dependency injection for FastAPI endpoints.

Provides reusable dependencies for services, configuration, and common operations.
"""

from typing import Optional, Dict, Any
import json

from fastapi import Depends, Header, HTTPException

from config import get_backend_settings, get_app_config, Config, BackendSettings
from gen_mentor.config import AppConfig
from services.llm_service import get_llm_service, LLMService
from services.memory_service import get_memory_service, MemoryService
from repositories.learner_repository import LearnerRepository
from gen_mentor.core.tools.retrieval.search_rag import SearchRagManager
from exceptions import ValidationError


# =============================================================================
# Configuration Dependencies
# =============================================================================

def get_settings() -> BackendSettings:
    """Get backend settings dependency.

    Returns:
        BackendSettings instance
    """
    return get_backend_settings()


def get_config() -> AppConfig:
    """Get application config dependency.

    Returns:
        AppConfig instance
    """
    return get_app_config()


# =============================================================================
# Repository Dependencies
# =============================================================================

_learner_repository = None


def get_learner_repository(
    settings: BackendSettings = Depends(get_settings)
) -> LearnerRepository:
    """Get learner repository dependency.

    Args:
        settings: Backend settings

    Returns:
        LearnerRepository instance (cached)
    """
    global _learner_repository

    if _learner_repository is None:
        _learner_repository = LearnerRepository(workspace=settings.workspace_dir)

    return _learner_repository


# =============================================================================
# Service Dependencies
# =============================================================================

def get_llm_service_dep() -> LLMService:
    """Get LLM service dependency.

    Returns:
        LLMService instance
    """
    return get_llm_service()


def get_memory_service_dep() -> MemoryService:
    """Get memory service dependency.

    Returns:
        MemoryService instance
    """
    return get_memory_service()


# =============================================================================
# Search RAG Manager Dependency
# =============================================================================

_search_rag_manager = None


def get_search_rag_manager(
    config: AppConfig = Depends(get_config)
) -> SearchRagManager:
    """Get search RAG manager dependency.

    Args:
        config: Application configuration

    Returns:
        SearchRagManager instance (cached)
    """
    global _search_rag_manager

    if _search_rag_manager is None:
        _search_rag_manager = SearchRagManager.from_config({
            "search": {
                "provider": config.search_defaults.provider,
                "max_results": config.search_defaults.max_results,
                "loader_type": config.search_defaults.loader_type,
                "enable_search": config.search_defaults.enable_search,
            },
            "embedder": {
                "provider": config.embedding_defaults.provider,
                "model_name": config.embedding_defaults.model_name,
                "dimension": config.embedding_defaults.dimension,
                "enable_vectordb": config.embedding_defaults.enable_vectordb,
            },
            "vectorstore": {
                "persist_directory": config.vectorstore.persist_directory,
                "collection_name": config.vectorstore.collection_name,
            },
            "rag": {
                "chunk_size": config.rag.chunk_size,
                "num_retrieval_results": config.rag.num_retrieval_results,
                "allow_parallel": config.rag.allow_parallel,
                "max_workers": config.rag.max_workers,
            },
        })

    return _search_rag_manager


# =============================================================================
# Helper Dependencies
# =============================================================================

def parse_json_string(value: str, field_name: str = "value") -> Dict[str, Any]:
    """Parse JSON string to dictionary.

    Args:
        value: JSON string to parse
        field_name: Field name for error messages

    Returns:
        Parsed dictionary

    Raises:
        ValidationError: If parsing fails
    """
    if not value or not value.strip():
        return {}

    try:
        return json.loads(value)
    except Exception as e:
        raise ValidationError(
            f"Invalid JSON for {field_name}",
            details={"field": field_name, "error": str(e)}
        )


def extract_learner_id(profile_data: str | Dict[str, Any]) -> Optional[str]:
    """Extract learner ID from profile data.

    Args:
        profile_data: Profile as string or dict

    Returns:
        Learner ID if found, None otherwise
    """
    if not profile_data:
        return None

    # If already a dict
    if isinstance(profile_data, dict):
        return profile_data.get("learner_id")

    # If string, try to parse
    try:
        profile_dict = parse_json_string(profile_data, "learner_profile")
        return profile_dict.get("learner_id")
    except Exception:
        return None


def resolve_learning_goal(
    memory_service: MemoryService,
    learner_id: Optional[str],
    goal_id: Optional[str] = None,
) -> str:
    """Resolve the learning goal text from memory.

    Looks up the goal by *goal_id* when provided, otherwise falls back to the
    learner's currently active goal.

    Args:
        memory_service: Memory service instance
        learner_id: Learner identifier
        goal_id: Optional explicit goal ID

    Returns:
        The learning goal string, or "" if not found
    """
    if not learner_id:
        return ""

    memory_store = memory_service.get_memory_store(learner_id)
    if memory_store is None:
        return ""

    if goal_id:
        # Try to find the specific goal by ID
        goals_data = memory_store.read_learning_goals()
        for goal in goals_data.get("goals", []):
            if goal.get("goal_id") == goal_id:
                return goal.get("learning_goal", "")
        return ""

    # Fall back to active goal
    active_goal = memory_store.get_active_goal()
    if active_goal:
        return active_goal.get("learning_goal", "")

    return ""


# =============================================================================
# Authentication Dependencies (Future)
# =============================================================================

def get_api_key(
    x_api_key: Optional[str] = Header(None, description="API key for authentication")
) -> Optional[str]:
    """Get API key from header (placeholder for future authentication).

    Args:
        x_api_key: API key from X-API-Key header

    Returns:
        API key if provided
    """
    # TODO: Implement actual API key validation
    return x_api_key


def verify_api_key(api_key: str = Depends(get_api_key)) -> str:
    """Verify API key (placeholder for future authentication).

    Args:
        api_key: API key to verify

    Returns:
        Verified API key

    Raises:
        HTTPException: If API key is invalid
    """
    # TODO: Implement actual API key verification
    # For now, just pass through
    return api_key or "default"


# =============================================================================
# Rate Limiting Dependencies (Future)
# =============================================================================

async def check_rate_limit(
    request_id: str = Header(None, alias="X-Request-ID"),
    settings: BackendSettings = Depends(get_settings)
) -> None:
    """Check rate limiting (placeholder for future implementation).

    Args:
        request_id: Request ID from header
        settings: Backend settings

    Raises:
        HTTPException: If rate limit exceeded
    """
    # TODO: Implement actual rate limiting
    # For now, just pass through
    pass


# =============================================================================
# Common Query Dependencies
# =============================================================================

class CommonQueryParams:
    """Common query parameters for list endpoints."""

    def __init__(
        self,
        skip: int = 0,
        limit: int = 100,
        sort_by: Optional[str] = None,
        order: str = "asc"
    ):
        """Initialize common query parameters.

        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            sort_by: Field to sort by
            order: Sort order (asc or desc)
        """
        self.skip = skip
        self.limit = min(limit, 1000)  # Max 1000 records
        self.sort_by = sort_by
        self.order = order.lower()


def get_common_params(
    skip: int = 0,
    limit: int = 100,
    sort_by: Optional[str] = None,
    order: str = "asc"
) -> CommonQueryParams:
    """Get common query parameters dependency.

    Args:
        skip: Number of records to skip
        limit: Maximum number of records to return
        sort_by: Field to sort by
        order: Sort order (asc or desc)

    Returns:
        CommonQueryParams instance
    """
    return CommonQueryParams(skip, limit, sort_by, order)
