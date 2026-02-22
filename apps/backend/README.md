# GenMentor Backend

**Version**: 1.0.0 | **Status**: Production Ready | [📖 Full Documentation (wiki.md)](wiki.md)

---

GenMentor is an AI-powered personalized learning platform that creates adaptive learning experiences tailored to individual learners' needs, skill gaps, and goals.

## 🚀 Quick Start

### Installation

```bash
# Navigate to backend directory
cd apps/backend

# Create virtual environment
uv venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies
uv pip install -r requirements.txt

# Set up configuration
cp ../../gen_mentor/config/config.example.yaml ../../gen_mentor/config/config.yaml

# Set API keys
export OPENAI_API_KEY="your-key"
export DEEPSEEK_API_KEY="your-key"
```

### Run Server

```bash
# Start the FastAPI server
python main.py

# Or use uvicorn directly
uvicorn main:app --reload --host 0.0.0.0 --port 5000
```

**Access**:
- API: http://localhost:5000/api/v1
- Swagger UI: http://localhost:5000/docs
- ReDoc: http://localhost:5000/redoc

### Quick Test

```bash
# Health check
curl http://localhost:5000/api/v1/health

# Chat with AI tutor
curl -X POST "http://localhost:5000/api/v1/chat/chat-with-tutor" \
  -H "Content-Type: application/json" \
  -d '{"messages": "[{\"role\": \"user\", \"content\": \"Hello!\"}]"}'
```

---

## ✨ Features

| Feature | Description | Endpoint |
|---------|-------------|----------|
| 🤖 **AI Chatbot Tutor** | Interactive conversational learning | `/api/v1/chat/*` |
| 🎯 **Goal Refinement** | Define clear learning objectives | `/api/v1/goals/*` |
| 📊 **Skill Gap Analysis** | Identify knowledge gaps | `/api/v1/skills/*` |
| 👤 **Learner Profiling** | Adaptive learner modeling | `/api/v1/profile/*` |
| 📚 **Content Delivery** | Personalized learning materials | `/api/v1/learning/*` |
| 📝 **Quiz Generation** | Automated assessments | `/api/v1/assessment/*` |
| 💾 **Memory System** | Context persistence | `/api/v1/memory/*` |

---

## 📁 Architecture

### Clean Modular Design

```
apps/backend/
├── main.py                    # FastAPI entry point (120 lines)
├── api/v1/endpoints/          # 8 endpoint modules (20 endpoints total)
├── models/                    # Pydantic models (29 models)
├── services/                  # Business logic (LLM, Memory)
├── middleware/                # Error handling
└── wiki.md                    # Complete documentation
```

### Technology Stack

- **Framework**: FastAPI 0.115+
- **Language**: Python 3.12+
- **Validation**: Pydantic V2
- **LLM**: LangChain + Multi-provider support
- **Configuration**: Hydra + YAML
- **Vector DB**: ChromaDB
- **Embeddings**: Sentence Transformers / OpenAI

---

## 📚 API Endpoints

> **Note**: All endpoints use `/api/v1` prefix. See [wiki.md](wiki.md) for detailed API reference.

### System (3 endpoints)

```bash
GET  /api/v1/health                  # Health check
GET  /api/v1/storage-info            # Storage configuration
GET  /api/v1/list-llm-models         # Available models
```

### Chat (1 endpoint)

```bash
POST /api/v1/chat/chat-with-tutor    # AI tutor chat
```

### Goals (1 endpoint)

```bash
POST /api/v1/goals/refine-learning-goal  # Refine learning goal
```

### Skills (2 endpoints)

```bash
POST /api/v1/skills/identify-skill-gap-with-info  # Skill gap (info)
POST /api/v1/skills/identify-skill-gap            # Skill gap (CV upload)
```

### Profile (3 endpoints)

```bash
POST /api/v1/profile/create-learner-profile            # Create profile (info)
POST /api/v1/profile/create-learner-profile-with-cv-pdf # Create profile (CV)
POST /api/v1/profile/update-learner-profile            # Update profile
```

### Learning (7 endpoints)

```bash
POST /api/v1/learning/schedule-learning-path        # Schedule learning path
POST /api/v1/learning/reschedule-learning-path      # Reschedule path
POST /api/v1/learning/explore-knowledge-points      # Explore topics
POST /api/v1/learning/draft-knowledge-point         # Draft single topic
POST /api/v1/learning/draft-knowledge-points        # Draft multiple topics
POST /api/v1/learning/integrate-learning-document   # Integrate drafts
POST /api/v1/learning/tailor-knowledge-content      # Complete content generation
```

### Assessment (1 endpoint)

```bash
POST /api/v1/assessment/generate-document-quizzes   # Generate quizzes
```

### Memory (2 endpoints)

```bash
GET  /api/v1/memory/learner-memory/{learner_id}              # Get memory
POST /api/v1/memory/learner-memory/{learner_id}/search-history # Search history
```

---

## 🔧 Configuration

