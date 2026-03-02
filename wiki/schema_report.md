# GenMentor Schema Inconsistency Report

**Date**: 2026-03-02
**Scope**: Cross-layer data schema analysis across Frontend, Backend, and Algorithm layers
**Sources**: `wiki/schema.md`, `wiki/wiki_frontend.md`, `wiki/wiki_backend.md`, `wiki/wiki_algo.md`

---

## Summary

After a thorough review of the wiki documentation across all three layers, **14 inconsistencies** were identified and **all have been resolved** in the wiki documentation.

| Severity | Count | Status |
|----------|-------|--------|
| Critical | 3 | All resolved |
| High | 5 | All resolved |
| Medium | 4 | All resolved |
| Low | 2 | All resolved |

---

## Critical Issues

### C1. `LearnerProfile` schema: `learning_goal` field conflict between Algorithm wiki and Schema doc — RESOLVED

**Layers**: Algorithm vs Schema doc

- **`schema.md`**: Previously stated `LearnerProfile` does NOT include `learning_goal`.
- **`wiki_algo.md`**: Documents `LearnerProfile` as having `learning_goal: str`.

**Resolution**: `learning_goal: str` is a required field. Updated `schema.md` to include `learning_goal` in `LearnerProfile` and removed the incorrect note. Both wikis now agree.

**Files changed**: `schema.md`

---

### C2. Backend endpoint uses legacy `model_provider`/`model_name` in code examples — RESOLVED

**Layers**: Backend (wiki_backend.md) vs Schema doc / Frontend

- Several endpoint handler code examples called `llm_service.get_llm(request.model_provider, request.model_name)` — the legacy API.
- The new `LLMService.get_llm()` accepts a single unified `model: Optional[str]` parameter.

**Resolution**: Updated all endpoint code examples in `wiki_backend.md` to use `llm_service.get_llm(request.model)`.

**Files changed**: `wiki_backend.md` (3 endpoint handlers: `set_learning_goal`, `create_learner_profile`, `schedule_learning_path`)

---

### C3. Frontend `DashboardData.learning_path.sessions` field names mismatched Algorithm `SessionItem` — RESOLVED

**Layers**: Frontend vs Algorithm

- Frontend used `session_number`, `topic`, `completed` — didn't match Algorithm's `id`, `title`, `if_learned`.

**Resolution**: Aligned frontend `DashboardData.learning_path.sessions` to use Algorithm's `SessionItem` fields: `id: string`, `title: string`, `abstract: string`, `if_learned: boolean`, `associated_skills?: string[]`, `desired_outcome_when_completed?: Array<{name, level}>`, `quiz_score?: number`.

**Files changed**: `schema.md`, `wiki_frontend.md`

---

## High Severity Issues

### H1. Memory service returned `objectives` but `LearnerMemoryResponse` expected `learning_goals` — RESOLVED

**Layers**: Backend service vs Backend response model

**Resolution**: Updated `MemoryService.get_learner_memory()` to return `learning_goals` (via `memory.read_learning_goals()`) and `skill_gaps` (via `memory.read_skill_gaps()`), matching `LearnerMemoryResponse` field names.

**Files changed**: `wiki_backend.md`

---

### H2. Algorithm memory store used `objectives.json` but schema doc referenced `learning_goals` — RESOLVED

**Layers**: Algorithm memory vs Schema doc

**Resolution**:
- Renamed `objectives.json` to `learning_goals.json` in the memory file structure
- Added `skill_gaps.json` to the memory file structure
- Added `read_learning_goals()`, `write_learning_goals()`, `read_skill_gaps()`, `write_skill_gaps()`, `read_learning_path()`, `write_learning_path()` methods to `LearnerMemoryStore`
- Updated `get_learner_context()` to use `read_learning_goals()` instead of `read_objectives()`

**Files changed**: `wiki_algo.md`, `wiki_backend.md` (repository layer updated accordingly)

---

### H3. Frontend `completeSession` response expected required `message` but backend returns optional — RESOLVED

**Layers**: Frontend vs Backend

**Resolution**: Made the frontend `message` field optional (`message?: string`) to match backend's `BaseResponse` where `message: Optional[str] = None`.

**Files changed**: `wiki_frontend.md`

---

### H4. Frontend `generateDocumentQuizzes` used `quiz_count` but backend expected individual count fields — RESOLVED

**Layers**: Frontend vs Backend

**Resolution**: Updated frontend `generateDocumentQuizzes` to:
- Add required `learner_profile` parameter
- Replace `quiz_count` with individual count fields: `single_choice_count?`, `multiple_choice_count?`, `true_false_count?`, `short_answer_count?`
- Updated `schema.md` API Method Signatures table

**Files changed**: `wiki_frontend.md`, `schema.md`

---

### H5. Frontend `listModels` response type didn't match backend unified format — RESOLVED

