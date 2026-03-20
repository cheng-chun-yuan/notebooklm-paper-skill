---
name: paper-store
description: Manage NotebookLM notebooks and paper storage for paper-skill.
---

# /paper store

Handles NotebookLM notebook management — uploading PDFs, listing/searching notebooks, and querying content.

## Commands

```bash
PY=~/.claude/skills/notebooklm-paper/.venv/bin/python3
SKILL=~/.claude/skills/notebooklm-paper

# Upload PDFs to a notebook
$PY $SKILL/scripts/run.py store upload --notebook-url "..." --pdf-dir PATH

# Notebook management
$PY $SKILL/scripts/run.py store notebook list
$PY $SKILL/scripts/run.py store notebook add --url "..." --name "..." --topics "..."
$PY $SKILL/scripts/run.py store notebook search --query "..."
$PY $SKILL/scripts/run.py store notebook activate --id ID
$PY $SKILL/scripts/run.py store notebook remove --id ID

# Ask a question against a notebook
$PY $SKILL/scripts/run.py store ask --question "..." --notebook-url "..."
```

## Workflow

1. **List notebooks**: Run `store notebook list` to see registered notebooks
2. **Add a notebook**: Use `store notebook add` with the NotebookLM URL, a human-readable name, and comma-separated topics
3. **Upload papers**: Use `store upload` to push PDFs from a local directory into a notebook
4. **Search notebooks**: Use `store notebook search` to find notebooks by topic or name
5. **Activate a notebook**: Use `store notebook activate` to set the default notebook for queries
6. **Ask questions**: Use `store ask` to query a notebook's content via NotebookLM

## Notes

- The survey phase delegates its upload step to store internally
- Requires authentication — run `/paper auth` first if not yet configured
- Future storage handlers (Heptabase, Obsidian) will be added as new sections
