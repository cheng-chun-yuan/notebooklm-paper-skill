#!/usr/bin/env python3
"""
Vault index builder — scans an Obsidian vault's sources/, notes/, concepts/,
questions/, insights/ directories and builds a CATALOG.md index file.
"""

from __future__ import annotations

import re
from datetime import date
from pathlib import Path


def _parse_frontmatter(text: str) -> dict:
    """Parse YAML frontmatter between --- markers.

    Handles simple key: value and [list, items] syntax.
    Returns empty dict if no frontmatter found.
    """
    m = re.match(r"^---\s*\n(.*?)\n---", text, re.DOTALL)
    if not m:
        return {}

    result: dict = {}
    for line in m.group(1).splitlines():
        line = line.strip()
        if not line or ":" not in line:
            continue
        key, _, value = line.partition(":")
        key = key.strip()
        value = value.strip()
        # Parse [list, items] syntax
        if value.startswith("[") and value.endswith("]"):
            inner = value[1:-1]
            result[key] = [item.strip() for item in inner.split(",") if item.strip()]
        else:
            result[key] = value
    return result


def _get_list(fm: dict, key: str) -> list:
    """Safely get a list field from frontmatter."""
    val = fm.get(key, [])
    return val if isinstance(val, list) else []


def scan_sources_dir(sources_dir: Path) -> list[dict]:
    """Scan sources/ directory for papers and documents.

    Returns entries with file, title, tags, authors, year.
    """
    if not sources_dir.exists():
        return []

    entries = []
    for f in sorted(sources_dir.iterdir()):
        if f.is_dir():
            continue
        entry = {
            "file": f"sources/{f.name}",
            "title": f.stem,
            "tags": [],
            "authors": [],
            "year": "",
        }
        if f.suffix == ".md":
            fm = _parse_frontmatter(f.read_text(encoding="utf-8"))
            entry["title"] = fm.get("title", f.stem)
            entry["tags"] = _get_list(fm, "tags")
            entry["authors"] = _get_list(fm, "authors")
            entry["year"] = str(fm.get("year", ""))
        entries.append(entry)
    return entries


def scan_notes_dir(notes_dir: Path) -> list[dict]:
    """Scan notes/ directory for per-paper reading notes.

    Returns entries with file, title, tags, paper.
    Naming convention: {author}-{year}-{short-title}.md
    """
    if not notes_dir.exists():
        return []

    entries = []
    for f in sorted(notes_dir.iterdir()):
        if f.is_dir() or f.suffix != ".md":
            continue
        fm = _parse_frontmatter(f.read_text(encoding="utf-8"))
        entries.append({
            "file": f"notes/{f.name}",
            "title": fm.get("title", f.stem),
            "tags": _get_list(fm, "tags"),
            "paper": fm.get("paper", ""),
        })
    return entries


def scan_concepts_dir(concepts_dir: Path) -> list[dict]:
    """Scan concepts/ directory for cross-paper synthesis articles.

    Returns entries with file, title, tags, sources.
    """
    if not concepts_dir.exists():
        return []

    entries = []
    for f in sorted(concepts_dir.iterdir()):
        if f.is_dir() or f.suffix != ".md":
            continue
        fm = _parse_frontmatter(f.read_text(encoding="utf-8"))
        entries.append({
            "file": f"concepts/{f.name}",
            "title": fm.get("title", f.stem),
            "tags": _get_list(fm, "tags"),
            "sources": _get_list(fm, "sources"),
        })
    return entries


def scan_questions_dir(questions_dir: Path) -> list[dict]:
    """Scan questions/ directory for Q&A sessions.

    Returns entries with file, title, source, date, tags.
    """
    if not questions_dir.exists():
        return []

    entries = []
    for f in sorted(questions_dir.iterdir()):
        if f.is_dir() or f.suffix != ".md":
            continue
        fm = _parse_frontmatter(f.read_text(encoding="utf-8"))
        entries.append({
            "file": f"questions/{f.name}",
            "title": fm.get("title", f.stem),
            "source": fm.get("source", ""),
            "date": str(fm.get("date", "")),
            "tags": _get_list(fm, "tags"),
        })
    return entries


def scan_insights_dir(insights_dir: Path) -> list[dict]:
    """Scan insights/ directory for original ideas and hypotheses.

    Returns entries with file, title, tags, date, based_on.
    Naming convention: {YYYY-MM-DD}-{insight-slug}.md
    """
    if not insights_dir.exists():
        return []

    entries = []
    for f in sorted(insights_dir.iterdir()):
        if f.is_dir() or f.suffix != ".md":
            continue
        fm = _parse_frontmatter(f.read_text(encoding="utf-8"))
        entries.append({
            "file": f"insights/{f.name}",
            "title": fm.get("title", f.stem),
            "tags": _get_list(fm, "tags"),
            "date": str(fm.get("date", "")),
            "based_on": _get_list(fm, "based_on"),
        })
    return entries


