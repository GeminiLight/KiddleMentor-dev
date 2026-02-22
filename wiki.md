# GenMentor Wiki

> **LLM-powered Multi-agent Framework for Goal-oriented Learning in Intelligent Tutoring System**
>
> WWW 2025 (Industry Track) - Oral Presentation

---

## Table of Contents

- [Introduction](#introduction)
- [Architecture Overview](#architecture-overview)
- [Getting Started](#getting-started)
- [Core Components](#core-components)
- [Agent System](#agent-system)
- [Configuration](#configuration)
- [API Reference](#api-reference)
- [Development](#development)
- [Testing](#testing)
- [Deployment](#deployment)
- [FAQ](#faq)
- [Contributing](#contributing)

---

## Introduction

### What is GenMentor?

GenMentor is an advanced Intelligent Tutoring System (ITS) that leverages Large Language Models (LLMs) and a multi-agent framework to provide personalized, goal-oriented learning experiences. Unlike traditional MOOCs or reactive chatbots, GenMentor proactively plans learning paths, adapts to individual learners, and aligns content with specific skill acquisition goals.

### Key Features

- 🎯 **Goal-Oriented Learning**: Focus on achieving specific learning objectives
- 👤 **Personalized Paths**: Tailored learning journeys based on individual profiles
- 🤖 **Multi-Agent System**: Specialized agents for different tutoring tasks
- 📊 **Adaptive Assessment**: Continuous evaluation and path adjustment
- 💬 **Interactive Tutoring**: AI chatbot for real-time support
- 🔍 **Skill Gap Analysis**: Precise identification of knowledge gaps
- 📝 **Custom Content**: Automatically generated learning materials

### ITS Paradigm Comparison

| Paradigm | Characteristics | Primary Focus |
|----------|----------------|---------------|
| Traditional MOOC | Static syllabus, pre-recorded lectures | Broad access, low personalization |
| Chatbot ITS | Reactive Q&A, session-based help | Instant support, limited adaptation |
| **GenMentor (Goal-oriented ITS)** | **Proactive planning, personalized paths** | **Targeted skills, continual adaptation** |

---

## Architecture Overview

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        GenMentor System                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────┐ │
│  │   Web Frontend   │  │   FastAPI        │  │   CLI Tool   │ │
│  │   (Streamlit)    │◄─┤   Backend        │  │              │ │
│  └──────────────────┘  └──────────────────┘  └──────────────┘ │
│           │                      │                    │         │
│           └──────────────────────┴────────────────────┘         │
│                                  │                              │
│                    ┌─────────────▼─────────────┐               │
│                    │    gen_mentor Package     │               │
│                    ├───────────────────────────┤               │
│                    │  • Agents                 │               │
│                    │  • Config                 │               │
│                    │  • Core (LLM, Tools)      │               │
│                    │  • Schemas                │               │
│                    │  • Utils                  │               │
│                    └───────────────────────────┘               │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Project Structure

```
gen-mentor/
├── gen_mentor/                    # Core package
│   ├── agents/                    # AI agent modules
│   │   ├── content/              # Content generation agents
│   │   ├── learning/             # Learning assessment agents
│   │   ├── assessment/           # Quiz & performance evaluation
│   │   └── tutoring/             # Chatbot tutor
│   ├── config/                   # Configuration system
│   ├── core/                     # Core infrastructure
│   │   ├── base/                 # Base classes
│   │   ├── llm/                  # LLM factory
│   │   └── tools/                # Tools (search, RAG, etc.)
│   ├── schemas/                  # Data models
│   ├── cli/                      # Command-line interface
│   └── utils/                    # Utilities
│
├── apps/                         # Applications
│   ├── backend/                  # FastAPI backend
│   │   ├── main.py              # API server
│   │   └── api/                 # API schemas
│   └── frontend_streamlit/       # Streamlit frontend
│
├── tests/                        # Test suite
│   ├── unit/                    # Unit tests
│   └── integration/             # Integration tests
│
├── scripts/                      # Helper scripts
├── resources/                    # Assets & examples
└── requirements.txt              # Dependencies
```

---

## Getting Started

### Prerequisites

- Python 3.10+
- pip or uv (package manager)
- API keys for at least one LLM provider (OpenAI, Anthropic, DeepSeek, etc.)

### Installation

#### Option 1: Using pip (Recommended)

```bash
# Clone the repository
git clone https://github.com/yourusername/gen-mentor.git
cd gen-mentor

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

#### Option 2: Using uv (Faster)

```bash
# Clone the repository
git clone https://github.com/yourusername/gen-mentor.git
cd gen-mentor

# Create virtual environment
uv venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies
uv pip install -r requirements.txt
pip install -e .
```

### Configuration

#### 1. Set Up API Keys

**Option A: Interactive Onboarding (Recommended)**

The easiest way to configure GenMentor is using the interactive setup wizard:

```bash
gen-mentor onboard
```

This will guide you through:
- Selecting your LLM provider
- Setting up API keys
- Configuring search providers
- Choosing advanced options

**Option B: Manual Configuration**

Create or edit `~/.gen-mentor/config.yaml`:

```yaml
agent_defaults:
  model: openai/gpt-5.1
  temperature: 0.0
  max_tokens: 8192

providers:
  openai:
    api_key: ${OPENAI_API_KEY}

  deepseek:
    api_key: ${DEEPSEEK_API_KEY}

  anthropic:
    api_key: ${ANTHROPIC_API_KEY}
```

Or set environment variables:

```bash
export OPENAI_API_KEY="your-api-key"
export DEEPSEEK_API_KEY="your-api-key"
export ANTHROPIC_API_KEY="your-api-key"
```

#### 2. Run the System

**Backend:**
```bash
cd apps/backend
uvicorn main:app --reload --port 5000
```

**Frontend:**
```bash
cd apps/frontend_streamlit
streamlit run main.py --server.port 8501
```

**Access:**
- Backend API: http://localhost:5000
- Frontend UI: http://localhost:8501

---

## Core Components

### 1. Configuration System

Location: `gen_mentor/config/`

**Features:**
- Centralized configuration management
- Environment variable interpolation
- Multiple LLM provider support
- Search provider configuration
- RAG settings

**Files:**
- `schemas.py` - Configuration data models
- `loader.py` - Configuration loading logic
- `config.example.yaml` - Example configuration

**Usage:**
```python
from gen_mentor.config import load_config

config = load_config()
print(config.agent_defaults.model)  # openai/gpt-5.1
```

### 2. LLM Factory

Location: `gen_mentor/core/llm/factory.py`

**Purpose:** Create LLM instances with consistent configuration

**Usage:**
```python
from gen_mentor.core.llm.factory import LLMFactory

# Create LLM with defaults from config
llm = LLMFactory.create()

# Create specific LLM
llm = LLMFactory.create(
    model="gpt-4",
    model_provider="openai",
    temperature=0.7
)
```

### 3. Base Agent

Location: `gen_mentor/agents/base_agent.py`

**Purpose:** Foundation class for all AI agents

**Features:**
- LangChain integration
- Tool support
- Prompt management
- JSON output parsing

**Usage:**
```python
from gen_mentor.agents.base_agent import BaseAgent

agent = BaseAgent(
    model=llm,
    system_prompt="You are a helpful tutor.",
    tools=[],
    jsonalize_output=True
)

result = agent.invoke(
    input_dict={"topic": "Python"},
    task_prompt="Explain {topic} basics."
)
```

### 4. Schemas

Location: `gen_mentor/schemas/`

**Files:**
- `content.py` - Learning content models
- `learning.py` - Learner profiles, skill gaps
- `tutoring.py` - Chat interactions
- `assessment.py` - Quizzes, performance evaluation

**Example:**
```python
from gen_mentor.schemas import LearnerProfile, SkillGap, LearningPath

profile = LearnerProfile(
    name="John Doe",
    learning_goal="Master Python",
    mastered_skills=[...],
    in_progress_skills=[...]
)
```

---

## Agent System

### Agent Categories

GenMentor uses four categories of specialized agents:

#### 1. Content Agents (`agents/content/`)

Generate and organize learning materials.

**Agents:**
- **Content Creator** (`content_creator.py`)
  - Creates tailored learning content
  - Generates examples and explanations

- **Path Scheduler** (`path_scheduler.py`)
  - Creates personalized learning paths
  - Schedules sessions and milestones

- **Knowledge Explorer** (`knowledge_explorer.py`)
  - Explores topics and concepts
  - Identifies key knowledge points

- **Knowledge Drafter** (`knowledge_drafter.py`)
  - Drafts detailed content for topics
  - Includes examples and exercises

- **Document Integrator** (`document_integrator.py`)
  - Integrates content into cohesive documents
  - Creates structured learning materials

- **Feedback Simulator** (`feedback_simulator.py`)
  - Simulates learner feedback
  - Tests content effectiveness

**Usage Example:**
```python
from gen_mentor.agents.content import create_learning_content_with_llm

content = create_learning_content_with_llm(
    llm=llm,
    learner_profile=profile,
    topic="Python Functions"
)
```

#### 2. Learning Agents (`agents/learning/`)

Analyze learners and identify skill gaps.

**Agents:**
- **Skill Gap Identifier** (`skill_gap_identifier.py`)
  - Identifies knowledge gaps
  - Compares current vs. required skills

- **Goal Refiner** (`goal_refiner.py`)
  - Refines vague learning goals
  - Breaks down into specific objectives

- **Skill Mapper** (`skill_mapper.py`)
  - Maps goals to required skills
  - Identifies prerequisites

- **Learner Profiler** (`learner_profiler.py`)
  - Creates and updates learner profiles
  - Tracks progress and preferences

- **Behavior Simulator** (`behavior_simulator.py`)
  - Simulates learner behavior
  - Predicts learning patterns

- **Profile Creator** (`profile_creator.py`)
  - Initializes learner profiles
  - Extracts information from CVs/documents

**Usage Example:**
```python
from gen_mentor.agents.learning import identify_skill_gap_with_llm

gaps = identify_skill_gap_with_llm(
    llm=llm,
    learning_goal="Become a data engineer",
    learner_information="CV text...",
    skill_requirements=requirements
)
```

#### 3. Assessment Agents (`agents/assessment/`)

Generate quizzes and evaluate performance.

**Agents:**
- **Quiz Generator** (`quiz_generator.py`)
  - Generates multiple question types
  - Creates assessments from documents

- **Performance Evaluator** (`performance_evaluator.py`)
  - Evaluates learner performance
  - Assesses skill mastery
  - Generates performance reports

**Usage Example:**
```python
from gen_mentor.agents.assessment import (
    generate_document_quiz_with_llm,
    evaluate_learner_performance_with_llm
)

# Generate quiz
quiz = generate_document_quiz_with_llm(
    llm=llm,
    learner_profile=profile,
    learning_document=document,
    single_choice_count=5
)

# Evaluate performance
evaluation = evaluate_learner_performance_with_llm(
    llm=llm,
    learner_profile=profile,
    learning_path=path,
    session_data=session,
    quiz_results=results
)
```

#### 4. Tutoring Agents (`agents/tutoring/`)

Interactive AI tutor for real-time support.

**Agents:**
- **Chatbot Tutor** (`chatbot.py`)
  - Answers learner questions
  - Provides explanations
  - Uses RAG for enhanced responses

**Usage Example:**
```python
from gen_mentor.agents.tutoring import chat_with_tutor_with_llm

response = chat_with_tutor_with_llm(
    llm=llm,
    messages=[
        {"role": "user", "content": "What are Python decorators?"}
    ],
    learner_profile=profile,
    search_rag_manager=rag_manager,
    use_search=True
)
```

---

## Configuration

### Configuration File Location

Default: `~/.gen-mentor/config.yaml`

The configuration file is automatically created on first run if it doesn't exist.

### Configuration Structure

```yaml
# Application settings
environment: dev
debug: true
log_level: INFO

# Agent defaults
agent_defaults:
  model: openai/gpt-5.1  # Format: provider/model
  temperature: 0.0
  max_tokens: 8192

# LLM providers
providers:
  openai:
    api_key: ${OPENAI_API_KEY}
    api_base: null

  deepseek:
    api_key: ${DEEPSEEK_API_KEY}
    api_base: null

  anthropic:
    api_key: ${ANTHROPIC_API_KEY}
    api_base: null

# Search configuration
search_defaults:
  provider: duckduckgo
  max_results: 5
  loader_type: web

# Embedding configuration
embedding:
  provider: huggingface
  model_name: sentence-transformers/all-mpnet-base-v2

# Vector store
vectorstore:
  persist_directory: data/vectorstore
  collection_name: genmentor

# RAG settings
rag:
  chunk_size: 1000
  num_retrieval_results: 5
  allow_parallel: true
  max_workers: 3
```

### Environment Variables

All API keys can be set via environment variables:

```bash
# LLM Providers
export OPENAI_API_KEY="sk-..."
export ANTHROPIC_API_KEY="sk-ant-..."
export DEEPSEEK_API_KEY="..."
export TOGETHER_API_KEY="..."
export GROQ_API_KEY="gsk_..."

# Search Providers
export TAVILY_API_KEY="..."
export SERPER_API_KEY="..."
export BING_SUBSCRIPTION_KEY="..."

# Backend Settings
export BACKEND_HOST="0.0.0.0"
export BACKEND_PORT="5000"
export UPLOAD_LOCATION="/tmp/uploads/"
```

### Overriding Configuration

```python
from gen_mentor.config import load_config

# Load with custom path
config = load_config(config_path="path/to/config.yaml")

# Load with overrides
config = load_config(overrides={
    "agent_defaults": {"temperature": 0.7}
})
```

---

## API Reference

### Backend API Endpoints

Base URL: `http://localhost:5000`

#### Learning Goal

**POST `/refine-learning-goal`**

Refine a vague learning goal into specific objectives.

**Request:**
```json
{
  "learning_goal": "Learn Python",
  "learner_information": "I know basic programming",
  "model_provider": "deepseek",
  "model_name": "deepseek-chat"
}
```

**Response:**
```json
{
  "original_goal": "Learn Python",
  "refined_goal": "Master Python fundamentals including...",
  "key_topics": ["Variables", "Functions", "Classes"],
  "estimated_duration": "3 months"
}
```

#### Skill Gap Analysis

**POST `/identify-skill-gap-with-info`**

Identify skill gaps based on learning goal and current knowledge.

**Request:**
```json
{
  "learning_goal": "Become a data engineer",
  "learner_information": "CV text or profile",
  "skill_requirements": {...},
  "model_provider": "deepseek",
  "model_name": "deepseek-chat"
}
```

**Response:**
```json
{
  "skill_gaps": [{
    "name": "Apache Spark",
    "is_gap": true,
    "required_level": "intermediate",
    "current_level": "unlearned"
  }]
}
```

#### Learner Profile

**POST `/create-learner-profile-with-info`**

Create a learner profile from information.

**POST `/update-learner-profile`**

Update an existing learner profile.

#### Learning Path

**POST `/schedule-learning-path`**

Generate a personalized learning path.

**POST `/reschedule-learning-path`**

Adjust an existing learning path based on progress.

#### Content Generation

**POST `/explore-knowledge-points`**

Explore knowledge points for a topic.

**POST `/draft-knowledge-point`**

Draft detailed content for a knowledge point.

**POST `/integrate-learning-document`**

Integrate knowledge drafts into a cohesive document.

**POST `/tailor-knowledge-content`**

Generate complete tailored content for a session.

#### Assessment

**POST `/generate-document-quizzes`**

Generate quizzes from learning documents.

#### Chatbot

**POST `/chat-with-tutor`**

Chat with the AI tutor.

**Request:**
```json
{
  "messages": "[{\"role\": \"user\", \"content\": \"What is Python?\"}]",
  "learner_profile": {...},
  "model_provider": "deepseek",
  "model_name": "deepseek-chat"
}
```

### CLI Commands

```bash
# Refine goal
gen-mentor refine-goal --goal "Learn Python" --learner-info "..."

# Identify skill gaps
gen-mentor identify-skill-gap --goal "..." --learner-info @cv.txt

# Schedule learning path
gen-mentor schedule-path --learner-profile @profile.json --session-count 8

# Chat with tutor
gen-mentor chat --message "What is Python?"

# Run agent query
gen-mentor agent -m "What is 2+2?"
```

---

## Development

### Setting Up Development Environment

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Install in editable mode
pip install -e .
```

### Code Style

GenMentor follows PEP 8 style guidelines.

```bash
# Format code
black gen_mentor tests

# Sort imports
isort gen_mentor tests

# Lint code
flake8 gen_mentor tests

# Type checking
mypy gen_mentor
```

### Project Structure Best Practices

- **Agents**: Keep agents focused on single responsibilities
- **Prompts**: Store prompts in `prompts/` subdirectories
- **Schemas**: Use Pydantic for all data models
- **Configuration**: Never hardcode API keys or settings
- **Tests**: Write tests for all new features

---

## Testing

### Running Tests

```bash
# Run all tests
make test
pytest

# Run unit tests
make test-unit
pytest tests/unit/

# Run integration tests
make test-integration
pytest tests/integration/

# Run with coverage
make test-cov
pytest --cov=gen_mentor --cov-report=html
```

### Writing Tests

```python
# tests/unit/test_my_module.py
import pytest
from gen_mentor.my_module import my_function

def test_my_function(mock_llm):
    """Test my_function with mocked LLM."""
    result = my_function(llm=mock_llm, input="test")
    assert result is not None
```

### Test Structure

```
tests/
├── conftest.py              # Shared fixtures
├── unit/                    # Unit tests
│   ├── test_config.py
│   ├── test_schemas.py
│   ├── test_base_agent.py
│   └── test_llm_factory.py
└── integration/             # Integration tests
    ├── test_content_agents.py
    ├── test_learning_agents.py
    ├── test_assessment_agents.py
    └── test_tutoring_agents.py
```

---

## Deployment

### Docker Deployment

```dockerfile
# Dockerfile
FROM python:3.10-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY gen_mentor ./gen_mentor
COPY apps/backend ./apps/backend

CMD ["uvicorn", "apps.backend.main:app", "--host", "0.0.0.0", "--port", "5000"]
```

```bash
# Build and run
docker build -t genmentor .
docker run -p 5000:5000 -e OPENAI_API_KEY=... genmentor
```

### Production Configuration

```yaml
# config.prod.yaml
environment: prod
debug: false
log_level: WARNING

agent_defaults:
  model: gpt-4
  temperature: 0.0
  max_tokens: 8192

# Use production API endpoints
providers:
  openai:
    api_key: ${OPENAI_API_KEY}
    api_base: https://api.openai.com/v1
```

### Environment Variables for Production

```bash
export GENMENTOR_CONFIG=/etc/genmentor/config.yaml
export BACKEND_HOST=0.0.0.0
export BACKEND_PORT=8080
export LOG_LEVEL=WARNING
```

---

## FAQ

### Q: How do I add a new LLM provider?

A: Add the provider to `config.yaml`:

```yaml
providers:
  my_provider:
    api_key: ${MY_PROVIDER_API_KEY}
    api_base: https://api.myprovider.com/v1
```

Then use it:
```python
llm = LLMFactory.create(model="my-model", model_provider="my_provider")
```

### Q: How do I create a custom agent?

A: Extend `BaseAgent`:

```python
from gen_mentor.agents.base_agent import BaseAgent

class MyAgent(BaseAgent):
    def __init__(self, model, **kwargs):
        super().__init__(
            model=model,
            system_prompt="You are my custom agent.",
            **kwargs
        )

    def custom_method(self, input_data):
        return self.invoke(
            input_dict=input_data,
            task_prompt="Process {data}"
        )
```

### Q: How do I use RAG with agents?

A: Initialize `SearchRagManager`:

```python
from gen_mentor.core.tools.retrieval.search_rag import SearchRagManager

rag_manager = SearchRagManager.from_config({
    "search": {"provider": "duckduckgo"},
    "embedder": {"provider": "huggingface"},
    "vectorstore": {"persist_directory": "data/vectorstore"},
    "rag": {"chunk_size": 1000}
})

# Use with tutor
response = chat_with_tutor_with_llm(
    llm=llm,
    messages=messages,
    search_rag_manager=rag_manager,
    use_search=True
)
```

### Q: Where are the agent prompts stored?

A: Prompts are colocated with agents in `prompts/` subdirectories:

```
agents/
├── content/
│   ├── content_creator.py
│   └── prompts/
│       └── content_creator.py  # Prompts here
```

### Q: How do I contribute?

A: See the [Contributing](#contributing) section below.

---

## Contributing

### Contribution Guidelines

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/my-new-feature
   ```
3. **Make your changes**
   - Follow code style guidelines
   - Add tests for new features
   - Update documentation
4. **Run tests**
   ```bash
   make test
   ```
5. **Commit your changes**
   ```bash
   git commit -m "Add: my new feature"
   ```
6. **Push to your fork**
   ```bash
   git push origin feature/my-new-feature
   ```
7. **Create a Pull Request**

### Code Review Process

- All PRs require at least one review
- All tests must pass
- Code coverage should not decrease
- Documentation must be updated

### Reporting Issues

Use GitHub Issues to report:
- Bugs
- Feature requests
- Documentation improvements

**Bug Report Template:**
```markdown
**Description:**
Brief description of the bug

**Steps to Reproduce:**
1. Step one
2. Step two

**Expected Behavior:**
What should happen

**Actual Behavior:**
What actually happens

**Environment:**
- OS: ...
- Python version: ...
- GenMentor version: ...
```

---

## Links

- 🌐 **Website**: https://www.tianfuwang.tech/gen-mentor
- 📄 **Paper**: https://arxiv.org/pdf/2501.15749
- 🎬 **Demo**: https://gen-mentor.streamlit.app/
- 🎥 **Video**: https://youtu.be/vTdtGZop-Zc
- 💻 **GitHub**: https://github.com/yourusername/gen-mentor

---

## Citation

```bibtex
@inproceedings{wang2025llm,
  title={LLM-powered Multi-agent Framework for Goal-oriented Learning in Intelligent Tutoring System},
  author={Wang, Tianfu and Zhan, Yi and Lian, Jianxun and Hu, Zhengyu and Yuan, Nicholas Jing and Zhang, Qi and Xie, Xing and Xiong, Hui},
  booktitle={Companion Proceedings of the ACM Web Conference},
  year={2025}
}
```

---

## License

[Add your license information here]

---

## Support

For questions and support:
- 📧 Email: [your-email@example.com]
- 💬 Discussions: GitHub Discussions
- 🐛 Issues: GitHub Issues

---

**Last Updated**: February 2026

**Version**: 1.0.0