### Default Model Configuration

Model defaults are loaded from `gen_mentor/config/config.yaml`:

```yaml
agent_defaults:
  model: "openai/gpt-4o"      # Format: provider/model_name
  temperature: 0.0
  max_tokens: 8192
  workspace: ~/.gen-mentor/workspace
```

All request models inherit these defaults. Clients can override per-request.

### Environment Variables

```bash
# Required: At least one LLM provider
export OPENAI_API_KEY="sk-..."
export ANTHROPIC_API_KEY="sk-ant-..."
export DEEPSEEK_API_KEY="sk-..."

# Optional: Custom defaults
export AGENT_DEFAULTS_MODEL="openai/gpt-4o"
export BACKEND_UPLOAD_LOCATION="/tmp/uploads"
export BACKEND_WORKSPACE_DIR="~/.gen-mentor/workspace"
```

### Supported LLM Providers

| Provider | Models | Configuration |
|----------|--------|---------------|
| **OpenAI** | gpt-4o, gpt-4o-mini, gpt-3.5-turbo | `OPENAI_API_KEY` |
| **Anthropic** | claude-3-5-sonnet, claude-3-sonnet, claude-3-haiku | `ANTHROPIC_API_KEY` |
| **DeepSeek** | deepseek-chat, deepseek-coder | `DEEPSEEK_API_KEY` |
| **Together** | Various open-source models | `TOGETHER_API_KEY` |
| **Groq** | Fast inference models | `GROQ_API_KEY` |
| **Ollama** | Local models (llama2, mistral, etc.) | Configure `api_base` |

