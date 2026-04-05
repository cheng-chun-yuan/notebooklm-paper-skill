# Paper Skill v0.3: Rename + Knowledge Base + .paper Config

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rename `notebooklm-paper` → `paper`, add `.paper` dotfile for project config, and integrate an Obsidian knowledge base (raw/wiki/qa) with three new researcher-verb commands: digest, ask, check.

**Architecture:** `.paper` YAML dotfile replaces `project.json` as the single source of truth for project config — vault path, NotebookLM URL, venue, deadline, keywords. Vault operations use the existing hybrid pattern: Python scripts for file I/O (indexing, ingestion), SKILL.md files for LLM-driven work (wiki compilation, Q&A, health checks). Skill rename is a global find-replace of paths + names.

**Tech Stack:** Python 3.11+, PyYAML, Obsidian-flavored Markdown, existing run.py router

---

## File Structure

```
# RENAME (global path change)
~/.claude/skills/notebooklm-paper/  →  ~/.claude/skills/paper/
~/.notebooklm-paper/                →  ~/.paper/

# CREATE
scripts/store/vault_index.py         — Build CATALOG.md from raw/wiki/qa scan
scripts/store/obsidian_handler.py    — Vault init, ingest, index CLI
scripts/core/dotpaper.py             — Read/write .paper YAML config
support/digest.md                    — SKILL.md: compile wiki from raw papers
support/ask.md                       — SKILL.md: Q&A with auto-filing
support/check.md                     — SKILL.md: vault health diagnostics
tests/test_dotpaper.py               — Tests for .paper config
tests/test_vault_index.py            — Tests for index generation
tests/test_obsidian_handler.py       — Tests for vault init/ingest

# MODIFY
SKILL.md                             — Rename, add init flow, add new routes
scripts/config.py                    — Rename paths, add vault dirs, read .paper
scripts/run.py                       — Add "kb" alias, rename paths
support/store.md                     — Add kb section
phases/01-discover.md                — Add vault auto-ingest hook
obsidian-preset/.obsidian/bookmarks.json — Add raw/wiki/qa bookmarks
```

---

### Task 1: Rename `notebooklm-paper` → `paper` Globally

**Files:**
- Modify: Every `.md` and `.py` file referencing old paths
- Modify: `SKILL.md`, `README.md`, `ARCHITECTURE.md`, `CHANGELOG.md`
- Modify: `scripts/config.py`, `scripts/run.py`
- Modify: All `phases/*.md`, all `support/*.md`
- Modify: `bin/paper-config`, `bin/paper-feedback`, `bin/paper-update-check`
- Modify: `setup`

- [ ] **Step 1: Find all references to old paths**

```bash
cd /Users/chengchunyuan/project/lab/notebooklm-paper-skill
grep -r "notebooklm-paper" --include="*.md" --include="*.py" --include="*.sh" -l
grep -r "notebooklm-paper" bin/ -l
grep -r "\.notebooklm-paper" --include="*.py" -l
```

- [ ] **Step 2: Replace skill path references**

In all files, replace:
- `~/.claude/skills/notebooklm-paper` → `~/.claude/skills/paper`
- `notebooklm-paper` (as skill name in frontmatter) → `paper`
- `.notebooklm-paper` (data dir) → `.paper`
- `PAPER_SKILL=~/.claude/skills/notebooklm-paper` → `PAPER_SKILL=~/.claude/skills/paper`

- [ ] **Step 3: Update `scripts/config.py` data dir**

```python
# Before
DATA_DIR = Path.home() / ".notebooklm-paper"
NOTEBOOKLM_STORAGE_PATH = Path.home() / ".notebooklm" / "storage_state.json"

# After
DATA_DIR = Path.home() / ".paper"
NOTEBOOKLM_STORAGE_PATH = Path.home() / ".notebooklm" / "storage_state.json"  # keep — this is notebooklm-py's own path
```

- [ ] **Step 4: Update SKILL.md name frontmatter**

```yaml
# Before
name: notebooklm-paper
# After
name: paper
```

- [ ] **Step 5: Update setup script migration path**

The `setup` script has a migration from `notebooklm-skill` → `notebooklm-paper`. Add migration from `notebooklm-paper` → `paper`:

```bash
# Migrate from notebooklm-paper if present
OLD_DATA="$HOME/.notebooklm-paper"
NEW_DATA="$HOME/.paper"
if [ -d "$OLD_DATA" ] && [ ! -d "$NEW_DATA" ]; then
  echo "Migrating data from $OLD_DATA to $NEW_DATA..."
  mv "$OLD_DATA" "$NEW_DATA"
fi
```

- [ ] **Step 6: Verify no old references remain**

```bash
grep -r "notebooklm-paper" --include="*.md" --include="*.py" .
```

Expected: No matches (except possibly CHANGELOG.md historical entries, which are fine).

- [ ] **Step 7: Run existing tests**

```bash
cd /Users/chengchunyuan/project/lab/notebooklm-paper-skill
.venv/bin/python3 -m pytest tests/ -v
```

Expected: All 26 existing tests pass.

- [ ] **Step 8: Commit**

```bash
git add -A
git commit -m "chore: rename notebooklm-paper to paper globally"
```

---

### Task 2: Create `.paper` Dotfile System — `scripts/core/dotpaper.py`

**Files:**
- Create: `scripts/core/dotpaper.py`
- Create: `tests/test_dotpaper.py`
- Modify: `requirements.txt` (add PyYAML)

The `.paper` file is the single source of truth for a research project. It replaces `project.json` and eliminates the need for `--vault-path` and `--notebook-url` flags.

- [ ] **Step 1: Add PyYAML to requirements.txt**

Add to `requirements.txt`:
```
PyYAML>=6.0
```

- [ ] **Step 2: Install updated dependencies**

```bash
cd /Users/chengchunyuan/project/lab/notebooklm-paper-skill
.venv/bin/pip install PyYAML>=6.0
```

- [ ] **Step 3: Write the failing tests**

Create `tests/test_dotpaper.py`:

