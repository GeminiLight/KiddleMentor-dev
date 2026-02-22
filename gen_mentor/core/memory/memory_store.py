"""Memory store system for context persistence and learning history.

Implements a domain-aligned memory system:
- user_facts.md: Extracted long-term context and insights
- chat_history.json: Structured tutor interactions
- learning_goal.json: Multi-goal learning goals (goal-centric)
- skill_gaps.json: Skill gaps keyed by goal_id
- learning_path.json: Learning paths keyed by goal_id
"""

from __future__ import annotations

import json
import os
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any, Optional


def ensure_dir(path: Path) -> Path:
    """Ensure directory exists."""
    path.mkdir(parents=True, exist_ok=True)
    return path


class MemoryStore:
    """Two-layer memory: user_facts.md (long-term facts) + chat_history.json (interaction log)."""

    def __init__(self, workspace: Path | str):
        """Initialize memory store.

        Args:
            workspace: Path to workspace directory
        """
        if isinstance(workspace, str):
            # Expand ~ and environment variables
            workspace = Path(os.path.expanduser(workspace)).expanduser()

        self.workspace = Path(workspace)
        self.memory_dir = ensure_dir(self.workspace / "memory")
        self.memory_file = self.memory_dir / "user_facts.md"
        self.history_file = self.memory_dir / "chat_history.json"

    def read_long_term(self) -> str:
        """Read long-term memory facts.

        Returns:
            Content of user_facts.md or empty string if file doesn't exist
        """
        if self.memory_file.exists():
            return self.memory_file.read_text(encoding="utf-8")
        return ""

    def write_long_term(self, content: str) -> None:
        """Write/update long-term memory facts.

        Args:
            content: New content for user_facts.md (replaces existing)
        """
        self.memory_file.write_text(content, encoding="utf-8")

    def append_to_long_term(self, content: str) -> None:
        """Append to long-term memory without replacing.

        Args:
            content: Content to append to user_facts.md
        """
        existing = self.read_long_term()
        if existing and not existing.endswith("\n\n"):
            existing += "\n\n"
        self.write_long_term(existing + content)

    def read_history(self) -> list[dict[str, Any]]:
        """Read chat history log.

        Returns:
            List of message dictionaries
        """
        if self.history_file.exists():
            try:
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return []
        return []

    def write_history(self, history: list[dict[str, Any]]) -> None:
        """Write full history log.

        Args:
            history: List of message dictionaries
        """
        with open(self.history_file, 'w', encoding='utf-8') as f:
            json.dump(history, f, indent=2, ensure_ascii=False)

    def append_history(self, role: str, content: str, metadata: Optional[dict] = None) -> None:
        """Append entry to history log.

        Args:
            role: Role (e.g., 'learner', 'tutor', 'system')
            content: Message content
            metadata: Optional metadata dict
        """
        history = self.read_history()
        entry = {
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        }
        if metadata:
            entry["metadata"] = metadata
        
        history.append(entry)
        self.write_history(history)

    def get_memory_context(self) -> str:
        """Get formatted memory context for agent prompts.

        Returns:
            Formatted string with long-term memory content
        """
        long_term = self.read_long_term()
        if long_term:
            return f"## User Facts & Context\n\n{long_term}"
        return ""

    def get_recent_history(self, n: int = 10) -> str:
        """Get recent history entries as formatted string.

        Args:
            n: Number of recent entries to retrieve (default: 10)

        Returns:
            Recent history entries as string
        """
        history = self.read_history()
        recent = history[-n:] if len(history) > n else history
        
        lines = []
        for entry in recent:
            role = entry.get("role", "unknown").upper()
            content = entry.get("content", "")
            lines.append(f"**{role}**: {content}")
        
        return "\n\n".join(lines)

    def search_history(self, query: str) -> list[dict[str, Any]]:
        """Search history for entries matching query.

        Args:
            query: Search query string

        Returns:
            List of matching history entry dictionaries
        """
        history = self.read_history()
        matches = [e for e in history if query.lower() in e.get("content", "").lower()]
        return matches

    def clear_history(self) -> None:
        """Clear all history entries."""
        if self.history_file.exists():
            self.history_file.unlink()

    def clear_memory(self) -> None:
        """Clear long-term memory."""
        if self.memory_file.exists():
            self.memory_file.unlink()

    def clear_all(self) -> None:
        """Clear both memory and history."""
        self.clear_memory()
        self.clear_history()


