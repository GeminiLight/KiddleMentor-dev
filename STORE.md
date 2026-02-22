# Gen-Mentor Local Memory Store Design

This document outlines the design for the local user data memory store used by Gen-Mentor. The system prioritizes a "local-first" approach, storing learner context, interaction history, and educational progress in human-readable formats (JSON and Markdown).

## Core Principles
- **Transparency**: Files are stored in plain text (Markdown/JSON) for easy inspection and manual adjustment.
- **Portability**: The entire memory store can be moved or backed up as a single directory.
- **Privacy**: User data remains local to the user's machine (in `local` storage mode).
- **Domain-Aligned**: Filenames reflect the educational and tutoring domain.

## Storage Hierarchy
The memory store is organized by `learner_id` within the workspace directory (default: `~/.gen-mentor/workspace`).

```text
~/.gen-mentor/workspace/
└── memory/
    └── <learner_id>/
        ├── profile.json       # Main learner profile (Identity, Preferences, Cognitive Status)
        ├── chat_history.json  # Structured tutor interactions (Messages, Roles, Timestamps)
        ├── user_facts.md      # Extracted long-term context and insights
        ├── objectives.json    # Refined learning goals and skill gaps
        ├── mastery.json       # Session logs, completion metrics, and performance evaluations
        └── learning_path.json # Personalized curriculum and roadmap
```

## File Specifications

### 1. `profile.json` (Learner Profile)
- **Format**: JSON
- **Description**: The **main information** of the user.
- **Contents**: Learner information, cognitive status (mastered/in-progress skills), learning preferences, and behavioral patterns.

### 2. `chat_history.json` (Interaction History)
- **Format**: JSON
- **Description**: A structured log of conversation messages between the learner and the tutor.
- **Structure**:
  ```json
  [
    {
      "role": "learner",
      "content": "I want to learn about Neural Networks.",
      "timestamp": "2026-02-22T10:00:00Z"
    },
    {
      "role": "tutor",
      "content": "Great! Do you have any prior experience with calculus?",
      "timestamp": "2026-02-22T10:00:05Z"
    }
  ]
  ```

### 3. `user_facts.md` (Long-Term Memory)
- **Format**: Markdown
- **Description**: Stores high-level, persistent facts about the learner extracted by agents.
- **Example**:
  ```markdown
  # User Facts
  - Struggles with linear algebra notation.
  - Prefers visual diagrams over mathematical proofs.
  ```

### 4. `objectives.json` (Learning Goals)
- **Format**: JSON
- **Contents**: The initial broad goal and the refined, actionable sub-goals (skills) the learner is targeting.

### 5. `mastery.json` (Learning Progress & Performance)
- **Format**: JSON
- **Contents**: Records of individual learning sessions merged with performance evaluations and skill mastery assessments.

### 6. `learning_path.json` (Curriculum)
- **Format**: JSON
- **Description**: Stores the personalized curriculum/roadmap generated for the learner.

## Implementation Notes
- **Persistence**: Managed by `LearnerMemoryStore` in `gen_mentor/core/memory/memory_store.py`.
- **Structured History**: `chat_history.json` allows for easier programmatic analysis compared to plain Markdown.
- **Merged Mastery**: The `mastery.json` file handles both granular session logs and high-level proficiency state.