```python
"""Tests for .paper dotfile config."""
import pytest
from pathlib import Path
from scripts.core.dotpaper import load_dotpaper, save_dotpaper, find_dotpaper, create_dotpaper


@pytest.fixture
def project_dir(tmp_path):
    return tmp_path / "my-research"


def test_create_dotpaper_minimal(project_dir):
    """Create .paper with only required fields."""
    project_dir.mkdir()
    dp = create_dotpaper(
        directory=project_dir,
        project="test-project",
        topic="Testing dotpaper creation",
        goal="Verify the system works",
    )
    assert (project_dir / ".paper").exists()
    assert dp["project"] == "test-project"
    assert dp["topic"] == "Testing dotpaper creation"


def test_create_dotpaper_full(project_dir):
    """Create .paper with all fields."""
    project_dir.mkdir()
    dp = create_dotpaper(
        directory=project_dir,
        project="behavioral-vcs",
        topic="Verifiable credentials for AI agent identity",
        goal="Propose a framework binding agent actions to verifiable identity",
        venue="USENIX Security 2027",
        venue_type="conference",
        deadline="2027-02-01",
        page_limit=18,
        format="usenix",
        notebook="https://notebooklm.google.com/notebook/abc123",
        keywords=["verifiable credentials", "agent identity", "zero-trust"],
        related_fields=["IAM", "decentralized identity"],
    )
    assert dp["venue"] == "USENIX Security 2027"
    assert dp["deadline"] == "2027-02-01"
    assert dp["keywords"] == ["verifiable credentials", "agent identity", "zero-trust"]
    assert dp["notebook"] == "https://notebooklm.google.com/notebook/abc123"


def test_load_dotpaper(project_dir):
    """Load .paper from a directory."""
    project_dir.mkdir()
    create_dotpaper(project_dir, project="test", topic="Test", goal="Test")
    dp = load_dotpaper(project_dir)
    assert dp["project"] == "test"
    assert "phase" in dp
    assert "created" in dp


def test_load_dotpaper_missing(tmp_path):
    """Load .paper returns None when not found."""
    dp = load_dotpaper(tmp_path)
    assert dp is None


def test_save_dotpaper_updates(project_dir):
    """Save .paper preserves existing fields and updates changed ones."""
    project_dir.mkdir()
    create_dotpaper(project_dir, project="test", topic="Old topic", goal="Old goal")
    dp = load_dotpaper(project_dir)
    dp["phase"] = "position"
    dp["phases_completed"] = ["discover"]
    save_dotpaper(project_dir, dp)
    reloaded = load_dotpaper(project_dir)
    assert reloaded["phase"] == "position"
    assert reloaded["phases_completed"] == ["discover"]
    assert reloaded["topic"] == "Old topic"


def test_find_dotpaper_walks_up(tmp_path):
    """find_dotpaper searches parent directories."""
    root = tmp_path / "project"
    root.mkdir()
    create_dotpaper(root, project="test", topic="Test", goal="Test")
    nested = root / "subdir" / "deep"
    nested.mkdir(parents=True)
    found = find_dotpaper(nested)
    assert found == root


def test_find_dotpaper_none(tmp_path):
    """find_dotpaper returns None when no .paper exists."""
    found = find_dotpaper(tmp_path)
    assert found is None


def test_dotpaper_vault_default(project_dir):
    """Vault path defaults to ~/.paper/vaults/{project}."""
    project_dir.mkdir()
    dp = create_dotpaper(project_dir, project="my-topic", topic="Test", goal="Test")
    expected = str(Path.home() / ".paper" / "vaults" / "my-topic")
    assert dp["vault"] == expected


def test_dotpaper_vault_custom(project_dir):
    """Vault path can be set explicitly."""
    project_dir.mkdir()
    dp = create_dotpaper(
        project_dir, project="test", topic="Test", goal="Test",
        vault="/custom/path/vault",
    )
    assert dp["vault"] == "/custom/path/vault"
```

- [ ] **Step 4: Run tests to verify they fail**

Run: `cd /Users/chengchunyuan/project/lab/notebooklm-paper-skill && .venv/bin/python3 -m pytest tests/test_dotpaper.py -v`
Expected: FAIL — `ModuleNotFoundError`

- [ ] **Step 5: Implement dotpaper.py**

Create `scripts/core/dotpaper.py`:

```python
#!/usr/bin/env python3
"""
Read/write .paper YAML config — the single source of truth for a research project.

.paper lives in the working directory and stores:
- Project identity (name, topic, goal)
- Target venue (name, type, deadline, format, page limit)
- Knowledge base (vault path, NotebookLM URL)
- Research scope (keywords, related fields)
- Status (current phase, completed phases, created date)
"""

from datetime import date
from pathlib import Path

import yaml


def create_dotpaper(
    directory: Path,
    project: str,
    topic: str,
    goal: str,
    venue: str = "",
    venue_type: str = "",
    deadline: str = "",
    page_limit: int = 0,
    format: str = "",
    notebook: str = "",
    vault: str = "",
    keywords: list[str] = None,
    related_fields: list[str] = None,
) -> dict:
    """Create a new .paper config file."""
    if not vault:
        vault = str(Path.home() / ".paper" / "vaults" / project)

    config = {
        "project": project,
        "topic": topic,
        "goal": goal,
        "venue": venue,
        "venue_type": venue_type,
        "deadline": deadline,
        "page_limit": page_limit,
        "format": format,
        "vault": vault,
        "notebook": notebook,
        "keywords": keywords or [],
        "related_fields": related_fields or [],
        "phase": "init",
        "phases_completed": [],
        "created": date.today().isoformat(),
    }

    save_dotpaper(directory, config)
    return config


def save_dotpaper(directory: Path, config: dict):
    """Write .paper config to directory."""
    path = directory / ".paper"
    with open(path, "w", encoding="utf-8") as f:
        f.write("# .paper — Research Project Config\n")
        f.write("# Managed by /paper skill. Edit freely.\n\n")
        yaml.dump(config, f, default_flow_style=False, sort_keys=False, allow_unicode=True)


def load_dotpaper(directory: Path) -> dict | None:
    """Load .paper config from directory. Returns None if not found."""
    path = directory / ".paper"
    if not path.exists():
        return None
    with open(path, encoding="utf-8") as f:
        content = f.read()
    # Strip comment lines before YAML parsing
    yaml_lines = [l for l in content.splitlines() if not l.startswith("#")]
    return yaml.safe_load("\n".join(yaml_lines))


def find_dotpaper(start: Path) -> Path | None:
    """Walk up from start directory to find nearest .paper file.
    Returns the directory containing .paper, or None."""
    current = start.resolve()
    while True:
        if (current / ".paper").exists():
            return current
        parent = current.parent
        if parent == current:
            return None
        current = parent
```