class LearnerMemoryStore(MemoryStore):
    """Specialized memory store for learner information and learning progress."""

    def __init__(self, workspace: Path | str, learner_id: Optional[str] = None):
        """Initialize learner memory store.

        Args:
            workspace: Path to workspace directory
            learner_id: Optional learner identifier for separate memory spaces
        """
        super().__init__(workspace)

        if learner_id:
            # Create learner-specific memory directory
            self.memory_dir = ensure_dir(self.workspace / "memory" / learner_id)
            self.memory_file = self.memory_dir / "user_facts.md"
            self.history_file = self.memory_dir / "chat_history.json"
            self.profile_file = self.memory_dir / "profile.json"
            self.learning_goal_file = self.memory_dir / "learning_goal.json"
            self.skill_gaps_file = self.memory_dir / "skill_gaps.json"
            self.mastery_file = self.memory_dir / "mastery.json"
            self.learning_path_file = self.memory_dir / "learning_path.json"

    def read_profile(self) -> dict[str, Any]:
        """Read learner profile."""
        if hasattr(self, 'profile_file') and self.profile_file.exists():
            try:
                with open(self.profile_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return {}
        return {}

    def write_profile(self, content: dict[str, Any]) -> None:
        """Write learner profile."""
        if hasattr(self, 'profile_file'):
            with open(self.profile_file, 'w', encoding='utf-8') as f:
                json.dump(content, f, indent=2, ensure_ascii=False)

    def read_learning_goals(self) -> dict[str, Any]:
        """Read learning goals."""
        if hasattr(self, 'learning_goal_file') and self.learning_goal_file.exists():
            try:
                with open(self.learning_goal_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return {}
        return {}

    def write_learning_goals(self, content: dict[str, Any]) -> None:
        """Write learning goals."""
        if hasattr(self, 'learning_goal_file'):
            with open(self.learning_goal_file, 'w', encoding='utf-8') as f:
                json.dump(content, f, indent=2, ensure_ascii=False)

    def get_active_goal(self) -> Optional[dict[str, Any]]:
        """Get the currently active goal from learning goals.

        Returns:
            Active goal dict, or None if no active goal
        """
        goals_data = self.read_learning_goals()
        active_id = goals_data.get("active_goal_id")
        if not active_id:
            return None
        for goal in goals_data.get("goals", []):
            if goal.get("goal_id") == active_id:
                return goal
        return None

    def get_active_goal_id(self) -> Optional[str]:
        """Get the active goal_id.

        Returns:
            Active goal_id string or None
        """
        goals_data = self.read_learning_goals()
        return goals_data.get("active_goal_id")

    def add_goal(self, learning_goal: str, refined_goal: Any = None) -> str:
        """Add a new goal and set it as active.

        Args:
            learning_goal: The learning goal text
            refined_goal: Optional refined goal data

        Returns:
            The generated goal_id
        """
        goals_data = self.read_learning_goals()
        if "goals" not in goals_data:
            goals_data["goals"] = []

        goal_id = f"goal_{datetime.now().strftime('%Y%m%d')}_{uuid.uuid4().hex[:6]}"
        now = datetime.now().isoformat()

        new_goal = {
            "goal_id": goal_id,
            "learning_goal": learning_goal,
            "refined_goal": refined_goal,
            "status": "active",
            "created_at": now,
            "updated_at": now,
        }

        # Deactivate any previously active goal
        for g in goals_data["goals"]:
            if g.get("status") == "active":
                g["status"] = "inactive"

        goals_data["goals"].append(new_goal)
        goals_data["active_goal_id"] = goal_id
        self.write_learning_goals(goals_data)
        return goal_id

    # --- Skill gaps ---

    def read_skill_gaps(self) -> dict[str, Any]:
        """Read all skill gaps (keyed by goal_id)."""
        if hasattr(self, 'skill_gaps_file') and self.skill_gaps_file.exists():
            try:
                with open(self.skill_gaps_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return {}
        return {}

    def write_skill_gaps(self, content: dict[str, Any]) -> None:
        """Write all skill gaps."""
        if hasattr(self, 'skill_gaps_file'):
            with open(self.skill_gaps_file, 'w', encoding='utf-8') as f:
                json.dump(content, f, indent=2, ensure_ascii=False)

    def read_skill_gaps_for_goal(self, goal_id: str) -> dict[str, Any]:
        """Read skill gaps for a specific goal.

        Args:
            goal_id: The goal identifier

        Returns:
            Skill gaps dict for that goal, or empty dict
        """
        all_gaps = self.read_skill_gaps()
        return all_gaps.get(goal_id, {})

    def write_skill_gaps_for_goal(self, goal_id: str, data: dict[str, Any]) -> None:
        """Write skill gaps for a specific goal.

        Args:
            goal_id: The goal identifier
            data: Skill gaps data for that goal
        """
        all_gaps = self.read_skill_gaps()
        data["updated_at"] = datetime.now().isoformat()
        all_gaps[goal_id] = data
        self.write_skill_gaps(all_gaps)

    # --- Goal-scoped learning path ---

    def read_learning_path_for_goal(self, goal_id: str) -> dict[str, Any]:
        """Read learning path for a specific goal.

        Args:
            goal_id: The goal identifier

        Returns:
            Learning path dict for that goal, or empty dict
        """
        all_paths = self.read_learning_path()
        return all_paths.get(goal_id, {})

    def write_learning_path_for_goal(self, goal_id: str, data: dict[str, Any]) -> None:
        """Write learning path for a specific goal.

        Args:
            goal_id: The goal identifier
            data: Learning path data for that goal
        """
        all_paths = self.read_learning_path()
        data["updated_at"] = datetime.now().isoformat()
        all_paths[goal_id] = data
        self.write_learning_path(all_paths)

    def read_mastery(self) -> dict[str, Any]:
        """Read learning mastery and progress."""
        if hasattr(self, 'mastery_file') and self.mastery_file.exists():
            try:
                with open(self.mastery_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return {}
        return {}

    def write_mastery(self, content: dict[str, Any]) -> None:
        """Write learning mastery."""
        if hasattr(self, 'mastery_file'):
            with open(self.mastery_file, 'w', encoding='utf-8') as f:
                json.dump(content, f, indent=2, ensure_ascii=False)

    def append_mastery_entry(self, entry: dict[str, Any]) -> None:
        """Append entry to mastery log."""
        existing = self.read_mastery()
        if 'entries' not in existing:
            existing['entries'] = []

        if 'timestamp' not in entry:
            entry['timestamp'] = datetime.now().isoformat()

        existing['entries'].append(entry)
        self.write_mastery(existing)

    def update_evaluations(self, evaluation: dict[str, Any]) -> None:
        """Update evaluations within mastery.json."""
        existing = self.read_mastery()
        existing['last_evaluation'] = evaluation
        
        if 'evaluations_history' not in existing:
            existing['evaluations_history'] = []
            
        history_entry = evaluation.copy()
        if 'timestamp' not in history_entry:
            history_entry['timestamp'] = datetime.now().isoformat()
            
        existing['evaluations_history'].append(history_entry)
        self.write_mastery(existing)

    def read_learning_path(self) -> dict[str, Any]:
        """Read learning path."""
        if hasattr(self, 'learning_path_file') and self.learning_path_file.exists():
            try:
                with open(self.learning_path_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return {}
        return {}

    def write_learning_path(self, content: dict[str, Any]) -> None:
        """Write learning path."""
        if hasattr(self, 'learning_path_file'):
            with open(self.learning_path_file, 'w', encoding='utf-8') as f:
                json.dump(content, f, indent=2, ensure_ascii=False)

    def get_learner_context(self) -> str:
        """Get complete learner context for agent prompts."""
        sections = []

        profile = self.read_profile()
        if profile:
            sections.append(f"## Learner Profile\n\n```json\n{json.dumps(profile, indent=2, ensure_ascii=False)}\n```")

        learning_goals = self.read_learning_goals()
        if learning_goals:
            sections.append(f"## Learning Goals\n\n```json\n{json.dumps(learning_goals, indent=2, ensure_ascii=False)}\n```")

        skill_gaps = self.read_skill_gaps()
        if skill_gaps:
            sections.append(f"## Skill Gaps\n\n```json\n{json.dumps(skill_gaps, indent=2, ensure_ascii=False)}\n```")

        mastery = self.read_mastery()
        if mastery:
            sections.append(f"## Learning Mastery & Performance\n\n```json\n{json.dumps(mastery, indent=2, ensure_ascii=False)}\n```")

        user_facts = self.read_long_term()
        if user_facts:
            sections.append(f"## User Facts & Context\n\n{user_facts}")

        return "\n\n".join(sections) if sections else ""

    def log_interaction(self, role: str, content: str, metadata: Optional[dict] = None) -> None:
        """Log a tutor interaction to history."""
        self.append_history(role, content, metadata)


if __name__ == "__main__":
    # Example usage
    memory = MemoryStore("~/.gen-mentor/workspace")
    memory.write_long_term("# User Facts\n\n- Interested in machine learning")
    memory.append_history("learner", "I want to learn about neural networks")
    memory.append_history("tutor", "Let's start with neurons")
    print(memory.get_memory_context())
    print(memory.get_recent_history())

    # Learner-specific memory
    learner_memory = LearnerMemoryStore("~/.gen-mentor/workspace", learner_id="user123")
    learner_memory.write_profile({"name": "John", "level": "Beginner"})
    learner_memory.add_goal("Learn Python")
    learner_memory.log_interaction("learner", "Hi!")
    learner_memory.update_evaluations({"overall_score": 90})
    print("\n" + learner_memory.get_learner_context())
