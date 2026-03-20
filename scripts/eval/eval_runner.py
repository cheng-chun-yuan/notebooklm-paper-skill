#!/usr/bin/env python3
"""Binary eval runner for paper-skill phases.

Loads per-phase criteria from JSON, evaluates phase output artifacts,
and reports pass/fail results.

Usage:
    python eval_runner.py run [--phase PHASE]     # Run evals for a phase (or all)
    python eval_runner.py show [--phase PHASE]    # Show criteria for a phase
    python eval_runner.py results [--phase PHASE] # Show last eval results
"""

import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

# Ensure project root is on sys.path for scripts.config import
_PROJECT_ROOT = Path(__file__).parent.parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from scripts.config import DATA_DIR, PROJECTS_DIR, SKILL_DIR, get_active_project

SCRIPT_DIR = Path(__file__).parent
CRITERIA_DIR = SCRIPT_DIR / "criteria"

# Phase name mapping
PHASE_NAMES = {
    "01": "discover",
    "02": "position",
    "03": "architect",
    "04": "evaluate",
    "05": "write",
    "06": "critique",
    "07": "refine",
    "08": "ship",
}

# Artifact files each phase produces
PHASE_ARTIFACTS = {
    "01": ["field-map.md", "gaps.md"],
    "02": ["position.md"],
    "03": ["architecture.md"],
    "04": ["evaluation.md"],
    "05": ["drafts/v1-draft.md"],
    "06": ["critique-report.md"],
    "07": ["drafts/v2-refined.md", "drafts/v2-changelog.md"],
    "08": ["venue-recommendation.md"],
}


def get_active_project_dir() -> Path | None:
    project = get_active_project()
    if not project:
        return None
    return PROJECTS_DIR / project["name"]


def load_criteria(phase: str) -> list[dict]:
    criteria_file = CRITERIA_DIR / f"phase-{phase}.json"
    if not criteria_file.exists():
        print(f"No criteria file for phase {phase}: {criteria_file}")
        return []

    criteria = json.loads(criteria_file.read_text())

    # Validate on load and print warnings (non-blocking)
    errors = validate_criteria_file(phase)
    if errors:
        print(f"WARNING: Validation issues in phase-{phase}.json:")
        for err in errors:
            print(f"  - {err}")

    return criteria


def check_file_exists(project_dir: Path, filepath: str) -> bool:
    return (project_dir / filepath).exists()


def check_file_nonempty(project_dir: Path, filepath: str) -> bool:
    f = project_dir / filepath
    return f.exists() and f.stat().st_size > 0


def check_file_contains(project_dir: Path, filepath: str, pattern: str) -> bool:
    f = project_dir / filepath
    if not f.exists():
        return False
    try:
        return pattern.lower() in f.read_text().lower()
    except UnicodeDecodeError:
        return False


def check_file_section_count(project_dir: Path, filepath: str,
                             heading_prefix: str, min_count: int) -> bool:
    f = project_dir / filepath
    if not f.exists():
        return False
    try:
        content = f.read_text()
    except UnicodeDecodeError:
        return False
    count = content.count(heading_prefix)
    return count >= min_count


def check_json_field(project_dir: Path, filepath: str,
                     field: str, min_items: int = 1) -> bool:
    f = project_dir / filepath
    if not f.exists():
        return False
    try:
        data = json.loads(f.read_text())
        if isinstance(data, dict):
            items = data.get(field, [])
            return len(items) >= min_items if isinstance(items, list) else bool(items)
        return False
    except (json.JSONDecodeError, KeyError):
        return False


def check_word_count(project_dir: Path, filepath: str,
                     min_words: int, max_words: int = 0) -> bool:
    f = project_dir / filepath
    if not f.exists():
        return False
    try:
        words = len(f.read_text().split())
    except UnicodeDecodeError:
        return False
    if max_words > 0:
        return min_words <= words <= max_words
    return words >= min_words


# Eval check dispatcher
CHECK_FUNCTIONS = {
    "file_exists": check_file_exists,
    "file_nonempty": check_file_nonempty,
    "file_contains": check_file_contains,
    "file_section_count": check_file_section_count,
    "json_field": check_json_field,
    "word_count": check_word_count,
}