- [ ] **Step 6: Run tests to verify they pass**

Run: `cd /Users/chengchunyuan/project/lab/notebooklm-paper-skill && .venv/bin/python3 -m pytest tests/test_dotpaper.py -v`
Expected: PASS (9 tests)

- [ ] **Step 7: Commit**

```bash
git add scripts/core/dotpaper.py tests/test_dotpaper.py requirements.txt
git commit -m "feat: add .paper dotfile config system with YAML read/write"
```

---

### Task 3: Create `scripts/store/vault_index.py` — CATALOG.md Builder

**Files:**
- Create: `scripts/store/vault_index.py`
- Create: `tests/test_vault_index.py`

Builds CATALOG.md — the AI-readable index matching the user's existing pattern from `/project/notebook/CATALOG.md`.

- [ ] **Step 1: Write the failing tests**

Create `tests/test_vault_index.py`:

```python
"""Tests for vault CATALOG.md builder."""
import pytest
from pathlib import Path
from scripts.store.vault_index import (
    scan_raw_dir,
    scan_wiki_dir,
    scan_qa_dir,
    build_catalog,
    write_catalog,
)


@pytest.fixture
def vault(tmp_path):
    for d in ("raw", "wiki", "qa"):
        (tmp_path / d).mkdir()
    return tmp_path


def test_scan_raw_empty(vault):
    assert scan_raw_dir(vault / "raw") == []


def test_scan_raw_markdown(vault):
    (vault / "raw" / "attention.md").write_text(
        "---\ntitle: Attention Is All You Need\nauthors: Vaswani et al.\n"
        "year: 2017\ntags: [transformer, attention]\n---\n\nContent."
    )
    entries = scan_raw_dir(vault / "raw")
    assert len(entries) == 1
    assert entries[0]["title"] == "Attention Is All You Need"
    assert entries[0]["file"] == "raw/attention.md"
    assert "transformer" in entries[0]["tags"]


def test_scan_raw_pdf(vault):
    (vault / "raw" / "paper.pdf").write_bytes(b"%PDF-1.4 fake")
    entries = scan_raw_dir(vault / "raw")
    assert len(entries) == 1
    assert entries[0]["title"] == "paper"


def test_scan_wiki(vault):
    (vault / "wiki" / "transformers.md").write_text(
        "---\ntitle: Transformer Architecture\ntags: [transformer]\n"
        "sources: [attention]\n---\nOverview."
    )
    entries = scan_wiki_dir(vault / "wiki")
    assert len(entries) == 1
    assert entries[0]["title"] == "Transformer Architecture"


def test_scan_qa(vault):
    (vault / "qa" / "2026-04-04-question.md").write_text(
        "---\ntitle: How do transformers work?\nsource: claude\n"
        "date: 2026-04-04\ntags: [transformer]\n---\nQ&A content."
    )
    entries = scan_qa_dir(vault / "qa")
    assert len(entries) == 1
    assert entries[0]["source"] == "claude"


def test_build_catalog(vault):
    (vault / "raw" / "paper-a.md").write_text("---\ntitle: Paper A\ntags: [ml]\n---\nContent.")
    (vault / "wiki" / "concept.md").write_text("---\ntitle: Concept X\ntags: [ml]\nsources: [paper-a]\n---\nContent.")
    catalog = build_catalog(vault)
    assert "# Research Catalog" in catalog
    assert "Paper A" in catalog
    assert "Concept X" in catalog


def test_write_catalog(vault):
    write_catalog(vault, "# Test\nContent.")
    assert (vault / "CATALOG.md").exists()
    assert "Test" in (vault / "CATALOG.md").read_text()
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd /Users/chengchunyuan/project/lab/notebooklm-paper-skill && .venv/bin/python3 -m pytest tests/test_vault_index.py -v`
Expected: FAIL — `ModuleNotFoundError`

- [ ] **Step 3: Implement vault_index.py**

Create `scripts/store/vault_index.py`:

