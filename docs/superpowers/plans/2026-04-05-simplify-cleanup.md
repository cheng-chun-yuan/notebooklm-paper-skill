# Simplify & Clean Up — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Eliminate duplication, standardize on one way to read `.paper`, simplify the SKILL.md preamble, and remove redundant code paths.

**Architecture:** Single principle — every file that needs vault/project config calls Python, never parses `.paper` with shell grep. The preamble becomes a Python script. Legacy `project.json` support moves to a migration path, not a parallel system.

**Tech Stack:** Python 3.11+, existing scripts/config.py + scripts/core/dotpaper.py

---

## File Structure

```
# CREATE
scripts/core/preamble.py              — Single Python preamble that replaces shell logic

# MODIFY (simplify)
scripts/store/vault_index.py          — Extract _get_list_field helper
scripts/store/obsidian_handler.py     — Use get_vault_dir() instead of manual .paper parsing
support/digest.md                     — Replace grep with Python call
support/ask.md                        — Replace grep with Python call
support/check.md                      — Replace grep with Python call
phases/01-discover.md                 — Replace grep with Python call
SKILL.md                              — Replace shell preamble with Python preamble script
```

---

### Task 1: Standardize .paper Reading in SKILL.md Files

**Files:**
- Modify: `support/digest.md`
- Modify: `support/ask.md`
- Modify: `support/check.md`
- Modify: `phases/01-discover.md`

All four files have this fragile shell pattern:
```bash
VAULT=$(grep '^vault:' .paper | awk '{print $2}')
```

Replace every instance with:
```bash
VAULT=$($PY $PAPER_SKILL/scripts/run.py vault-path 
```

But wait — we need a simpler approach. Since every SKILL.md already defines `$PY` and `$PAPER_SKILL`, the cleanest pattern is:

```bash
VAULT=$($PY -c "from scripts.config import get_vault_dir; print(get_vault_dir())")
```

- [ ] **Step 1: Update support/digest.md**

Replace the Setup section:
```markdown
## Setup

```bash
PAPER_SKILL=~/.claude/skills/paper
PY=$PAPER_SKILL/.venv/bin/python3
VAULT=$($PY -c "from scripts.config import get_vault_dir; print(get_vault_dir())")
```

If no vault found (empty output), tell user to run `/paper init` first.
```

- [ ] **Step 2: Update support/ask.md**

Same pattern — replace grep-based VAULT with Python call.

- [ ] **Step 3: Update support/check.md**

Same pattern.

- [ ] **Step 4: Update phases/01-discover.md vault integration section**

Replace:
```bash
VAULT=$(grep '^vault:' .paper 2>/dev/null | awk '{print $2}')
if [ -d "$VAULT/raw" ]; then
```

With:
```bash
VAULT=$($PY -c "from scripts.config import get_vault_dir; print(get_vault_dir())" 2>/dev/null)
if [ -n "$VAULT" ] && [ -d "$VAULT/raw" ]; then
```

- [ ] **Step 5: Commit**

```bash
git add support/digest.md support/ask.md support/check.md phases/01-discover.md
git commit -m "refactor: standardize .paper reading via get_vault_dir() across all skills"
```

---

### Task 2: Simplify obsidian_handler.py — Remove Duplicate .paper Logic

**Files:**
- Modify: `scripts/store/obsidian_handler.py`

The `main()` function manually reads `.paper` (lines 48-55) duplicating `get_vault_dir()`.

- [ ] **Step 1: Simplify main()**

Replace the manual `.paper` parsing block:
```python
vault_dir = None
dp_dir = find_dotpaper(Path.cwd())
if dp_dir:
    dp = load_dotpaper(dp_dir)
    if dp and dp.get("vault"):
        vault_dir = Path(dp["vault"])
```

With:
```python
from scripts.config import get_vault_dir
vault_dir = get_vault_dir()
```

Remove the unused `find_dotpaper`, `load_dotpaper` imports from the main() block.

- [ ] **Step 2: Update command handlers**

For `init`: keep allowing explicit path arg override:
```python
if command == "init":
    vault_dir = Path(args[0]) if args else get_vault_dir()
```

For `ingest` and `index`: just use `get_vault_dir()` directly (already the default).

- [ ] **Step 3: Run tests**

```bash
.venv/bin/python3 -m pytest tests/test_obsidian_handler.py -v
```

- [ ] **Step 4: Commit**

```bash
git add scripts/store/obsidian_handler.py
git commit -m "refactor: use get_vault_dir() instead of manual .paper parsing in obsidian_handler"
```

---

### Task 3: Extract _get_list_field Helper in vault_index.py

**Files:**
- Modify: `scripts/store/vault_index.py`

Replace 5 `isinstance` checks with a helper.

- [ ] **Step 1: Add helper after _parse_frontmatter**

```python
def _get_list(fm: dict, key: str) -> list:
    """Safely get a list field from frontmatter."""
    val = fm.get(key, [])
    return val if isinstance(val, list) else []
```

- [ ] **Step 2: Replace all isinstance patterns**

In `scan_raw_dir`:
```python
entry["tags"] = _get_list(fm, "tags")
```

In `scan_wiki_dir`:
```python
"tags": _get_list(fm, "tags"),
"sources": _get_list(fm, "sources"),
```

In `scan_qa_dir`:
```python
"tags": _get_list(fm, "tags"),
```

- [ ] **Step 3: Run tests**

```bash
.venv/bin/python3 -m pytest tests/test_vault_index.py -v
```

- [ ] **Step 4: Commit**

```bash
git add scripts/store/vault_index.py
git commit -m "refactor: extract _get_list helper to deduplicate isinstance checks"
```

---

### Task 4: Create preamble.py — Replace Shell Preamble

