---
name: paper-feedback
description: Collect and review user feedback for paper-skill phases.
---

# /paper feedback

Collects user ratings and comments after each phase to improve the skill over time.

## Command

```bash
PAPER_SKILL=~/.claude/skills/paper

$PAPER_SKILL/bin/paper-feedback <phase> <rating> "<comment>"
```

### Parameters

| Parameter | Description |
|-----------|-------------|
| `phase` | Phase name (e.g., `survey`, `gap`, `scout`, `position`, etc.) |
| `rating` | Integer 1-5 (1 = poor, 5 = excellent) |
| `comment` | Free-text feedback (quoted string) |

## Rating Flow

After each phase completes, the phase transition template prompts: "Rate this phase? (1-5, or skip)"

- **Rating < 4**: Ask "What would make it better?" then save the feedback
- **Rating = 5**: Ask "What worked well?" then save the positive feedback
- **Skip**: No feedback saved, proceed to next phase

## Feedback File Format

Files are stored at `~/.paper/feedback/` with the naming pattern `YYYY-MM-DD-<phase>.md`.

Each file has YAML frontmatter:

```markdown
---
phase: survey
rating: 4
date: 2026-03-20
version: 0.1.0
---

## Feedback
The search results were comprehensive but took too long.
```

## Aggregation

To review collected feedback, read all files from `~/.paper/feedback/` and summarize:

1. List each phase with its average rating across all feedback entries
2. Highlight phases with average rating below 3 as needing attention
3. Group comments by phase for qualitative review
4. Show trend over time if multiple entries exist for the same phase
