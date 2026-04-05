---
name: paper-check
description: "Health-check the knowledge base vault. Find orphans, broken links, gaps, and suggest improvements."
---

# /paper check — Knowledge Base Health

Diagnose your knowledge base: find unread sources, broken wikilinks, thin notes, disconnected insights, and suggest new connections and concepts to write.

## Setup

```bash
PAPER_SKILL=~/.claude/skills/paper
PY=$PAPER_SKILL/.venv/bin/python3
VAULT=$($PY -c "from scripts.config import get_vault_dir; print(get_vault_dir())")
```

## Checks

### A. Coverage
- **Unread sources**: sources/ files with no matching notes/ entry
- **Uncompiled notes**: Notes not referenced by any concepts/ article's `sources:`
- **Orphan concepts**: Concepts with no incoming links from other concepts
- **Disconnected insights**: insights/ files not linked from any concept
- **Stale questions**: questions/ entries referencing deleted concepts or notes

### B. Consistency
- **Broken wikilinks**: `[[links]]` pointing to non-existent files
- **Missing frontmatter**: notes/, concepts/, questions/, or insights/ files without required fields (title, tags)
- **Tag drift**: Similar tags that should merge (e.g., `ml` vs `machine-learning`)
- **Stale concepts**: Concept `updated:` older than its source notes' modification date

### C. Quality
- **Thin notes**: notes/ entries under 100 words
- **Thin concepts**: concepts/ articles under 200 words
- **Unlinked concepts**: Concepts with no `related:` entries
- **Missing concepts**: Topics in 3+ notes with no concept article

### D. Suggestions
- New concepts to write (topics spanning multiple papers)
- Merge candidates (high tag overlap)
- Research questions worth investigating

## Report Format

```
Knowledge Base Health — {date}

Stats: {N} sources | {M} notes | {K} concepts | {L} questions | {J} insights

Healthy:
  {checks that passed}

Warnings:
  {N} unread sources (no matching notes)
  {N} disconnected insights
  {N} thin notes (under 100 words)
  {N} broken wikilinks
  {details}

Suggestions:
  New concept: "{concept}" (in {N} notes, no concept entry)
  Merge: "{a}" + "{b}" (similar tags)
  Question: "{interesting question from gap}"

Run /paper digest to address unread sources.
```

## Actions

After the report, offer:

**A) Auto-fix** — Fix broken links, normalize tags, update stale dates
**B) Digest missing** — Run `/paper digest` for unread sources
**C) Report only** — No action (default)
