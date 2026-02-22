# GenMentor Frontend (Streamlit) Wiki

## 1. Scope and Purpose

This wiki documents the `apps/frontend_streamlit` application:
- Architecture and folder responsibilities
- User flow across pages
- State and persistence model
- Backend API integration strategy
- Mock mode behavior for offline/demo use
- Operational and development guidance

This frontend is a Streamlit web app for learner onboarding, skill-gap analysis, learning path planning, in-session study, and progress management.

---

## 2. High-Level Architecture

The frontend follows a feature-oriented Streamlit structure:
- `main.py` orchestrates app startup, navigation, and global UI behavior
- `pages/` implements user journey screens
- `components/` contains reusable view blocks
- `services/` encapsulates backend API calls
- `utils/` handles state persistence, formatting, style, and helpers
- `assets/` stores static files and mock JSON fixtures

### Runtime pattern
1. Initialize and restore `st.session_state`
2. Route user to onboarding or learning pages based on completion state
3. Render page-level workflows
4. Persist key state fields continuously to local JSON
5. Call backend APIs (or mock fixtures in offline mode)

---

## 3. Directory Responsibilities

```text
apps/frontend_streamlit/
├─ main.py
├─ config.py
├─ pages/
├─ components/
├─ services/
├─ utils/
├─ assets/
└─ .streamlit/
```

### Key folders
- `pages/`: Core screens (`onboarding`, `skill_gap`, `learning_path`, `knowledge_document`, `goal_management`, `learner_profile`, `dashboard`)
- `components/`: Reusable UI modules (chatbot, goal refinement, skill info, top bar, navigation)
- `services/`: HTTP API wrapper (`api_client.py`) and endpoint mapping
- `utils/`: Session-state persistence, PDF parsing, formatting, styling
- `assets/data_example/`: Mock JSON responses used when `use_mock_data=True`

---

## 4. Startup and Navigation Model

File: `main.py`

### Responsibilities
- Calls `initialize_session_state()` at startup
- Enables autosave and persists state changes
- Sets page config, logo, and global CSS
- Performs first-load auto-navigation to learning path after onboarding completion
- Configures dynamic page navigation based on onboarding status
- Provides reset dialog to clear persisted history with backup snapshots

### Navigation groups
- Before onboarding complete:
  - `onboarding`, `skill_gap`, `learning_path`
- After onboarding complete:
  - `goal_management`, `learning_path`, `knowledge_document`, `learner_profile`, `dashboard`

### Reset behavior
- Backs up persisted state to timestamped JSON
- Clears session state
- Redirects user to onboarding page

---

## 5. State and Persistence

File: `utils/state.py`

### Persistence strategy
The app whitelists persistent keys in `PERSIST_KEYS` and stores them in:
- `apps/frontend_streamlit/user_data/data_store.json`

Important persisted entities:
- current goal/session/point selections
- goal list and generated artifacts (`skill_gaps`, `learner_profile`, `learning_path`)
- chat history
- document cache and session learning times
- onboarding and workflow flags

### State lifecycle
1. Initialize defaults for missing session keys
2. Load persisted values into `st.session_state`
3. Update state during interactions
4. Save state opportunistically after major actions and page transitions

### Goal model in session state
Each goal entry includes:
- `id`
- `learning_goal`
- `skill_gaps`
- `learner_profile`
- `learning_path`
- `is_completed`
- `is_deleted`

---

## 6. Core User Flows

## 6.1 Onboarding (`pages/onboarding.py`)
- Two-step card flow:
  1. learning goal input and AI refinement
  2. learner information collection (occupation + optional PDF + free text)
- Continue action validates required fields then routes to skill-gap page

## 6.2 Learning Path (`pages/learning_path.py`)
- Validates onboarding and skill-gap completion gates
- Auto-schedules path if absent via API
- Displays progress, session cards, and reschedule controls
- Routes selected session to knowledge-document page

