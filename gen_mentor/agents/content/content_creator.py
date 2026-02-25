from __future__ import annotations

from typing import Any, Mapping, Optional

from pydantic import BaseModel, Field, field_validator

from gen_mentor.agents.base_agent import BaseAgent
from gen_mentor.core.tools.retrieval.search_rag import SearchRagManager, format_docs
from gen_mentor.agents.content.prompts.content_creator import (
    learning_content_creator_system_prompt,
    learning_content_creator_task_prompt_content,
    learning_content_creator_task_prompt_draft,
    learning_content_creator_task_prompt_outline,
)
from gen_mentor.schemas import ContentOutline, KnowledgeDraft, LearningContent


class ContentBasePayload(BaseModel):
    learner_profile: Any
    learning_path: Any
    learning_session: Any
    external_resources: str | None = ""
    learning_goal: str = ""


class ContentDraftPayload(ContentBasePayload):
    document_section: Any


class LearningContentCreator(BaseAgent):
    name: str = "LearningContentCreator"

    def __init__(self, model: Any, *, search_rag_manager: Optional[SearchRagManager] = None):
        super().__init__(model=model, system_prompt=learning_content_creator_system_prompt, jsonalize_output=True)
        self.search_rag_manager = search_rag_manager

    def prepare_outline(self, payload: ContentBasePayload | Mapping[str, Any] | str):
        if not isinstance(payload, ContentBasePayload):
            payload = ContentBasePayload.model_validate(payload)
        raw_output = self.invoke(payload.model_dump(), task_prompt=learning_content_creator_task_prompt_outline)
        validated_output = ContentOutline.model_validate(raw_output)
        return validated_output.model_dump()

    def draft_section(self, payload: ContentDraftPayload | Mapping[str, Any] | str):
        if not isinstance(payload, ContentDraftPayload):
            payload = ContentDraftPayload.model_validate(payload)
        raw_output = self.invoke(payload.model_dump(), task_prompt=learning_content_creator_task_prompt_draft)
        validated_output = KnowledgeDraft.model_validate(raw_output)
        return validated_output.model_dump()

    def create_content(self, payload: ContentBasePayload | Mapping[str, Any] | str):
        if not isinstance(payload, ContentBasePayload):
            payload = ContentBasePayload.model_validate(payload)
        raw_output = self.invoke(payload.model_dump(), task_prompt=learning_content_creator_task_prompt_content)
        validated_output = LearningContent.model_validate(raw_output)
        return validated_output.model_dump()


def prepare_content_outline_with_llm(llm, learner_profile, learning_path, learning_session, learning_goal="", *, search_rag_manager: Optional[SearchRagManager] = None):
    creator = LearningContentCreator(llm, search_rag_manager=search_rag_manager)
    payload = {
        "learner_profile": learner_profile,
        "learning_path": learning_path,
        "learning_session": learning_session,
        "learning_goal": learning_goal,
    }
    return creator.prepare_outline(payload)


def create_learning_content_with_llm(
    llm,
    learner_profile,
    learning_path,
    learning_session,
    document_outline=None,
    allow_parallel=True,
    with_quiz=True,
    max_workers=3,
    use_search=True,
    output_markdown=True,
    method_name="genmentor",
    learning_goal="",
    *,
    search_rag_manager: Optional[SearchRagManager] = None,
):
    from .knowledge_explorer import explore_knowledge_points_with_llm
    from .knowledge_drafter import draft_knowledge_points_with_llm
    from .document_integrator import integrate_learning_document_with_llm
    from ..assessment.quiz_generator import generate_document_quizzes_with_llm

    if method_name == "genmentor":
        knowledge_points = explore_knowledge_points_with_llm(
            llm, learner_profile, learning_path, learning_session,
            learning_goal=learning_goal,
        )
        # Unwrap {"knowledge_points": [...]} to a plain list
        if isinstance(knowledge_points, dict) and "knowledge_points" in knowledge_points:
            knowledge_points = knowledge_points["knowledge_points"]
        knowledge_drafts = draft_knowledge_points_with_llm(
            llm,
            learner_profile,
            learning_path,
            learning_session,
            knowledge_points,
            allow_parallel=allow_parallel,
            use_search=use_search,
            max_workers=max_workers,
            learning_goal=learning_goal,
            search_rag_manager=search_rag_manager,
        )
        learning_document = integrate_learning_document_with_llm(
            llm,
            learner_profile,
            learning_path,
            learning_session,
            knowledge_points,
            knowledge_drafts,
            output_markdown=output_markdown,
            learning_goal=learning_goal,
        )
        learning_content = {"document": learning_document}
        if not with_quiz:
            return learning_content
        document_quiz = generate_document_quizzes_with_llm(
            llm,
            learner_profile,
            learning_document,
            single_choice_count=3,
            multiple_choice_count=0,
            true_false_count=0,
            short_answer_count=0,
            learning_goal=learning_goal,
        )
        learning_content["quizzes"] = document_quiz
        return learning_content
    else:
        creator = LearningContentCreator(llm, search_rag_manager=search_rag_manager)
        if document_outline is None:
            document_outline = prepare_content_outline_with_llm(
                llm,
                learner_profile,
                learning_path,
                learning_session,
                learning_goal=learning_goal,
                search_rag_manager=search_rag_manager,
            )
        outline = document_outline if isinstance(document_outline, dict) else document_outline
        payload = {
            "learner_profile": learner_profile,
            "learning_path": learning_path,
            "learning_session": learning_session,
            "external_resources": "",
            "learning_goal": learning_goal,
        }
        return creator.create_content(payload)
