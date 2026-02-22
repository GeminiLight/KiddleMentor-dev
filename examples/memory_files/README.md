# Memory Files Examples

Example data files for the `MemoryStore` and `LearnerMemoryStore` classes defined in `gen_mentor/core/memory/memory_store.py`.

At runtime these files live under a learner-specific workspace directory (e.g. `~/.gen-mentor/workspace/memory/<learner_id>/`). The examples here use a sample HR-Manager-in-training learner so you can inspect the expected structure of each file.

## File Reference

### `user_facts.md`

Long-term memory — free-form Markdown notes extracted from interactions. Contains background info, learning preferences, and tutor observations that persist across sessions. Goal-agnostic; does not contain goal-specific data.

| Store class | Key methods |
|---|---|
| `MemoryStore` | `read_long_term()`, `write_long_term()`, `append_to_long_term()`, `get_memory_context()` |

### `chat_history.json`

Structured interaction log. Each entry has `role` (`learner` / `tutor` / `system`), `content`, `timestamp`, and an optional `metadata` dict for session/topic tags.

| Store class | Key methods |
|---|---|
| `MemoryStore` | `read_history()`, `write_history()`, `append_history()`, `get_recent_history()`, `search_history()` |

### `profile.json`

Learner identity and preferences — education, work experience, learning style, and behavioral patterns. Does **not** contain goal or refined goal fields (those live in `learning_goal.json`).

| Store class | Key methods |
|---|---|
| `LearnerMemoryStore` | `read_profile()`, `write_profile()` |

### `learning_goal.json`

Multi-goal learning goals with an active goal pointer. Each goal has a `goal_id`, `learning_goal` text, `refined_goal` data, `status`, and timestamps. Replaces the old `objectives.json`.

| Store class | Key methods |
|---|---|
| `LearnerMemoryStore` | `read_learning_goals()`, `write_learning_goals()`, `get_active_goal()`, `get_active_goal_id()`, `add_goal()` |

### `skill_gaps.json`

Skill gap data keyed by `goal_id`. Each goal entry contains a `skill_gaps` list with gap details (name, required/current level, reason, confidence) and an `updated_at` timestamp.

| Store class | Key methods |
|---|---|
| `LearnerMemoryStore` | `read_skill_gaps()`, `write_skill_gaps()`, `read_skill_gaps_for_goal()`, `write_skill_gaps_for_goal()` |

### `mastery.json`

Skill mastery tracking and evaluation history. Contains:

- `mastered_skills` / `in_progress_skills` — skill-level proficiency snapshots
- `entries` — granular log entries (quizzes, reading completions) appended via `append_mastery_entry()`
- `last_evaluation` / `evaluations_history` — session-level evaluations written by `update_evaluations()`

| Store class | Key methods |
|---|---|
| `LearnerMemoryStore` | `read_mastery()`, `write_mastery()`, `append_mastery_entry()`, `update_evaluations()` |

### `learning_path.json`

Learning paths keyed by `goal_id`. Each goal entry contains a `learning_path` list of sessions (title, abstract, associated skills, knowledge points, completion flag) and timestamps.

| Store class | Key methods |
|---|---|
| `LearnerMemoryStore` | `read_learning_path()`, `write_learning_path()`, `read_learning_path_for_goal()`, `write_learning_path_for_goal()` |

## Directory Layout at Runtime

```
~/.gen-mentor/workspace/
  memory/
    user_facts.md          # shared long-term memory (MemoryStore)
    chat_history.json      # shared chat log        (MemoryStore)
    <learner_id>/
      user_facts.md        # per-learner long-term memory
      chat_history.json    # per-learner chat log
      profile.json         # learner profile (no goal fields)
      learning_goal.json   # multi-goal learning goals
      skill_gaps.json      # skill gaps keyed by goal_id
      mastery.json         # mastery & evaluations
      learning_path.json   # learning paths keyed by goal_id
```
