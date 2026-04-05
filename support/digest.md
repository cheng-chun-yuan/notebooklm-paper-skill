---
name: paper-digest
description: "Two-pass knowledge compiler. Reading pass: sources/ → notes/ (per-paper summaries). Synthesis pass: notes/ → concepts/ (cross-paper understanding)."
---

# /paper digest — Organize Your Knowledge

Two-pass knowledge compiler. **Reading pass**: read each unprocessed paper in `sources/` and write a `notes/` entry. **Synthesis pass**: look across all notes, create or update `concepts/` entries with cross-paper understanding.

## Setup

```bash
PAPER_SKILL=~/.claude/skills/paper
PY=$PAPER_SKILL/.venv/bin/python3
```

Read `.paper` in the current directory to find the vault path:

```bash
VAULT=$($PY -c "from scripts.config import get_vault_dir; print(get_vault_dir())")
```

If VAULT is empty, tell user to run `/paper init` first.

## Workflow

### Step 1: Read CATALOG.md

```bash
cat "$VAULT/CATALOG.md"
```

Understand current state: which papers exist in sources/, which notes have been written, which concepts exist, and which questions/insights are recorded.

### Step 2: Identify unprocessed sources

Compare sources/ entries against notes/. A source `sources/{author}-{year}-{short-title}.{ext}` is unprocessed if no matching `notes/{author}-{year}-{short-title}.md` exists.

### Step 3: Reading pass — Write notes

For each unprocessed source:
1. Read full content: `cat "$VAULT/sources/{filename}"`
2. Write `notes/{author}-{year}-{short-title}.md`:

```markdown
---
title: "{Paper Title}"
paper: "sources/{author}-{year}-{title}"
tags: [{tags}]
key_findings: [{finding1}, {finding2}]
updated: {YYYY-MM-DD}
---

# {Paper Title}

## Summary
{2-3 paragraph summary in your own words}

## Key Findings
- {Finding 1 with direct quote or specific result}
- {Finding 2}

## Methods
{Notable methods worth remembering}

## Strengths & Weaknesses
- Strength: {what's good}
- Weakness: {what's missing or questionable}

## Relevant Quotes
> "{exact quote}" (Section X, p.Y)

## Connections
- Related to [[concepts/{concept}]] because {why}
- Similar approach to [[notes/{other-paper}]] but {difference}
```

### Step 4: Synthesis pass — Write/update concepts

Look across all notes/ entries. For each concept that spans multiple papers, create or update `concepts/{concept-name}.md`:

```markdown
---
title: "{Concept Name}"
tags: [{tags}]
sources: [{notes-that-inform-this}]
related: [{other-concept-stems}]
updated: {YYYY-MM-DD}
---

# {Concept Name}

## Overview
{2-3 paragraph synthesis across papers}

## Key Points
- {Facts drawn from multiple sources}

## Connections
- [[concepts/{related}]] — {relationship}

## Sources
- [[notes/{paper-note}]] — {what this paper contributes}
```

### Step 5: Update existing concepts

When a new paper adds to an existing concept:
1. Read the existing concept article
2. Add new information under appropriate sections
3. Append the note to `sources:` frontmatter
4. Add new `[[wikilinks]]` under Connections
5. Update `updated:` date

### Step 6: Rebuild index

```bash
$PY $PAPER_SKILL/scripts/run.py vault index
```

## Rules

- **Never fabricate** — Only write what source papers say. Quote directly when uncertain.
- **Always link** — Use `[[wikilinks]]` between concepts, notes, and back to sources.
- **Always attribute** — Every claim traces to a specific notes/ entry and its source.
- **Incremental** — Don't rewrite unchanged articles. Only add new information.
- **Reuse tags** — Check existing tags in CATALOG.md before creating new ones.

## Modes

When user runs `/paper digest`:

**A) Full digest** — Reading pass + synthesis pass for all unprocessed sources (default)
**B) Single paper** — Reading pass only for one paper: `/paper digest vaswani-2017-attention.pdf`
**C) Synthesize** — Synthesis pass only: update concepts from existing notes (skip reading pass)
