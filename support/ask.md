---
name: paper-ask
description: "Research Q&A against the knowledge base wiki. Answers filed to qa/ to accumulate knowledge."
---

# /paper ask — Research Q&A

Ask questions against your knowledge base. Claude searches wiki/ and raw/ to synthesize answers with source citations. Every Q&A session is auto-filed to `qa/` so your explorations accumulate into the knowledge base.

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
1. Identify relevant wiki articles and raw papers from CATALOG.md tags/titles
2. Read relevant files: `cat "$VAULT/wiki/{article}.md"` and `cat "$VAULT/raw/{paper}.md"`
3. Cross-reference multiple sources
4. Synthesize a comprehensive answer

### Step 3: Present answer

Show the user:
- Synthesized answer with source attribution
- Confidence: **high** (multiple sources agree), **medium** (single source), **low** (inferred/sparse)
- 2-3 suggested follow-up questions

### Step 4: File to qa/

Save to `qa/{YYYY-MM-DD}-{question-slug}.md`:

```markdown
---
title: "{Question text}"
source: claude
date: {YYYY-MM-DD}
tags: [{relevant}, {tags}]
wiki_refs: [{wiki-articles-consulted}]
raw_refs: [{raw-papers-consulted}]
confidence: {high|medium|low}
---

## Question

{Full question text}

## Answer

{Answer with [[wikilinks]] to sources}

## Sources Consulted

- [[wiki/{article}]] — {contribution}
- [[raw/{paper}]] — {contribution}

## Follow-up Questions

- {Question 1}
- {Question 2}
```

### Step 5: Rebuild index

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
3. Save to qa/ with `source: notebooklm`

## Modes

**A) Ask** — New question against the wiki (default)
**B) Log** — Record a NotebookLM or external Q&A session
**C) Review** — Browse past Q&A, find patterns, suggest new questions
