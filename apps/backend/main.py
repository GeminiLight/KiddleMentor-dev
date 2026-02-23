"""
GenMentor Backend - Refactored Entry Point

Modular FastAPI application using the refactored architecture.
"""

import os
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Configuration and core
from config import get_backend_settings, get_app_config
from middleware.error_handler import setup_error_handlers
from api.v1.router import api_router

# Initialize configuration
backend_settings = get_backend_settings()
app_config = get_app_config()

# Create FastAPI application
app = FastAPI(
    title="GenMentor API",
    description="Personalized AI-powered learning platform",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# Setup CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=backend_settings.cors_origins,
    allow_credentials=backend_settings.cors_allow_credentials,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Setup error handlers
setup_error_handlers(app)


# Root endpoint
@app.get("/", include_in_schema=False)
async def root():
    """Root endpoint - API information."""
    return {
        "message": "GenMentor API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": f"{backend_settings.api_prefix}/health",
        "api_prefix": backend_settings.api_prefix,
    }


# Include API router
app.include_router(api_router, prefix=backend_settings.api_prefix)


# Startup event
@app.on_event("startup")
async def startup_event():
    """Run on application startup."""
    print("\n" + "="*60)
    print("  GenMentor API Starting")
    print("="*60)
    print(f"  Environment: {app_config.environment}")
    print(f"  Debug Mode: {backend_settings.debug}")
    print(f"  Storage Mode: {backend_settings.storage_mode}")
    print(f"  Workspace: {backend_settings.workspace_dir}")
    print(f"  API Prefix: {backend_settings.api_prefix}")
    print(f"  CORS Origins: {backend_settings.cors_origins}")
    print("="*60)

    # Ensure upload directory exists
    if backend_settings.storage_mode == "local":
        os.makedirs(backend_settings.expanded_upload_location, exist_ok=True)
        print(f"  ✓ Upload directory ready: {backend_settings.upload_location}")

    # Ensure workspace directory exists
    if backend_settings.storage_mode == "local":
        os.makedirs(backend_settings.expanded_workspace_dir, exist_ok=True)
        print(f"  ✓ Workspace directory ready: {backend_settings.workspace_dir}")

    # Sync user registry from existing learner profiles
    from services.user_registry import get_user_registry
    registry = get_user_registry()
    synced = registry.sync_from_disk()
    print(f"  ✓ User registry synced: {synced} users found")

    print("="*60 + "\n")


# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Run on application shutdown."""
    print("\n" + "="*60)
    print("  GenMentor API Shutting Down")
    print("="*60 + "\n")


# Main entry point
def main():
    """Run the application."""
    log_level = "debug" if backend_settings.debug else "info"

    print("\nStarting GenMentor Backend API...")
    print(f"Server: http://{backend_settings.host}:{backend_settings.port}")
    print(f"Docs: http://{backend_settings.host}:{backend_settings.port}/docs")
    print(f"ReDoc: http://{backend_settings.host}:{backend_settings.port}/redoc\n")

    uvicorn.run(
        "main:app",
        host=backend_settings.host,
        port=backend_settings.port,
        reload=backend_settings.reload,
        log_level=log_level,
        access_log=True,
    )


if __name__ == "__main__":
    main()
