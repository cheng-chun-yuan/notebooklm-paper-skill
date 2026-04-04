---
name: paper-update
description: Check for and apply updates to paper-skill.
---

# /paper update

Checks for available updates and applies them.

## Commands

```bash
SKILL=~/.claude/skills/paper
PY=$SKILL/.venv/bin/python3

# Check for updates (compares local VERSION to remote)
$SKILL/bin/paper-update-check

# Apply update
cd $SKILL && git pull origin main

# If requirements.txt changed, reinstall dependencies
$PY -m pip install -r $SKILL/requirements.txt
```

## Workflow

1. Run `$SKILL/bin/paper-update-check` to see if an update is available
2. If output contains `UPGRADE_AVAILABLE`, inform the user of the current and available versions
3. If the user confirms, run `cd $SKILL && git pull origin main`
4. After pulling, check if `requirements.txt` was modified in the update:
   ```bash
   cd $SKILL && git diff HEAD~1 --name-only | grep requirements.txt
   ```
5. If `requirements.txt` changed, run `$PY -m pip install -r $SKILL/requirements.txt`
6. Report the new version from `$SKILL/VERSION`

## Notes

- The preamble in the root SKILL.md automatically runs the update check on startup
- If `UPGRADE_AVAILABLE` appears during preamble, the user is prompted to run `/paper update`
- Updates are pulled from the `main` branch via git
