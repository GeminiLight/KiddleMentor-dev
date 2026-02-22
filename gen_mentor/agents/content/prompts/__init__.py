"""Content generation prompts."""

from .content_creator import *
from .path_scheduling import *
from .knowledge_exploration import *
from .document_integration import *
from .knowledge_drafting import *
from .feedback_simulation import *

__all__ = [
    "CONTENT_CREATOR_PROMPT",
    "LEARNING_PATH_SCHEDULING_PROMPT",
    "KNOWLEDGE_EXPLORATION_PROMPT",
    "LEARNING_DOCUMENT_INTEGRATION_PROMPT",
    "KNOWLEDGE_DRAFTING_PROMPT",
    "FEEDBACK_SIMULATION_PROMPT",
]
