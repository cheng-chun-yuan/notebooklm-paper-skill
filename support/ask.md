---
name: paper-ask
description: "Research Q&A against the knowledge base. Answers filed to questions/ to accumulate knowledge. Novel insights offered to insights/."
---

# /paper ask — Research Q&A

Ask questions against your knowledge base. Claude searches concepts/, notes/, sources/, and insights/ to synthesize answers with source citations. Every Q&A session is auto-filed to `questions/` so your explorations accumulate into the knowledge base.

## Setup

```bash
PAPER_SKILL=~/.claude/skills/paper
PY=$PAPER_SKILL/.venv/bin/python3
VAULT=$($PY -c "from scripts.config import get_vault_dir; print(get_vault_dir())")
```

## Workflow

### Step 1: Read CATALOG.md

```bash
cat "$VAULT/CATALOG.md"
```

### Step 2: Research the answer

Based on the user's question:
1. Identify relevant concepts, notes, sources, and insights from CATALOG.md tags/titles
2. Read relevant files: `cat "$VAULT/concepts/{article}.md"`, `cat "$VAULT/notes/{paper}.md"`, `cat "$VAULT/sources/{paper}"`, `cat "$VAULT/insights/{insight}.md"`
3. Cross-reference multiple sources
4. Synthesize a comprehensive answer

### Step 3: Present answer

Show the user:
- Synthesized answer with source attribution
- Confidence: **high** (multiple sources agree), **medium** (single source), **low** (inferred/sparse)
- 2-3 suggested follow-up questions

### Step 4: File to questions/

Save to `questions/{YYYY-MM-DD}-{question-slug}.md`:

```markdown
---
title: "{Question text}"
source: claude
date: {YYYY-MM-DD}
tags: [{relevant}, {tags}]
concepts_refs: [{concepts-consulted}]
notes_refs: [{notes-consulted}]
confidence: {high|medium|low}
---

## Question

{Full question text}

## Answer

{Answer with [[wikilinks]] to sources}

## Sources Consulted

- [[concepts/{article}]] — {contribution}
- [[notes/{paper}]] — {contribution}
- [[sources/{paper}]] — {contribution}

## Follow-up Questions

- {Question 1}
- {Question 2}
```

### Step 5: Offer insight filing

If the answer reveals a novel insight — a non-obvious connection, surprising synthesis, or original observation not stated in any single source — offer to file it to `insights/{YYYY-MM-DD}-{insight-slug}.md`.

### Step 6: Rebuild index

```bash
$PY $PAPER_SKILL/scripts/run.py vault index
```

## Logging NotebookLM Q&A

When the user had a conversation in NotebookLM and wants to log it:

```
/paper ask log
```

Prompt:
1. "What was the question?"
2. "Paste or summarize NotebookLM's answer"
3. Save to questions/ with `source: notebooklm`

## Modes

**A) Ask** — New question against the knowledge base (default)
**B) Log** — Record a NotebookLM or external Q&A session
**C) Review** — Browse past Q&A, find patterns, suggest new questions