```python
#!/usr/bin/env python3
"""
Build CATALOG.md — AI-readable index for the Obsidian vault.
Scans raw/, wiki/, qa/ and produces a structured catalog with
file paths, tags, and metadata for LLM navigation.
"""

from datetime import date
from pathlib import Path


def _parse_frontmatter(text: str) -> dict:
    """Extract YAML frontmatter from markdown."""
    if not text.startswith("---"):
        return {}
    end = text.find("---", 3)
    if end == -1:
        return {}
    fm = {}
    for line in text[3:end].strip().splitlines():
        if ":" not in line:
            continue
        key, val = line.split(":", 1)
        key = key.strip()
        val = val.strip()
        if val.startswith("[") and val.endswith("]"):
            val = [v.strip() for v in val[1:-1].split(",") if v.strip()]
        fm[key] = val
    return fm


def scan_raw_dir(raw_dir: Path) -> list[dict]:
    """Scan raw/ for papers and source documents."""
    entries = []
    if not raw_dir.exists():
        return entries
    for f in sorted(raw_dir.rglob("*")):
        if f.is_dir():
            continue
        entry = {"file": f"raw/{f.relative_to(raw_dir)}", "title": f.stem, "tags": [], "authors": "", "year": ""}
        if f.suffix == ".md":
            fm = _parse_frontmatter(f.read_text(encoding="utf-8", errors="replace"))
            entry["title"] = fm.get("title", f.stem)
            entry["tags"] = fm.get("tags", [])
            entry["authors"] = fm.get("authors", "")
            entry["year"] = fm.get("year", "")
        entries.append(entry)
    return entries


def scan_wiki_dir(wiki_dir: Path) -> list[dict]:
    """Scan wiki/ for compiled concept articles."""
    entries = []
    if not wiki_dir.exists():
        return entries
    for f in sorted(wiki_dir.rglob("*.md")):
        fm = _parse_frontmatter(f.read_text(encoding="utf-8", errors="replace"))
        entries.append({
            "file": f"wiki/{f.relative_to(wiki_dir)}",
            "title": fm.get("title", f.stem),
            "tags": fm.get("tags", []),
            "sources": fm.get("sources", []),
        })
    return entries


def scan_qa_dir(qa_dir: Path) -> list[dict]:
    """Scan qa/ for Q&A session records."""
    entries = []
    if not qa_dir.exists():
        return entries
    for f in sorted(qa_dir.rglob("*.md")):
        fm = _parse_frontmatter(f.read_text(encoding="utf-8", errors="replace"))
        entries.append({
            "file": f"qa/{f.relative_to(qa_dir)}",
            "title": fm.get("title", f.stem),
            "source": fm.get("source", "unknown"),
            "date": fm.get("date", ""),
            "tags": fm.get("tags", []),
        })
    return entries


def build_catalog(vault_dir: Path) -> str:
    """Build CATALOG.md content from vault scan."""
    raw = scan_raw_dir(vault_dir / "raw")
    wiki = scan_wiki_dir(vault_dir / "wiki")
    qa = scan_qa_dir(vault_dir / "qa")

    lines = [
        "---",
        "purpose: AI-readable index for locating papers, wiki articles, and Q&A sessions",
        f"updated: {date.today().isoformat()}",
        f"stats: {len(raw)} raw, {len(wiki)} wiki, {len(qa)} qa",
        "---", "", "# Research Catalog", "",
        "> **For AI agents**: Scan this file first to determine which document to read. "
        "Entries grouped by section with tags and file paths.", "", "---", "",
    ]

    lines.append("## Raw — Source Papers & Documents\n")
    if not raw:
        lines.append("*No papers ingested yet. Add PDFs or markdown to `raw/`.*\n")
    for e in raw:
        lines.append(f"### {e['title']}")
        lines.append(f"- **File**: `{e['file']}`")
        if e.get("authors"):
            lines.append(f"- **Authors**: {e['authors']}")
        if e.get("year"):
            lines.append(f"- **Year**: {e['year']}")
        if e.get("tags"):
            lines.append(f"- **Tags**: {', '.join(f'`{t}`' for t in e['tags'])}")
        lines.append("")

    lines.append("## Wiki — Compiled Knowledge\n")
    if not wiki:
        lines.append("*No wiki articles yet. Run `/paper digest` to generate from raw sources.*\n")
    for e in wiki:
        lines.append(f"### {e['title']}")
        lines.append(f"- **File**: `{e['file']}`")
        if e.get("tags"):
            lines.append(f"- **Tags**: {', '.join(f'`{t}`' for t in e['tags'])}")
        if e.get("sources"):
            lines.append(f"- **Sources**: {', '.join(f'[[{s}]]' for s in e['sources'])}")
        lines.append("")

    lines.append("## Q&A — Research Questions & Answers\n")
    if not qa:
        lines.append("*No Q&A sessions yet. Run `/paper ask` to start.*\n")
    for e in qa:
        lines.append(f"### {e['title']}")
        lines.append(f"- **File**: `{e['file']}`")
        lines.append(f"- **Source**: {e['source']}")
        if e.get("date"):
            lines.append(f"- **Date**: {e['date']}")
        if e.get("tags"):
            lines.append(f"- **Tags**: {', '.join(f'`{t}`' for t in e['tags'])}")
        lines.append("")

    return "\n".join(lines)


def write_catalog(vault_dir: Path, content: str):
    """Write CATALOG.md to vault root."""
    (vault_dir / "CATALOG.md").write_text(content, encoding="utf-8")
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `cd /Users/chengchunyuan/project/lab/notebooklm-paper-skill && .venv/bin/python3 -m pytest tests/test_vault_index.py -v`
Expected: PASS (8 tests)

- [ ] **Step 5: Commit**

```bash
git add scripts/store/vault_index.py tests/test_vault_index.py
git commit -m "feat: add vault_index.py for CATALOG.md generation"
```

---

### Task 4: Create `scripts/store/obsidian_handler.py` — Vault Init & Ingest

**Files:**
- Create: `scripts/store/obsidian_handler.py`
- Create: `tests/test_obsidian_handler.py`

- [ ] **Step 1: Write the failing tests**

Create `tests/test_obsidian_handler.py`:

```python
"""Tests for Obsidian vault handler."""
import pytest
from pathlib import Path
from scripts.store.obsidian_handler import init_vault, ingest_paper


@pytest.fixture
def vault(tmp_path):
    return tmp_path / "vault"


def test_init_creates_structure(vault):
    init_vault(vault)
    assert (vault / "raw").is_dir()
    assert (vault / "wiki").is_dir()
    assert (vault / "qa").is_dir()
    assert (vault / "CATALOG.md").exists()
    assert (vault / ".obsidian").is_dir()


def test_init_idempotent(vault):
    init_vault(vault)
    (vault / "raw" / "test.md").write_text("# Test")
    init_vault(vault)
    assert (vault / "raw" / "test.md").exists()


def test_ingest_md(vault):
    init_vault(vault)
    source = vault.parent / "paper.md"
    source.write_text("---\ntitle: Test\n---\nContent.")
    ingest_paper(vault, source)
    assert (vault / "raw" / "paper.md").exists()


def test_ingest_pdf(vault):
    init_vault(vault)
    source = vault.parent / "paper.pdf"
    source.write_bytes(b"%PDF-1.4 fake")
    ingest_paper(vault, source)
    assert (vault / "raw" / "paper.pdf").exists()


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
    assert len(list((vault / "raw").glob("paper*.md"))) == 1
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `cd /Users/chengchunyuan/project/lab/notebooklm-paper-skill && .venv/bin/python3 -m pytest tests/test_obsidian_handler.py -v`
Expected: FAIL — `ModuleNotFoundError`

