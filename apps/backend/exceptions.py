"""
Custom exceptions for the backend API.

Provides structured error handling with appropriate HTTP status codes.
"""

from typing import Any, Optional


class BackendException(Exception):
    """Base exception for backend errors."""

    def __init__(
        self,
        message: str,
        status_code: int = 500,
        error_code: Optional[str] = None,
        details: Optional[dict[str, Any]] = None
    ):
        """Initialize exception.

        Args:
            message: Error message
            status_code: HTTP status code
            error_code: Application-specific error code
            details: Additional error details
        """
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.error_code = error_code or self.__class__.__name__
        self.details = details or {}


class ValidationError(BackendException):
    """Raised when input validation fails."""

    def __init__(self, message: str, details: Optional[dict[str, Any]] = None):
        super().__init__(
            message=message,
            status_code=400,
            error_code="VALIDATION_ERROR",
            details=details
        )


class NotFoundError(BackendException):
    """Raised when a resource is not found."""

    def __init__(self, message: str, resource_type: Optional[str] = None):
        super().__init__(
            message=message,
            status_code=404,
            error_code="NOT_FOUND",
            details={"resource_type": resource_type} if resource_type else {}
        )


class LLMError(BackendException):
    """Raised when LLM operations fail."""

    def __init__(self, message: str, details: Optional[dict[str, Any]] = None):
        super().__init__(
            message=message,
            status_code=500,
            error_code="LLM_ERROR",
            details=details
        )


class StorageError(BackendException):
    """Raised when storage operations fail."""

    def __init__(self, message: str, details: Optional[dict[str, Any]] = None):
        super().__init__(
            message=message,
            status_code=500,
            error_code="STORAGE_ERROR",
            details=details
        )


class MemoryError(BackendException):
    """Raised when memory operations fail."""

    def __init__(self, message: str, details: Optional[dict[str, Any]] = None):
        super().__init__(
            message=message,
            status_code=500,
            error_code="MEMORY_ERROR",
            details=details
        )


class ConfigurationError(BackendException):
    """Raised when configuration is invalid or missing."""

    def __init__(self, message: str, details: Optional[dict[str, Any]] = None):
        super().__init__(
            message=message,
            status_code=500,
            error_code="CONFIGURATION_ERROR",
            details=details
        )


class ServiceUnavailableError(BackendException):
    """Raised when a required service is unavailable."""

    def __init__(self, message: str, service_name: Optional[str] = None):
        super().__init__(
            message=message,
            status_code=503,
            error_code="SERVICE_UNAVAILABLE",
            details={"service_name": service_name} if service_name else {}
        )
