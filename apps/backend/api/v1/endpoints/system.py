"""
System endpoints - health, storage info, model listing.
"""

from fastapi import APIRouter, Depends
from datetime import datetime

from models import HealthResponse, StorageInfo, LLMModelsResponse, LLMModel
from services.llm_service import get_llm_service, LLMService
from config import get_backend_settings, BackendSettings

router = APIRouter()


@router.get("/health", response_model=HealthResponse, tags=["System"])
async def health_check():
    """Health check endpoint.

    Returns the current status and version of the API.
    """
    return HealthResponse(
        status="healthy",
        version="1.0.0",
        timestamp=datetime.now().isoformat()
    )


@router.get("/storage-info", response_model=StorageInfo, tags=["System"])
async def get_storage_info(
    settings: BackendSettings = Depends(get_backend_settings)
):
    """Get storage configuration information.

    Returns details about the current storage mode and configuration.
    """
    return StorageInfo(
        storage_mode=settings.storage_mode,
        upload_location=str(settings.upload_location) if settings.storage_mode == "local" else None,
        workspace_dir=str(settings.workspace_dir) if settings.storage_mode == "local" else None,
        cloud_bucket=settings.cloud_bucket if settings.storage_mode == "cloud" else None,
        cloud_region=settings.cloud_region if settings.storage_mode == "cloud" else None,
    )


@router.get("/list-llm-models", response_model=LLMModelsResponse, tags=["System"])
async def list_llm_models(
    llm_service: LLMService = Depends(get_llm_service)
):
    """List available LLM models.

    Returns a list of configured LLM models that can be used for generation.
    """
    models_data = llm_service.list_available_models()
    models = [LLMModel(**model) for model in models_data]
    return LLMModelsResponse(
        success=True,
        message="Models retrieved successfully",
        models=models
    )