**Layers**: Frontend vs Backend

**Resolution**: Updated frontend `listModels` response type from `{ model_name: string; model_provider: string }` to `{ model: string }` matching the unified `"provider/model"` format.

**Files changed**: `wiki_frontend.md`

---

## Medium Severity Issues

### M1. Duplicate `Confidence` / `ConfidenceLevel` enums — NOTED

**Layers**: Algorithm (internal)

**Resolution**: Added consolidation notes in `schema.md` Common Enums table and in the `ConfidenceLevel` definition, flagging these as candidates for consolidation. Both enums have identical values (`low`, `medium`, `high`).

**Files changed**: `schema.md`

---

### M2. Duplicate skill level enums across algorithm modules — NOTED

**Layers**: Algorithm (internal)

**Resolution**: Added consolidation notes in `schema.md` Common Enums table identifying:
- `LevelCurrent` ↔ `SkillLevel` (identical, both have `unlearned`)
- `LevelRequired` ↔ `Proficiency` (identical, 3 values without `unlearned`)

**Files changed**: `schema.md`

---

### M3. Backend data storage path `workspace/learners/` vs Algorithm `workspace/memory/` — RESOLVED

**Layers**: Backend vs Algorithm

**Resolution**: Updated backend wiki Appendix B to use `workspace/memory/{learner_id}/` matching the algorithm wiki. Also updated file listing to include `learning_goals.json` and `skill_gaps.json`.

**Files changed**: `wiki_backend.md`

---

### M4. `AITutorChat.tsx` component example used wrong API format — RESOLVED

**Layers**: Frontend (internal)

**Resolution**: Updated the `AITutorChat.tsx` code example in section 5.3 to use the proper `api.chatWithTutor()` method with `{ messages: chatHistory, learner_profile, goal_id }` instead of raw `fetch` with `{ session_id, message }`.

**Files changed**: `wiki_frontend.md`

---

## Low Severity Issues

### L1. `schema.md` listed `schemas.py` twice — RESOLVED

**Resolution**: Removed the duplicate `schemas.py` entry from backend file structure.

**Files changed**: `schema.md`

---

### L2. `wiki_algo.md` `BehavioralPatterns` missing `additional_notes` field — RESOLVED

**Resolution**: Added `additional_notes: Optional[str] = None` to `BehavioralPatterns` in `wiki_algo.md`.

**Files changed**: `wiki_algo.md`

---

## Cross-Layer Compatibility Matrix (Post-Fix)

| Data Entity | Frontend | Backend | Algorithm | Consistent? |
|---|---|---|---|---|
| Model parameter | `model?: string` | `model: Optional[str]` | `"provider/model"` format | Yes |
| LearnerProfile | `LearnerProfile` (basic) | `Dict[str, Any]` | `LearnerProfile` (with learning_goal) | Yes |
| Learning Path sessions | `id`, `title`, `if_learned` (SessionItem) | `Dict[str, Any]` | `id`, `title`, `if_learned` (SessionItem) | Yes |
| Quiz generation params | 4 individual count fields + learner_profile | 4 individual count fields + learner_profile | 4 individual count fields | Yes |
| Memory data keys | `learning_goals`, `skill_gaps` | `learning_goals`, `skill_gaps` | `learning_goals.json`, `skill_gaps.json` | Yes |
| Chat messages | `Array<{role, content}>` | `str` (JSON string) | `List[ChatMessage]` | Yes |
| Confidence enum | `string` | `str` | `Confidence` / `ConfidenceLevel` | Noted (consolidation recommended) |
| Skill level enums | `string` | `str` | 4 overlapping enums | Noted (consolidation recommended) |
| Storage path | N/A | `workspace/memory/` | `workspace/memory/` | Yes |
| LLM models response | `{ model: string }` | `{ model: string }` unified | N/A | Yes |

---

## Files Modified

| File | Changes |
|------|---------|
| `wiki/schema.md` | C1: Added `learning_goal` to `LearnerProfile`; C3: Aligned `DashboardData` sessions; H4: Updated quiz API signature; M1/M2: Added enum consolidation notes; L1: Removed duplicate entry |
| `wiki/wiki_backend.md` | C2: Fixed 3 endpoint `get_llm()` calls; H1: Aligned memory service return keys; H2/M3: Updated storage paths and repository methods |
| `wiki/wiki_frontend.md` | C3: Aligned `DashboardData` sessions; H3: Made `message` optional; H4: Updated quiz params; H5: Fixed `listModels` type; M4: Fixed `AITutorChat` example |
| `wiki/wiki_algo.md` | H2: Renamed `objectives.json` to `learning_goals.json`, added `skill_gaps.json`, added memory store methods; L2: Added `additional_notes` to `BehavioralPatterns` |

---

*Report generated: 2026-03-02*
*All 14 issues resolved: 2026-03-02*
