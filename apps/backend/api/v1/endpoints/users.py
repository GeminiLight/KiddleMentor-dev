"""
Users endpoints - user listing, login, and sync.
"""

from typing import List, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from services.user_registry import get_user_registry

router = APIRouter()


# ---------------------------------------------------------------------------
# Pydantic models
# ---------------------------------------------------------------------------

class UserInfo(BaseModel):
    learner_id: str
    name: str
    email: Optional[str] = None
    created_at: Optional[str] = None


class UserListResponse(BaseModel):
    success: bool
    users: List[UserInfo]
    count: int


class LoginRequest(BaseModel):
    learner_id: str


class LoginResponse(BaseModel):
    success: bool
    learner_id: str
    name: str
    email: Optional[str] = None


class SyncResponse(BaseModel):
    success: bool
    synced_count: int


class DeleteRequest(BaseModel):
    learner_id: str


class DeleteResponse(BaseModel):
    success: bool
    message: str


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@router.get("/list", response_model=UserListResponse)
async def list_users():
    """List all registered users."""
    registry = get_user_registry()
    users = registry.list_users()
    return UserListResponse(
        success=True,
        users=[UserInfo(**u) for u in users],
        count=len(users),
    )


@router.post("/login", response_model=LoginResponse)
async def login_user(request: LoginRequest):
    """Login as an existing user by learner_id."""
    registry = get_user_registry()
    user = registry.get_user(request.learner_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return LoginResponse(
        success=True,
        learner_id=user["learner_id"],
        name=user.get("name", "Anonymous Learner"),
        email=user.get("email"),
    )


@router.post("/sync", response_model=SyncResponse)
async def sync_users():
    """Sync user registry from existing learner profiles on disk."""
    registry = get_user_registry()
    count = registry.sync_from_disk()
    return SyncResponse(success=True, synced_count=count)


@router.post("/delete", response_model=DeleteResponse)
async def delete_user(request: DeleteRequest):
    """Delete a user account and all associated learner data."""
    registry = get_user_registry()
    deleted = registry.delete_user(request.learner_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="User not found")
    return DeleteResponse(
        success=True,
        message=f"Account {request.learner_id} deleted successfully",
    )