# JSON schema for criteria validation
CRITERIA_SCHEMA = {
    "required_fields": ["id", "description", "check", "params"],
    "id_pattern": r"^P\d{2}-\d{2}$",
    "valid_checks": list(CHECK_FUNCTIONS.keys()),
    "required_params": {
        "file_exists": ["filepath"],
        "file_nonempty": ["filepath"],
        "file_contains": ["filepath", "pattern"],
        "file_section_count": ["filepath", "heading_prefix", "min_count"],
        "json_field": ["filepath", "field"],
        "word_count": ["filepath", "min_words"],
    },
}


def validate_criterion(criterion: dict) -> list[str]:
    """Validate a single criterion dict. Returns list of error messages (empty if valid)."""
    errors: list[str] = []

    # Check required fields
    for field in CRITERIA_SCHEMA["required_fields"]:
        if field not in criterion:
            errors.append(f"Missing required field: '{field}'")

    # If id present, check pattern
    cid = criterion.get("id", "")
    if cid and not re.match(CRITERIA_SCHEMA["id_pattern"], cid):
        errors.append(f"Invalid id format '{cid}': must match {CRITERIA_SCHEMA['id_pattern']}")

    # If description present, check non-empty
    desc = criterion.get("description", "")
    if "description" in criterion and not desc.strip():
        errors.append("Description must be a non-empty string")

    # Check check type is known
    check_type = criterion.get("check", "")
    if check_type and check_type not in CHECK_FUNCTIONS:
        errors.append(f"Unknown check type: '{check_type}'")

    # Validate params has required keys for the check type
    params = criterion.get("params")
    if params is not None and check_type in CRITERIA_SCHEMA["required_params"]:
        required_keys = CRITERIA_SCHEMA["required_params"][check_type]
        for key in required_keys:
            if key not in params:
                errors.append(f"Check '{check_type}' requires param '{key}'")

    return errors


def validate_criteria_file(phase: str) -> list[str]:
    """Load a criteria JSON file for a phase and validate every criterion.
    Returns a list of error messages (empty if all valid)."""
    criteria_file = CRITERIA_DIR / f"phase-{phase}.json"
    errors: list[str] = []

    if not criteria_file.exists():
        errors.append(f"Criteria file not found: {criteria_file}")
        return errors

    try:
        criteria = json.loads(criteria_file.read_text())
    except json.JSONDecodeError as e:
        errors.append(f"Invalid JSON in {criteria_file}: {e}")
        return errors

    if not isinstance(criteria, list):
        errors.append(f"Criteria file must contain a JSON array: {criteria_file}")
        return errors

    for i, criterion in enumerate(criteria):
        criterion_errors = validate_criterion(criterion)
        for err in criterion_errors:
            cid = criterion.get("id", f"index {i}")
            errors.append(f"[{cid}] {err}")

    return errors


def run_criterion(project_dir: Path, criterion: dict) -> dict:
    cid = criterion["id"]
    description = criterion["description"]
    check_type = criterion["check"]
    params = criterion.get("params", {})

    check_fn = CHECK_FUNCTIONS.get(check_type)
    if not check_fn:
        return {
            "id": cid,
            "description": description,
            "pass": False,
            "detail": f"Unknown check type: {check_type}",
        }

    try:
        result = check_fn(project_dir, **params)
        return {
            "id": cid,
            "description": description,
            "pass": result,
            "detail": None if result else f"Check '{check_type}' failed with params {params}",
        }
    except Exception as e:
        return {
            "id": cid,
            "description": description,
            "pass": False,
            "detail": str(e),
        }


def run_phase_eval(phase: str, project_dir: Path) -> dict:
    criteria = load_criteria(phase)
    if not criteria:
        return {"phase": phase, "error": "No criteria found"}

    results = [run_criterion(project_dir, c) for c in criteria]
    passed = sum(1 for r in results if r["pass"])
    total = len(results)

    return {
        "phase": PHASE_NAMES.get(phase, phase),
        "phase_number": phase,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "criteria": results,
        "score": f"{passed}/{total}",
        "pass_rate": round(passed / total * 100, 1) if total > 0 else 0,
    }


