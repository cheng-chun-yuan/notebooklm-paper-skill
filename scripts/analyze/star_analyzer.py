#!/usr/bin/env python3
"""STAR analysis persistence for paper-skill."""

import sys
from pathlib import Path

# Allow running as script with correct imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from scripts.config import ANALYSES_DIR


def save_analysis(paper_id: str, analysis_md: str):
    """Save a STAR analysis for a paper."""
    ANALYSES_DIR.mkdir(parents=True, exist_ok=True)
    path = ANALYSES_DIR / f"{paper_id}-star.md"
    path.write_text(analysis_md)
    print(f"Saved analysis: {path}")


def load_analysis(paper_id: str) -> str | None:
    """Load a STAR analysis for a paper."""
    path = ANALYSES_DIR / f"{paper_id}-star.md"
    if path.exists():
        return path.read_text()
    return None


def list_analyses():
    """List all saved analyses."""
    if not ANALYSES_DIR.exists():
        print("No analyses yet.")
        return []
    files = sorted(ANALYSES_DIR.glob("*-star.md"))
    if not files:
        print("No analyses yet.")
        return []
    results = []
    for f in files:
        paper_id = f.name.removesuffix("-star.md")
        first_line = f.read_text().split("\n", 1)[0].strip().lstrip("# ")
        results.append((paper_id, first_line))
        print(f"  {paper_id}: {first_line}")
    return results


def main():
    if len(sys.argv) < 2:
        print("Usage: star_analyzer.py list|load <paper_id>|save <paper_id> <file>")
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == "list":
        list_analyses()
    elif cmd == "load":
        if len(sys.argv) < 3:
            print("Usage: star_analyzer.py load <paper_id>")
            sys.exit(1)
        content = load_analysis(sys.argv[2])
        if content is None:
            print(f"No analysis found for {sys.argv[2]}")
            sys.exit(1)
        print(content)
    elif cmd == "save":
        if len(sys.argv) < 4:
            print("Usage: star_analyzer.py save <paper_id> <file>")
            sys.exit(1)
        paper_id = sys.argv[2]
        file_path = Path(sys.argv[3])
        if not file_path.exists():
            print(f"File not found: {file_path}")
            sys.exit(1)
        save_analysis(paper_id, file_path.read_text())
    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)


if __name__ == "__main__":
    main()
