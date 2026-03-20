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
import sys
from datetime import datetime, timezone
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
CRITERIA_DIR = SCRIPT_DIR / "criteria"
SKILL_DIR = SCRIPT_DIR.parent.parent
DATA_DIR = Path.home() / ".notebooklm-paper-skill"
PROJECTS_DIR = DATA_DIR / "projects"

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
    if not PROJECTS_DIR.exists():
        return None
    for pf in PROJECTS_DIR.glob("*/project.json"):
        try:
            project = json.loads(pf.read_text())
            if project.get("active"):
                return pf.parent
        except (json.JSONDecodeError, KeyError):
            continue
    return None


def load_criteria(phase: str) -> list[dict]:
    criteria_file = CRITERIA_DIR / f"phase-{phase}.json"
    if not criteria_file.exists():
        print(f"No criteria file for phase {phase}: {criteria_file}")
        return []
    return json.loads(criteria_file.read_text())


def check_file_exists(project_dir: Path, filepath: str) -> bool:
    return (project_dir / filepath).exists()


def check_file_nonempty(project_dir: Path, filepath: str) -> bool:
    f = project_dir / filepath
    return f.exists() and f.stat().st_size > 0


def check_file_contains(project_dir: Path, filepath: str, pattern: str) -> bool:
    f = project_dir / filepath
    if not f.exists():
        return False
    return pattern.lower() in f.read_text().lower()


def check_file_section_count(project_dir: Path, filepath: str,
                             heading_prefix: str, min_count: int) -> bool:
    f = project_dir / filepath
    if not f.exists():
        return False
    content = f.read_text()
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
    words = len(f.read_text().split())
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
    results_file.write_text(json.dumps(all_results, indent=2))


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


def main():
    if len(sys.argv) < 2:
        print("Usage: eval_runner.py <run|show|results> [phase]")
        sys.exit(1)

    cmd = sys.argv[1]
    args = sys.argv[2:]

    if cmd == "run":
        cmd_run(args)
    elif cmd == "show":
        cmd_show(args)
    elif cmd == "results":
        cmd_results(args)
    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)


if __name__ == "__main__":
    main()
