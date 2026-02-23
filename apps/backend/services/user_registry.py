"""
User registry service for managing user accounts.

Maintains a users.json registry and can sync from existing learner profiles on disk.
"""

import json
import shutil
from datetime import datetime
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, List, Optional

from config import get_backend_settings


class UserRegistryService:
    """Service for managing the user registry (users.json)."""

    def __init__(self):
        settings = get_backend_settings()
        self.workspace = Path(settings.expanded_workspace_dir)
        self.registry_path = self.workspace / "users.json"

    def _load_registry(self) -> Dict[str, Any]:
        if self.registry_path.exists():
            try:
                return json.loads(self.registry_path.read_text(encoding="utf-8"))
            except Exception:
                pass
        return {"users": []}

    def _save_registry(self, data: Dict[str, Any]) -> None:
        self.registry_path.parent.mkdir(parents=True, exist_ok=True)
        self.registry_path.write_text(
            json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8"
        )

    def list_users(self) -> List[Dict[str, Any]]:
        """Return all registered users."""
        return self._load_registry().get("users", [])

    def get_user(self, learner_id: str) -> Optional[Dict[str, Any]]:
        """Return a single user by learner_id, or None."""
        for u in self.list_users():
            if u.get("learner_id") == learner_id:
                return u
        return None

    def register_user(
        self,
        learner_id: str,
        name: str = "Anonymous Learner",
        email: Optional[str] = None,
        created_at: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Register a new user (or update existing) in the registry."""
        registry = self._load_registry()
        users: List[Dict[str, Any]] = registry.get("users", [])

        # Check if already registered
        for u in users:
            if u.get("learner_id") == learner_id:
                # Update name/email if provided
                u["name"] = name
                if email:
                    u["email"] = email
                self._save_registry(registry)
                return u

        user = {
            "learner_id": learner_id,
            "name": name,
            "email": email,
            "created_at": created_at or datetime.now().isoformat(),
        }
        users.append(user)
        registry["users"] = users
        self._save_registry(registry)
        return user

    def delete_user(self, learner_id: str) -> bool:
        """Delete a user from the registry and remove their memory directory.

        Returns:
            True if user was found and deleted, False otherwise.
        """
        registry = self._load_registry()
        users: List[Dict[str, Any]] = registry.get("users", [])
        original_len = len(users)
        users = [u for u in users if u.get("learner_id") != learner_id]

        if len(users) == original_len:
            return False

        registry["users"] = users
        self._save_registry(registry)

        # Remove the learner memory directory from disk
        memory_dir = self.workspace / "memory" / learner_id
        if memory_dir.exists():
            shutil.rmtree(memory_dir)

        return True

    def sync_from_disk(self) -> int:
        """Scan workspace/memory/learner_*/profile.json to bootstrap registry.

        Returns:
            Number of users synced.
        """
        memory_dir = self.workspace / "memory"
        if not memory_dir.exists():
            return 0

        count = 0
        for learner_dir in sorted(memory_dir.iterdir()):
            if not learner_dir.is_dir() or not learner_dir.name.startswith("learner_"):
                continue
            profile_path = learner_dir / "profile.json"
            if not profile_path.exists():
                continue
            try:
                profile = json.loads(profile_path.read_text(encoding="utf-8"))
                learner_id = profile.get("learner_id", learner_dir.name)
                name = profile.get("name", "Anonymous Learner")
                email = profile.get("email")
                created_at = profile.get("created_at")
                self.register_user(learner_id, name, email, created_at)
                count += 1
            except Exception:
                continue

        return count


@lru_cache()
def get_user_registry() -> UserRegistryService:
    """Get cached user registry instance."""
    return UserRegistryService()
