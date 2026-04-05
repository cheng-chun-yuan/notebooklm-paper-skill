#!/usr/bin/env python3
"""Tests for vault_index.py CATALOG.md builder."""

import textwrap
from pathlib import Path

import pytest

from scripts.store.vault_index import (
    _parse_frontmatter,
    build_catalog,
    scan_concepts_dir,
    scan_insights_dir,
    scan_notes_dir,
    scan_questions_dir,
    scan_sources_dir,
    write_catalog,
)


# ── 1. scan_sources_empty ──────────────────────────────────────────────
def test_scan_sources_empty(tmp_path):
    sources = tmp_path / "sources"
    sources.mkdir()
    assert scan_sources_dir(sources) == []


# ── 2. scan_sources_markdown ────────────────────────────────────────────
def test_scan_sources_markdown(tmp_path):
    sources = tmp_path / "sources"
    sources.mkdir()
    (sources / "paper.md").write_text(textwrap.dedent("""\
        ---
        title: My Great Paper
        authors: [Alice, Bob]
        year: 2025
        tags: [ml, trust]
        ---
        # Content here
    """))
    entries = scan_sources_dir(sources)
    assert len(entries) == 1
    e = entries[0]
    assert e["file"] == "sources/paper.md"
    assert e["title"] == "My Great Paper"
    assert e["authors"] == ["Alice", "Bob"]
    assert e["year"] == "2025"
    assert e["tags"] == ["ml", "trust"]


# ── 3. scan_sources_pdf ────────────────────────────────────────────────
def test_scan_sources_pdf(tmp_path):
    sources = tmp_path / "sources"
    sources.mkdir()
    (sources / "Some Research Paper.pdf").write_bytes(b"%PDF-fake")
    entries = scan_sources_dir(sources)
    assert len(entries) == 1
    e = entries[0]
    assert e["file"] == "sources/Some Research Paper.pdf"
    assert e["title"] == "Some Research Paper"
    assert e["tags"] == []
    assert e["authors"] == []


# ── 4. scan_notes ──────────────────────────────────────────────────────
def test_scan_notes(tmp_path):
    notes = tmp_path / "notes"
    notes.mkdir()
    (notes / "vaswani-2017-attention.md").write_text(textwrap.dedent("""\
        ---
        title: Attention Is All You Need
        tags: [transformer, attention]
        paper: vaswani-2017-attention
        ---
        # Reading Notes
    """))
    entries = scan_notes_dir(notes)
    assert len(entries) == 1
    e = entries[0]
    assert e["file"] == "notes/vaswani-2017-attention.md"
    assert e["title"] == "Attention Is All You Need"
    assert e["tags"] == ["transformer", "attention"]
    assert e["paper"] == "vaswani-2017-attention"


# ── 5. scan_concepts ────────────────────────────────────────────────────
def test_scan_concepts(tmp_path):
    concepts = tmp_path / "concepts"
    concepts.mkdir()
    (concepts / "topic.md").write_text(textwrap.dedent("""\
        ---
        title: Trust Models Overview
        tags: [trust, reputation]
        sources: [paperA, paperB]
        ---
        # Trust Models
    """))
    entries = scan_concepts_dir(concepts)
    assert len(entries) == 1
    e = entries[0]
    assert e["file"] == "concepts/topic.md"
    assert e["title"] == "Trust Models Overview"
    assert e["tags"] == ["trust", "reputation"]
    assert e["sources"] == ["paperA", "paperB"]


# ── 6. scan_questions ──────────────────────────────────────────────────
def test_scan_questions(tmp_path):
    questions = tmp_path / "questions"
    questions.mkdir()
    (questions / "question1.md").write_text(textwrap.dedent("""\
        ---
        title: What is zero trust?
        source: claude
        date: 2025-06-01
        tags: [zero-trust, security]
        ---
        # Answer
    """))
    entries = scan_questions_dir(questions)
    assert len(entries) == 1
    e = entries[0]
    assert e["file"] == "questions/question1.md"
    assert e["title"] == "What is zero trust?"
    assert e["source"] == "claude"
    assert e["date"] == "2025-06-01"
    assert e["tags"] == ["zero-trust", "security"]


# ── 7. scan_insights ──────────────────────────────────────────────────
def test_scan_insights(tmp_path):
    insights = tmp_path / "insights"
    insights.mkdir()
    (insights / "2026-04-05-sparse-meets-moe.md").write_text(textwrap.dedent("""\
        ---
        title: Sparse Attention Meets MoE
        tags: [sparse, moe, efficiency]
        date: 2026-04-05
        based_on: [attention-mechanisms, moe-routing]
        ---
        # Hypothesis
    """))
    entries = scan_insights_dir(insights)
    assert len(entries) == 1
    e = entries[0]
    assert e["file"] == "insights/2026-04-05-sparse-meets-moe.md"
    assert e["title"] == "Sparse Attention Meets MoE"
    assert e["tags"] == ["sparse", "moe", "efficiency"]
    assert e["date"] == "2026-04-05"
    assert e["based_on"] == ["attention-mechanisms", "moe-routing"]


# ── 8. build_catalog ────────────────────────────────────────────────
def test_build_catalog(tmp_path):
    # Set up all five directories
    sources = tmp_path / "sources"
    sources.mkdir()
    (sources / "paper.md").write_text(textwrap.dedent("""\
        ---
        title: Paper One
        authors: [Alice]
        year: 2025
        tags: [ml]
        ---
    """))

    notes = tmp_path / "notes"
    notes.mkdir()
    (notes / "alice-2025-paper-one.md").write_text(textwrap.dedent("""\
        ---
        title: Notes on Paper One
        tags: [ml]
        paper: paper-one
        ---
    """))

    concepts = tmp_path / "concepts"
    concepts.mkdir()
    (concepts / "topic.md").write_text(textwrap.dedent("""\
        ---
        title: Topic One
        tags: [trust]
        sources: [paper-one]
        ---
    """))

    questions = tmp_path / "questions"
    questions.mkdir()
    (questions / "q1.md").write_text(textwrap.dedent("""\
        ---
        title: Question One
        source: notebooklm
        date: 2025-07-01
        tags: [identity]
        ---
    """))

    insights = tmp_path / "insights"
    insights.mkdir()
    (insights / "2026-04-05-idea.md").write_text(textwrap.dedent("""\
        ---
        title: Big Idea
        tags: [novel]
        date: 2026-04-05
        based_on: [topic-one]
        ---
    """))

    content = build_catalog(tmp_path)

    # Check frontmatter stats
    assert "1 sources, 1 notes, 1 concepts, 1 questions, 1 insights" in content
    # Check sections exist
    assert "## Sources — Original Papers & Documents" in content
    assert "## Notes — Paper Reading Notes" in content
    assert "## Concepts — Cross-Paper Synthesis" in content
    assert "## Questions — Research Q&A" in content
    assert "## Insights — Original Ideas & Hypotheses" in content
    # Check entries
    assert "### Paper One" in content
    assert "`sources/paper.md`" in content
    assert "Alice" in content
    assert "### Notes on Paper One" in content
    assert "[[paper-one]]" in content
    assert "### Topic One" in content
    assert "### Question One" in content
    assert "notebooklm" in content
    assert "### Big Idea" in content
    assert "[[topic-one]]" in content


# ── 9. write_catalog ────────────────────────────────────────────────
def test_write_catalog(tmp_path):
    content = "# Test Catalog\nSome content."
    write_catalog(tmp_path, content)
    catalog_path = tmp_path / "CATALOG.md"
    assert catalog_path.exists()
    assert catalog_path.read_text() == content
