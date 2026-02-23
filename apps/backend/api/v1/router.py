"""
API v1 router - aggregates all v1 endpoints.
"""

from fastapi import APIRouter

from api.v1.endpoints import (
    system,
    chat,
    goals,
    skills,
    profile,
    learning_path,
    assessment,
    memory,
    dashboard,
    progress,
    users,
)

# Create main API router
api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(system.router, tags=["System"])
api_router.include_router(chat.router, prefix="/chat", tags=["Chat"])
api_router.include_router(goals.router, prefix="/goals", tags=["Goals"])
api_router.include_router(skills.router, prefix="/skills", tags=["Skills"])
api_router.include_router(profile.router, prefix="/profile", tags=["Profile", "Session"])
api_router.include_router(learning_path.router, prefix="/learning", tags=["Learning Path", "Content"])
api_router.include_router(assessment.router, prefix="/assessment", tags=["Assessment"])
api_router.include_router(memory.router, prefix="/memory", tags=["Memory"])
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["Dashboard"])
api_router.include_router(progress.router, prefix="/progress", tags=["Progress"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
