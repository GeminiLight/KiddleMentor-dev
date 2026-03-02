# GenMentor Backend Endpoint Summary & Gap Analysis

**Date**: 2026-03-02

---

## 1. Existing Endpoints

### Category A: Algo-Agent-Related Endpoints

These endpoints invoke LLM-based algorithm agents from `gen_mentor` package.

| # | Method | Endpoint | Algo Agent Function | Description |
|---|--------|----------|-------------------|-------------|
| A1 | POST | `/profile/set-goal` | `refine_learning_goal_with_llm()` | Refine & set learning goal |
| A2 | POST | `/profile/create-learner-profile` | `initialize_learner_profile_with_llm()` | Create structured learner profile from info + skill gaps |
| A3 | POST | `/goals/refine-learning-goal` | `refine_learning_goal_with_llm()` | Standalone goal refinement (no save) |
| A4 | POST | `/skills/identify-skill-gap` | `identify_skill_gap_with_llm()` | Identify skill gaps (no save) |
| A5 | POST | `/skills/identify-skill-gap-with-info` | `identify_skill_gap_with_llm()` | Identify skill gaps with extra info |
| A6 | POST | `/skills/identify-and-save-skill-gap` | `identify_skill_gap_with_llm()` | Identify skill gaps and persist to memory |
| A7 | POST | `/learning/schedule-learning-path` | `schedule_learning_path_with_llm()` | Generate personalized learning path |
| A8 | POST | `/learning/reschedule-learning-path` | `reschedule_learning_path_with_llm()` | Reschedule path based on feedback |
| A9 | POST | `/learning/explore-knowledge-points` | `explore_knowledge_points_with_llm()` | Explore knowledge points for a session |
| A10 | POST | `/learning/draft-knowledge-point` | `draft_knowledge_point_with_llm()` | Draft a single knowledge point |
| A11 | POST | `/learning/integrate-learning-document` | `integrate_learning_document_with_llm()` | Integrate drafts into final document |
| A12 | POST | `/learning/tailor-knowledge-content` | `create_learning_content_with_llm()` | Full pipeline: explore + draft + integrate + quiz |
| A13 | POST | `/assessment/generate-document-quizzes` | `generate_document_quizzes_with_llm()` | Generate quizzes from a document |
| A14 | POST | `/chat/chat-with-tutor` | `chat_with_tutor_with_llm()` | AI tutor conversation with RAG + memory |

**Total: 14 algo-agent endpoints**

---

### Category B: Non-Agent Endpoints (CRUD / System / Utility)

These endpoints do NOT invoke LLM agents. They handle data access, user management, and system operations.

| # | Method | Endpoint | Description |
|---|--------|----------|-------------|
| B1 | GET | `/health` | Health check |
| B2 | GET | `/storage-info` | Storage configuration info |
| B3 | GET | `/list-llm-models` | List available LLM models |
| B4 | GET | `/users/list` | List all registered users |
| B5 | POST | `/users/login` | Login existing user |
| B6 | POST | `/users/sync` | Sync user registry from disk |
| B7 | POST | `/users/delete` | Delete user account + data |
| B8 | POST | `/profile/initialize-session` | Initialize new learner session (generate ID, save basic profile) |
| B9 | GET | `/profile/{learner_id}` | Get learner profile |
| B10 | POST | `/profile/update-learner-profile` | Update profile fields |
| B11 | GET | `/dashboard/{learner_id}` | Get aggregated dashboard data |
| B12 | POST | `/progress/{learner_id}/session-complete` | Mark session complete, update mastery |
| B13 | GET | `/memory/learner-memory/{id}` | Get full learner memory dump |
| B14 | POST | `/memory/learner-memory/{id}/search-history` | Search interaction history |

**Total: 14 non-agent endpoints**

---

## 2. Missing Endpoints (Should Be Added)

Based on cross-referencing the algorithm agent functions (wiki_algo.md) and frontend needs (wiki_frontend.md), the following endpoints are missing from the backend:

### Category A: Missing Algo-Agent Endpoints

| # | Proposed Endpoint | Algo Agent Function | Rationale |
|---|------------------|-------------------|-----------|
| MA1 | `POST /profile/update-learner-profile-with-ai` | `update_learner_profile_with_llm()` | The algo layer has a profile UPDATE function that adapts the profile based on recent interactions, session data, and performance. Currently the backend only has a CRUD `update-learner-profile` (B10) which does not invoke AI. After each session, the profile should be AI-updated to reflect new cognitive status, preference changes, and behavioral patterns. |
| MA2 | `POST /assessment/evaluate-performance` | `evaluate_learner_performance_with_llm()` | The algo layer has a full performance evaluator that assesses overall score, strengths/weaknesses, progress status, skill evaluations, and recommendations. No backend endpoint exposes this. The frontend's session-complete flow (B12) only does simple mastery averaging, not AI-powered evaluation. |
| MA3 | `POST /assessment/evaluate-skill-mastery` | `evaluate_skill_mastery_with_llm()` | Evaluates mastery of a specific skill with understanding/proficiency scores, gap analysis, improvement tracking, and time-to-mastery estimates. No endpoint exists for this. |
| MA4 | `POST /assessment/generate-performance-report` | `generate_performance_report_with_llm()` | Generates a comprehensive text report of learner performance over a time period. Useful for the Library page's "Goal Summary" feature and Profile page stats. |
| MA5 | `POST /learning/simulate-feedback` | `LearnerFeedbackSimulator.feedback_path()` / `feedback_content()` | The algo layer can simulate learner feedback for paths and content (for quality evaluation). Could be exposed for internal testing or as a "rate this path" AI feature. |

