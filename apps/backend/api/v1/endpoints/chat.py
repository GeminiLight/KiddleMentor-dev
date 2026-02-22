"""
Chat endpoints - AI tutor conversation.
"""

import json
from fastapi import APIRouter, Depends

from models import ChatWithTutorRequest, ChatResponse
from services.llm_service import get_llm_service, LLMService
from services.memory_service import get_memory_service, MemoryService
from dependencies import get_search_rag_manager, extract_learner_id
from gen_mentor.core.tools.retrieval.search_rag import SearchRagManager
from gen_mentor.agents.tutoring.chatbot import chat_with_tutor_with_llm
from exceptions import ValidationError, LLMError

router = APIRouter()


@router.post("/chat-with-tutor", response_model=ChatResponse, tags=["Chat"])
async def chat_with_tutor(
    request: ChatWithTutorRequest,
    llm_service: LLMService = Depends(get_llm_service),
    memory_service: MemoryService = Depends(get_memory_service),
    search_rag_manager: SearchRagManager = Depends(get_search_rag_manager)
):
    """Chat with AI tutor.

    Provides interactive conversational learning with personalized responses
    based on the learner's profile and history.

    Args:
        request: Chat request with messages and learner profile
        llm_service: LLM service dependency
        memory_service: Memory service dependency
        search_rag_manager: Search RAG manager dependency

    Returns:
        ChatResponse with tutor's response

    Raises:
        ValidationError: If request validation fails
        LLMError: If chat generation fails
    """
    # Get LLM
    llm = llm_service.get_llm(request.model)

    # Extract learner_id from profile
    learner_id = extract_learner_id(request.learner_profile)

    # Parse messages
    try:
        if isinstance(request.messages, str) and request.messages.strip().startswith("["):
            converted_messages = json.loads(request.messages)
        else:
            raise ValidationError(
                "messages must be a JSON array string",
                details={"field": "messages", "format": "JSON array"}
            )
    except Exception as e:
        raise ValidationError(
            f"Failed to parse messages: {str(e)}",
            details={"field": "messages"}
        )

    # Get last user message for logging
    last_message = converted_messages[-1] if converted_messages else {}

    # Get memory store for context-aware chat
    memory_store = memory_service.get_memory_store(learner_id) if learner_id else None

    # Load learner profile from memory if not provided
    learner_profile = request.learner_profile
    if not learner_profile and learner_id:
        learner_profile = memory_service.load_profile_from_memory(learner_id)

    # Generate response with memory context
    try:
        response = chat_with_tutor_with_llm(
            llm,
            converted_messages,
            learner_profile,
            search_rag_manager=search_rag_manager,
            memory_store=memory_store,  # Pass memory for context injection
            use_search=True,
        )
    except Exception as e:
        raise LLMError(
            f"Chat generation failed: {str(e)}",
            details={"error": str(e)}
        )

    # Log interaction to workspace memory
    if last_message.get("content"):
        memory_service.log_interaction(learner_id, "learner", last_message["content"])
        memory_service.log_interaction(learner_id, "tutor", response)

    return ChatResponse(success=True, response=response)
