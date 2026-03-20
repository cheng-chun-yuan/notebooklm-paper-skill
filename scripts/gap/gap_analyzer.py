#!/usr/bin/env python3
"""Gap analysis persistence for paper-skill."""

import sys
from pathlib import Path

# Allow running as script with correct imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from scripts.config import GAPS_DIR


def save_gap(paper_id: str, gap_md: str):
    """Save a gap analysis for a paper."""
    GAPS_DIR.mkdir(parents=True, exist_ok=True)
    path = GAPS_DIR / f"{paper_id}-gap.md"
    path.write_text(gap_md)
    print(f"Saved gap analysis: {path}")


def load_gap(paper_id: str) -> str | None:
    """Load a gap analysis for a paper."""
    path = GAPS_DIR / f"{paper_id}-gap.md"
    if path.exists():
        return path.read_text()
    return None


def list_gaps():
    """List all saved gap analyses."""
    if not GAPS_DIR.exists():
        print("No gaps yet.")
        return []
    files = sorted(GAPS_DIR.glob("*-gap.md"))
    if not files:
        print("No gaps yet.")
        return []
    results = []
    for f in files:
        paper_id = f.name.removesuffix("-gap.md")
        first_line = f.read_text().split("\n", 1)[0].strip().lstrip("# ")
        results.append((paper_id, first_line))
        print(f"  {paper_id}: {first_line}")
    return results


def main():
    if len(sys.argv) < 2:
        print("Usage: gap_analyzer.py list|load <paper_id>|save <paper_id> <file>")
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == "list":
        list_gaps()
    elif cmd == "load":
        if len(sys.argv) < 3:
            print("Usage: gap_analyzer.py load <paper_id>")
            sys.exit(1)
        content = load_gap(sys.argv[2])
        if content is None:
            print(f"No gap analysis found for {sys.argv[2]}")
            sys.exit(1)
        print(content)
    elif cmd == "save":
        if len(sys.argv) < 4:
            print("Usage: gap_analyzer.py save <paper_id> <file>")
            sys.exit(1)
        paper_id = sys.argv[2]
        file_path = Path(sys.argv[3])
        if not file_path.exists():
            print(f"File not found: {file_path}")
            sys.exit(1)
        save_gap(paper_id, file_path.read_text())
    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)


if __name__ == "__main__":
    main()
