# Memory Files Examples

Example data files for the `MemoryStore` and `LearnerMemoryStore` classes defined in `gen_mentor/core/memory/memory_store.py`.

At runtime these files live under a learner-specific workspace directory (e.g. `~/.gen-mentor/workspace/memory/<learner_id>/`). The examples here use a sample HR-Manager-in-training learner so you can inspect the expected structure of each file.

## File Reference

### `user_facts.md`

Long-term memory — free-form Markdown notes extracted from interactions. Contains background info, learning preferences, and tutor observations that persist across sessions.

| Store class | Key methods |
|---|---|
| `MemoryStore` | `read_long_term()`, `write_long_term()`, `append_to_long_term()`, `get_memory_context()` |

### `chat_history.json`

Structured interaction log. Each entry has `role` (`learner` / `tutor` / `system`), `content`, `timestamp`, and an optional `metadata` dict for session/topic tags.

| Store class | Key methods |
|---|---|
| `MemoryStore` | `read_history()`, `write_history()`, `append_history()`, `get_recent_history()`, `search_history()` |

### `profile.json`

Learner identity and preferences — education, work experience, learning style, and behavioral patterns.

| Store class | Key methods |
|---|---|
| `LearnerMemoryStore` | `read_profile()`, `write_profile()` |

### `objectives.json`

Goal-oriented learning objectives broken down by skill, with target/current proficiency levels and sub-objective checklists.

| Store class | Key methods |
|---|---|
| `LearnerMemoryStore` | `read_objectives()`, `write_objectives()` |

### `mastery.json`

Skill mastery tracking and evaluation history. Contains:

- `mastered_skills` / `in_progress_skills` — skill-level proficiency snapshots
- `entries` — granular log entries (quizzes, reading completions) appended via `append_mastery_entry()`
- `last_evaluation` / `evaluations_history` — session-level evaluations written by `update_evaluations()`

| Store class | Key methods |
|---|---|
| `LearnerMemoryStore` | `read_mastery()`, `write_mastery()`, `append_mastery_entry()`, `update_evaluations()` |

### `learning_path.json`

Ordered sequence of learning sessions, each with a title, abstract, associated skills, knowledge points, and a completion flag (`if_learned`).

| Store class | Key methods |
|---|---|
| `LearnerMemoryStore` | `read_learning_path()`, `write_learning_path()` |

## Directory Layout at Runtime

```
~/.gen-mentor/workspace/
  memory/
    user_facts.md          # shared long-term memory (MemoryStore)
    chat_history.json      # shared chat log        (MemoryStore)
    <learner_id>/
      user_facts.md        # per-learner long-term memory
      chat_history.json    # per-learner chat log
      profile.json         # learner profile
      objectives.json      # learning objectives
      mastery.json         # mastery & evaluations
      learning_path.json   # learning path sessions
```
