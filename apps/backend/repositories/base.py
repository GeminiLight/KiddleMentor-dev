"""
Base repository interfaces for storage layer.

Defines abstract base classes for data access patterns.
"""

from abc import ABC, abstractmethod
from typing import Optional, Any


class BaseRepository(ABC):
    """Abstract base repository for data persistence."""

    @abstractmethod
    def exists(self, entity_id: str) -> bool:
        """Check if entity exists.

        Args:
            entity_id: Entity identifier

        Returns:
            True if entity exists, False otherwise
        """
        pass

    @abstractmethod
    def get(self, entity_id: str) -> Optional[dict[str, Any]]:
        """Get entity by ID.

        Args:
            entity_id: Entity identifier

        Returns:
            Entity data or None if not found
        """
        pass

    @abstractmethod
    def save(self, entity_id: str, data: dict[str, Any]) -> None:
        """Save entity data.

        Args:
            entity_id: Entity identifier
            data: Entity data to save
        """
        pass

    @abstractmethod
    def delete(self, entity_id: str) -> None:
        """Delete entity.

        Args:
            entity_id: Entity identifier
        """
        pass