- [ ] **Step 3: Implement obsidian_handler.py**

Create `scripts/store/obsidian_handler.py`:

```python
#!/usr/bin/env python3
"""
Obsidian vault handler — init, ingest, index.

Vault structure:
  raw/   — Original papers (PDFs, markdown, web clips)
  wiki/  — LLM-compiled concept articles
  qa/    — Q&A session records
"""

import shutil
import sys
from pathlib import Path

from scripts.store.vault_index import build_catalog, write_catalog


OBSIDIAN_PRESET = Path(__file__).parent.parent.parent / "obsidian-preset" / ".obsidian"


def init_vault(vault_dir: Path):
    """Initialize vault with raw/wiki/qa and Obsidian config."""
    vault_dir.mkdir(parents=True, exist_ok=True)
    for sub in ("raw", "wiki", "qa"):
        (vault_dir / sub).mkdir(exist_ok=True)

    obsidian_dir = vault_dir / ".obsidian"
    if not obsidian_dir.exists() and OBSIDIAN_PRESET.exists():
        shutil.copytree(OBSIDIAN_PRESET, obsidian_dir)

    catalog = build_catalog(vault_dir)
    write_catalog(vault_dir, catalog)


def ingest_paper(vault_dir: Path, source: Path):
    """Copy a paper into raw/ and rebuild catalog."""
    dest = vault_dir / "raw" / source.name
    if dest.exists():
        return
    shutil.copy2(source, dest)
    catalog = build_catalog(vault_dir)
    write_catalog(vault_dir, catalog)


def ingest_directory(vault_dir: Path, source_dir: Path):
    """Ingest all supported files from a directory."""
    extensions = {".md", ".pdf", ".txt", ".html"}
    for f in sorted(source_dir.iterdir()):
        if f.is_file() and f.suffix.lower() in extensions:
            ingest_paper(vault_dir, f)


def main():
    """CLI: kb init|ingest|index."""
    from scripts.core.dotpaper import find_dotpaper, load_dotpaper
    from scripts.config import get_vault_dir

    if len(sys.argv) < 2:
        print("Usage: obsidian_handler.py <init|ingest|index> [args...]")
        sys.exit(1)

    command = sys.argv[1]
    args = sys.argv[2:]

    # Resolve vault path: .paper > args > config default
    vault_dir = None
    dp_dir = find_dotpaper(Path.cwd())
    if dp_dir:
        dp = load_dotpaper(dp_dir)
        if dp and dp.get("vault"):
            vault_dir = Path(dp["vault"])

    if command == "init":
        vault_dir = Path(args[0]) if args else (vault_dir or get_vault_dir())
        init_vault(vault_dir)
        print(f"Vault initialized at {vault_dir}")

    elif command == "ingest":
        if not args:
            print("Usage: obsidian_handler.py ingest <file-or-directory>")
            sys.exit(1)
        vault_dir = vault_dir or get_vault_dir()
        source = Path(args[0])
        if source.is_dir():
            ingest_directory(vault_dir, source)
        elif source.is_file():
            ingest_paper(vault_dir, source)
        else:
            print(f"Not found: {source}")
            sys.exit(1)

    elif command == "index":
        vault_dir = vault_dir or get_vault_dir()
        catalog = build_catalog(vault_dir)
        write_catalog(vault_dir, catalog)
        print(f"CATALOG.md rebuilt at {vault_dir}")

    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `cd /Users/chengchunyuan/project/lab/notebooklm-paper-skill && .venv/bin/python3 -m pytest tests/test_obsidian_handler.py -v`
Expected: PASS (6 tests)

- [ ] **Step 5: Commit**

```bash
git add scripts/store/obsidian_handler.py tests/test_obsidian_handler.py
git commit -m "feat: add obsidian_handler.py for vault init, ingest, and index"
```

---

### Task 5: Update `scripts/config.py` — Vault Paths + `.paper` Integration

**Files:**
- Modify: `scripts/config.py`

- [ ] **Step 1: Add vault path constants after the DATA_DIR block**

Add after `CONFIG_FILE` line in `scripts/config.py`:

```python
# Vault paths
VAULTS_DIR = DATA_DIR / "vaults"


def get_vault_dir() -> Path:
    """Get vault dir from .paper in cwd, or config, or default."""
    from scripts.core.dotpaper import find_dotpaper, load_dotpaper
    dp_dir = find_dotpaper(Path.cwd())
    if dp_dir:
        dp = load_dotpaper(dp_dir)
        if dp and dp.get("vault"):
            return Path(dp["vault"])
    config = load_config()
    if config.get("vault_path"):
        return Path(config["vault_path"])
    return VAULTS_DIR / "default"
```

- [ ] **Step 2: Run all tests**

Run: `cd /Users/chengchunyuan/project/lab/notebooklm-paper-skill && .venv/bin/python3 -m pytest tests/ -v`
Expected: All tests pass.

- [ ] **Step 3: Commit**

```bash
git add scripts/config.py
git commit -m "feat: add vault path resolution with .paper dotfile support"
```

---

### Task 6: Register `kb` in `scripts/run.py`

**Files:**
- Modify: `scripts/run.py:9-27`

- [ ] **Step 1: Add kb alias**

Add to `SCRIPT_ALIASES` dict:

```python
    "kb": "store/obsidian_handler.py",
```

- [ ] **Step 2: Verify routing**

Run: `cd /Users/chengchunyuan/project/lab/notebooklm-paper-skill && .venv/bin/python3 scripts/run.py kb 2>&1 | head -2`
Expected: `Usage: obsidian_handler.py <init|ingest|index> [args...]`

- [ ] **Step 3: Commit**

```bash
git add scripts/run.py
git commit -m "feat: register kb command in run.py router"
```

---

### Task 7: Create `support/digest.md` — Wiki Compilation Skill

**Files:**
- Create: `support/digest.md`

- [ ] **Step 1: Write the skill file**

Create `support/digest.md`:

```markdown
---
name: paper-digest
description: "Compile wiki articles from raw papers. Reads raw/, identifies concepts, writes wiki/ with summaries, wikilinks, and source attribution."
---