**Files:**
- Create: `scripts/core/preamble.py`
- Modify: `SKILL.md`

The SKILL.md preamble is ~50 lines of shell doing: venv check, version read, session cleanup, auth check, .paper/.project.json reading, feedback mode. Move it all to one Python script.

- [ ] **Step 1: Create scripts/core/preamble.py**

```python
#!/usr/bin/env python3
"""Preamble check for /paper skill — outputs structured status."""

import json
import os
import subprocess
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).parent.parent.parent
VENV = SKILL_DIR / ".venv"
PY = VENV / "bin" / "python3"


def main():
    status = {}

    # Venv check
    if not VENV.exists() or not PY.exists():
        status["setup"] = "NEEDS_SETUP"
    else:
        status["setup"] = "READY"

    # Version
    version_file = SKILL_DIR / "VERSION"
    status["version"] = version_file.read_text().strip() if version_file.exists() else "0.0.0"

    # Update check
    update_check = SKILL_DIR / "bin" / "paper-update-check"
    try:
        result = subprocess.run([str(update_check)], capture_output=True, text=True, timeout=5)
        if result.stdout.strip():
            status["update"] = result.stdout.strip()
    except Exception:
        pass

    # Session cleanup
    sessions_dir = Path.home() / ".paper" / "sessions"
    sessions_dir.mkdir(parents=True, exist_ok=True)
    (sessions_dir / str(os.getppid())).touch()
    for f in sessions_dir.iterdir():
        try:
            if f.is_file() and (f.stat().st_mtime < (__import__("time").time() - 7200)):
                f.unlink()
        except OSError:
            pass

    # Auth
    try:
        result = subprocess.run(
            [str(PY), str(SKILL_DIR / "scripts" / "run.py"), "auth", "status", "--quiet"],
            capture_output=True, text=True, timeout=10
        )
        status["auth"] = result.stdout.strip() or "NO_AUTH"
    except Exception:
        status["auth"] = "NO_AUTH"

    # Project — .paper first, fallback to project.json
    dotpaper = Path.cwd() / ".paper"
    if dotpaper.exists():
        from scripts.core.dotpaper import load_dotpaper
        dp = load_dotpaper(Path.cwd())
        if dp:
            status["project"] = dp.get("project", "unnamed")
            status["phase"] = dp.get("phase", "init")
            status["vault"] = dp.get("vault", "")
            status["notebook"] = dp.get("notebook", "")
            status["topic"] = dp.get("topic", "")
    else:
        from scripts.config import get_active_project
        proj = get_active_project()
        if proj:
            status["project"] = proj.get("name", "unnamed")
            status["phase"] = proj.get("phase_name", "unknown")
        else:
            status["project"] = "none"

    # Feedback mode
    try:
        result = subprocess.run(
            [str(SKILL_DIR / "bin" / "paper-config"), "get", "feedback_mode"],
            capture_output=True, text=True, timeout=5
        )
        status["feedback"] = result.stdout.strip() or "on"
    except Exception:
        status["feedback"] = "on"

    # Output
    for key, val in status.items():
        print(f"{key.upper()}: {val}")


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Replace SKILL.md preamble**

Replace the entire bash block in the Preamble section with:

```bash
PAPER_SKILL=~/.claude/skills/paper
PY=$PAPER_SKILL/.venv/bin/python3
$PY $PAPER_SKILL/scripts/core/preamble.py
```

Keep the conditional logic below it (NEEDS_SETUP, NO_AUTH, UPGRADE_AVAILABLE handling) — those are Claude instructions, not shell.

- [ ] **Step 3: Run all tests**

```bash
.venv/bin/python3 -m pytest tests/ -v
```

- [ ] **Step 4: Commit**

```bash
git add scripts/core/preamble.py SKILL.md
git commit -m "refactor: move shell preamble to Python preamble.py for maintainability"
```

---

### Task 5: Remove Legacy project.json Parallel Path

**Files:**
- Modify: `SKILL.md` — Remove project.json fallback from guided flow
- Modify: `scripts/config.py` — Keep functions but mark as legacy

The `.paper` file is now the primary config. The guided flow in SKILL.md still references `~/.paper/projects/` as a fallback. Simplify: if no `.paper` found, suggest `/paper init`. Don't maintain two systems.

- [ ] **Step 1: Simplify guided flow option G**

In SKILL.md, replace:
```
G) Continue previous project
   → list .paper files or projects from ~/.paper/projects/
```

With:
```
G) Continue previous project
   → Look for .paper in current or parent directories
```

- [ ] **Step 2: Simplify phase transition template**

The phase transition currently has an if/else for .paper vs project.json. Simplify to just .paper:

```bash
$PY -c "
from pathlib import Path
from scripts.core.dotpaper import find_dotpaper, load_dotpaper, save_dotpaper
dp_dir = find_dotpaper(Path('.'))
if dp_dir:
    dp = load_dotpaper(dp_dir)
    dp['phases_completed'].append('{current_phase}')
    dp['phase'] = '{next_phase_name}'
    save_dotpaper(dp_dir, dp)
else:
    print('No .paper found — run /paper init first')
"
```

- [ ] **Step 3: Commit**

```bash
git add SKILL.md
git commit -m "refactor: simplify SKILL.md to use .paper as single config source"
```

---

## Self-Review

**1. Spec coverage:**
- Duplicate .paper grep parsing → Task 1 (4 files) ✅
- Duplicate vault resolution in obsidian_handler → Task 2 ✅
- isinstance duplication in vault_index → Task 3 ✅
- Complex shell preamble → Task 4 ✅
- Dual config system (.paper + project.json) → Task 5 ✅

**2. Placeholder scan:** No TBD/TODO found.

**3. Type consistency:** `get_vault_dir()` used consistently across all fixes.
