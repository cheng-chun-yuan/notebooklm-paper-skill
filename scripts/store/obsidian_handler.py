#!/usr/bin/env python3
"""Obsidian vault handler — init, ingest, index."""

import shutil
import sys
from pathlib import Path

# Ensure project root is on sys.path for scripts.* imports
_PROJECT_ROOT = Path(__file__).parent.parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

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
    """CLI: vault init|ingest|index."""
    from scripts.core.dotpaper import find_dotpaper, load_dotpaper
    from scripts.config import get_vault_dir

    if len(sys.argv) < 2:
        print("Usage: obsidian_handler.py <init|ingest|index> [args...]")
        sys.exit(1)

    command = sys.argv[1]
    args = sys.argv[2:]

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