# /paper digest — Organize Your Knowledge

Read all unprocessed papers in `raw/` and compile them into wiki articles — one per key concept. Each article has a summary, key points, cross-links, and traces back to source papers.

## Setup

```bash
PAPER_SKILL=~/.claude/skills/paper
PY=$PAPER_SKILL/.venv/bin/python3
```

Read `.paper` in the current directory to find the vault path:

```bash
VAULT=$(grep '^vault:' .paper | awk '{print $2}')
```

If no `.paper` found, tell user to run `/paper init` first.

## Workflow

### Step 1: Read CATALOG.md

```bash
cat "$VAULT/CATALOG.md"
```

Understand current state: which papers exist in raw/, which wiki articles already exist, which Q&A sessions are recorded.

### Step 2: Identify unprocessed papers

Compare raw/ entries against wiki/ source lists. Papers in raw/ not referenced by any wiki article's `sources:` field are unprocessed.

### Step 3: Read unprocessed papers

For each unprocessed paper:
1. Read full content: `cat "$VAULT/raw/{filename}"`
2. Extract key concepts (2-5 per paper)
3. Note methods, claims, findings
4. Identify connections to existing wiki articles

### Step 4: Write wiki articles

For each concept, create `wiki/{concept-slug}.md`:

```markdown
---
title: "{Concept Name}"
tags: [{relevant}, {tags}]
sources: [{raw-paper-stems}]
related: [{other-wiki-stems}]
updated: {YYYY-MM-DD}
---

# {Concept Name}

## Overview
{2-3 paragraph summary}

## Key Points
- {Essential facts as bullet points}

## Connections
- [[wiki/{related-concept}]] — {relationship}

## Sources
- [[raw/{paper-filename}]] — {what this paper contributes}
```

### Step 5: Update existing articles

When a new paper adds to an existing concept:
1. Read the existing wiki article
2. Add new information under appropriate sections
3. Append the paper to `sources:` frontmatter
4. Add new `[[wikilinks]]` under Connections
5. Update `updated:` date

### Step 6: Rebuild index

```bash
$PY $PAPER_SKILL/scripts/run.py kb index
```

## Rules

- **Never fabricate** — Only write what raw papers say. Quote directly when uncertain.
- **Always link** — Use `[[wikilinks]]` between wiki articles and back to raw papers.
- **Always attribute** — Every claim traces to a specific raw/ source.
- **Incremental** — Don't rewrite unchanged articles. Only add new information.
- **Reuse tags** — Check existing tags in CATALOG.md before creating new ones.

## Modes

When user runs `/paper digest`:

**A) Full digest** — Process all uncompiled papers (default)
**B) Single paper** — Specify which: `/paper digest attention.md`
**C) Refresh** — Re-scan all raw/ and enrich existing wiki articles with new connections
```

- [ ] **Step 2: Commit**

```bash
git add support/digest.md
git commit -m "feat: add digest skill for LLM wiki compilation"
```

---

### Task 8: Create `support/ask.md` — Q&A Skill

**Files:**
- Create: `support/ask.md`

- [ ] **Step 1: Write the skill file**

Create `support/ask.md`:

```markdown
---
name: paper-ask
description: "Research Q&A against the knowledge base wiki. Answers filed to qa/ to accumulate knowledge."
---

# /paper ask — Research Q&A

Ask questions against your knowledge base. Claude searches wiki/ and raw/ to synthesize answers with source citations. Every Q&A session is auto-filed to `qa/` so your explorations accumulate into the knowledge base.

## Setup

```bash
PAPER_SKILL=~/.claude/skills/paper
PY=$PAPER_SKILL/.venv/bin/python3
VAULT=$(grep '^vault:' .paper | awk '{print $2}')
```

## Workflow

### Step 1: Read CATALOG.md

```bash
cat "$VAULT/CATALOG.md"
```

### Step 2: Research the answer

Based on the user's question:
1. Identify relevant wiki articles and raw papers from CATALOG.md tags/titles
2. Read relevant files: `cat "$VAULT/wiki/{article}.md"` and `cat "$VAULT/raw/{paper}.md"`
3. Cross-reference multiple sources
4. Synthesize a comprehensive answer

### Step 3: Present answer

Show the user:
- Synthesized answer with source attribution
- Confidence: **high** (multiple sources agree), **medium** (single source), **low** (inferred/sparse)
- 2-3 suggested follow-up questions

### Step 4: File to qa/

Save to `qa/{YYYY-MM-DD}-{question-slug}.md`:

```markdown
---
title: "{Question text}"
source: claude
date: {YYYY-MM-DD}
tags: [{relevant}, {tags}]
wiki_refs: [{wiki-articles-consulted}]
raw_refs: [{raw-papers-consulted}]
confidence: {high|medium|low}
---

## Question

{Full question text}

## Answer

{Answer with [[wikilinks]] to sources}

## Sources Consulted

- [[wiki/{article}]] — {contribution}
- [[raw/{paper}]] — {contribution}

## Follow-up Questions

- {Question 1}
- {Question 2}
```

### Step 5: Rebuild index

```bash
$PY $PAPER_SKILL/scripts/run.py kb index
```

## Logging NotebookLM Q&A

When the user had a conversation in NotebookLM and wants to log it:

```
/paper ask log
```

Prompt:
1. "What was the question?"
2. "Paste or summarize NotebookLM's answer"
3. Save to qa/ with `source: notebooklm`

## Modes

**A) Ask** — New question against the wiki (default)
**B) Log** — Record a NotebookLM or external Q&A session
**C) Review** — Browse past Q&A, find patterns, suggest new questions
```

- [ ] **Step 2: Commit**

```bash
git add support/ask.md
git commit -m "feat: add ask skill for research Q&A with auto-filing"
```

---

### Task 9: Create `support/check.md` — Health Check Skill

**Files:**
- Create: `support/check.md`

- [ ] **Step 1: Write the skill file**

Create `support/check.md`:

```markdown
---
name: paper-check
description: "Health-check the knowledge base vault. Find orphans, broken links, gaps, and suggest improvements."
---

