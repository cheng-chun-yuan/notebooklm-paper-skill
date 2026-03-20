#!/usr/bin/env python3
"""Claim-Evidence Chain — tracks claims and their supporting evidence."""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from config import PROJECTS_DIR, get_active_project


def load_claims(project_name: str) -> dict:
    path = PROJECTS_DIR / project_name / "claims.json"
    if path.exists():
        return json.loads(path.read_text())
    return {"claims": []}


def save_claims(project_name: str, data: dict):
    path = PROJECTS_DIR / project_name / "claims.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2))


def add_claim(project_name: str, text: str, phase: str) -> str:
    data = load_claims(project_name)
    claim_id = f"C{len(data['claims']) + 1}"
    data["claims"].append({
        "id": claim_id,
        "text": text,
        "evidence": None,
        "strength": "unsupported",
        "phase_added": phase,
        "phase_validated": None,
    })
    save_claims(project_name, data)
    print(f"Added claim {claim_id}: {text}")
    return claim_id


def validate_claim(project_name: str, claim_id: str, evidence: str,
                   strength: str, phase: str):
    data = load_claims(project_name)
    for claim in data["claims"]:
        if claim["id"] == claim_id:
            claim["evidence"] = evidence
            claim["strength"] = strength
            claim["phase_validated"] = phase
            break
    else:
        print(f"Claim not found: {claim_id}")
        sys.exit(1)
    save_claims(project_name, data)
    print(f"Validated {claim_id} -> {strength}")


def show_claims(project_name: str):
    data = load_claims(project_name)
    print(f"\n=== Claim-Evidence Chain: {project_name} ===\n")
    if not data["claims"]:
        print("  (no claims)")
        print()
        return
    icons = {
        "strong": "[+++]",
        "moderate": "[++ ]",
        "weak": "[+  ]",
        "unsupported": "[   ]",
    }
    for c in data["claims"]:
        icon = icons.get(c["strength"], "[?  ]")
        print(f"  {icon} {c['id']}: {c['text']}")
        print(f"        strength={c['strength']}, added={c['phase_added']}, validated={c['phase_validated'] or '-'}")
        if c["evidence"]:
            print(f"        evidence: {c['evidence']}")
    print()


def main():
    parser = argparse.ArgumentParser(description="Claim-Evidence Chain")
    sub = parser.add_subparsers(dest="command")

    p_show = sub.add_parser("show", help="Show claims")
    p_show.add_argument("--project", default=None)

    p_add = sub.add_parser("add", help="Add a claim")
    p_add.add_argument("text", help="Claim text")
    p_add.add_argument("phase", help="Phase when claim was added")
    p_add.add_argument("--project", default=None)

    p_val = sub.add_parser("validate", help="Validate a claim with evidence")
    p_val.add_argument("claim_id", help="Claim ID (e.g. C1)")
    p_val.add_argument("evidence", help="Evidence description")
    p_val.add_argument("strength", choices=["strong", "moderate", "weak", "unsupported"])
    p_val.add_argument("phase", help="Phase when validated")
    p_val.add_argument("--project", default=None)

    args = parser.parse_args()

    project_name = getattr(args, "project", None)
    if not project_name:
        active = get_active_project()
        if not active:
            print("No active project. Specify --project or create one.")
            sys.exit(1)
        project_name = active["name"]

    if args.command == "show":
        show_claims(project_name)
    elif args.command == "add":
        add_claim(project_name, args.text, args.phase)
    elif args.command == "validate":
        validate_claim(project_name, args.claim_id, args.evidence,
                       args.strength, args.phase)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
