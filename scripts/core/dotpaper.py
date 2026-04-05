"""YAML-based .paper config file reader/writer for research projects.

The `.paper` file is the single source of truth for a research project's
configuration — topic, venue, vault path, phase tracking, etc.
"""

from __future__ import annotations

import datetime
from pathlib import Path

import yaml


DOTPAPER_FILENAME = ".paper"

HEADER = (
    "# .paper — Research Project Config\n"
    "# Managed by /paper skill. Edit freely.\n\n"
)


def _default_vault(project: str) -> str:
    """Return the default vault path for a project."""
    return str(Path.home() / ".paper" / "vaults" / project)


def create_dotpaper(
    directory: str,
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
    keywords: list[str] | None = None,
    related_fields: list[str] | None = None,
) -> dict:
    """Create a new .paper config file in *directory* and return the config dict."""
    config = {
        "project": project,
        "topic": topic,
        "goal": goal,
        "venue": venue,
        "venue_type": venue_type,
        "deadline": deadline,
        "page_limit": page_limit,
        "format": format,
        "vault": vault if vault else _default_vault(project),
        "notebook": notebook,
        "keywords": keywords or [],
        "related_fields": related_fields or [],
        "phase": "init",
        "phases_completed": [],
        "created": str(datetime.date.today()),
    }
    save_dotpaper(directory, config)
    return config


def save_dotpaper(directory: str, config: dict) -> None:
    """Write *config* to the .paper file in *directory*."""
    path = Path(directory) / DOTPAPER_FILENAME
    with open(path, "w") as f:
        f.write(HEADER)
        yaml.dump(
            config,
            f,
            default_flow_style=False,
            sort_keys=False,
            allow_unicode=True,
        )


def load_dotpaper(directory: str) -> dict | None:
    """Read the .paper file from *directory*. Returns None if it doesn't exist."""
    path = Path(directory) / DOTPAPER_FILENAME
    if not path.exists():
        return None
    with open(path) as f:
        return yaml.safe_load(f)


def find_dotpaper(start: str) -> Path | None:
    """Walk up from *start* looking for a .paper file. Returns the Path or None."""
    current = Path(start).resolve()
    while True:
        candidate = current / DOTPAPER_FILENAME
        if candidate.exists():
            return candidate
        parent = current.parent
        if parent == current:
            # Reached filesystem root
            return None
        current = parent