### Category B: Missing Non-Agent Endpoints

| # | Proposed Endpoint | Rationale |
|---|------------------|-----------|
| MB1 | `GET /profile/{learner_id}/goals` | The frontend Goals page needs to list all goals for a learner. Currently this data comes from `getLearnerMemory` (B13), but a dedicated endpoint would be cleaner and support pagination. |
| MB2 | `POST /profile/{learner_id}/goals/{goal_id}/activate` | The frontend Goals page shows active/inactive goal badges and allows switching. No dedicated endpoint for changing goal status exists. |
| MB3 | `GET /profile/{learner_id}/goals/{goal_id}/skill-gaps` | The frontend Skill Gap page and Goals detail sidebar need skill gaps per goal. Currently embedded in memory dump. A dedicated endpoint would be more efficient. |
| MB4 | `GET /profile/{learner_id}/goals/{goal_id}/learning-path` | Similar to above — the frontend Learning Path page needs the learning path for the current goal. Currently requires full memory dump + client-side filtering. |
| MB5 | `POST /progress/{learner_id}/session-complete` (enhanced) | The existing endpoint (B12) does simple averaging. It should also trigger `update_learner_profile_with_llm()` and optionally `evaluate_learner_performance_with_llm()` as a post-processing step, or at minimum accept `goal_id` to update the correct goal's path. |
| MB6 | `GET /profile/{learner_id}/activity` | The frontend Progress page shows "recent activity" and Library page shows archived content. No dedicated activity/history endpoint exists beyond search-history (B14). |
| MB7 | `POST /profile/{learner_id}/upload-cv` | The frontend Onboarding and Profile pages support CV upload with drag-and-drop. While `initialize-session` (B8) accepts a `cv` field in FormData, there's no standalone CV upload endpoint for updating an existing profile's background. |

---

## 3. Summary Matrix

```
                    Existing    Missing    Total Needed
                    --------    -------    ------------
Algo-Agent            14          5            19
Non-Agent             14          7            21
                    --------    -------    ------------
Total                 28         12            40
```

### Priority Recommendations

**High Priority** (core learning loop gaps):

| # | Endpoint | Why |
|---|----------|-----|
| MA1 | `update-learner-profile-with-ai` | Without this, learner profiles become stale after onboarding. The profile never adapts to actual learning behavior. |
| MA2 | `evaluate-performance` | The session-complete flow lacks meaningful AI assessment. Quiz scores are averaged naively instead of being evaluated holistically. |
| MB5 | Enhanced `session-complete` | Current endpoint doesn't support `goal_id`, so multi-goal progress tracking breaks. |

**Medium Priority** (UX improvements):

| # | Endpoint | Why |
|---|----------|-----|
| MB1 | `GET goals` | Cleaner API than filtering memory dump client-side. |
| MB3 | `GET skill-gaps per goal` | Skill Gap page currently has no dedicated data source. |
| MB4 | `GET learning-path per goal` | Learning Path page needs goal-scoped data. |
| MA4 | `generate-performance-report` | Library page "Goal Summary" feature is currently mocked/simulated. |

**Low Priority** (nice-to-have):

| # | Endpoint | Why |
|---|----------|-----|
| MA3 | `evaluate-skill-mastery` | Granular skill-level evaluation, useful but not blocking. |
| MA5 | `simulate-feedback` | Internal testing/quality tool. |
| MB2 | `activate goal` | Can be approximated via memory operations. |
| MB6 | `GET activity` | Can be approximated via search-history. |
| MB7 | `upload-cv` | Can be worked around via initialize-session. |

---

## 4. Algo Agent Coverage Map

Maps every algorithm agent function to its backend endpoint status:

| Algo Agent Function | Backend Endpoint | Status |
|---|---|---|
| `refine_learning_goal_with_llm` | `/profile/set-goal`, `/goals/refine-learning-goal` | Covered (2 endpoints) |
| `identify_skill_gap_with_llm` | `/skills/identify-skill-gap`, `/skills/identify-skill-gap-with-info`, `/skills/identify-and-save-skill-gap` | Covered (3 endpoints) |
| `initialize_learner_profile_with_llm` | `/profile/create-learner-profile` | Covered |
| `update_learner_profile_with_llm` | -- | **MISSING** |
| `simulate_learner_interactions_with_llm` | -- | Not needed (internal testing only) |
| `schedule_learning_path_with_llm` | `/learning/schedule-learning-path` | Covered |
| `reschedule_learning_path_with_llm` | `/learning/reschedule-learning-path` | Covered |
| `explore_knowledge_points_with_llm` | `/learning/explore-knowledge-points` | Covered |
| `draft_knowledge_point_with_llm` | `/learning/draft-knowledge-point` | Covered |
| `integrate_learning_document_with_llm` | `/learning/integrate-learning-document` | Covered |
| `create_learning_content_with_llm` | `/learning/tailor-knowledge-content` | Covered |
| `LearnerFeedbackSimulator` | -- | **MISSING** (low priority) |
| `chat_with_tutor_with_llm` | `/chat/chat-with-tutor` | Covered |
| `generate_document_quizzes_with_llm` | `/assessment/generate-document-quizzes` | Covered |
| `evaluate_learner_performance_with_llm` | -- | **MISSING** |
| `evaluate_skill_mastery_with_llm` | -- | **MISSING** |
| `generate_performance_report_with_llm` | -- | **MISSING** |

**Coverage**: 11/16 agent functions exposed (69%), 5 missing

---

*Report generated: 2026-03-02*
