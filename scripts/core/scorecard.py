#!/usr/bin/env python3
"""Acceptance Scorecard — tracks venue requirements and acceptance probability."""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from config import PROJECTS_DIR, get_active_project


def load_scorecard(project_name: str) -> dict:
    path = PROJECTS_DIR / project_name / "scorecard.json"
    if path.exists():
        return json.loads(path.read_text())
    return {
        "target_venue": None,
        "based_on": 0,
        "requirements": [],
        "acceptance_probability": 0.0,
        "top_risk": None,
    }


def save_scorecard(project_name: str, scorecard: dict):
    path = PROJECTS_DIR / project_name / "scorecard.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(scorecard, indent=2))


def _recalculate(scorecard: dict):
    reqs = scorecard["requirements"]
    if not reqs:
        scorecard["acceptance_probability"] = 0.0
        scorecard["top_risk"] = None
        return
    met = sum(1 for r in reqs if r["status"] == "met")
    scorecard["acceptance_probability"] = round(met / len(reqs), 2)
    missing = [r for r in reqs if r["status"] == "missing"]
    if missing:
        missing.sort(key=lambda r: r["frequency"], reverse=True)
        scorecard["top_risk"] = missing[0]["name"]
    else:
        scorecard["top_risk"] = None


def add_requirement(project_name: str, name: str, frequency: float):
    sc = load_scorecard(project_name)
    sc["requirements"].append({
        "name": name,
        "frequency": frequency,
        "status": "missing",
        "phase_filled": None,
    })
    _recalculate(sc)
    save_scorecard(project_name, sc)
    print(f"Added requirement: {name} (frequency={frequency})")


def update_requirement(project_name: str, name: str, status: str, phase: str):
    sc = load_scorecard(project_name)
    for req in sc["requirements"]:
        if req["name"] == name:
            req["status"] = status
            req["phase_filled"] = phase
            break
    else:
        print(f"Requirement not found: {name}")
        sys.exit(1)
    _recalculate(sc)
    save_scorecard(project_name, sc)
    print(f"Updated '{name}' -> {status} (phase: {phase})")


def show_scorecard(project_name: str):
    sc = load_scorecard(project_name)
    print(f"\n=== Acceptance Scorecard: {project_name} ===")
    print(f"Target venue: {sc['target_venue'] or '(not set)'}")
    print(f"Based on: {sc['based_on']} papers")
    print(f"Acceptance probability: {sc['acceptance_probability']:.0%}")
    print(f"Top risk: {sc['top_risk'] or '(none)'}")
    print()
    if sc["requirements"]:
        for r in sc["requirements"]:
            icon = {"met": "[+]", "planned": "[~]", "missing": "[-]"}.get(r["status"], "[?]")
            print(f"  {icon} {r['name']} (freq={r['frequency']}, phase={r['phase_filled'] or '-'})")
    else:
        print("  (no requirements)")
    print()


def main():
    parser = argparse.ArgumentParser(description="Acceptance Scorecard")
    sub = parser.add_subparsers(dest="command")

    p_show = sub.add_parser("show", help="Show scorecard")
    p_show.add_argument("--project", default=None)

    p_add = sub.add_parser("add", help="Add requirement")
    p_add.add_argument("name", help="Requirement name")
    p_add.add_argument("frequency", type=float, help="How often required (0-1)")
    p_add.add_argument("--project", default=None)

    p_update = sub.add_parser("update", help="Update requirement status")
    p_update.add_argument("name", help="Requirement name")
    p_update.add_argument("status", choices=["missing", "met", "planned"])
    p_update.add_argument("phase", help="Phase where filled")
    p_update.add_argument("--project", default=None)

    args = parser.parse_args()

    # Resolve project name
    project_name = getattr(args, "project", None)
    if not project_name:
        active = get_active_project()
        if not active:
            print("No active project. Specify --project or create one.")
            sys.exit(1)
        project_name = active["name"]

    if args.command == "show":
        show_scorecard(project_name)
    elif args.command == "add":
        add_requirement(project_name, args.name, args.frequency)
    elif args.command == "update":
        update_requirement(project_name, args.name, args.status, args.phase)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
