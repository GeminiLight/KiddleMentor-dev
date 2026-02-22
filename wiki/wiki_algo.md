# GenMentor Algorithm Documentation

## Table of Contents

1. [Overview](#1-overview)
2. [Architecture](#2-architecture)
3. [Core Infrastructure](#3-core-infrastructure)
4. [Learning Agents](#4-learning-agents)
5. [Content Agents](#5-content-agents)
6. [Tutoring Agents](#6-tutoring-agents)
7. [Assessment Agents](#7-assessment-agents)
8. [Schema System](#8-schema-system)
9. [Memory System](#9-memory-system)
10. [RAG & Search System](#10-rag--search-system)
11. [Complete Workflows](#11-complete-workflows)
12. [Configuration](#12-configuration)

---

## 1. Overview

GenMentor is an intelligent tutoring system (ITS) that leverages Large Language Models (LLMs) to provide personalized, adaptive learning experiences. The system implements a multi-agent architecture where specialized agents handle different aspects of the learning process.

### 1.1 Key Features

- **Goal-Oriented Learning**: Learners define learning goals that guide the entire system
- **Adaptive Profiling**: Dynamic learner profiles that evolve based on interactions
- **Personalized Content**: Learning materials tailored to individual needs
- **Intelligent Tutoring**: Interactive chatbot with context-aware responses
- **Performance Assessment**: Comprehensive evaluation and feedback mechanisms

### 1.2 Design Principles

1. **Modularity**: Each agent is self-contained with clear interfaces
2. **Extensibility**: Easy to add new agents or modify existing ones
3. **Type Safety**: Pydantic schemas ensure data validation throughout
4. **Configuration-Driven**: Flexible configuration via YAML files

---

## 2. Architecture

### 2.1 System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           GenMentor System                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                         Application Layer                            │   │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────────┐  │   │
│  │  │   CLI App    │  │  FastAPI     │  │   Streamlit Frontend     │  │   │
│  │  │  (cli/main)  │  │  (backend)   │  │   (frontend_streamlit)   │  │   │
│  │  └──────────────┘  └──────────────┘  └──────────────────────────┘  │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                        │
│  ┌─────────────────────────────────▼───────────────────────────────────┐   │
│  │                          Agent Layer                                 │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌───────────┐  │   │
│  │  │  Learning   │  │   Content   │  │  Tutoring   │  │ Assessment│  │   │
│  │  │   Agents    │  │   Agents    │  │   Agents    │  │  Agents   │  │   │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └───────────┘  │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                        │
│  ┌─────────────────────────────────▼───────────────────────────────────┐   │
│  │                          Core Layer                                  │   │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────────┐  │   │
│  │  │ LLM Factory  │  │ Memory Store │  │    RAG & Search System   │  │   │
│  │  │  (core/llm)  │  │ (core/memory)│  │   (core/tools/retrieval) │  │   │
│  │  └──────────────┘  └──────────────┘  └──────────────────────────┘  │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                        │
│  ┌─────────────────────────────────▼───────────────────────────────────┐   │
│  │                       Foundation Layer                               │   │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────────┐  │   │
│  │  │   Schemas    │  │   Config     │  │       Utilities          │  │   │
│  │  │  (schemas/)  │  │  (config/)   │  │       (utils/)           │  │   │
│  │  └──────────────┘  └──────────────┘  └──────────────────────────┘  │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 2.2 Package Structure

```
gen_mentor/
├── agents/                    # Agent implementations
│   ├── base_agent.py         # Base agent class
│   ├── learning/             # Learning & profiling agents
│   ├── content/              # Content generation agents
│   ├── tutoring/             # Chatbot tutoring agents
│   └── assessment/           # Quiz & evaluation agents
├── core/                     # Core infrastructure
│   ├── llm/                  # LLM factory
│   ├── memory/               # Memory storage
│   ├── base/                 # Base classes
│   └── tools/                # RAG, search, embedding tools
├── schemas/                  # Pydantic data models
├── config/                   # Configuration management
├── cli/                      # CLI interface
└── utils/                    # Helper utilities
```

---

## 3. Core Infrastructure

### 3.1 Base Agent Class

All agents inherit from `BaseAgent`, which provides a unified interface for LLM interactions.

```python
class BaseAgent:
    def __init__(
        self,
        model: BaseChatModel,
        system_prompt: Optional[str] = None,
        tools: Optional[list[Any]] = None,
        **kwargs
    ):
        """Initialize agent with LLM model and prompts."""
        self._model = model
        self._system_prompt = system_prompt
        self._agent = self._build_agent()
        self.jsonalize_output = kwargs.get("jsonalize_output", True)

    def invoke(self, input_dict: dict, task_prompt: Optional[str] = None) -> Any:
        """Execute agent with input and return processed output."""
        input_prompt = self._build_prompt(input_dict, task_prompt)
        raw_output = self._agent.invoke(input_prompt)
        return preprocess_response(raw_output, json_output=self.jsonalize_output)
```

**Key Features:**
- Automatic JSON output parsing
- Think-tag exclusion for reasoning models
- Consistent prompt building
- Validation integration

### 3.2 LLM Factory

The `LLMFactory` provides a unified interface for creating LLM instances.

```python
class LLMFactory:
    @staticmethod
    def create(
        model: str = "anthropic/claude-3-5-sonnet-20241022",
        temperature: float = 0,
        base_url: Optional[str] = None,
        **kwargs
    ) -> BaseChatModel:
        """Create LLM instance with specified parameters.
        
        Args:
            model: Model identifier in "provider/model" format.
                   Examples: "openai/gpt-4", "anthropic/claude-3-5-sonnet",
                            "deepseek/deepseek-chat"
                   If only model name is provided (e.g., "gpt-4"), 
                   falls back to default provider.
        """
        # Parse "provider/model" format
        if "/" in model:
            model_provider, model_name = model.split("/", 1)
        else:
            model_provider = DEFAULT_MODEL_PROVIDER
            model_name = model
        
        return init_chat_model(
            model=model_name,
            model_provider=model_provider,
            temperature=temperature,
            **kwargs
        )
```

**Supported Model Formats:**
- `"openai/gpt-4"` - OpenAI GPT-4
- `"openai/gpt-3.5-turbo"` - OpenAI GPT-3.5 Turbo
- `"anthropic/claude-3-5-sonnet"` - Anthropic Claude 3.5 Sonnet
- `"anthropic/claude-3-opus"` - Anthropic Claude 3 Opus
- `"deepseek/deepseek-chat"` - DeepSeek Chat
- `"deepseek/deepseek-coder"` - DeepSeek Coder
- `"ollama/llama3"` - Ollama local models
- Custom endpoints (VLLM, etc.)

---

## 4. Learning Agents

Learning agents handle learner profiling, goal refinement, and skill gap identification.

### 4.1 Goal Refiner

**Purpose:** Refines raw learning goals into structured, actionable objectives.

```python
def refine_learning_goal_with_llm(
    llm: Any,
    learning_goal: str,
    learner_information: str = "",
) -> JSONDict:
    """Refine a learner's goal using the provided LLM."""
    refiner = LearningGoalRefiner(llm)
    return refiner.refine_goal({
        "learning_goal": learning_goal,
        "learner_information": learner_information,
    })
```

**Algorithm Flow:**
```
Input: learning_goal (str), learner_information (str)
    │
    ▼
┌─────────────────────────────────────┐
│  LearningGoalRefiner Agent          │
│  ┌─────────────────────────────┐    │
│  │ Validate Input Payload      │    │
│  │ (RefineGoalPayload)         │    │
│  └─────────────────────────────┘    │
│              │                       │
│              ▼                       │
│  ┌─────────────────────────────┐    │
│  │ Format Task Prompt          │    │
│  │ with input variables        │    │
│  └─────────────────────────────┘    │
│              │                       │
│              ▼                       │
│  ┌─────────────────────────────┐    │
│  │ Invoke LLM with             │    │
│  │ system + task prompts       │    │
│  └─────────────────────────────┘    │
│              │                       │
│              ▼                       │
│  ┌─────────────────────────────┐    │
│  │ Parse & Validate            │    │
│  │ RefinedLearningGoal schema  │    │
│  └─────────────────────────────┘    │
└─────────────────────────────────────┘
    │
    ▼
Output: {"refined_goal": "..."}
```

**Output Schema:**
```python
class RefinedLearningGoal(BaseModel):
    refined_goal: str
```

### 4.2 Skill Gap Identifier

**Purpose:** Identifies gaps between current skills and required skills for the learning goal.

```python
def identify_skill_gap_with_llm(
    llm: Any,
    learning_goal: str,
    learner_information: str,
    skill_requirements: Optional[Dict[str, Any]] = None,
) -> Tuple[JSONDict, JSONDict]:
    """Identify skill gaps and return both gaps and skill requirements."""
    
    # Compute requirements if not provided
    if not skill_requirements:
        mapper = SkillRequirementMapper(llm)
        effective_requirements = mapper.map_goal_to_skill({"learning_goal": learning_goal})
    else:
        effective_requirements = skill_requirements

    skill_gap_identifier = SkillGapIdentifier(llm)
    skill_gaps = skill_gap_identifier.identify_skill_gap({
        "learning_goal": learning_goal,
        "learner_information": learner_information,
        "skill_requirements": effective_requirements,
    })
    return skill_gaps, effective_requirements
```

**Algorithm Flow:**
```
Input: learning_goal, learner_information, [skill_requirements]
    │
    ├── [No skill_requirements provided] ──▶ SkillRequirementMapper
    │                                              │
    │                                              ▼
    │                                    Generate skill requirements
    │                                    from learning goal
    │                                              │
    └──────────────────────────────────────────────┘
                        │
                        ▼
         ┌──────────────────────────────────────┐
         │     SkillGapIdentifier Agent         │
         │                                      │
         │  1. Compare current skills vs        │
         │     required skills                  │
         │  2. Determine gap status for each    │
         │  3. Calculate confidence level       │
         │  4. Generate rationale               │
         └──────────────────────────────────────┘
                        │
                        ▼
Output: SkillGaps, SkillRequirements
```

**Output Schema:**
```python
class SkillGap(BaseModel):
    name: str
    is_gap: bool
    required_level: LevelRequired  # beginner|intermediate|advanced
    current_level: LevelCurrent    # unlearned|beginner|intermediate|advanced
    reason: str                    # ≤20 words rationale
    level_confidence: Confidence   # low|medium|high

class SkillGaps(BaseModel):
    skill_gaps: List[SkillGap]  # 1-10 items
```

### 4.3 Learner Profiler

**Purpose:** Creates and maintains comprehensive learner profiles.

```python
def initialize_learner_profile_with_llm(
    llm: Any,
    learning_goal: str,
    learner_information: Union[str, Mapping[str, Any]],
    skill_gaps: Union[str, Mapping[str, Any], List[Any]],
) -> Dict[str, Any]:
    """Generate initial learner profile."""
    learner_profiler = AdaptiveLearnerProfiler(llm)
    return learner_profiler.initialize_profile({
        "learning_goal": learning_goal,
        "learner_information": learner_information,
        "skill_gaps": skill_gaps,
    })

def update_learner_profile_with_llm(
    llm: Any,
    learner_profile: Mapping[str, Any],
    learner_interactions: Mapping[str, Any],
    learner_information: Mapping[str, Any],
    session_information: Optional[Mapping[str, Any]] = None,
) -> Dict[str, Any]:
    """Update existing learner profile with new interactions."""
    learner_profiler = AdaptiveLearnerProfiler(llm)
    return learner_profiler.update_profile({
        "learner_profile": learner_profile,
        "learner_interactions": learner_interactions,
        "learner_information": learner_information,
        "session_information": session_information,
    })
```

**Profile Structure:**
```python
class LearnerProfile(BaseModel):
    learner_information: str       # Summary of learner context
    learning_goal: str             # Learning objective
    cognitive_status: CognitiveStatus     # Skills mastery status
    learning_preferences: LearningPreferences  # Content/activity preferences
    behavioral_patterns: BehavioralPatterns    # Usage patterns

class CognitiveStatus(BaseModel):
    overall_progress: int          # 0-100
    mastered_skills: List[MasteredSkill]
    in_progress_skills: List[InProgressSkill]

class LearningPreferences(BaseModel):
    content_style: str            # e.g., "Concise summaries"
    activity_type: str            # e.g., "Interactive exercises"
    additional_notes: Optional[str]

class BehavioralPatterns(BaseModel):
    system_usage_frequency: str
    session_duration_engagement: str
    motivational_triggers: Optional[str]
```

**Profiling Algorithm:**
```
┌──────────────────────────────────────────────────────────────────┐
│                  Adaptive Learner Profiler                       │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  INITIALIZATION PHASE:                                           │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ 1. Parse learner information (resume, background)          │ │
│  │ 2. Identify relevant skills from learning goal             │ │
│  │ 3. Map skill gaps to mastered/in-progress categories       │ │
│  │ 4. Infer learning preferences from context                 │ │
│  │ 5. Initialize behavioral patterns with defaults            │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                  │
│  UPDATE PHASE:                                                   │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ 1. Analyze recent interactions                             │ │
│  │ 2. Check session completion status                         │ │
│  │ 3. Update skill proficiency levels                         │ │
│  │ 4. Move skills to mastered if level achieved               │ │
│  │ 5. Adjust preferences based on engagement                  │ │
│  │ 6. Update behavioral metrics                               │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

### 4.4 Behavior Simulator

**Purpose:** Simulates learner interactions for testing and evaluation.

```python
def simulate_learner_interactions_with_llm(
    llm: Any,
    ground_truth_profile: Mapping[str, Any],
    session_count: int = 5,
) -> List[Dict[str, Any]]:
    """Simulate interactions for multiple sessions."""
    simulator = LearnerInteractionSimulator(llm)
    behavior_logs = []
    
    for session in range(1, session_count + 1):
        behavior_log = simulator.simulate_interactions({
            "ground_truth_profile": ground_truth_profile,
            "session_number": session,
        })
        behavior_logs.append(behavior_log)
    
    return behavior_logs
```

**Output Schema:**
```python
class LearnerBehaviorLog(BaseModel):
    session_number: int
    interactions: List[Dict[str, Any]]
    notes: Optional[str]
```

---

## 5. Content Agents

Content agents handle learning path scheduling, knowledge exploration, and content generation.

### 5.1 Path Scheduler

**Purpose:** Creates and manages personalized learning paths.

```python
def schedule_learning_path_with_llm(
    llm: Any,
    learner_profile: Mapping[str, Any],
    session_count: int = 0,
) -> JSONDict:
    """Create a new learning path based on learner profile."""
    scheduler = LearningPathScheduler(llm)
    return scheduler.schedule_session({
        "learner_profile": learner_profile,
        "session_count": session_count,
    })

def reschedule_learning_path_with_llm(
    llm: Any,
    learning_path: Sequence[Any],
    learner_profile: Mapping[str, Any],
    session_count: Optional[int] = None,
    other_feedback: Optional[Mapping[str, Any]] = None,
) -> JSONDict:
    """Reschedule existing learning path based on feedback."""
    scheduler = LearningPathScheduler(llm)
    return scheduler.reschedule({
        "learner_profile": learner_profile,
        "learning_path": learning_path,
        "session_count": session_count,
        "other_feedback": other_feedback,
    })
```

**Output Schema:**
```python
class SessionItem(BaseModel):
    id: str                          # "Session 1"
    title: str
    abstract: str
    if_learned: bool
    associated_skills: List[str]
    desired_outcome_when_completed: List[DesiredOutcome]

class LearningPath(BaseModel):
    learning_path: List[SessionItem]  # 1-10 sessions

class DesiredOutcome(BaseModel):
    name: str                         # Skill name
    level: Proficiency               # beginner|intermediate|advanced
```

**Scheduling Algorithm:**
```
┌──────────────────────────────────────────────────────────────────┐
│                  Learning Path Scheduler                         │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  INPUT ANALYSIS:                                                 │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ • Parse learner profile (skills, preferences, gaps)        │ │
│  │ • Identify skill dependencies                              │ │
│  │ • Determine session count (explicit or inferred)           │ │
│  └────────────────────────────────────────────────────────────┘ │
│                              │                                   │
│                              ▼                                   │
│  PATH GENERATION:                                                │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ 1. Order skills by dependency (foundational → advanced)    │ │
│  │ 2. Group skills into sessions based on:                    │ │
│  │    - Logical relationships                                 │ │
│  │    - Session complexity limits                             │ │
│  │    - Learner preferences                                   │ │
│  │ 3. Generate session titles and abstracts                   │ │
│  │ 4. Define desired outcomes for each session                │ │
│  └────────────────────────────────────────────────────────────┘ │
│                              │                                   │
│                              ▼                                   │
│  OUTPUT VALIDATION:                                              │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ • Verify session count within limits (1-10)                │ │
│  │ • Ensure skill coverage                                    │ │
│  │ • Validate outcome consistency                             │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

### 5.2 Knowledge Explorer

**Purpose:** Explores and identifies key knowledge points for a learning session.

```python
def explore_knowledge_points_with_llm(
    llm: Any,
    learner_profile: Any,
    learning_path: Any,
    learning_session: Any,
) -> JSONDict:
    """Explore knowledge points for a session."""
    explorer = GoalOrientedKnowledgeExplorer(llm)
    return explorer.explore({
        "learner_profile": learner_profile,
        "learning_path": learning_path,
        "learning_session": learning_session,
    })
```

**Output Schema:**
```python
class KnowledgePoint(BaseModel):
    name: str
    type: KnowledgeType  # foundational|practical|strategic

class KnowledgePoints(BaseModel):
    knowledge_points: List[KnowledgePoint]
```

### 5.3 Knowledge Drafter

**Purpose:** Generates detailed content for each knowledge point.

```python
def draft_knowledge_points_with_llm(
    llm: Any,
    learner_profile: Any,
    learning_path: Any,
    learning_session: Any,
    knowledge_points: List[Any],
    allow_parallel: bool = True,
    use_search: bool = True,
    max_workers: int = 8,
    search_rag_manager: Optional[SearchRagManager] = None,
) -> List[Any]:
    """Draft multiple knowledge points in parallel or sequentially."""
    
    def draft_one(kp):
        return draft_knowledge_point_with_llm(
            llm, learner_profile, learning_path, learning_session,
            knowledge_points, kp, use_search=use_search,
            search_rag_manager=search_rag_manager,
        )

    if allow_parallel:
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            return list(executor.map(draft_one, knowledge_points))
    else:
        return [draft_one(kp) for kp in knowledge_points]
```

**Output Schema:**
```python
class KnowledgeDraft(BaseModel):
    title: str
    content: str
```

**Drafting Algorithm with RAG:**
```
┌──────────────────────────────────────────────────────────────────┐
│              Search-Enhanced Knowledge Drafter                   │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  For each knowledge point:                                       │
│                                                                  │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ 1. Build search query from:                                │ │
│  │    - Session title                                         │ │
│  │    - Knowledge point name                                  │ │
│  └────────────────────────────────────────────────────────────┘ │
│                              │                                   │
│                              ▼                                   │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ 2. Execute search (if use_search=True):                    │ │
│  │    • Web search via SearchRunner                           │ │
│  │    • Vector store retrieval                                │ │
│  │    • Combine and format results                            │ │
│  └────────────────────────────────────────────────────────────┘ │
│                              │                                   │
│                              ▼                                   │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ 3. Generate content:                                       │ │
│  │    • Use learner profile for personalization               │ │
│  │    • Incorporate external resources                        │ │
│  │    • Match knowledge type (foundational/practical/etc)     │ │
│  └────────────────────────────────────────────────────────────┘ │
│                              │                                   │
│                              ▼                                   │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ 4. Validate output:                                        │ │
│  │    • Check title and content presence                      │ │
│  │    • Validate against KnowledgeDraft schema                │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

### 5.4 Document Integrator

**Purpose:** Integrates all knowledge drafts into a cohesive learning document.

```python
def integrate_learning_document_with_llm(
    llm: Any,
    learner_profile: Any,
    learning_path: Any,
    learning_session: Any,
    knowledge_points: Any,
    knowledge_drafts: Any,
    output_markdown: bool = True,
) -> Union[Dict[str, Any], str]:
    """Integrate drafts into a learning document."""
    integrator = LearningDocumentIntegrator(llm)
    document_structure = integrator.integrate({
        "learner_profile": learner_profile,
        "learning_path": learning_path,
        "learning_session": learning_session,
        "knowledge_points": knowledge_points,
        "knowledge_drafts": knowledge_drafts,
    })
    
    if output_markdown:
        return prepare_markdown_document(
            document_structure, knowledge_points, knowledge_drafts
        )
    return document_structure
```

**Markdown Output Structure:**
```markdown
# {Document Title}

{Overview}

## Foundational Concepts

### {Knowledge Point Title 1}
{Content 1}

### {Knowledge Point Title 2}
{Content 2}

## Practical Applications

### {Knowledge Point Title 3}
{Content 3}

## Strategic Insights

### {Knowledge Point Title 4}
{Content 4}

## Summary

{Summary}
```

### 5.5 Content Creator (High-Level API)

**Purpose:** Provides a unified interface for complete content generation.

```python
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
    search_rag_manager: Optional[SearchRagManager] = None,
):
    """Create complete learning content with optional quiz generation."""
    
    if method_name == "genmentor":
        # Multi-stage content generation
        knowledge_points = explore_knowledge_points_with_llm(...)
        knowledge_drafts = draft_knowledge_points_with_llm(...)
        learning_document = integrate_learning_document_with_llm(...)
        
        if with_quiz:
            document_quiz = generate_document_quizzes_with_llm(...)
            return {"document": learning_document, "quizzes": document_quiz}
        return {"document": learning_document}
    else:
        # Single-stage content generation
        creator = LearningContentCreator(llm, search_rag_manager=search_rag_manager)
        return creator.create_content(payload)
```

### 5.6 Feedback Simulator

**Purpose:** Simulates learner feedback for learning paths and content.

```python
class LearnerFeedbackSimulator(BaseAgent):
    def feedback_path(self, payload):
        """Simulate feedback for a learning path."""
        ...
    
    def feedback_content(self, payload):
        """Simulate feedback for learning content."""
        ...
```

**Output Schema:**
```python
class LearnerFeedback(BaseModel):
    feedback: FeedbackDetail
    suggestions: FeedbackDetail

class FeedbackDetail(BaseModel):
    progression: str
    engagement: str
    personalization: str
```

---

## 6. Tutoring Agents

### 6.1 AI Tutor Chatbot

**Purpose:** Provides interactive tutoring with context-aware responses.

```python
def chat_with_tutor_with_llm(
    llm: Any,
    messages: Optional[Sequence[Mapping[str, Any]]] | str = None,
    learner_profile: Any = "",
    search_rag_manager: Optional[SearchRagManager] = None,
    memory_store: Optional[LearnerMemoryStore] = None,
    use_search: bool = True,
    top_k: int = 5,
) -> str:
    """Run an AI tutor chat turn with optional RAG and memory."""
    agent = AITutorChatbot(
        llm,
        search_rag_manager=search_rag_manager,
        memory_store=memory_store,
    )
    return agent.chat({
        "learner_profile": learner_profile,
        "messages": messages,
        "use_search": use_search,
        "top_k": top_k,
    })
```

**Chatbot Algorithm:**
```
┌──────────────────────────────────────────────────────────────────┐
│                      AI Tutor Chatbot                            │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ 1. PARSE INPUT                                             │ │
│  │    • Convert messages to history text                      │ │
│  │    • Extract last user query                               │ │
│  └────────────────────────────────────────────────────────────┘ │
│                              │                                   │
│                              ▼                                   │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ 2. GATHER CONTEXT                                          │ │
│  │    • Get memory context from memory_store                  │ │
│  │    • Search/retrieve via search_rag_manager                │ │
│  │    • Combine contexts                                      │ │
│  └────────────────────────────────────────────────────────────┘ │
│                              │                                   │
│                              ▼                                   │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ 3. GENERATE RESPONSE                                       │ │
│  │    • Build prompt with learner profile, history, context   │ │
│  │    • Invoke LLM with system + task prompts                 │ │
│  │    • Return raw text response (no JSON parsing)            │ │
│  └────────────────────────────────────────────────────────────┘ │
│                              │                                   │
│                              ▼                                   │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ 4. LOG INTERACTION (if memory_store provided)              │ │
│  │    • Log learner query                                     │ │
│  │    • Log tutor response                                    │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

**Key Features:**
- **Context-Aware**: Uses learner profile and memory for personalization
- **RAG-Enhanced**: Retrieves relevant documents for grounded responses
- **Memory Persistence**: Stores conversation history for continuity
- **Flexible Search**: Supports both web search and vector-only retrieval

---

## 7. Assessment Agents

### 7.1 Quiz Generator

**Purpose:** Generates various quiz types from learning documents.

```python
def generate_document_quizzes_with_llm(
    llm,
    learner_profile,
    learning_document,
    single_choice_count: int = 3,
    multiple_choice_count: int = 0,
    true_false_count: int = 0,
    short_answer_count: int = 0,
) -> Dict[str, Any]:
    """Generate document-based quizzes."""
    generator = DocumentQuizGenerator(llm)
    return generator.generate({
        "learner_profile": learner_profile,
        "learning_document": learning_document,
        "single_choice_count": single_choice_count,
        "multiple_choice_count": multiple_choice_count,
        "true_false_count": true_false_count,
        "short_answer_count": short_answer_count,
    })
```

**Quiz Types:**
```python
class SingleChoiceQuestion(BaseModel):
    question: str
    options: List[str]
    correct_option: int | str
    explanation: Optional[str]

class MultipleChoiceQuestion(BaseModel):
    question: str
    options: List[str]
    correct_options: List[int | str]
    explanation: Optional[str]

class TrueFalseQuestion(BaseModel):
    question: str
    correct_answer: bool
    explanation: Optional[str]

class ShortAnswerQuestion(BaseModel):
    question: str
    expected_answer: str
    explanation: Optional[str]

class DocumentQuiz(BaseModel):
    single_choice_questions: List[SingleChoiceQuestion]
    multiple_choice_questions: List[MultipleChoiceQuestion]
    true_false_questions: List[TrueFalseQuestion]
    short_answer_questions: List[ShortAnswerQuestion]
```

### 7.2 Performance Evaluator

**Purpose:** Evaluates learner performance based on profile, sessions, and quiz results.

```python
def evaluate_learner_performance_with_llm(
    llm: BaseChatModel,
    learner_profile: Dict[str, Any],
    learning_path: Dict[str, Any],
    session_data: Dict[str, Any],
    quiz_results: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Evaluate learner performance."""
    ...

def evaluate_skill_mastery_with_llm(
    llm: BaseChatModel,
    skill_name: str,
    learner_responses: Dict[str, Any],
    quiz_results: Optional[Dict[str, Any]] = None,
    previous_attempts: Optional[list] = None,
) -> Dict[str, Any]:
    """Evaluate mastery level of a specific skill."""
    ...

def generate_performance_report_with_llm(
    llm: BaseChatModel,
    learner_profile: Dict[str, Any],
    performance_history: List[Dict[str, Any]],
    time_period: str = "current session",
) -> str:
    """Generate a comprehensive performance report."""
    ...
```

**Evaluation Output Schema:**
```python
class PerformanceEvaluation(BaseModel):
    overall_score: float                # 0-100
    performance_level: PerformanceLevel # excellent|good|satisfactory|needs_improvement
    strengths: List[str]
    weaknesses: List[str]
    progress_status: ProgressStatus
    skill_evaluations: List[SkillEvaluation]
    recommendations: List[Recommendation]
    next_steps: str

class SkillEvaluation(BaseModel):
    skill_name: str
    current_level: SkillLevel
    confidence: ConfidenceLevel
    ready_to_advance: bool
    notes: str

class Recommendation(BaseModel):
    priority: Priority  # high|medium|low
    action: str
    rationale: str

class SkillMasteryEvaluation(BaseModel):
    skill_name: str
    current_level: SkillLevel
    understanding_score: float        # 0-100
    proficiency_score: float          # 0-100
    ready_to_advance: bool
    mastered_aspects: List[str]
    gaps: List[str]
    improvement_from_previous: ImprovementStatus
    practice_recommendations: List[str]
    estimated_time_to_mastery: str
```

---

## 8. Schema System

### 8.1 Schema Organization

```
schemas/
├── __init__.py          # Exports all schemas
├── learning.py          # Skill gaps, goals, profiles
├── content.py           # Learning paths, knowledge, quizzes
├── tutoring.py          # Chat messages, responses
└── assessment.py        # Performance, mastery evaluations
```

### 8.2 Key Enums

```python
# Skill Levels
class LevelRequired(str, Enum):
    beginner = "beginner"
    intermediate = "intermediate"
    advanced = "advanced"

class LevelCurrent(str, Enum):
    unlearned = "unlearned"
    beginner = "beginner"
    intermediate = "intermediate"
    advanced = "advanced"

# Knowledge Types
class KnowledgeType(str, Enum):
    foundational = "foundational"
    practical = "practical"
    strategic = "strategic"

# Performance Levels
class PerformanceLevel(str, Enum):
    excellent = "excellent"
    good = "good"
    satisfactory = "satisfactory"
    needs_improvement = "needs_improvement"

# Confidence
class Confidence(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"
```

### 8.3 Validation Patterns

All schemas use Pydantic validation:

```python
class SkillGap(BaseModel):
    name: str
    is_gap: bool
    required_level: LevelRequired
    current_level: LevelCurrent
    reason: str = Field(..., description="≤20 words concise rationale")
    level_confidence: Confidence

    @field_validator("reason")
    @classmethod
    def limit_reason_words(cls, v: str) -> str:
        words = v.split()
        if len(words) > 20:
            raise ValueError("Reason must be 20 words or fewer.")
        return v

    @field_validator("is_gap")
    @classmethod
    def check_gap_consistency(cls, is_gap_value, info):
        # Ensure is_gap matches the actual level difference
        required = info.data.get("required_level")
        current = info.data.get("current_level")
        order = {"unlearned": 0, "beginner": 1, "intermediate": 2, "advanced": 3}
        gap_should_be = order[current.value] < order[required.value]
        if is_gap_value != gap_should_be:
            raise ValueError("is_gap inconsistency detected")
        return is_gap_value
```

---

## 9. Memory System

### 9.1 Memory Architecture

```
workspace/
└── memory/
    └── {learner_id}/
        ├── user_facts.md         # Long-term facts and context
        ├── chat_history.json     # Interaction log
        ├── profile.json          # Learner profile
        ├── objectives.json       # Learning objectives
        ├── mastery.json          # Mastery and progress
        └── learning_path.json    # Current learning path
```

### 9.2 Memory Store API

```python
class MemoryStore:
    """Two-layer memory: user_facts.md + chat_history.json"""
    
    def read_long_term(self) -> str:
        """Read long-term memory facts."""
    
    def write_long_term(self, content: str) -> None:
        """Write/update long-term memory."""
    
    def read_history(self) -> list[dict]:
        """Read chat history."""
    
    def append_history(self, role: str, content: str, metadata: Optional[dict] = None) -> None:
        """Append to history log."""
    
    def get_memory_context(self) -> str:
        """Get formatted context for agent prompts."""
    
    def search_history(self, query: str) -> list[dict]:
        """Search history for matching entries."""

class LearnerMemoryStore(MemoryStore):
    """Extended memory for learner-specific data."""
    
    def read_profile(self) -> dict:
        """Read learner profile."""
    
    def write_profile(self, content: dict) -> None:
        """Write learner profile."""
    
    def read_mastery(self) -> dict:
        """Read learning mastery and progress."""
    
    def update_evaluations(self, evaluation: dict) -> None:
        """Update evaluations within mastery.json."""
    
    def get_learner_context(self) -> str:
        """Get complete learner context for prompts."""
    
    def log_interaction(self, role: str, content: str, metadata: Optional[dict] = None) -> None:
        """Log a tutor interaction."""
```

### 9.3 Context Generation

```python
def get_learner_context(self) -> str:
    """Generate formatted context for agent prompts."""
    sections = []
    
    profile = self.read_profile()
    if profile:
        sections.append(f"## Learner Profile\n\n```json\n{json.dumps(profile)}\n```")
    
    objectives = self.read_objectives()
    if objectives:
        sections.append(f"## Learning Objectives\n\n```json\n{json.dumps(objectives)}\n```")
    
    mastery = self.read_mastery()
    if mastery:
        sections.append(f"## Learning Mastery & Performance\n\n```json\n{json.dumps(mastery)}\n```")
    
    user_facts = self.read_long_term()
    if user_facts:
        sections.append(f"## User Facts & Context\n\n{user_facts}")
    
    return "\n\n".join(sections)
```

---

## 10. RAG & Search System

### 10.1 SearchRagManager

```python
class SearchRagManager:
    """Unified manager for search and RAG operations."""
    
    def __init__(
        self,
        embedder: Embeddings,
        text_splitter: Optional[TextSplitter] = None,
        vectorstore: Optional[VectorStore] = None,
        search_runner: Optional[SearchRunner] = None,
        max_retrieval_results: int = 5,
    ):
        ...
    
    @staticmethod
    def from_config(config: DictConfig) -> "SearchRagManager":
        """Create manager from configuration."""
    
    def search(self, query: str) -> List[SearchResult]:
        """Perform web search."""
    
    def add_documents(self, documents: List[Document]) -> None:
        """Add documents to vectorstore."""
    
    def retrieve(self, query: str, k: Optional[int] = None) -> List[Document]:
        """Retrieve from vectorstore."""
    
    def invoke(self, query: str) -> List[Document]:
        """Combined search + RAG pipeline."""
```

### 10.2 RAG Pipeline

```
┌──────────────────────────────────────────────────────────────────┐
│                     SearchRagManager.invoke()                    │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │              Configuration Mode Check                        ││
│  │                                                               ││
│  │  ┌───────────────┐    ┌───────────────┐                     ││
│  │  │ Search Enabled│    │ Vectordb Enabled│                    ││
│  │  │     (Y/N)     │    │     (Y/N)       │                    ││
│  │  └───────┬───────┘    └───────┬───────┘                     ││
│  │          │                    │                               ││
│  │          ▼                    ▼                               ││
│  │  ┌───────────────┐    ┌───────────────┐                     ││
│  │  │Web Search API │    │  Vector Store  │                     ││
│  │  │(DuckDuckGo/   │    │    (Chroma)    │                     ││
│  │  │ Tavily/etc)   │    │               │                     ││
│  │  └───────┬───────┘    └───────┬───────┘                     ││
│  │          │                    │                               ││
│  └──────────┼────────────────────┼───────────────────────────────┘│
│             │                    │                                 │
│             ▼                    ▼                                 │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │                    Mode Behaviors                            ││
│  │                                                               ││
│  │  Both Enabled:  Search → Store → Retrieve similar            ││
│  │  Search Only:   Return search results directly               ││
│  │  Vectordb Only: Retrieve from existing store                 ││
│  │  Both Disabled: Return empty list                            ││
│  │                                                               ││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

### 10.3 Document Formatting

```python
def format_docs(docs: List[Document]) -> str:
    """Format documents for context inclusion."""
    formatted_chunks = []
    for idx, doc in enumerate(docs):
        title = doc.metadata.get("title", "")
        source = doc.metadata.get("source", "")
        header = f"[{idx}] {title} | Source: {source}"
        body = doc.page_content.strip()
        formatted_chunks.append(f"{header}\n{body}")
    return "\n\n".join(formatted_chunks)
```

---

## 11. Complete Workflows

### 11.1 Learner Onboarding Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│                   LEARNER ONBOARDING                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. INPUT COLLECTION                                            │
│     ┌──────────────────────────────────────────────────────┐   │
│     │ • Learning Goal (user input)                          │   │
│     │ • Learner Information (resume/background)             │   │
│     └──────────────────────────────────────────────────────┘   │
│                              │                                  │
│                              ▼                                  │
│  2. GOAL REFINEMENT                                             │
│     ┌──────────────────────────────────────────────────────┐   │
│     │ refine_learning_goal_with_llm()                       │   │
│     │ → Structured, actionable learning objective           │   │
│     └──────────────────────────────────────────────────────┘   │
│                              │                                  │
│                              ▼                                  │
│  3. SKILL GAP IDENTIFICATION                                    │
│     ┌──────────────────────────────────────────────────────┐   │
│     │ identify_skill_gap_with_llm()                         │   │
│     │ → Skill requirements from goal                        │   │
│     │ → Current skill assessment                            │   │
│     │ → Gap analysis                                        │   │
│     └──────────────────────────────────────────────────────┘   │
│                              │                                  │
│                              ▼                                  │
│  4. PROFILE INITIALIZATION                                      │
│     ┌──────────────────────────────────────────────────────┐   │
│     │ initialize_learner_profile_with_llm()                 │   │
│     │ → Complete LearnerProfile                             │   │
│     │ → Cognitive status, preferences, patterns            │   │
│     └──────────────────────────────────────────────────────┘   │
│                              │                                  │
│                              ▼                                  │
│  5. LEARNING PATH SCHEDULING                                    │
│     ┌──────────────────────────────────────────────────────┐   │
│     │ schedule_learning_path_with_llm()                     │   │
│     │ → Ordered sessions with outcomes                      │   │
│     └──────────────────────────────────────────────────────┘   │
│                              │                                  │
│                              ▼                                  │
│  OUTPUT: LearnerProfile + LearningPath                         │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 11.2 Content Generation Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│                 CONTENT GENERATION (GenMentor Method)           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Input: LearnerProfile, LearningPath, Session                   │
│                                                                 │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │ 1. KNOWLEDGE EXPLORATION                                   │ │
│  │    explore_knowledge_points_with_llm()                     │ │
│  │    → List of knowledge points by type                      │ │
│  │      (foundational, practical, strategic)                  │ │
│  └───────────────────────────────────────────────────────────┘ │
│                              │                                  │
│                              ▼                                  │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │ 2. KNOWLEDGE DRAFTING (Parallel)                           │ │
│  │    draft_knowledge_points_with_llm()                       │ │
│  │    → For each knowledge point:                             │ │
│  │      • Build search query                                  │ │
│  │      • Execute web search (optional)                       │ │
│  │      • Generate content with RAG context                   │ │
│  │    → Returns list of KnowledgeDraft                        │ │
│  └───────────────────────────────────────────────────────────┘ │
│                              │                                  │
│                              ▼                                  │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │ 3. DOCUMENT INTEGRATION                                    │ │
│  │    integrate_learning_document_with_llm()                  │ │
│  │    → Generate document structure                           │ │
│  │    → Render to markdown format                             │ │
│  └───────────────────────────────────────────────────────────┘ │
│                              │                                  │
│                              ▼                                  │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │ 4. QUIZ GENERATION (Optional)                              │ │
│  │    generate_document_quizzes_with_llm()                    │ │
│  │    → Single choice, multiple choice, T/F, short answer     │ │
│  └───────────────────────────────────────────────────────────┘ │
│                              │                                  │
│                              ▼                                  │
│  Output: {document: str, quizzes: DocumentQuiz}                │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 11.3 Learning Session Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│                    LEARNING SESSION                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. SESSION START                                               │
│     ┌──────────────────────────────────────────────────────┐   │
│     │ • Load learner profile from memory                    │   │
│     │ • Load current learning path                          │   │
│     │ • Get current session details                         │   │
│     └──────────────────────────────────────────────────────┘   │
│                              │                                  │
│                              ▼                                  │
│  2. CONTENT DELIVERY                                            │
│     ┌──────────────────────────────────────────────────────┐   │
│     │ create_learning_content_with_llm()                    │   │
│     │ → Generate personalized content                       │   │
│     │ → Present to learner                                  │   │
│     └──────────────────────────────────────────────────────┘   │
│                              │                                  │
│                              ▼                                  │
│  3. INTERACTIVE TUTORING                                        │
│     ┌──────────────────────────────────────────────────────┐   │
│     │ Loop:                                                  │   │
│     │   chat_with_tutor_with_llm()                          │   │
│     │   • Answer questions                                   │   │
│     │   • Provide explanations                              │   │
│     │   • Log interactions to memory                        │   │
│     └──────────────────────────────────────────────────────┘   │
│                              │                                  │
│                              ▼                                  │
│  4. QUIZ & ASSESSMENT                                           │
│     ┌──────────────────────────────────────────────────────┐   │
│     │ • Present quiz questions                              │   │
│     │ • Collect answers                                     │   │
│     │ • evaluate_learner_performance_with_llm()             │   │
│     └──────────────────────────────────────────────────────┘   │
│                              │                                  │
│                              ▼                                  │
│  5. PROFILE UPDATE                                              │
│     ┌──────────────────────────────────────────────────────┐   │
│     │ update_learner_profile_with_llm()                     │   │
│     │ • Update skill levels                                 │   │
│     │ • Mark session as complete                            │   │
│     │ • Store in memory                                     │   │
│     └──────────────────────────────────────────────────────┘   │
│                              │                                  │
│                              ▼                                  │
│  6. PATH ADJUSTMENT (if needed)                                 │
│     ┌──────────────────────────────────────────────────────┐   │
│     │ reschedule_learning_path_with_llm()                   │   │
│     │ • Based on performance                                │   │
│     │ • Adjust future sessions                              │   │
│     └──────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 12. Configuration

### 12.1 Configuration Structure

```yaml
# config.example.yaml
llm:
  # Model in "provider/model" format
  model: "deepseek/deepseek-chat"
  base_url: null

embedder:
  enable_vectordb: true
  model_name: "sentence-transformers/all-mpnet-base-v2"
  provider: "huggingface"

search:
  enable_search: true
  provider: "duckduckgo"
  max_results: 5

vectorstore:
  type: "chroma"
  collection_name: "gen_mentor"
  persist_directory: "./data/vectorstore"

rag:
  text_splitter_type: "recursive_character"
  chunk_size: 1000
  chunk_overlap: 0
  num_retrieval_results: 5

log_level: "INFO"
```

### 12.2 Configuration Loading

```python
from gen_mentor.config import load_config, default_config

# Load from file
config = load_config("path/to/config.yaml")

# Use default
config = default_config

# Access configuration
llm = LLMFactory.create(
    model=config.llm.model,  # "provider/model" format
)
```

**Model Parameter Format:**
The `model` parameter uses a unified `"provider/model"` format:
- Full format: `"openai/gpt-4"`, `"anthropic/claude-3-5-sonnet"`, `"deepseek/deepseek-chat"`
- Model only: `"gpt-4"` (falls back to default provider)
- Default: Uses config default (e.g., `"openai/gpt-5.1"`)
```

### 12.3 Agent Default Configuration

```python
class AgentDefaults(BaseModel):
    """Default settings for all agents."""
    temperature: float = 0.0
    max_tokens: int = 4096
    timeout: int = 120
    retry_attempts: int = 3
```

---

## Appendix A: API Reference Summary

### Learning Agents
| Function | Purpose | Input | Output |
|----------|---------|-------|--------|
| `refine_learning_goal_with_llm` | Refine goal | goal, info | RefinedLearningGoal |
| `identify_skill_gap_with_llm` | Find skill gaps | goal, info | SkillGaps, SkillRequirements |
| `initialize_learner_profile_with_llm` | Create profile | goal, info, gaps | LearnerProfile |
| `update_learner_profile_with_llm` | Update profile | profile, interactions | LearnerProfile |

### Content Agents
| Function | Purpose | Input | Output |
|----------|---------|-------|--------|
| `schedule_learning_path_with_llm` | Create path | profile | LearningPath |
| `explore_knowledge_points_with_llm` | Find KP | profile, path, session | KnowledgePoints |
| `draft_knowledge_points_with_llm` | Draft content | KP, profile, path | List[KnowledgeDraft] |
| `integrate_learning_document_with_llm` | Build document | drafts, KP | DocumentStructure/str |
| `create_learning_content_with_llm` | Full pipeline | profile, path, session | {document, quizzes} |

### Tutoring Agents
| Function | Purpose | Input | Output |
|----------|---------|-------|--------|
| `chat_with_tutor_with_llm` | Chat turn | messages, profile | str |

### Assessment Agents
| Function | Purpose | Input | Output |
|----------|---------|-------|--------|
| `generate_document_quizzes_with_llm` | Create quiz | document | DocumentQuiz |
| `evaluate_learner_performance_with_llm` | Evaluate | profile, session, quiz | PerformanceEvaluation |
| `evaluate_skill_mastery_with_llm` | Skill eval | skill, responses | SkillMasteryEvaluation |

---

## Appendix B: Error Handling

All agents use Pydantic validation for input/output. Common error patterns:

```python
try:
    result = agent.invoke(payload)
except ValidationError as e:
    # Handle schema validation errors
    logger.error(f"Validation error: {e}")
except Exception as e:
    # Handle LLM or other errors
    logger.error(f"Agent error: {e}")
```

---

## Appendix C: Best Practices

1. **Always validate inputs** before passing to agents
2. **Use memory stores** for persistent learner context
3. **Enable parallel drafting** for faster content generation
4. **Configure search/RAG** based on content needs
5. **Update profiles** after each learning session
6. **Log interactions** for analysis and improvement

---

*Documentation generated: 2026-02-23*
*GenMentor Version: Current*
