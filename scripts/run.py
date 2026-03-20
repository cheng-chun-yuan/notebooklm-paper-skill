#!/usr/bin/env python3
"""Universal runner for paper-skill scripts."""

import os
import sys
import subprocess
from pathlib import Path

SCRIPT_ALIASES = {
    "auth": "core/auth_manager.py",
    "ask": "notebook/ask_question.py",
    "notebook": "notebook/notebook_manager.py",
    "upload": "notebook/upload_pdfs.py",
    "store": "store/notebooklm_handler.py",
    "search": "search/paper_search.py",
    "download": "download/paper_downloader.py",
    "survey": "survey/survey_manager.py",
    "scorecard": "core/scorecard.py",
    "claims": "core/claims.py",
    "matrix": "core/matrix.py",
    "analyze": "analyze/star_analyzer.py",
    "gap": "gap/gap_analyzer.py",
    "synthesize": "synthesize/synthesizer.py",
    "cleanup": "utils/cleanup_manager.py",
    "eval": "eval/eval_runner.py",
    "optimize": "optimize/backup_manager.py",
}


def get_venv_python():
    skill_dir = Path(__file__).parent.parent
    return skill_dir / ".venv" / "bin" / "python3"


def ensure_venv():
    skill_dir = Path(__file__).parent.parent
    venv_dir = skill_dir / ".venv"
    setup_script = skill_dir / "setup"

    if not venv_dir.exists():
        print("First-time setup: Creating virtual environment...")
        result = subprocess.run(["bash", str(setup_script)])
        if result.returncode != 0:
            print("Setup failed. Run setup manually.")
            sys.exit(1)

    python = get_venv_python()
    if not python.exists():
        print(f"Python not found at {python}. Run setup again.")
        sys.exit(1)

    return python


def main():
    if len(sys.argv) < 2:
        print("Usage: run.py <command> [args...]")
        print(f"Available commands: {', '.join(sorted(SCRIPT_ALIASES.keys()))}")
        sys.exit(1)

    command = sys.argv[1]
    args = sys.argv[2:]

    if command not in SCRIPT_ALIASES:
        print(f"Unknown command: {command}")
        print(f"Available: {', '.join(sorted(SCRIPT_ALIASES.keys()))}")
        sys.exit(1)

    python = ensure_venv()
    script_path = Path(__file__).parent / SCRIPT_ALIASES[command]

    if not script_path.exists():
        print(f"Script not found: {script_path}")
        print(f"This command may not be implemented yet.")
        sys.exit(1)

    result = subprocess.run(
        [str(python), str(script_path)] + args,
        cwd=Path(__file__).parent.parent,
    )
    sys.exit(result.returncode)


if __name__ == "__main__":
    main()
