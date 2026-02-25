"""Tutoring-related schemas for chatbot interactions."""

from __future__ import annotations

from typing import Any, List, Literal, Mapping, Optional

from pydantic import BaseModel, Field, field_validator


class ChatMessage(BaseModel):
    """A single chat message in the conversation."""
    role: Literal["user", "assistant", "system"] = Field(..., description="Role of the message sender")
    content: str = Field(..., description="Content of the message")


class TutorChatPayload(BaseModel):
    """Payload for tutor chatbot interactions."""
    learner_profile: Any = Field(default="", description="Learner profile information")
    messages: Any = Field(..., description="Conversation history")
    use_search: bool = Field(default=True, description="Whether to use web search for context")
    top_k: int = Field(default=5, description="Number of documents to retrieve")
    external_resources: Optional[str] = Field(default=None, description="Additional external resources")

    @field_validator("learner_profile")
    @classmethod
    def coerce_profile(cls, v: Any) -> Any:
        """Coerce learner profile to dict format."""
        if isinstance(v, BaseModel):
            return v.model_dump()
        if isinstance(v, Mapping):
            return dict(v)
        return v


class TutorResponse(BaseModel):
    """Response from the tutor chatbot."""
    response: str = Field(..., description="The tutor's response text")
    sources: Optional[List[str]] = Field(default=None, description="Sources used for the response")
    follow_up_questions: Optional[List[str]] = Field(default=None, description="Suggested follow-up questions")


def parse_tutor_response(data: Any) -> TutorResponse:
    """Parse tutor response from various formats."""
    if isinstance(data, str):
        return TutorResponse(response=data)
    if isinstance(data, dict):
        return TutorResponse.model_validate(data)
    if isinstance(data, BaseModel):
        return TutorResponse.model_validate(data.model_dump())
    return TutorResponse(response=str(data))


__all__ = [
    "ChatMessage",
    "TutorChatPayload",
    "TutorResponse",
    "parse_tutor_response",
]