# /paper check — Knowledge Base Health

Diagnose your knowledge base: find unprocessed papers, broken wikilinks, thin articles, and suggest new connections and articles to write.

## Setup

```bash
PAPER_SKILL=~/.claude/skills/paper
PY=$PAPER_SKILL/.venv/bin/python3
VAULT=$(grep '^vault:' .paper | awk '{print $2}')
```

## Checks

### A. Coverage
- **Uncompiled papers**: raw/ files not in any wiki article's `sources:`
- **Orphan wiki articles**: Articles with no incoming links from other wiki articles
- **Stale Q&A**: qa/ entries referencing deleted wiki articles

### B. Consistency
- **Broken wikilinks**: `[[links]]` pointing to non-existent files
- **Missing frontmatter**: wiki/ or qa/ files without required fields (title, tags)
- **Tag drift**: Similar tags that should merge (e.g., `ml` vs `machine-learning`)
- **Stale articles**: Wiki `updated:` older than raw source modification date

### C. Quality
- **Thin articles**: Wiki articles under 200 words
- **Unlinked articles**: Wiki articles with no `related:` entries
- **Missing concepts**: Topics in 3+ raw papers with no wiki article

### D. Suggestions
- New articles to write (concepts spanning multiple papers)
- Merge candidates (high tag overlap)
- Research questions worth investigating

## Report Format

```
Knowledge Base Health — {date}

Stats: {N} raw | {M} wiki | {K} qa

Healthy:
  {checks that passed}

Warnings:
  {N} uncompiled raw papers
  {N} broken wikilinks
  {details}

Suggestions:
  New article: "{concept}" (in {N} papers, no wiki entry)
  Merge: "{a}" + "{b}" (similar tags)
  Question: "{interesting question from gap}"

Run /paper digest to address uncompiled papers.
```

## Actions

After the report, offer:

**A) Auto-fix** — Fix broken links, normalize tags, update stale dates
**B) Digest missing** — Run `/paper digest` for uncompiled papers
**C) Report only** — No action (default)
```

- [ ] **Step 2: Commit**

```bash
git add support/check.md
git commit -m "feat: add check skill for vault health diagnostics"
```

---

### Task 10: Update `SKILL.md` — Init Flow + New Routes

**Files:**
- Modify: `SKILL.md`

This is the biggest integration task. The SKILL.md preamble now reads `.paper`, the guided flow adds init + KB options, and the routing table gets new entries.

- [ ] **Step 1: Update the preamble to read .paper**

Replace the `_PROJECT` detection block in the preamble with:

```bash
# Read .paper if present
if [ -f .paper ]; then
  _PROJ_NAME=$(grep '^project:' .paper | awk '{print $2}')
  _PHASE=$(grep '^phase:' .paper | awk '{print $2}')
  _VAULT=$(grep '^vault:' .paper | awk '{print $2}')
  _NOTEBOOK=$(grep '^notebook:' .paper | awk '{$1=""; print substr($0,2)}')
  echo "PROJECT: $_PROJ_NAME — Phase: $_PHASE"
  [ -n "$_VAULT" ] && echo "VAULT: $_VAULT"
  [ -n "$_NOTEBOOK" ] && echo "NOTEBOOK: $_NOTEBOOK"
else
  # Fallback to legacy project.json
  _PROJECT=$("$PY" -c "
import pathlib, json
projects_dir = pathlib.Path.home() / '.paper' / 'projects'
if not projects_dir.exists():
    print('none'); exit()
for pf in projects_dir.glob('*/project.json'):
    try:
        p = json.loads(pf.read_text())
        if p.get('active'):
            print(f\"{p['name']} — Phase {p['current_phase']}/8 ({p['phase_name']})\"); exit()
    except: pass
print('none')
" 2>/dev/null || echo "none")
  echo "PROJECT: $_PROJECT"
fi
```

- [ ] **Step 2: Update the guided flow**

Replace the guided flow section with:

```markdown
## Guided Flow

When user invokes `/paper` with no sub-command, show:

```
Paper Skill — Research Paper Pipeline

Where are you in your research?

A) Starting fresh — "I have a topic but haven't started"
   → /paper init

B) Finding papers — "I need to survey the field"
   → /paper discover

C) Organizing notes — "I have papers, need to digest them"
   → /paper digest

D) Have a question — "I want to ask something about my research"
   → /paper ask

E) Check my progress — "How's my knowledge base looking?"
   → /paper check

F) Ready to write — "I know my angle, time to write the paper"
   → /paper position → architect → evaluate → write → critique → refine → ship

G) Continue previous project
   → list .paper files or projects from ~/.paper/projects/
```
```

- [ ] **Step 3: Add /paper init instructions**

Add a new section after Guided Flow:

```markdown
## /paper init — First-Time Setup

Walk the user through project setup conversationally:

1. **"What's your research topic?"**
   → topic field

2. **"What's your goal? (one sentence)"**
   → goal field

3. **"Targeting a venue?"**
   A) Conference — ask name + deadline
   B) Journal — ask name
   C) Workshop — ask name + deadline
   D) Not sure yet / preprint
   → venue, venue_type, deadline fields

4. **"Any keywords to guide paper discovery? (comma-separated)"**
   → keywords field

5. **"Do you have a NotebookLM notebook? (paste URL or skip)"**
   → notebook field. If no auth: suggest `/paper auth setup` first.

6. **"Custom vault path? (default: ~/.paper/vaults/{project-name})"**
   → vault field

Create .paper:
```bash
$PY -c "
from scripts.core.dotpaper import create_dotpaper
from pathlib import Path
create_dotpaper(
    Path('.'),
    project='{project}',
    topic='{topic}',
    goal='{goal}',
    venue='{venue}',
    venue_type='{venue_type}',
    deadline='{deadline}',
    notebook='{notebook}',
    keywords={keywords},
    vault='{vault}',
)
"
```

Initialize vault:
```bash
$PY $PAPER_SKILL/scripts/run.py kb init "$VAULT"
```

