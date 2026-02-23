from __future__ import annotations

import ast
import json
from typing import Any, Mapping, Optional, List
from concurrent.futures import ThreadPoolExecutor

from pydantic import BaseModel, field_validator

from gen_mentor.agents.base_agent import BaseAgent
from gen_mentor.core.tools.retrieval.search_rag import SearchRagManager, format_docs
from gen_mentor.agents.content.prompts.knowledge_drafting import (
    search_enhanced_knowledge_drafter_system_prompt,
    search_enhanced_knowledge_drafter_task_prompt,
)
from gen_mentor.schemas import KnowledgeDraft
from gen_mentor.config import default_config


class KnowledgeDraftPayload(BaseModel):
    learner_profile: Any
    learning_path: Any
    learning_session: Any
    knowledge_points: Any
    knowledge_point: Any
    external_resources: str | None = ""
    learning_goal: str = ""

    @field_validator("learner_profile", "learning_path", "learning_session", "knowledge_points", "knowledge_point")
    @classmethod
    def coerce_jsonish(cls, v: Any) -> Any:
        if isinstance(v, BaseModel):
            return v.model_dump()
        if isinstance(v, Mapping):
            return dict(v)
        if isinstance(v, str):
            return v.strip()
        return v


class SearchEnhancedKnowledgeDrafter(BaseAgent):

    name: str = "SearchEnhancedKnowledgeDrafter"

    def __init__(self, model: Any, *, search_rag_manager: Optional[SearchRagManager] = None, use_search: bool = True):
        super().__init__(model=model, system_prompt=search_enhanced_knowledge_drafter_system_prompt, jsonalize_output=True)
        if search_rag_manager is not None:
            self.search_rag_manager = search_rag_manager
        elif use_search:
            self.search_rag_manager = SearchRagManager.from_config(default_config.model_dump() if hasattr(default_config, 'model_dump') else default_config)
        else:
            self.search_rag_manager = None
        self.use_search = use_search

    def draft(self, payload: KnowledgeDraftPayload | Mapping[str, Any] | str):
        if not isinstance(payload, KnowledgeDraftPayload):
            payload = KnowledgeDraftPayload.model_validate(payload)
        data = payload.model_dump()
        # Optionally enrich external resources using the search RAG manager
        if self.use_search and self.search_rag_manager is not None:
            session = data.get("learning_session") or {}
            session_title = str(session.get("title", "")).strip() or "learning_session"
            knowledge_point = data.get("knowledge_point") or {}
            knowledge_point_name = str(knowledge_point.get('name', '')).strip()
            query = f"{session_title} {knowledge_point_name}".strip()
            docs = self.search_rag_manager.invoke(query)
            context = format_docs(docs)
            if context:
                ext = data.get("external_resources") or ""
                data["external_resources"] = f"{ext}{context}"
        raw_output = self.invoke(data, task_prompt=search_enhanced_knowledge_drafter_task_prompt)
        validated_output = KnowledgeDraft.model_validate(raw_output)
        return validated_output.model_dump()

def draft_knowledge_point_with_llm(
    llm,
    learner_profile,
    learning_path,
    learning_session,
    knowledge_points,
    knowledge_point,
    use_search: bool = True,
    learning_goal: str = "",
    *,
    search_rag_manager: Optional[SearchRagManager] = None,
):
    """Draft a single knowledge point using the agent, optionally enriching with a SearchRagManager."""
    drafter = SearchEnhancedKnowledgeDrafter(llm, search_rag_manager=search_rag_manager, use_search=use_search)
    payload = {
        "learner_profile": learner_profile,
        "learning_path": learning_path,
        "learning_session": learning_session,
        "knowledge_points": knowledge_points,
        "knowledge_point": knowledge_point,
        "learning_goal": learning_goal,
    }
    return drafter.draft(payload)


def draft_knowledge_points_with_llm(
    llm,
    learner_profile,
    learning_path,
    learning_session,
    knowledge_points,
    allow_parallel: bool = True,
    use_search: bool = True,
    max_workers: int = 8,
    learning_goal: str = "",
    *,
    search_rag_manager: Optional[SearchRagManager] = None,
):
    """Draft multiple knowledge points in parallel or sequentially using the agent."""
    if isinstance(learning_session, str):
        try:
            learning_session = json.loads(learning_session)
        except (json.JSONDecodeError, ValueError):
            learning_session = ast.literal_eval(learning_session)
    if isinstance(knowledge_points, str):
        try:
            knowledge_points = json.loads(knowledge_points)
        except (json.JSONDecodeError, ValueError):
            knowledge_points = ast.literal_eval(knowledge_points)
    if search_rag_manager is None and use_search:
        search_rag_manager = SearchRagManager.from_config(default_config.model_dump() if hasattr(default_config, 'model_dump') else default_config)
    def draft_one(kp):
        return draft_knowledge_point_with_llm(
            llm,
            learner_profile,
            learning_path,
            learning_session,
            knowledge_points,
            kp,
            use_search=use_search,
            learning_goal=learning_goal,
            search_rag_manager=search_rag_manager,
        )

    if allow_parallel:
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            return list(executor.map(draft_one, knowledge_points))
    else:
        results: List[Any] = []
        for kp in knowledge_points:
            results.append(draft_one(kp))
        return results


if __name__ == "__main__":
    from gen_mentor.config import default_config
    from gen_mentor.core.llm.factory import LLMFactory
    import logging

    llm = LLMFactory.from_config(default_config.llm)
    search_rag_manager = SearchRagManager.from_config(default_config)
    logging.basicConfig(level=default_config.log_level)
    logger = logging.getLogger(__name__)

    learner_profile = {"name": "Alice", "level": "intermediate"}
    learning_path = {"title": "Data Science Basics"}
    learning_session = {"title": "Introduction to Pandas"}
    knowledge_points = [
        {"name": "Pandas DataFrames"},
        {"name": "Data Cleaning with Pandas"},
    ]

    drafts = draft_knowledge_points_with_llm(
        llm,
        learner_profile,
        learning_path,
        learning_session,
        knowledge_points,
        allow_parallel=True,
        use_search=True,
    )

    for draft in drafts:
        logger.info(f"Drafted Knowledge Point: {draft}")