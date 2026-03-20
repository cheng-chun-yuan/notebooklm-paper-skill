#!/usr/bin/env python3
"""Synthesis persistence for paper-skill."""

import json
import sys
from pathlib import Path

# Allow running as script with correct imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from scripts.config import PROJECTS_DIR, get_active_project


def save_synthesis(project_name: str, content: str, working_dir: str = None):
    """Save synthesis to project directory and optionally to working directory."""
    proj_dir = PROJECTS_DIR / project_name
    proj_dir.mkdir(parents=True, exist_ok=True)
    synthesis_path = proj_dir / "synthesis.md"
    synthesis_path.write_text(content)
    print(f"Saved synthesis: {synthesis_path}")

    if working_dir:
        wd = Path(working_dir)
        if wd.is_dir():
            # Save RESEARCH_SYNTHESIS.md
            wd_synthesis = wd / "RESEARCH_SYNTHESIS.md"
            wd_synthesis.write_text(content)
            print(f"Saved working copy: {wd_synthesis}")

            # Create .notebooklm-paper/project.json link-back
            ps_dir = wd / ".notebooklm-paper"
            ps_dir.mkdir(exist_ok=True)
            link_back = {
                "project_name": project_name,
                "project_dir": str(proj_dir),
            }
            (ps_dir / "project.json").write_text(json.dumps(link_back, indent=2))

            # Add .notebooklm-paper/ to .gitignore if not already there
            gitignore = wd / ".gitignore"
            marker = ".notebooklm-paper/"
            if gitignore.exists():
                existing = gitignore.read_text()
                if marker not in existing:
                    with gitignore.open("a") as f:
                        if not existing.endswith("\n"):
                            f.write("\n")
                        f.write(f"{marker}\n")
                    print(f"Added {marker} to .gitignore")
            else:
                gitignore.write_text(f"{marker}\n")
                print(f"Created .gitignore with {marker}")


def load_synthesis(project_name: str) -> str | None:
    """Load synthesis for a project."""
    path = PROJECTS_DIR / project_name / "synthesis.md"
    if path.exists():
        return path.read_text()
    return None


def main():
    if len(sys.argv) < 2:
        print("Usage: synthesizer.py save <file> [--working-dir DIR]|load")
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == "load":
        project = get_active_project()
        if not project:
            print("No synthesis yet.")
            sys.exit(0)
        content = load_synthesis(project["name"])
        if content is None:
            print("No synthesis yet.")
            sys.exit(0)
        print(content)
    elif cmd == "save":
        if len(sys.argv) < 3:
            print("Usage: synthesizer.py save <file> [--working-dir DIR]")
            sys.exit(1)
        project = get_active_project()
        if not project:
            print("No active project. Create one first.")
            sys.exit(1)
        file_path = Path(sys.argv[2])
        if not file_path.exists():
            print(f"File not found: {file_path}")
            sys.exit(1)

        working_dir = None
        if "--working-dir" in sys.argv:
            idx = sys.argv.index("--working-dir")
            if idx + 1 < len(sys.argv):
                working_dir = sys.argv[idx + 1]
            else:
                working_dir = project.get("working_directory")
        elif project.get("working_directory"):
            working_dir = project["working_directory"]

        save_synthesis(project["name"], file_path.read_text(), working_dir)
    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)


if __name__ == "__main__":
    main()
