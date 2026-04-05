#!/usr/bin/env python3
"""
Vault index builder — scans an Obsidian vault's raw/, wiki/, qa/
directories and builds a CATALOG.md index file.
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


def scan_raw_dir(raw_dir: Path) -> list[dict]:
    """Scan raw/ directory for papers and documents.

    Returns entries with file, title, tags, authors, year.
    """
    if not raw_dir.exists():
        return []

    entries = []
    for f in sorted(raw_dir.iterdir()):
        if f.is_dir():
            continue
        entry = {
            "file": f"raw/{f.name}",
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


def scan_wiki_dir(wiki_dir: Path) -> list[dict]:
    """Scan wiki/ directory for compiled knowledge articles.

    Returns entries with file, title, tags, sources.
    """
    if not wiki_dir.exists():
        return []

    entries = []
    for f in sorted(wiki_dir.iterdir()):
        if f.is_dir() or f.suffix != ".md":
            continue
        fm = _parse_frontmatter(f.read_text(encoding="utf-8"))
        entries.append({
            "file": f"wiki/{f.name}",
            "title": fm.get("title", f.stem),
            "tags": _get_list(fm, "tags"),
            "sources": _get_list(fm, "sources"),
        })
    return entries


def scan_qa_dir(qa_dir: Path) -> list[dict]:
    """Scan qa/ directory for Q&A sessions.

    Returns entries with file, title, source, date, tags.
    """
    if not qa_dir.exists():
        return []

    entries = []
    for f in sorted(qa_dir.iterdir()):
        if f.is_dir() or f.suffix != ".md":
            continue
        fm = _parse_frontmatter(f.read_text(encoding="utf-8"))
        entries.append({
            "file": f"qa/{f.name}",
            "title": fm.get("title", f.stem),
            "source": fm.get("source", ""),
            "date": str(fm.get("date", "")),
            "tags": _get_list(fm, "tags"),
        })
    return entries


def build_catalog(vault_dir: Path) -> str:
    """Build full CATALOG.md content from vault directories."""
    raw_entries = scan_raw_dir(vault_dir / "raw")
    wiki_entries = scan_wiki_dir(vault_dir / "wiki")
    qa_entries = scan_qa_dir(vault_dir / "qa")

    today = date.today().isoformat()
    lines: list[str] = []

    # Frontmatter
    lines.append("---")
    lines.append("purpose: AI-readable index for locating papers, wiki articles, and Q&A sessions")
    lines.append(f"updated: {today}")
    lines.append(f"stats: {len(raw_entries)} raw, {len(wiki_entries)} wiki, {len(qa_entries)} qa")
    lines.append("---")
    lines.append("")
    lines.append("# Research Catalog")
    lines.append("")
    lines.append("> **For AI agents**: Scan this file first to determine which document to read.")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Raw section
    lines.append("## Raw — Source Papers & Documents")
    lines.append("")
    for e in raw_entries:
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

    # Wiki section
    lines.append("## Wiki — Compiled Knowledge")
    lines.append("")
    for e in wiki_entries:
        lines.append(f"### {e['title']}")
        lines.append(f"- **File**: `{e['file']}`")
        if e["tags"]:
            lines.append(f"- **Tags**: {', '.join(f'`{t}`' for t in e['tags'])}")
        if e["sources"]:
            lines.append(f"- **Sources**: {', '.join(f'[[{s}]]' for s in e['sources'])}")
        lines.append("")

    lines.append("---")
    lines.append("")

    # QA section
    lines.append("## Q&A — Research Questions & Answers")
    lines.append("")
    for e in qa_entries:
        lines.append(f"### {e['title']}")
        lines.append(f"- **File**: `{e['file']}`")
        if e["source"]:
            lines.append(f"- **Source**: {e['source']}")
        if e["date"]:
            lines.append(f"- **Date**: {e['date']}")
        if e["tags"]:
            lines.append(f"- **Tags**: {', '.join(f'`{t}`' for t in e['tags'])}")
        lines.append("")

    return "\n".join(lines)


def write_catalog(vault_dir: Path, content: str) -> None:
    """Write CATALOG.md to vault root."""
    catalog_path = vault_dir / "CATALOG.md"
    catalog_path.write_text(content, encoding="utf-8")