def build_catalog(vault_dir: Path) -> str:
    """Build full CATALOG.md content from vault directories."""
    sources_entries = scan_sources_dir(vault_dir / "sources")
    notes_entries = scan_notes_dir(vault_dir / "notes")
    concepts_entries = scan_concepts_dir(vault_dir / "concepts")
    questions_entries = scan_questions_dir(vault_dir / "questions")
    insights_entries = scan_insights_dir(vault_dir / "insights")

    today = date.today().isoformat()
    lines: list[str] = []

    # Frontmatter
    lines.append("---")
    lines.append("purpose: AI-readable index for locating sources, notes, concepts, questions, and insights")
    lines.append(f"updated: {today}")
    stats = (
        f"{len(sources_entries)} sources, {len(notes_entries)} notes, "
        f"{len(concepts_entries)} concepts, {len(questions_entries)} questions, "
        f"{len(insights_entries)} insights"
    )
    lines.append(f"stats: {stats}")
    lines.append("---")
    lines.append("")
    lines.append("# Research Catalog")
    lines.append("")
    lines.append("> **For AI agents**: Scan this file first to determine which document to read.")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Sources section
    lines.append("## Sources — Original Papers & Documents")
    lines.append("")
    for e in sources_entries:
        lines.append(f"### {e['title']}")
        lines.append(f"- **File**: `{e['file']}`")
        if e["authors"]:
            lines.append(f"- **Authors**: {', '.join(e['authors'])}")
        if e["year"]:
            lines.append(f"- **Year**: {e['year']}")
        if e["tags"]:
            lines.append(f"- **Tags**: {', '.join(f'`{t}`' for t in e['tags'])}")
        lines.append("")

    lines.append("---")
    lines.append("")

    # Notes section
    lines.append("## Notes — Paper Reading Notes")
    lines.append("")
    for e in notes_entries:
        lines.append(f"### {e['title']}")
        lines.append(f"- **File**: `{e['file']}`")
        if e["paper"]:
            lines.append(f"- **Paper**: [[{e['paper']}]]")
        if e["tags"]:
            lines.append(f"- **Tags**: {', '.join(f'`{t}`' for t in e['tags'])}")
        lines.append("")

    lines.append("---")
    lines.append("")

    # Concepts section
    lines.append("## Concepts — Cross-Paper Synthesis")
    lines.append("")
    for e in concepts_entries:
        lines.append(f"### {e['title']}")
        lines.append(f"- **File**: `{e['file']}`")
        if e["tags"]:
            lines.append(f"- **Tags**: {', '.join(f'`{t}`' for t in e['tags'])}")
        if e["sources"]:
            lines.append(f"- **Sources**: {', '.join(f'[[{s}]]' for s in e['sources'])}")
        lines.append("")

    lines.append("---")
    lines.append("")

    # Questions section
    lines.append("## Questions — Research Q&A")
    lines.append("")
    for e in questions_entries:
        lines.append(f"### {e['title']}")
        lines.append(f"- **File**: `{e['file']}`")
        if e["source"]:
            lines.append(f"- **Source**: {e['source']}")
        if e["date"]:
            lines.append(f"- **Date**: {e['date']}")
        if e["tags"]:
            lines.append(f"- **Tags**: {', '.join(f'`{t}`' for t in e['tags'])}")
        lines.append("")

    lines.append("---")
    lines.append("")

    # Insights section
    lines.append("## Insights — Original Ideas & Hypotheses")
    lines.append("")
    for e in insights_entries:
        lines.append(f"### {e['title']}")
        lines.append(f"- **File**: `{e['file']}`")
        if e["date"]:
            lines.append(f"- **Date**: {e['date']}")
        if e["tags"]:
            lines.append(f"- **Tags**: {', '.join(f'`{t}`' for t in e['tags'])}")
        if e["based_on"]:
            lines.append(f"- **Based on**: {', '.join(f'[[{b}]]' for b in e['based_on'])}")
        lines.append("")

    return "\n".join(lines)


def write_catalog(vault_dir: Path, content: str) -> None:
    """Write CATALOG.md to vault root."""
    catalog_path = vault_dir / "CATALOG.md"
    catalog_path.write_text(content, encoding="utf-8")
