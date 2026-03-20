---
name: paper-auth
description: Manage NotebookLM authentication for paper-skill.
---

# /paper auth

Manages NotebookLM authentication via notebooklm-py.

## Commands

```bash
PY=~/project/lab/trust_ai_identity/paper-skill/.venv/bin/python3
SKILL=~/project/lab/trust_ai_identity/paper-skill

$PY $SKILL/scripts/run.py auth status   # Check auth state
$PY $SKILL/scripts/run.py auth setup    # Interactive login (opens browser)
$PY $SKILL/scripts/run.py auth reauth   # Re-authenticate expired session
$PY $SKILL/scripts/run.py auth clear    # Remove stored credentials
```

## Workflow

1. Run `auth status` to check current state
2. If not authenticated, run `auth setup` — opens browser for Google login
3. After login, press Enter in terminal to confirm
4. Auth stored at `~/.notebooklm/storage_state.json` (managed by notebooklm-py)

## Troubleshooting

| Issue | Fix |
|-------|-----|
| Auth expired | Run `auth reauth` |
| Login fails | Run `auth clear` then `auth setup` |
| Rate limited | Wait or use different Google account (~50 queries/day free) |