def save_eval_results(project_dir: Path, eval_result: dict):
    results_file = project_dir / "eval-results.json"
    if results_file.exists():
        all_results = json.loads(results_file.read_text())
    else:
        all_results = []

    all_results.append(eval_result)
    all_results = all_results[-100:]

    tmp_file = results_file.with_suffix('.tmp')
    tmp_file.write_text(json.dumps(all_results, indent=2))
    os.replace(tmp_file, results_file)


def cmd_run(args):
    project_dir = get_active_project_dir()
    if not project_dir:
        print("No active project. Create one with /paper first.")
        sys.exit(1)

    phase = args[0] if args else None

    if phase:
        phases = [phase.zfill(2)]
    else:
        phases = sorted(PHASE_NAMES.keys())

    print(f"Project: {project_dir.name}")
    print(f"Evaluating phases: {', '.join(PHASE_NAMES[p] for p in phases)}")
    print()

    for p in phases:
        # Check if phase artifacts exist
        artifacts = PHASE_ARTIFACTS.get(p, [])
        has_artifacts = any(check_file_exists(project_dir, a) for a in artifacts)
        if not has_artifacts:
            print(f"Phase {p} ({PHASE_NAMES[p]}): SKIPPED — no artifacts found")
            continue

        result = run_phase_eval(p, project_dir)
        if "error" in result:
            print(f"Phase {p} ({PHASE_NAMES[p]}): ERROR — {result['error']}")
            continue

        save_eval_results(project_dir, result)

        # Display results
        print(f"Phase {p} ({PHASE_NAMES[p]}): {result['score']} ({result['pass_rate']}%)")
        for c in result["criteria"]:
            status = "PASS" if c["pass"] else "FAIL"
            print(f"  [{status}] {c['id']}: {c['description']}")
            if c["detail"]:
                print(f"         {c['detail']}")
        print()


def cmd_show(args):
    phase = args[0].zfill(2) if args else None
    if phase:
        phases = [phase]
    else:
        phases = sorted(PHASE_NAMES.keys())

    for p in phases:
        criteria = load_criteria(p)
        if not criteria:
            print(f"Phase {p} ({PHASE_NAMES.get(p, '?')}): No criteria defined")
            continue

        print(f"Phase {p} ({PHASE_NAMES[p]}): {len(criteria)} criteria")
        for c in criteria:
            print(f"  {c['id']}: {c['description']} [{c['check']}]")
        print()


def cmd_results(args):
    project_dir = get_active_project_dir()
    if not project_dir:
        print("No active project.")
        sys.exit(1)

    results_file = project_dir / "eval-results.json"
    if not results_file.exists():
        print("No eval results yet. Run: /paper eval")
        sys.exit(0)

    all_results = json.loads(results_file.read_text())
    phase = args[0].zfill(2) if args else None

    for r in all_results:
        if phase and r.get("phase_number") != phase:
            continue
        print(f"{r['timestamp']} — Phase {r.get('phase_number', '?')} ({r['phase']}): "
              f"{r['score']} ({r['pass_rate']}%)")
        for c in r.get("criteria", []):
            status = "PASS" if c["pass"] else "FAIL"
            print(f"  [{status}] {c['id']}: {c['description']}")


def cmd_validate(args):
    """Validate one or all criteria files and print errors."""
    if args:
        phases = [args[0].zfill(2)]
    else:
        phases = sorted(PHASE_NAMES.keys())

    total_errors = 0
    for p in phases:
        errors = validate_criteria_file(p)
        phase_name = PHASE_NAMES.get(p, "?")
        if errors:
            print(f"Phase {p} ({phase_name}): {len(errors)} error(s)")
            for err in errors:
                print(f"  - {err}")
            total_errors += len(errors)
        else:
            print(f"Phase {p} ({phase_name}): OK")

    print()
    if total_errors:
        print(f"Total: {total_errors} validation error(s)")
        sys.exit(1)
    else:
        print("All criteria files valid.")


def main():
    if len(sys.argv) < 2:
        print("Usage: eval_runner.py <run|show|results|validate> [phase]")
        sys.exit(1)

    cmd = sys.argv[1]
    args = sys.argv[2:]

    if cmd == "run":
        cmd_run(args)
    elif cmd == "show":
        cmd_show(args)
    elif cmd == "results":
        cmd_results(args)
    elif cmd == "validate":
        cmd_validate(args)
    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)


if __name__ == "__main__":
    main()
