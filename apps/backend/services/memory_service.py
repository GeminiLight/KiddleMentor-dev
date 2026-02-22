"""
Memory service for managing learner context and history.

Handles workspace-based memory persistence for learner profiles, objectives, and interactions.
"""

from typing import Optional, Dict, Any
from functools import lru_cache

from gen_mentor.core.memory.memory_store import LearnerMemoryStore
from config import get_backend_settings
from exceptions import MemoryError


class MemoryService:
    """Service for managing learner memory and context."""

    def __init__(self):
        """Initialize memory service."""
        self.settings = get_backend_settings()

    def is_available(self) -> bool:
        """Check if memory storage is available.

        Returns:
            True if local storage mode is enabled
        """
        return self.settings.storage_mode.lower() == "local"

    def get_memory_store(self, learner_id: Optional[str] = None) -> Optional[LearnerMemoryStore]:
        """Get learner memory store.

        Args:
            learner_id: Optional learner identifier for separate memory spaces

        Returns:
            LearnerMemoryStore instance if local storage mode, None otherwise
        """
        if not self.is_available():
            return None

        try:
            return LearnerMemoryStore(
                workspace=self.settings.workspace_dir,
                learner_id=learner_id
            )
        except Exception as e:
            raise MemoryError(
                f"Failed to create memory store: {str(e)}",
                details={"learner_id": learner_id, "error": str(e)}
            )

    def get_learner_memory(self, learner_id: str) -> Dict[str, Any]:
        """Get all memory and context for a learner.

        Args:
            learner_id: Learner identifier

        Returns:
            Dictionary containing profile, objectives, mastery, and history

        Raises:
            MemoryError: If memory storage is not available or retrieval fails
        """
        if not self.is_available():
            raise MemoryError(
                "Memory storage not available in cloud mode",
                details={"storage_mode": self.settings.storage_mode}
            )

        try:
            memory = self.get_memory_store(learner_id)
            if not memory:
                raise MemoryError("Failed to get memory store")

            return {
                "learner_id": learner_id,
                "profile": memory.read_profile(),
                "objectives": memory.read_objectives(),
                "mastery": memory.read_mastery(),
                "learning_path": memory.read_learning_path(),
                "context": memory.get_learner_context(),
                "recent_history": memory.get_recent_history(n=20),
            }
        except Exception as e:
            if isinstance(e, MemoryError):
                raise
            raise MemoryError(
                f"Failed to retrieve learner memory: {str(e)}",
                details={"learner_id": learner_id, "error": str(e)}
            )

    def search_history(self, learner_id: str, query: str) -> list[dict[str, Any]]:
        """Search learner interaction history.

        Args:
            learner_id: Learner identifier
            query: Search query string

        Returns:
            List of matching history entries

        Raises:
            MemoryError: If memory storage is not available or search fails
        """
        if not self.is_available():
            raise MemoryError(
                "Memory storage not available in cloud mode",
                details={"storage_mode": self.settings.storage_mode}
            )

        try:
            memory = self.get_memory_store(learner_id)
            if not memory:
                raise MemoryError("Failed to get memory store")

            return memory.search_history(query)
        except Exception as e:
            if isinstance(e, MemoryError):
                raise
            raise MemoryError(
                f"Failed to search history: {str(e)}",
                details={"learner_id": learner_id, "query": query, "error": str(e)}
            )

    def log_interaction(
        self,
        learner_id: Optional[str],
        role: str,
        content: str,
        metadata: Optional[dict] = None
    ) -> None:
        """Log a learning interaction to history.

        Args:
            learner_id: Learner identifier (optional)
            role: Role (e.g., 'learner', 'tutor', 'system')
            content: Interaction content
            metadata: Optional metadata dict
        """
        if not self.is_available() or not learner_id:
            return

        try:
            memory = self.get_memory_store(learner_id)
            if memory:
                memory.log_interaction(role, content, metadata)
        except Exception:
            # Don't fail the request if logging fails
            pass

    def save_profile(self, learner_id: Optional[str], profile: Dict[str, Any]) -> None:
        """Save learner profile to memory.

        Args:
            learner_id: Learner identifier (optional)
            profile: Profile data to save
        """
        if not self.is_available() or not learner_id:
            return

        try:
            memory = self.get_memory_store(learner_id)
            if memory:
                memory.write_profile(profile)
        except Exception:
            # Don't fail the request if save fails
            pass

    def save_objectives(self, learner_id: Optional[str], objectives: Dict[str, Any]) -> None:
        """Save learning objectives to memory.

        Args:
            learner_id: Learner identifier (optional)
            objectives: Objectives data to save
        """
        if not self.is_available() or not learner_id:
            return

        try:
            memory = self.get_memory_store(learner_id)
            if memory:
                memory.write_objectives(objectives)
        except Exception:
            # Don't fail the request if save fails
            pass

    def append_mastery_entry(
        self,
        learner_id: Optional[str],
        mastery_entry: Dict[str, Any]
    ) -> None:
        """Append mastery entry to memory.

        Args:
            learner_id: Learner identifier (optional)
            mastery_entry: Mastery entry to append
        """
        if not self.is_available() or not learner_id:
            return

        try:
            memory = self.get_memory_store(learner_id)
            if memory:
                memory.append_mastery_entry(mastery_entry)
        except Exception:
            # Don't fail the request if append fails
            pass

    def save_learning_path(self, learner_id: Optional[str], learning_path: Dict[str, Any]) -> None:
        """Save learning path to memory.

        Args:
            learner_id: Learner identifier (optional)
            learning_path: Learning path data to save
        """
        if not self.is_available() or not learner_id:
            return

        try:
            memory = self.get_memory_store(learner_id)
            if memory:
                memory.write_learning_path(learning_path)
        except Exception:
            # Don't fail the request if save fails
            pass

    def get_context_for_llm(self, learner_id: Optional[str]) -> Dict[str, Any]:
        """Get all context needed for LLM prompts.

        Args:
            learner_id: Learner identifier

        Returns:
            Dictionary with profile, objectives, mastery, path, context, and history
        """
        if not self.is_available() or not learner_id:
            return {}

        try:
            memory = self.get_memory_store(learner_id)
            if not memory:
                return {}

            return {
                "profile": memory.read_profile(),
                "objectives": memory.read_objectives(),
                "mastery": memory.read_mastery(),
                "learning_path": memory.read_learning_path(),
                "context_summary": memory.get_learner_context(),
                "recent_history": memory.get_recent_history(n=5),
            }
        except Exception:
            return {}

    def load_profile_from_memory(
        self,
        learner_id: Optional[str],
        provided_profile: Optional[Any] = None
    ) -> Any:
        """Load learner profile from memory if not provided.

        Args:
            learner_id: Learner identifier
            provided_profile: Profile provided in request (takes precedence)

        Returns:
            Profile from request or memory, or empty dict if neither available
        """
        # If profile provided in request, use it
        if provided_profile:
            return provided_profile

        # Try to load from memory
        if not self.is_available() or not learner_id:
            return {}

        try:
            memory = self.get_memory_store(learner_id)
            if memory:
                stored_profile = memory.read_profile()
                return stored_profile if stored_profile else {}
        except Exception:
            pass

        return {}

    def load_objectives_from_memory(
        self,
        learner_id: Optional[str],
        provided_objectives: Optional[Any] = None
    ) -> Any:
        """Load learning objectives from memory if not provided.

        Args:
            learner_id: Learner identifier
            provided_objectives: Objectives provided in request (takes precedence)

        Returns:
            Objectives from request or memory, or empty dict if neither available
        """
        # If objectives provided in request, use them
        if provided_objectives:
            return provided_objectives

        # Try to load from memory
        if not self.is_available() or not learner_id:
            return {}

        try:
            memory = self.get_memory_store(learner_id)
            if memory:
                stored_objectives = memory.read_objectives()
                return stored_objectives if stored_objectives else {}
        except Exception:
            pass

        return {}


@lru_cache()
def get_memory_service() -> MemoryService:
    """Get cached memory service instance.

    Returns:
        MemoryService instance
    """
    return MemoryService()
