from __future__ import annotations

from typing import Any, Mapping

from pydantic import BaseModel, Field, field_validator

from gen_mentor.agents.base_agent import BaseAgent
from gen_mentor.agents.assessment.prompts.quiz_generation import (
    document_quiz_generator_system_prompt,
    document_quiz_generator_task_prompt,
)
from gen_mentor.schemas import DocumentQuiz, DocumentQuizPayload


class DocumentQuizGenerator(BaseAgent):
    name: str = "DocumentQuizGenerator"

    def __init__(self, model: Any):
        super().__init__(model=model, system_prompt=document_quiz_generator_system_prompt, jsonalize_output=True)

    def generate(self, payload: DocumentQuizPayload | Mapping[str, Any] | str, *, learning_goal: str = ""):
        if not isinstance(payload, DocumentQuizPayload):
            payload = DocumentQuizPayload.model_validate(payload)
        data = payload.model_dump()
        data["learning_goal"] = learning_goal
        raw_output = self.invoke(data, task_prompt=document_quiz_generator_task_prompt)
        validated_output = DocumentQuiz.model_validate(raw_output)
        return validated_output.model_dump()


def generate_document_quizzes_with_llm(
    llm,
    learner_profile,
    learning_document,
    single_choice_count: int = 3,
    multiple_choice_count: int = 0,
    true_false_count: int = 0,
    short_answer_count: int = 0,
    learning_goal: str = "",
):
    payload = {
        "learner_profile": learner_profile,
        "learning_document": learning_document,
        "single_choice_count": single_choice_count,
        "multiple_choice_count": multiple_choice_count,
        "true_false_count": true_false_count,
        "short_answer_count": short_answer_count,
    }
    gen = DocumentQuizGenerator(llm)
    return gen.generate(payload, learning_goal=learning_goal)