See [wiki.md - Configuration](wiki.md#configuration) for complete details.

---

## 📖 Documentation

### Core Documentation

- **[wiki.md](wiki.md)** - Complete backend documentation (architecture, API reference, development guide)
- **[README.md](README.md)** - This file (quick start and overview)

### Additional Documentation

- **[REFACTORING_COMPLETE.md](REFACTORING_COMPLETE.md)** - Refactoring details and improvements
- **[ENDPOINT_MIGRATION.md](ENDPOINT_MIGRATION.md)** - Migration guide from legacy API
- **[MODEL_DEFAULTS_ALIGNMENT.md](MODEL_DEFAULTS_ALIGNMENT.md)** - Configuration alignment details
- **[ENDPOINT_NAMING_IMPROVEMENT.md](ENDPOINT_NAMING_IMPROVEMENT.md)** - Endpoint naming changes

### Interactive Documentation

- **Swagger UI**: http://localhost:5000/docs - Interactive API testing
- **ReDoc**: http://localhost:5000/redoc - Beautiful API documentation
- **OpenAPI**: http://localhost:5000/openapi.json - OpenAPI specification

---

## 🧪 Testing

### Run Tests

```bash
# Test refactored API
python test_refactored.py

# Integration tests
python test_integration.py

# Using pytest (if configured)
pytest tests/ -v
```

### Test Coverage

- ✅ Health and system endpoints
- ✅ Chat functionality
- ✅ Goal refinement
- ✅ Skill gap identification
- ✅ Profile management
- ✅ Learning path generation
- ✅ Quiz generation
- ✅ Memory persistence

---

## 🏗️ Development

### Project Structure

```
apps/backend/
├── main.py                          # Application entry point
├── config.py                        # Backend settings
├── dependencies.py                  # FastAPI dependencies
├── exceptions.py                    # Custom exceptions
│
├── api/v1/                          # API Layer
│   ├── router.py                    # Route aggregation
│   └── endpoints/                   # Endpoint modules
│       ├── system.py                # Health, storage, models
│       ├── chat.py                  # AI tutor
│       ├── goals.py                 # Goal management
│       ├── skills.py                # Skill analysis
│       ├── profile.py               # Profile management
│       ├── learning_path.py         # Learning paths & content
│       ├── assessment.py            # Quiz generation
│       └── memory.py                # Context management
│
├── models/                          # Data Models
│   ├── common.py                    # Base models
│   ├── defaults.py                  # Config-driven defaults
│   ├── requests.py                  # Request schemas (15)
│   └── responses.py                 # Response schemas (14)
│
├── services/                        # Service Layer
│   ├── llm_service.py               # LLM provider management
│   └── memory_service.py            # Memory persistence
│
└── middleware/                      # Middleware
    └── error_handler.py             # Global error handling
```

### Adding New Endpoints

See [wiki.md - Development Guide](wiki.md#development-guide) for step-by-step instructions.

### Code Style

- Follow PEP 8
- Use type hints
- Document public APIs
- Write meaningful commit messages
- Add tests for new features

---

## 🚀 Deployment

### Production Server

```bash
# Install Gunicorn
pip install gunicorn

# Run with Gunicorn + Uvicorn workers
gunicorn main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:5000 \
  --access-logfile - \
  --error-logfile -
```

### Docker

```dockerfile
FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
EXPOSE 5000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000"]
```

### Production Checklist

- [ ] Set `debug: false` in config
- [ ] Use environment variables for secrets
- [ ] Configure proper logging
- [ ] Set up authentication/authorization
- [ ] Configure CORS
- [ ] Use HTTPS
- [ ] Set up monitoring
- [ ] Configure rate limiting
- [ ] Backup workspace data

See [wiki.md - Deployment](wiki.md#deployment) for detailed deployment guide.

---

## 🔍 Memory System

The backend automatically persists learner context in local mode:

### Storage Structure

```
~/.gen-mentor/workspace/
└── learners/
    └── {learner_id}/
        ├── profile.json       # Learner profile
        ├── goals.json         # Learning goals
        ├── progress.json      # Learning progress
        └── history.jsonl      # Interaction history
```

### Automatic Logging

All endpoints automatically log interactions to memory:

- Profile creation/updates
- Goal refinement
- Skill gap identification
- Learning path scheduling
- Content generation
- Quiz completion

See [wiki.md - Memory System](wiki.md#memory-system) for details.

---

## 🆘 Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| Import errors | Use absolute imports (`from services import ...`) |
| 404 errors | Ensure using `/api/v1` prefix |
| API key errors | Set environment variables for LLM providers |
| Memory not persisting | Check workspace directory permissions |
| Model default mismatch | Update `gen_mentor/config/config.yaml` |

See [wiki.md - Troubleshooting](wiki.md#troubleshooting) for complete troubleshooting guide.

### Debug Mode

```yaml
# config.yaml
debug: true
log_level: DEBUG
```

### Health Checks

```bash
curl http://localhost:5000/api/v1/health
curl http://localhost:5000/api/v1/list-llm-models
curl http://localhost:5000/api/v1/storage-info
```

---

## 📊 API Request/Response Examples

### Example 1: Chat with Tutor

**Request**:
```bash
curl -X POST "http://localhost:5000/api/v1/chat/chat-with-tutor" \
  -H "Content-Type: application/json" \
  -d '{
    "messages": "[{\"role\": \"user\", \"content\": \"Explain recursion\"}]",
    "learner_profile": "{\"level\": \"beginner\"}"
  }'
```

**Response**:
```json
{
  "success": true,
  "message": "Chat response generated",
  "response": "Recursion is a programming technique where a function calls itself..."
}
```

### Example 2: Refine Learning Goal

**Request**:
```bash
curl -X POST "http://localhost:5000/api/v1/goals/refine-learning-goal" \
  -H "Content-Type: application/json" \
  -d '{
    "learning_goal": "Learn programming",
    "learner_information": "No experience"
  }'
```

**Response**:
```json
{
  "success": true,
  "message": "Learning goal refined",
  "refined_goal": {
    "original_goal": "Learn programming",
    "refined_goal": "Master Python fundamentals for web development",
    "subgoals": ["Learn Python syntax", "Build simple web apps"],
    "timeline": "3-6 months"
  }
}
```

### Example 3: Generate Learning Content

**Request**:
```bash
curl -X POST "http://localhost:5000/api/v1/learning/tailor-knowledge-content" \
  -H "Content-Type: application/json" \
  -d '{
    "learner_profile": "{\"level\": \"beginner\"}",
    "learning_path": "{\"sessions\": []}",
    "learning_session": "{\"topic\": \"JavaScript Basics\"}",
    "use_search": true,
    "with_quiz": true
  }'
```

**Response**:
```json
{
  "success": true,
  "message": "Learning content generated",
  "learning_document": {
    "topic": "JavaScript Basics",
    "content": "...",
    "quizzes": [...]
  }
}
```

See [wiki.md - API Reference](wiki.md#api-reference) for complete examples.

---

## 🔄 Recent Updates

### v1.0.0 (2026-02-22)

**Major Refactoring**:
- ✅ Refactored from monolithic 815-line `main.py` to modular architecture
- ✅ Implemented 20 endpoints across 8 logical modules
- ✅ Added configuration-driven model defaults
- ✅ Improved endpoint naming for clarity
- ✅ Integrated memory persistence system
- ✅ Added comprehensive error handling
- ✅ Created full documentation (wiki.md)

**Breaking Changes**:
- All endpoints now require `/api/v1` prefix
- Profile endpoints renamed for clarity

See [ENDPOINT_MIGRATION.md](ENDPOINT_MIGRATION.md) for migration guide.

---

## 📄 License

This project is part of the GenMentor research initiative.

---

## 🤝 Support

- **Documentation**: See [wiki.md](wiki.md) for complete documentation
- **Interactive API**: Visit http://localhost:5000/docs for Swagger UI
- **Issues**: Report issues in the repository

---

## 🎯 Next Steps

1. **Explore the API**: Visit http://localhost:5000/docs
2. **Read the Wiki**: See [wiki.md](wiki.md) for detailed documentation
3. **Try Examples**: Test the API with the examples above
4. **Build Something**: Integrate GenMentor into your application

---

**Built with ❤️ by the GenMentor Team**
