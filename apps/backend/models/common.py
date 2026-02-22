"""
Common models and types shared across the API.
"""

from typing import Any, Optional
from pydantic import BaseModel, Field

from .defaults import DEFAULT_MODEL_PROVIDER, DEFAULT_MODEL_NAME


class BaseRequest(BaseModel):
    """Base request model with common fields."""

    model: Optional[str] = Field(
        default=f"{DEFAULT_MODEL_PROVIDER}/{DEFAULT_MODEL_NAME}",
        description="Model in 'provider/model' format (e.g., 'openai/gpt-4', 'anthropic/claude-3-5-sonnet', 'openai/gpt-5.1')"
    )

    def get_model_parts(self) -> tuple[str, str]:
        """Parse model string into provider and model name.

        Returns:
            Tuple of (provider, model_name)
        """
        if self.model and "/" in self.model:
            parts = self.model.split("/", 1)
            return parts[0], parts[1]
        # Default fallback
        return DEFAULT_MODEL_PROVIDER, self.model or DEFAULT_MODEL_NAME

    class Config:
        json_schema_extra = {
            "example": {
                "model": f"{DEFAULT_MODEL_PROVIDER}/{DEFAULT_MODEL_NAME}"
            }
        }


class BaseResponse(BaseModel):
    """Base response model with common fields."""

    success: bool = Field(default=True, description="Operation success status")
    message: Optional[str] = Field(default=None, description="Optional message")

    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Operation completed successfully"
            }
        }


class ErrorResponse(BaseModel):
    """Error response model."""

    success: bool = Field(default=False, description="Always false for errors")
    error_code: str = Field(..., description="Error code")
    message: str = Field(..., description="Error message")
    details: Optional[dict[str, Any]] = Field(default=None, description="Error details")

    class Config:
        json_schema_extra = {
            "example": {
                "success": False,
                "error_code": "VALIDATION_ERROR",
                "message": "Invalid input provided",
                "details": {"field": "learning_goal", "issue": "cannot be empty"}
            }
        }


class HealthResponse(BaseModel):
    """Health check response."""

    status: str = Field(..., description="Service status")
    version: str = Field(..., description="API version")
    timestamp: str = Field(..., description="Current timestamp")

    class Config:
        json_schema_extra = {
            "example": {
                "status": "healthy",
                "version": "1.0.0",
                "timestamp": "2024-01-15T10:30:00Z"
            }
        }


class StorageInfo(BaseModel):
    """Storage configuration information."""

    storage_mode: str = Field(..., description="Storage mode (local or cloud)")
    upload_location: Optional[str] = Field(None, description="Upload location for local storage")
    workspace_dir: Optional[str] = Field(None, description="Workspace directory for local storage")
    cloud_bucket: Optional[str] = Field(None, description="Cloud bucket name")
    cloud_region: Optional[str] = Field(None, description="Cloud region")

    class Config:
        json_schema_extra = {
            "example": {
                "storage_mode": "local",
                "upload_location": "/tmp/uploads/",
                "workspace_dir": "~/.gen-mentor/workspace",
                "cloud_bucket": None,
                "cloud_region": None
            }
        }
