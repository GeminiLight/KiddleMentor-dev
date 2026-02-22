"""
Learner repository for learner data persistence.

Provides clean CRUD interface for learner profiles, learning goals, skill gaps, learning paths,
and interaction history using local file storage.
"""

from typing import Optional, Any
from pathlib import Path
from datetime import datetime

from gen_mentor.core.memory.memory_store import LearnerMemoryStore
from repositories.base import BaseRepository


class LearnerRepository(BaseRepository):
    """Repository for learner data using file-based storage.

    Wraps LearnerMemoryStore to provide a clean, standardized interface
    for learner data access.
    """

    def __init__(self, workspace: str | Path):
        """Initialize learner repository.

        Args:
            workspace: Workspace directory for learner data
        """
        self.workspace = Path(workspace).expanduser()

    def _get_memory_store(self, learner_id: str) -> LearnerMemoryStore:
        """Get memory store instance for learner.

        Args:
            learner_id: Learner identifier

        Returns:
            LearnerMemoryStore instance
        """
        return LearnerMemoryStore(
            workspace=str(self.workspace),
            learner_id=learner_id
        )

    # Base repository methods

    def exists(self, learner_id: str) -> bool:
        """Check if learner profile exists.

        Args:
            learner_id: Learner identifier

        Returns:
            True if profile exists, False otherwise
        """
        profile_path = self.workspace / "learners" / learner_id / "profile.json"
        return profile_path.exists()

    def get(self, learner_id: str) -> Optional[dict[str, Any]]:
        """Get learner profile (alias for get_profile).

        Args:
            learner_id: Learner identifier

        Returns:
            Learner profile or None
        """
        return self.get_profile(learner_id)

    def save(self, learner_id: str, data: dict[str, Any]) -> None:
        """Save learner profile (alias for save_profile).

        Args:
            learner_id: Learner identifier
            data: Profile data
        """
        self.save_profile(learner_id, data)

    def delete(self, learner_id: str) -> None:
        """Delete all learner data.

        Args:
            learner_id: Learner identifier
        """
        import shutil
        learner_dir = self.workspace / "learners" / learner_id
        if learner_dir.exists():
            shutil.rmtree(learner_dir)

    # Profile operations

    def get_profile(self, learner_id: str) -> Optional[dict[str, Any]]:
        """Get learner profile.

        Args:
            learner_id: Learner identifier

        Returns:
            Learner profile or None if not found
        """
        try:
            memory_store = self._get_memory_store(learner_id)
            profile = memory_store.read_profile()
            return profile if profile else None
        except Exception:
            return None

    def save_profile(self, learner_id: str, profile: dict[str, Any]) -> None:
        """Save learner profile.

        Args:
            learner_id: Learner identifier
            profile: Profile data to save
        """
        memory_store = self._get_memory_store(learner_id)
        memory_store.write_profile(profile)

    # Learning goals operations

    def get_learning_goals(self, learner_id: str) -> Optional[dict[str, Any]]:
        """Get learning goals.

        Args:
            learner_id: Learner identifier

        Returns:
            Learning goals or None if not found
        """
        try:
            memory_store = self._get_memory_store(learner_id)
            goals = memory_store.read_learning_goals()
            return goals if goals else None
        except Exception:
            return None

    def save_learning_goals(self, learner_id: str, learning_goals: dict[str, Any]) -> None:
        """Save learning goals.

        Args:
            learner_id: Learner identifier
            learning_goals: Learning goals data to save
        """
        memory_store = self._get_memory_store(learner_id)
        memory_store.write_learning_goals(learning_goals)

    # Skill gaps operations

    def get_skill_gaps(self, learner_id: str) -> Optional[dict[str, Any]]:
        """Get all skill gaps.

        Args:
            learner_id: Learner identifier

        Returns:
            All skill gaps (keyed by goal_id) or None if not found
        """
        try:
            memory_store = self._get_memory_store(learner_id)
            gaps = memory_store.read_skill_gaps()
            return gaps if gaps else None
        except Exception:
            return None

    def save_skill_gaps(self, learner_id: str, skill_gaps: dict[str, Any]) -> None:
        """Save all skill gaps.

        Args:
            learner_id: Learner identifier
            skill_gaps: Skill gaps data to save
        """
        memory_store = self._get_memory_store(learner_id)
        memory_store.write_skill_gaps(skill_gaps)

    def get_skill_gaps_for_goal(self, learner_id: str, goal_id: str) -> dict[str, Any]:
        """Get skill gaps for a specific goal.

        Args:
            learner_id: Learner identifier
            goal_id: Goal identifier

        Returns:
            Skill gaps for the goal
        """
        memory_store = self._get_memory_store(learner_id)
        return memory_store.read_skill_gaps_for_goal(goal_id)

    def save_skill_gaps_for_goal(self, learner_id: str, goal_id: str, data: dict[str, Any]) -> None:
        """Save skill gaps for a specific goal.

        Args:
            learner_id: Learner identifier
            goal_id: Goal identifier
            data: Skill gaps data for the goal
        """
        memory_store = self._get_memory_store(learner_id)
        memory_store.write_skill_gaps_for_goal(goal_id, data)

    def get_learning_path_for_goal(self, learner_id: str, goal_id: str) -> dict[str, Any]:
        """Get learning path for a specific goal.

        Args:
            learner_id: Learner identifier
            goal_id: Goal identifier

        Returns:
            Learning path for the goal
        """
        memory_store = self._get_memory_store(learner_id)
        return memory_store.read_learning_path_for_goal(goal_id)

    def save_learning_path_for_goal(self, learner_id: str, goal_id: str, data: dict[str, Any]) -> None:
        """Save learning path for a specific goal.

        Args:
            learner_id: Learner identifier
            goal_id: Goal identifier
            data: Learning path data for the goal
        """
        memory_store = self._get_memory_store(learner_id)
        memory_store.write_learning_path_for_goal(goal_id, data)

    # Learning path operations

    def get_learning_path(self, learner_id: str) -> Optional[dict[str, Any]]:
        """Get learning path.

        Args:
            learner_id: Learner identifier

        Returns:
            Learning path or None if not found
        """
        try:
            memory_store = self._get_memory_store(learner_id)
            path = memory_store.read_learning_path()
            return path if path else None
        except Exception:
            return None

    def save_learning_path(self, learner_id: str, learning_path: dict[str, Any]) -> None:
        """Save learning path.

        Args:
            learner_id: Learner identifier
            learning_path: Learning path data to save
        """
        memory_store = self._get_memory_store(learner_id)
        memory_store.write_learning_path(learning_path)

    # Mastery operations

    def get_mastery(self, learner_id: str) -> Optional[dict[str, Any]]:
        """Get mastery data.

        Args:
            learner_id: Learner identifier

        Returns:
            Mastery data or None if not found
        """
        try:
            memory_store = self._get_memory_store(learner_id)
            mastery = memory_store.read_mastery()
            return mastery if mastery else None
        except Exception:
            return None

    def save_mastery(self, learner_id: str, mastery: dict[str, Any]) -> None:
        """Save mastery data.

        Args:
            learner_id: Learner identifier
            mastery: Mastery data to save
        """
        memory_store = self._get_memory_store(learner_id)
        memory_store.write_mastery(mastery)

    def append_mastery_entry(self, learner_id: str, entry: dict[str, Any]) -> None:
        """Append mastery entry.

        Args:
            learner_id: Learner identifier
            entry: Mastery entry to append
        """
        memory_store = self._get_memory_store(learner_id)
        memory_store.append_mastery_entry(entry)

    # History operations

    def get_history(self, learner_id: str, limit: int = 100) -> list[dict[str, Any]]:
        """Get interaction history.

        Args:
            learner_id: Learner identifier
            limit: Maximum number of entries to return (0 = all)

        Returns:
            List of interaction history entries
        """
        try:
            memory_store = self._get_memory_store(learner_id)
            history = memory_store.read_history()
            if limit > 0 and len(history) > limit:
                return history[-limit:]
            return history
        except Exception:
            return []

    def append_history(
        self,
        learner_id: str,
        role: str,
        content: str,
        metadata: Optional[dict] = None
    ) -> None:
        """Append to interaction history.

        Args:
            learner_id: Learner identifier
            role: Role (e.g., 'learner', 'tutor', 'system')
            content: Interaction content
            metadata: Optional metadata dict
        """
        memory_store = self._get_memory_store(learner_id)
        memory_store.append_history(role, content, metadata)

    def log_interaction(
        self,
        learner_id: str,
        role: str,
        content: str,
        metadata: Optional[dict] = None
    ) -> None:
        """Log an interaction (alias for append_history).

        Args:
            learner_id: Learner identifier
            role: Role (e.g., 'learner', 'tutor', 'system')
            content: Interaction content
            metadata: Optional metadata dict
        """
        memory_store = self._get_memory_store(learner_id)
        memory_store.log_interaction(role, content, metadata)

    def search_history(self, learner_id: str, query: str) -> list[dict[str, Any]]:
        """Search interaction history.

        Args:
            learner_id: Learner identifier
            query: Search query

        Returns:
            List of matching history entries
        """
        memory_store = self._get_memory_store(learner_id)
        return memory_store.search_history(query)

    # Aggregate operations

    def get_learner_context(self, learner_id: str) -> dict[str, Any]:
        """Get complete learner context for AI agents.

        Args:
            learner_id: Learner identifier

        Returns:
            Dictionary with profile, learning_goals, skill_gaps, mastery, path, and history
        """
        return {
            "learner_id": learner_id,
            "profile": self.get_profile(learner_id) or {},
            "learning_goals": self.get_learning_goals(learner_id) or {},
            "skill_gaps": self.get_skill_gaps(learner_id) or {},
            "mastery": self.get_mastery(learner_id) or {},
            "learning_path": self.get_learning_path(learner_id) or {},
            "recent_history": self.get_history(learner_id, limit=10)
        }

    def get_context_summary(self, learner_id: str) -> str:
        """Get formatted context summary for LLM prompts.

        Args:
            learner_id: Learner identifier

        Returns:
            Formatted context string
        """
        memory_store = self._get_memory_store(learner_id)
        return memory_store.get_learner_context()
