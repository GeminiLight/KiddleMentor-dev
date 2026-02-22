"""Performance evaluator agent for assessing learner progress and performance."""

from __future__ import annotations

from typing import Any, Dict, Optional

from langchain_core.language_models import BaseChatModel

from gen_mentor.agents.base_agent import BaseAgent
from gen_mentor.schemas import LearnerProfile, LearningPath, SkillGap


def evaluate_learner_performance_with_llm(
    llm: BaseChatModel,
    learner_profile: Dict[str, Any],
    learning_path: Dict[str, Any],
    session_data: Dict[str, Any],
    quiz_results: Optional[Dict[str, Any]] = None,
    task_prompt: Optional[str] = None,
) -> Dict[str, Any]:
    """Evaluate learner performance based on profile, path, and quiz results.

    Args:
        llm: Language model to use
        learner_profile: Current learner profile with cognitive status
        learning_path: The learning path being followed
        session_data: Data from the learning session
        quiz_results: Optional quiz results for assessment
        task_prompt: Optional custom task prompt

    Returns:
        Performance evaluation with metrics and recommendations
    """
    from gen_mentor.agents.assessment.prompts.performance_evaluation import (
        PERFORMANCE_EVALUATION_PROMPT,
    )

    if task_prompt is None:
        task_prompt = PERFORMANCE_EVALUATION_PROMPT

    # Create agent
    agent = BaseAgent(
        model=llm,
        system_prompt="You are an expert learning performance evaluator. Analyze learner progress, identify strengths and weaknesses, and provide actionable recommendations.",
        tools=[],
        jsonalize_output=True,
    )

    # Prepare input
    input_dict = {
        "learner_profile": learner_profile,
        "learning_path": learning_path,
        "session_data": session_data,
        "quiz_results": quiz_results or {},
    }

    # Invoke agent
    result = agent.invoke(input_dict=input_dict, task_prompt=task_prompt)

    return result


def evaluate_skill_mastery_with_llm(
    llm: BaseChatModel,
    skill_name: str,
    learner_responses: Dict[str, Any],
    quiz_results: Optional[Dict[str, Any]] = None,
    previous_attempts: Optional[list] = None,
) -> Dict[str, Any]:
    """Evaluate mastery level of a specific skill.

    Args:
        llm: Language model to use
        skill_name: Name of the skill being evaluated
        learner_responses: Learner's responses and interactions
        quiz_results: Optional quiz results for the skill
        previous_attempts: Optional history of previous attempts

    Returns:
        Skill mastery evaluation with level and confidence
    """
    from gen_mentor.agents.assessment.prompts.performance_evaluation import (
        SKILL_MASTERY_EVALUATION_PROMPT,
    )

    agent = BaseAgent(
        model=llm,
        system_prompt="You are an expert skill mastery evaluator. Assess learner's understanding and proficiency in specific skills.",
        tools=[],
        jsonalize_output=True,
    )

    input_dict = {
        "skill_name": skill_name,
        "learner_responses": learner_responses,
        "quiz_results": quiz_results or {},
        "previous_attempts": previous_attempts or [],
    }

    result = agent.invoke(
        input_dict=input_dict,
        task_prompt=SKILL_MASTERY_EVALUATION_PROMPT
    )

    return result


def generate_performance_report_with_llm(
    llm: BaseChatModel,
    learner_profile: Dict[str, Any],
    performance_history: list[Dict[str, Any]],
    time_period: str = "current session",
) -> str:
    """Generate a comprehensive performance report.

    Args:
        llm: Language model to use
        learner_profile: Current learner profile
        performance_history: List of performance evaluations over time
        time_period: Time period for the report (e.g., "week", "month", "current session")

    Returns:
        Formatted performance report
    """
    from gen_mentor.agents.assessment.prompts.performance_evaluation import (
        PERFORMANCE_REPORT_PROMPT,
    )

    agent = BaseAgent(
        model=llm,
        system_prompt="You are an expert educational report writer. Create clear, actionable performance reports.",
        tools=[],
        jsonalize_output=False,
    )

    input_dict = {
        "learner_profile": learner_profile,
        "performance_history": performance_history,
        "time_period": time_period,
    }

    result = agent.invoke(
        input_dict=input_dict,
        task_prompt=PERFORMANCE_REPORT_PROMPT
    )

    return result


__all__ = [
    "evaluate_learner_performance_with_llm",
    "evaluate_skill_mastery_with_llm",
    "generate_performance_report_with_llm",
]
