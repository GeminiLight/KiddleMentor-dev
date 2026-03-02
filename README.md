<div align="center">
  <p align="center">
    <img src="resources/logo.png" alt="GenMentor Logo" width="300"/>
  </p>
  <p><b>LLM-powered & Goal-oriented Tutoring System</b></p>

  <p>
    <a href="https://www.tianfuwang.tech/gen-mentor">Website</a> &nbsp;·&nbsp;
    <a href="https://arxiv.org/pdf/2501.15749">Paper</a> &nbsp;·&nbsp;
    <a href="https://gen-mentor.streamlit.app/">Demo</a> &nbsp;·&nbsp;
    <a href="https://youtu.be/vTdtGZop-Zc">Video</a>
  </p>

</div>

---

> [!IMPORTANT]
> :sparkles: Welcome to visit the [GenMentor website](https://www.tianfuwang.tech/gen-mentor) to learn more about our work!

This is the official code for our paper "*LLM-powered Multi-agent Framework for Goal-oriented Learning in Intelligent Tutoring System*", accepted by **WWW 2025 (Industry Track) as an Oral Presentation**.

GenMentor is a large language model (LLM)-powered multi-agent framework designed for goal-oriented learning in Intelligent Tutoring Systems (ITS). It delivers **personalized, adaptive, goal-aligned** learning experiences through coordinated AI agents — from skill-gap analysis and learning-path scheduling to tailored content generation and real-time performance evaluation.

## 📑 Table of Contents

- [🏫 ITS Paradigm Comparison](#-its-paradigm-comparison)
- [✨ Core Features](#-core-features)
  - [🤖 Agent Modules](#-agent-modules)
  - [🔧 Platform Capabilities](#-platform-capabilities)
- [🏗️ Project Architecture](#️-project-architecture)
- [🚀 Quick Start](#-quick-start)
  - [📋 Prerequisites](#-prerequisites)
  - [1️⃣ Install dependencies](#1️⃣-install-dependencies)
  - [2️⃣ Configure](#2️⃣-configure)
  - [3️⃣ Run the application](#3️⃣-run-the-application)
  - [4️⃣ Open in browser](#4️⃣-open-in-browser)
  - [5️⃣ CLI mode](#5️⃣-cli-mode-no-web-server-needed)
- [🎮 Demo](#-demo)
- [📚 Citation](#-citation)


## 🏫 ITS Paradigm Comparison

<div align="center">
  <p align="center">
    <img src="resources/its-paradigms.png" alt="ITS Paradigm Comparison" width="500" style="box-shadow: 0 8px 24px rgba(0,0,0,0.15); border-radius: 8px;"/>
  </p>
</div>

| Paradigm | Typical characteristics | Primary focus |
|---|---|---|
| 🏫 Traditional MOOC | Static syllabus; pre-recorded lectures; fragmented learning | Broad access, low personalization |
| 🤖 Chatbot ITS | Reactive Q&A; rule/LLM-driven; session-based help | Instant support, limited long-term adaptation |
| 🎯 **Goal-oriented ITS** | Proactive planning; personalized paths; goal-aligned assessments | Targeted skill acquisition, continual adaptation |


## ✨ Core Features

<div align="center">
  <p align="center">
    <img src="resources/genmentor-framework.png" alt="GenMentor Framework" width="700" style="box-shadow: 0 8px 24px rgba(0,0,0,0.15); border-radius: 8px;"/>
  </p>
</div>

### 🤖 Agent Modules

| Agent | Responsibility |
|-------|---------------|
| 🧭 **Goal Refiner** | Transforms raw learning intentions into structured, actionable goals |
| 🔍 **Skill Gap Identifier** | Analyzes current knowledge against goal requirements to surface gaps |
| 👤 **Adaptive Learner Modeler** | Builds and continuously updates learner profiles from interactions |
| 🗓️ **Learning Path Scheduler** | Creates and reschedules personalized session sequences |
| 📝 **Tailored Content Generator** | Produces customized learning materials, knowledge drafts, and documents |
| 📊 **Quiz Generator** | Generates multi-format quizzes (single-choice, multiple-choice, true/false, short answer) |
| 📈 **Performance Evaluator** | Evaluates session performance, skill mastery, and generates progress reports |
| 💬 **Feedback Simulator** | Simulates learner feedback on paths and content for quality assurance |
| 🧑‍🏫 **AI Chatbot Tutor** | Engages learners in context-aware dialogue with memory of past interactions |

### 🔧 Platform Capabilities

- 🎯 **Multi-goal management** — learners can maintain multiple learning goals with independent skill gaps, learning paths, and progress tracking per goal
- 💾 **Goal-scoped persistence** — all data (skill gaps, learning paths, mastery) is stored per goal, allowing learners to switch contexts
- 🔌 **Pluggable LLM backend** — supports OpenAI, DeepSeek, and other LangChain-compatible providers via a unified `provider/model` format
- 🌐 **Web search augmentation** — optional web search integration for knowledge drafting and content generation
- 🛜 **Full REST API** — 25+ endpoints across profile, goals, skills, learning path, content, assessment, chat, and progress domains
- ⌨️ **CLI mode** — run core agent capabilities directly without starting the web application


## 🏗️ Project Architecture

```
gen-mentor/
├── gen_mentor/                    # 📦 Core library (provider-agnostic)
│   ├── agents/                    # 🤖 AI agent implementations
│   │   ├── learning/              #   Goal Refiner, Skill Gap Identifier, Learner Profiler
│   │   ├── content/               #   Path Scheduler, Knowledge Explorer/Drafter,
│   │   │                          #   Document Integrator, Feedback Simulator
│   │   ├── assessment/            #   Quiz Generator, Performance Evaluator
│   │   └── tutoring/              #   Chatbot Tutor
│   ├── core/
│   │   ├── llm/                   # 🧠 LLM factory (LangChain-based)
│   │   ├── memory/                # 💾 LearnerMemoryStore (file-based persistence)
│   │   └── tools/                 # 🔧 Search, RAG, embedding, filesystem tools
│   ├── schemas/                   # 📐 Pydantic domain schemas
│   ├── cli/                       # ⌨️ Command-line interface
│   └── config/                    # ⚙️ YAML config loader & schema definitions
│
├── apps/
│   ├── backend/                   # 🖥️ FastAPI REST API server
│   │   ├── api/v1/endpoints/      #   Route handlers (profile, goals, skills,
│   │   │                          #   learning_path, assessment, chat, progress, ...)
│   │   ├── models/                #   Request / response Pydantic models
│   │   ├── services/              #   LLM service, memory service, user registry
│   │   ├── repositories/          #   Data access layer (LearnerRepository)
│   │   └── middleware/             #   CORS, error handling
│   │
│   └── frontend/                  # 🌐 Next.js web application
│       └── src/
│           ├── app/               #   Pages: onboarding, goals, learning-path,
│           │                      #   session, progress, profile, library
│           ├── components/        #   Reusable UI components
│           └── lib/api.ts         #   Typed API client (all backend endpoints)
│
├── scripts/                       # 📜 Start/stop helper scripts
├── tests/                         # 🧪 Test suite
└── resources/                     # 🖼️ Static assets (images, sample data)
```

**🔄 Data flow:**

```
Frontend (Next.js)  ──HTTP──>  Backend (FastAPI)  ──invokes──>  Agent (gen_mentor)
                                     │                               │
                                     │                          LLM Provider
                                     v                         (OpenAI / DeepSeek / ...)
                              LearnerMemoryStore
                            (workspace/memory/{id}/)
```


## 🚀 Quick Start

### 📋 Prerequisites

- 🐍 Python 3.11+, [uv](https://github.com/astral-sh/uv) (recommended) or pip
- 📗 Node.js 18+ and npm
- 🔑 At least one LLM API key (OpenAI or DeepSeek)

### 1️⃣ Install dependencies

```bash
# Backend
cd apps/backend
uv venv
source .venv/bin/activate  # on Windows: .venv\Scripts\activate
uv pip install -r requirements.txt

# Frontend
cd apps/frontend
npm install
```

### 2️⃣ Configure

GenMentor uses two configuration layers:

| Layer | File | Purpose |
|-------|------|---------|
| **API keys** | `apps/backend/.env` | LLM provider secrets (loaded via `dotenv`) |
| **App config** | `~/.gen-mentor/config.yaml` | Default model, provider endpoints, search, embedding, RAG settings |

**Step A — Set API keys** (required)

Create a `.env` file in `apps/backend/`:

```bash
# At least one is required
OPENAI_API_KEY="your-openai-api-key"
DEEPSEEK_API_KEY="your-deepseek-api-key"
```

**Step B — Set up config.yaml** (optional, auto-created on first run)

```bash
# Copy the example config to the default location
mkdir -p ~/.gen-mentor
cp gen_mentor/config/config.example.yaml ~/.gen-mentor/config.yaml
```

Edit `~/.gen-mentor/config.yaml` to customize:

```yaml
# Default model used by all agents
agent_defaults:
  model: openai/gpt-5.1        # Format: provider/model-name
  temperature: 0.0
  workspace: ~/.gen-mentor/workspace

# Provider endpoints (API keys are read from .env)
providers:
  openai:
    api_key: null               # ← resolved from OPENAI_API_KEY env var
    api_base: null              # optional custom endpoint
  deepseek:
    api_key: null               # ← resolved from DEEPSEEK_API_KEY env var
    api_base: null

# Web search (disabled by default)
search_defaults:
  provider: duckduckgo
  enable_search: false
```

> [!TIP]
> If you skip Step B, GenMentor auto-creates `~/.gen-mentor/config.yaml` from the built-in example on first run. You can always override the model per-request via the `model` parameter (e.g. `"model": "deepseek/deepseek-chat"`).

### 3️⃣ Run the application

> [!NOTE]
> Default ports: **5000** (backend), **3000** (frontend).

**Option A — Manual**

```bash
# Terminal 1: start backend
cd apps/backend
source .venv/bin/activate
uvicorn main:app --reload --port 5000

# Terminal 2: start frontend
cd apps/frontend
npm run dev
```

**Option B — Helper scripts**

```bash
# start both backend and frontend
bash ./scripts/start_service.sh

# stop all
bash ./scripts/stop_service.sh
```

Ports default to 5000/3000. Override with environment variables:

```bash
BACKEND_PORT=8000 FRONTEND_PORT=3001 bash ./scripts/start_service.sh
```

### 4️⃣ Open in browser

| Service | URL |
|---------|-----|
| 🌐 Frontend UI | http://127.0.0.1:3000 |
| 🖥️ Backend API | http://127.0.0.1:5000 |
| 📖 API Docs (Swagger) | http://127.0.0.1:5000/docs |

### 5️⃣ CLI mode (no web server needed)

Run core agent capabilities directly:

```bash
python -m gen_mentor.cli --help
```

```bash
# 🧭 Refine a goal
python -m gen_mentor.cli refine-goal \
  --goal "Become a data engineer" \
  --learner-info "I know Python and SQL" \
  --provider deepseek --model deepseek-chat

# 🔍 Identify skill gaps
python -m gen_mentor.cli identify-skill-gap \
  --goal "Become a data engineer" \
  --learner-info @./resources/learner_info.txt \
  --provider deepseek --model deepseek-chat

# 🗓️ Schedule learning path
python -m gen_mentor.cli schedule-path \
  --learner-profile @./resources/learner_profile.json \
  --session-count 8 \
  --provider deepseek --model deepseek-chat
```


## 🎮 Demo

Welcome to explore the demo version of the GenMentor web application:

👉 [GenMentor Web App](https://gen-mentor.streamlit.app/)

This interactive demo showcases GenMentor's core functionalities, including:

- 🔍 **Skill Gap Identification**: Precisely map learner goals to required skills.
- 👤 **Adaptive Learner Modeling**: Capture learner progress and preferences.
- 📝 **Personalized Content Delivery**: Generate tailored learning resources.

You could also watch the demo video for a quick overview (click the image below):

[![Video Preview](https://img.youtube.com/vi/vTdtGZop-Zc/0.jpg)](https://youtu.be/vTdtGZop-Zc)

## 📚 Citation

```bibtex
@inproceedings{wang2025llm,
  title={LLM-powered Multi-agent Framework for Goal-oriented Learning in Intelligent Tutoring System},
  author={Wang, Tianfu and Zhan, Yi and Lian, Jianxun and Hu, Zhengyu and Yuan, Nicholas Jing and Zhang, Qi and Xie, Xing and Xiong, Hui},
  booktitle={Companion Proceedings of the ACM Web Conference},
  year={2025}
}
```