## 6.3 Knowledge Document (`pages/knowledge_document.py`)
- Prepares content per session (or reads from cache)
- Multi-stage generation pipeline:
  1. explore knowledge points
  2. draft knowledge points
  3. integrate learning document
  4. generate quizzes
- Supports regenerate, complete-session, and feedback updates
- Uses section-based pagination and anchor navigation
- Tracks session learning time and motivational prompts

---

## 7. Backend API Integration

File: `services/api_client.py`

### Integration pattern
- `API_NAMES` defines endpoint name mapping
- `make_post_request()` sends HTTP POST to `config.backend_endpoint`
- timeout is long (`500s`) for LLM-heavy tasks
- returns parsed JSON or fallback placeholders

### Primary frontend API methods
- `chat_with_tutor`
- `refine_learning_goal`
- `identify_skill_gap`
- `create_learner_profile`
- `update_learner_profile`
- `schedule_learning_path`
- `reschedule_learning_path`
- `explore_knowledge_points`
- `draft_knowledge_points`
- `integrate_learning_document`
- `generate_document_quizzes`

### Contract caveat
Some payload fields still use stringified objects and legacy names (`llm_type`, `method_name`), while backend has model-provider fields. Current backend defaults tolerate this, but contract cleanup is recommended.

---

## 8. Configuration and Modes

File: `config.py`

```python
backend_endpoint = "http://127.0.0.1:5000/"
use_mock_data = False
use_search = True
```

### Mode A: live backend
- `use_mock_data=False`
- frontend calls backend endpoints

### Mode B: mock/offline
- `use_mock_data=True`
- API wrappers load fixture JSON from `assets/data_example/`
- useful for UI demos and front-end iteration without backend

---

## 9. Assets and Styling

- Global CSS loaded in `main.py` from `assets/css/main.css`
- Additional static data fixtures in `assets/data_example/`
- JS helper for document auto-scroll in `assets/js/doc_reading.py`

---

## 10. Run and Dev Workflow

## Local startup
```bash
cd apps/frontend_streamlit
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
streamlit run main.py
```

## Backend integration
- Ensure backend is reachable at `config.backend_endpoint`
- For changed host/port, update `config.py`

## Development tips
- Keep reusable UI logic in `components/`
- Keep page orchestration in `pages/`
- Keep API logic centralized in `services/api_client.py`
- Preserve session-state keys to avoid migration breaks

---

## 11. Troubleshooting

### App cannot reach backend
- verify backend process and endpoint URL
- inspect response status in Streamlit logs

### Missing/incorrect styles
- verify `assets/css/main.css` path
- run from `apps/frontend_streamlit` directory

### Slow or timeout requests
- LLM pipelines are multi-stage and can be slow
- increase request timeout in `services/api_client.py` if needed

### Unexpected page state
- check persisted file at `user_data/data_store.json`
- use reset button (sidebar) to clear local history safely

---

## 12. Known Technical Debt

1. `services/api_client.py` and `utils/request_api.py` overlap in role (compatibility residue)
2. Mixed/new endpoint naming exists in `API_NAMES`
3. Some API payload contracts are string-based rather than strongly typed JSON
4. Error handling often returns broad fallback objects; typed error envelopes would improve debuggability

---

## 13. Suggested Improvements (Incremental)

1. Consolidate all API calls to `services/api_client.py` only
2. Normalize payload schemas and remove stringified object transport
3. Add page-level smoke tests for onboarding → path → knowledge flow
4. Formalize session-state schema and migration strategy for persisted keys
5. Add a small diagnostics panel for backend connectivity and current config values

---

## 14. Quick File Index

Start here when onboarding new contributors:
- `main.py`
- `config.py`
- `utils/state.py`
- `services/api_client.py`
- `pages/onboarding.py`
- `pages/learning_path.py`
- `pages/knowledge_document.py`

This set gives full visibility into startup, state, API contracts, and core learning workflows.
