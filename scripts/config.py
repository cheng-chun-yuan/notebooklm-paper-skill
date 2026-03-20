"""
Configuration for paper-skill.
Centralizes constants, paths, and paper ID normalization.
"""

import hashlib
import json
import re
from pathlib import Path

# Paths
SKILL_DIR = Path(__file__).parent.parent
DATA_DIR = Path.home() / ".paper-skill"
PAPERS_DIR = DATA_DIR / "papers"
ANALYSES_DIR = DATA_DIR / "analyses"
GAPS_DIR = DATA_DIR / "gaps"
SURVEYS_DIR = DATA_DIR / "surveys"
PROJECTS_DIR = DATA_DIR / "projects"
FEEDBACK_DIR = DATA_DIR / "feedback"
LIBRARY_FILE = DATA_DIR / "library.json"
DOWNLOADS_FILE = DATA_DIR / "downloads.json"
AUTH_INFO_FILE = DATA_DIR / "auth_info.json"
CONFIG_FILE = DATA_DIR / "config.json"

# notebooklm-py auth storage
NOTEBOOKLM_STORAGE_PATH = Path.home() / ".notebooklm" / "storage_state.json"

# Timeouts
QUERY_TIMEOUT_SECONDS = 120
SOURCE_WAIT_TIMEOUT = 180


def normalize_paper_id(doi: str = None, arxiv_id: str = None,
                       title: str = None, author: str = None) -> str:
    """Normalize paper identifiers to filesystem-safe canonical IDs.
    Priority: arxiv_id > doi > title+author hash.
    """
    if arxiv_id:
        return arxiv_id.strip()
    if doi:
        return re.sub(r'/', '_', doi.strip())
    if title:
        key = f"{title.strip()}|{(author or '').strip()}"
        return hashlib.sha256(key.encode()).hexdigest()[:16]
    raise ValueError("At least one of doi, arxiv_id, or title must be provided")


def load_config() -> dict:
    if CONFIG_FILE.exists():
        return json.loads(CONFIG_FILE.read_text())
    return {"feedback_mode": "on", "feedback_auto_collect": True}


def save_config(config: dict):
    CONFIG_FILE.write_text(json.dumps(config, indent=2))


def get_active_project() -> dict | None:
    if not PROJECTS_DIR.exists():
        return None
    for pf in PROJECTS_DIR.glob("*/project.json"):
        try:
            project = json.loads(pf.read_text())
            if project.get("active"):
                return project
        except (json.JSONDecodeError, KeyError):
            continue
    return None


def load_project(name: str) -> dict | None:
    pf = PROJECTS_DIR / name / "project.json"
    if pf.exists():
        return json.loads(pf.read_text())
    return None


def save_project(project: dict):
    name = project["name"]
    proj_dir = PROJECTS_DIR / name
    proj_dir.mkdir(parents=True, exist_ok=True)
    (proj_dir / "project.json").write_text(json.dumps(project, indent=2))


def create_project(name: str, working_directory: str = None,
                   survey_id: str = None, target_venue: str = None) -> dict:
    """Create a new paper project and set it as active."""
    current = get_active_project()
    if current:
        current["active"] = False
        save_project(current)

    project = {
        "name": name,
        "active": True,
        "created": __import__("datetime").date.today().isoformat(),
        "current_phase": 1,
        "phase_name": "survey",
        "phases_completed": [],
        "survey_id": survey_id,
        "target_venue": target_venue,
        "working_directory": working_directory,
        "notebook_url": None,
    }

    proj_dir = PROJECTS_DIR / name
    proj_dir.mkdir(parents=True, exist_ok=True)
    (proj_dir / "drafts").mkdir(exist_ok=True)
    save_project(project)
    return project
