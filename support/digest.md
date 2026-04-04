---
name: paper-digest
description: "Compile wiki articles from raw papers. Reads raw/, identifies concepts, writes wiki/ with summaries, wikilinks, and source attribution."
---

# /paper digest — Organize Your Knowledge

Read all unprocessed papers in `raw/` and compile them into wiki articles — one per key concept. Each article has a summary, key points, cross-links, and traces back to source papers.

## Setup

```bash
PAPER_SKILL=~/.claude/skills/paper
PY=$PAPER_SKILL/.venv/bin/python3
```

Read `.paper` in the current directory to find the vault path:

```bash
VAULT=$(grep '^vault:' .paper | awk '{print $2}')
```

If no `.paper` found, tell user to run `/paper init` first.

## Workflow

### Step 1: Read CATALOG.md

```bash
cat "$VAULT/CATALOG.md"
```

Understand current state: which papers exist in raw/, which wiki articles already exist, which Q&A sessions are recorded.

### Step 2: Identify unprocessed papers

Compare raw/ entries against wiki/ source lists. Papers in raw/ not referenced by any wiki article's `sources:` field are unprocessed.

### Step 3: Read unprocessed papers

For each unprocessed paper:
1. Read full content: `cat "$VAULT/raw/{filename}"`
2. Extract key concepts (2-5 per paper)
3. Note methods, claims, findings
4. Identify connections to existing wiki articles

### Step 4: Write wiki articles

For each concept, create `wiki/{concept-slug}.md`:

```markdown
---
title: "{Concept Name}"
tags: [{relevant}, {tags}]
sources: [{raw-paper-stems}]
related: [{other-wiki-stems}]
updated: {YYYY-MM-DD}
---

# {Concept Name}

## Overview
{2-3 paragraph summary}

## Key Points
- {Essential facts as bullet points}

## Connections
- [[wiki/{related-concept}]] — {relationship}

## Sources
- [[raw/{paper-filename}]] — {what this paper contributes}
```

### Step 5: Update existing articles

When a new paper adds to an existing concept:
1. Read the existing wiki article
2. Add new information under appropriate sections
3. Append the paper to `sources:` frontmatter
4. Add new `[[wikilinks]]` under Connections
5. Update `updated:` date

### Step 6: Rebuild index

```bash
$PY $PAPER_SKILL/scripts/run.py vault index
```

## Rules

- **Never fabricate** — Only write what raw papers say. Quote directly when uncertain.
- **Always link** — Use `[[wikilinks]]` between wiki articles and back to raw papers.
- **Always attribute** — Every claim traces to a specific raw/ source.
- **Incremental** — Don't rewrite unchanged articles. Only add new information.
- **Reuse tags** — Check existing tags in CATALOG.md before creating new ones.

## Modes

When user runs `/paper digest`:

**A) Full digest** — Process all uncompiled papers (default)
**B) Single paper** — Specify which: `/paper digest attention.md`
**C) Refresh** — Re-scan all raw/ and enrich existing wiki articles with new connections
