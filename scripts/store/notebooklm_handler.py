#!/usr/bin/env python3
"""
NotebookLM storage handler.
Thin wrapper that delegates to notebook/ scripts with unified interface.
"""

import sys
import subprocess
from pathlib import Path

SCRIPTS_DIR = Path(__file__).parent.parent


def main():
    if len(sys.argv) < 2:
        print("Usage: notebooklm_handler.py <subcommand> [args...]")
        print("Subcommands: upload, notebook, ask")
        sys.exit(1)

    subcommand = sys.argv[1]
    args = sys.argv[2:]

    script_map = {
        "upload": SCRIPTS_DIR / "notebook" / "upload_pdfs.py",
        "notebook": SCRIPTS_DIR / "notebook" / "notebook_manager.py",
        "ask": SCRIPTS_DIR / "notebook" / "ask_question.py",
    }

    if subcommand not in script_map:
        print(f"Unknown subcommand: {subcommand}")
        sys.exit(1)

    script = script_map[subcommand]
    python = Path(__file__).parent.parent.parent / ".venv" / "bin" / "python3"
    result = subprocess.run([str(python), str(script)] + args)
    sys.exit(result.returncode)


if __name__ == "__main__":
    main()
