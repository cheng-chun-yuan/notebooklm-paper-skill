#!/usr/bin/env python3
"""Comparison Matrix — tracks how papers compare across dimensions."""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from config import PROJECTS_DIR, get_active_project


def load_matrix(project_name: str) -> dict:
    path = PROJECTS_DIR / project_name / "matrix.json"
    if path.exists():
        return json.loads(path.read_text())
    return {"dimensions": [], "papers": {}}


def save_matrix(project_name: str, data: dict):
    path = PROJECTS_DIR / project_name / "matrix.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2))


def add_dimension(project_name: str, dimension: str):
    data = load_matrix(project_name)
    if dimension in data["dimensions"]:
        print(f"Dimension already exists: {dimension}")
        return
    data["dimensions"].append(dimension)
    # Extend existing papers with None for the new dimension
    for paper in data["papers"]:
        data["papers"][paper].append(None)
    save_matrix(project_name, data)
    print(f"Added dimension: {dimension}")


def add_paper(project_name: str, paper: str, values: list = None):
    data = load_matrix(project_name)
    if paper in data["papers"]:
        print(f"Paper already exists: {paper}")
        return
    if values is None:
        values = [None] * len(data["dimensions"])
    data["papers"][paper] = values
    save_matrix(project_name, data)
    print(f"Added paper: {paper}")


def set_value(project_name: str, paper: str, dimension: str, value: bool):
    data = load_matrix(project_name)
    if paper not in data["papers"]:
        print(f"Paper not found: {paper}")
        sys.exit(1)
    if dimension not in data["dimensions"]:
        print(f"Dimension not found: {dimension}")
        sys.exit(1)
    idx = data["dimensions"].index(dimension)
    data["papers"][paper][idx] = value
    save_matrix(project_name, data)
    print(f"Set {paper} x {dimension} = {value}")


def show_matrix(project_name: str):
    data = load_matrix(project_name)
    dims = data["dimensions"]
    papers = data["papers"]

    print(f"\n=== Comparison Matrix: {project_name} ===\n")
    if not dims:
        print("  (no dimensions)")
        print()
        return

    # Calculate column widths
    paper_col_w = max((len(p) for p in papers), default=5)
    paper_col_w = max(paper_col_w, 5)
    dim_col_w = max(len(d) for d in dims)
    dim_col_w = max(dim_col_w, 3)

    # Header
    header = f"  {'Paper':<{paper_col_w}}"
    for d in dims:
        header += f" | {d:<{dim_col_w}}"
    print(header)
    print("  " + "-" * (len(header) - 2))

    # Rows
    for paper, vals in papers.items():
        row = f"  {paper:<{paper_col_w}}"
        for v in vals:
            if v is True:
                cell = "Y"
            elif v is False:
                cell = "N"
            else:
                cell = "-"
            row += f" | {cell:<{dim_col_w}}"
        print(row)
    print()


def main():
    parser = argparse.ArgumentParser(description="Comparison Matrix")
    sub = parser.add_subparsers(dest="command")

    p_show = sub.add_parser("show", help="Show matrix")
    p_show.add_argument("--project", default=None)

    p_dim = sub.add_parser("add-dim", help="Add a dimension")
    p_dim.add_argument("dimension", help="Dimension name")
    p_dim.add_argument("--project", default=None)

    p_paper = sub.add_parser("add-paper", help="Add a paper")
    p_paper.add_argument("paper", help="Paper name")
    p_paper.add_argument("--project", default=None)

    p_set = sub.add_parser("set", help="Set a value")
    p_set.add_argument("paper", help="Paper name")
    p_set.add_argument("dimension", help="Dimension name")
    p_set.add_argument("value", help="Value (true/false)")
    p_set.add_argument("--project", default=None)

    args = parser.parse_args()

    project_name = getattr(args, "project", None)
    if not project_name:
        active = get_active_project()
        if not active:
            print("No active project. Specify --project or create one.")
            sys.exit(1)
        project_name = active["name"]

    if args.command == "show":
        show_matrix(project_name)
    elif args.command == "add-dim":
        add_dimension(project_name, args.dimension)
    elif args.command == "add-paper":
        add_paper(project_name, args.paper)
    elif args.command == "set":
        value = args.value.lower() in ("true", "1", "yes", "y")
        set_value(project_name, args.paper, args.dimension, value)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
