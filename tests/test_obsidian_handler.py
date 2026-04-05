"""Tests for Obsidian vault handler."""
import pytest
from pathlib import Path
from scripts.store.obsidian_handler import init_vault, ingest_paper


@pytest.fixture
def vault(tmp_path):
    return tmp_path / "vault"


def test_init_creates_structure(vault):
    init_vault(vault)
    assert (vault / "sources").is_dir()
    assert (vault / "notes").is_dir()
    assert (vault / "concepts").is_dir()
    assert (vault / "questions").is_dir()
    assert (vault / "insights").is_dir()
    assert (vault / "CATALOG.md").exists()
    assert (vault / ".obsidian").is_dir()


def test_init_idempotent(vault):
    init_vault(vault)
    (vault / "sources" / "test.md").write_text("# Test")
    init_vault(vault)
    assert (vault / "sources" / "test.md").exists()


def test_ingest_md(vault):
    init_vault(vault)
    source = vault.parent / "paper.md"
    source.write_text("---\ntitle: Test\n---\nContent.")
    ingest_paper(vault, source)
    assert (vault / "sources" / "paper.md").exists()


def test_ingest_pdf(vault):
    init_vault(vault)
    source = vault.parent / "paper.pdf"
    source.write_bytes(b"%PDF-1.4 fake")
    ingest_paper(vault, source)
    assert (vault / "sources" / "paper.pdf").exists()


def test_ingest_updates_catalog(vault):
    init_vault(vault)
    source = vault.parent / "paper.md"
    source.write_text("---\ntitle: New Paper\ntags: [nlp]\n---\nContent.")
    ingest_paper(vault, source)
    assert "New Paper" in (vault / "CATALOG.md").read_text()


def test_ingest_duplicate_skips(vault):
    init_vault(vault)
    source = vault.parent / "paper.md"
    source.write_text("---\ntitle: Dup\n---\nContent.")
    ingest_paper(vault, source)
    ingest_paper(vault, source)
    assert len(list((vault / "sources").glob("paper*.md"))) == 1