Show:
```
Project "{project}" initialized!

.paper created in current directory
Vault at {vault} — open in Obsidian
{NotebookLM linked / NotebookLM skipped}

Ready! Run /paper discover to start surveying the field.
```
```

- [ ] **Step 4: Add new routes to the routing table**

Add to the Sub-skill Routing table:

```markdown
| `/paper init` | `SKILL.md` (inline) | Conversational setup |
| `/paper digest` | `support/digest.md` | SKILL.md-only |
| `/paper ask` | `support/ask.md` | SKILL.md-only |
| `/paper check` | `support/check.md` | SKILL.md-only |
```

- [ ] **Step 5: Update phase transition template**

In the phase transition template, update `$PY -c` block to write to `.paper` instead of project.json:

```bash
$PY -c "
from scripts.core.dotpaper import find_dotpaper, load_dotpaper, save_dotpaper
dp_dir = find_dotpaper(Path('.'))
if dp_dir:
    dp = load_dotpaper(dp_dir)
    dp['phases_completed'].append('{current_phase}')
    dp['phase'] = '{next_phase_name}'
    save_dotpaper(dp_dir, dp)
"
```

- [ ] **Step 6: Commit**

```bash
git add SKILL.md
git commit -m "feat: add /paper init flow, digest/ask/check routes, .paper preamble"
```

---

### Task 11: Update `phases/01-discover.md` — Auto-Ingest Hook

**Files:**
- Modify: `phases/01-discover.md`

- [ ] **Step 1: Read current discover phase ending**

```bash
tail -40 /Users/chengchunyuan/project/lab/notebooklm-paper-skill/phases/01-discover.md
```

- [ ] **Step 2: Add vault ingest hook**

Add before the phase exit section at the end of `phases/01-discover.md`:

```markdown
### Vault Integration

After papers are downloaded and analyzed, check for an active vault:

```bash
VAULT=$(grep '^vault:' .paper 2>/dev/null | awk '{print $2}')
if [ -d "$VAULT/raw" ]; then
  echo "VAULT_ACTIVE"
fi
```

If vault is active, offer: "Ingest discovered papers into your knowledge base? (Y/n)"

If yes:
```bash
$PY $PAPER_SKILL/scripts/run.py kb ingest <papers-directory>
```

This copies downloaded papers into `vault/raw/` and rebuilds CATALOG.md. The user can then run `/paper digest` to compile wiki articles from these papers.
```

- [ ] **Step 3: Commit**

```bash
git add phases/01-discover.md
git commit -m "feat: add vault auto-ingest hook to discover phase"
```

---

### Task 12: Update `obsidian-preset/.obsidian/bookmarks.json`

**Files:**
- Modify: `obsidian-preset/.obsidian/bookmarks.json`

- [ ] **Step 1: Update bookmarks for raw/wiki/qa structure**

Replace `obsidian-preset/.obsidian/bookmarks.json` with:

```json
{
  "items": [
    {
      "type": "file",
      "ctime": 1710892800000,
      "title": "CATALOG",
      "path": "CATALOG.md"
    },
    {
      "type": "folder",
      "ctime": 1710892800000,
      "title": "Raw Papers",
      "items": [
        {
          "type": "folder",
          "ctime": 1710892800000,
          "path": "raw"
        }
      ]
    },
    {
      "type": "folder",
      "ctime": 1710892800000,
      "title": "Wiki",
      "items": [
        {
          "type": "folder",
          "ctime": 1710892800000,
          "path": "wiki"
        }
      ]
    },
    {
      "type": "folder",
      "ctime": 1710892800000,
      "title": "Q&A",
      "items": [
        {
          "type": "folder",
          "ctime": 1710892800000,
          "path": "qa"
        }
      ]
    }
  ]
}
```

- [ ] **Step 2: Commit**

```bash
git add obsidian-preset/.obsidian/bookmarks.json
git commit -m "feat: update obsidian bookmarks for raw/wiki/qa vault structure"
```

---

### Task 13: Update `~/.claude/CLAUDE.md` with New Commands

**Files:**
- Modify: `~/.claude/CLAUDE.md`

- [ ] **Step 1: Replace the notebooklm-paper section**

Replace the existing `## notebooklm-paper skill` section in `~/.claude/CLAUDE.md`:

```markdown
## paper skill

- Available skills: /paper, /paper init, /paper discover, /paper digest, /paper ask, /paper check, /paper position, /paper architect, /paper evaluate, /paper write, /paper critique, /paper refine, /paper ship, /paper auth, /paper store, /paper search, /paper analyze, /paper eval, /paper optimize
- Always use `bun` instead of `npm` for all package management and script execution in this project. Use `bun run <script>` instead of `npm run <script>`.
```

- [ ] **Step 2: No commit needed** — this is a global user config, not in the repo.

---

## Self-Review

**1. Spec coverage:**

| Requirement | Task |
|-------------|------|
| Rename notebooklm-paper → paper | Task 1 |
| `.paper` dotfile with topic/goal/venue/deadline/keywords | Task 2 |
| `/paper init` conversational setup | Task 10 |
| raw/ for original papers | Task 4 (init_vault) |
| wiki/ for compiled knowledge | Task 7 (digest.md) |
| qa/ for Q&A records | Task 8 (ask.md) |
| CATALOG.md index | Task 3 (vault_index.py) |
| Health checks | Task 9 (check.md) |
| Discover → vault auto-ingest | Task 11 |
| Obsidian bookmarks | Task 12 |
| Command documentation | Task 13 |

**2. Placeholder scan:** No TBD/TODO/placeholder patterns found.

**3. Type consistency:**
- `get_vault_dir()` defined in config.py (Task 5), used in obsidian_handler.py (Task 4) ✅
- `find_dotpaper`/`load_dotpaper`/`save_dotpaper`/`create_dotpaper` defined in dotpaper.py (Task 2), used in obsidian_handler.py (Task 4) and SKILL.md (Task 10) ✅
- `build_catalog`/`write_catalog` defined in vault_index.py (Task 3), used in obsidian_handler.py (Task 4) ✅
- `init_vault`/`ingest_paper` defined in obsidian_handler.py (Task 4), used by discover hook (Task 11) via CLI ✅
