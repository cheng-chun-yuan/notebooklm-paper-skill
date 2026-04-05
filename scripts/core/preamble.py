#!/usr/bin/env python3
"""Preamble check for /paper skill — outputs structured status."""

import os
import subprocess
import sys
import time
from pathlib import Path

SKILL_DIR = Path(__file__).parent.parent.parent
VENV = SKILL_DIR / ".venv"
PY = VENV / "bin" / "python3"


def main():
    # Venv check
    if not VENV.exists() or not PY.exists():
        print("SETUP: NEEDS_SETUP")
    else:
        print("SETUP: READY")

    # Version
    version_file = SKILL_DIR / "VERSION"
    version = version_file.read_text().strip() if version_file.exists() else "0.0.0"
    print(f"VERSION: {version}")

    # Update check
    try:
        result = subprocess.run(
            [str(SKILL_DIR / "bin" / "paper-update-check")],
            capture_output=True, text=True, timeout=5
        )
        if result.stdout.strip():
            print(result.stdout.strip())
    except Exception:
        pass

    # Session cleanup
    sessions_dir = Path.home() / ".paper" / "sessions"
    sessions_dir.mkdir(parents=True, exist_ok=True)
    (sessions_dir / str(os.getppid())).touch()
    cutoff = time.time() - 7200
    for f in sessions_dir.iterdir():
        try:
            if f.is_file() and f.stat().st_mtime < cutoff:
                f.unlink()
        except OSError:
            pass

    # Auth
    try:
        result = subprocess.run(
            [str(PY), str(SKILL_DIR / "scripts" / "run.py"), "auth", "status", "--quiet"],
            capture_output=True, text=True, timeout=10
        )
        print(f"AUTH: {result.stdout.strip() or 'NO_AUTH'}")
    except Exception:
        print("AUTH: NO_AUTH")

    # Project — .paper first, fallback to project.json
    dotpaper_path = Path.cwd() / ".paper"
    if dotpaper_path.exists():
        # Add skill dir to path so imports work
        sys.path.insert(0, str(SKILL_DIR))
        from scripts.core.dotpaper import load_dotpaper

        dp = load_dotpaper(str(Path.cwd()))
        if dp:
            proj = dp.get("project", "unnamed")
            phase = dp.get("phase", "init")
            print(f"PROJECT: {proj} — Phase: {phase}")
            vault = dp.get("vault", "")
            if vault:
                print(f"VAULT: {vault}")
            notebook = dp.get("notebook", "")
            if notebook:
                print(f"NOTEBOOK: {notebook}")
        else:
            print("PROJECT: none")
    else:
        sys.path.insert(0, str(SKILL_DIR))
        from scripts.config import get_active_project

        proj = get_active_project()
        if proj:
            name = proj.get("name", "unnamed")
            phase_num = proj.get("current_phase", "?")
            phase_name = proj.get("phase_name", "unknown")
            print(f"PROJECT: {name} — Phase {phase_num}/8 ({phase_name})")
        else:
            print("PROJECT: none")

    # Feedback mode
    try:
        result = subprocess.run(
            [str(SKILL_DIR / "bin" / "paper-config"), "get", "feedback_mode"],
            capture_output=True, text=True, timeout=5
        )
        print(f"FEEDBACK: {result.stdout.strip() or 'on'}")
    except Exception:
        print("FEEDBACK: on")


if __name__ == "__main__":
    main()
