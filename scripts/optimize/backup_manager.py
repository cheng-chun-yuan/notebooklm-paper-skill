#!/usr/bin/env python3
"""Backup and restore manager for SKILL.md phase files during optimization."""

import sys
import shutil
import difflib
from datetime import datetime
from pathlib import Path

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

PHASES_DIR = Path.home() / ".claude" / "skills" / "notebooklm-paper-skill" / "phases"
BACKUP_DIR = Path.home() / ".notebooklm-paper-skill" / "optimize-backups"


def resolve_phase(phase_input: str) -> tuple[str, Path]:
    """Resolve a phase number (e.g. '5' or '05') to its padded key and file path."""
    padded = phase_input.zfill(2)
    if padded not in PHASE_NAMES:
        print(f"Error: Unknown phase '{phase_input}'. Valid phases: {', '.join(PHASE_NAMES.keys())}")
        sys.exit(1)
    name = PHASE_NAMES[padded]
    phase_file = PHASES_DIR / f"{padded}-{name}.md"
    if not phase_file.exists():
        print(f"Error: Phase file not found: {phase_file}")
        sys.exit(1)
    return padded, phase_file


def get_backup_dir(padded: str) -> Path:
    return BACKUP_DIR / padded


def cmd_backup(phase_input: str) -> None:
    padded, phase_file = resolve_phase(phase_input)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    dest_dir = get_backup_dir(padded) / timestamp
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest_file = dest_dir / phase_file.name
    shutil.copy2(phase_file, dest_file)
    print(f"Backed up phase {padded}-{PHASE_NAMES[padded]}")
    print(f"  Source: {phase_file}")
    print(f"  Backup: {dest_file}")


def cmd_list(phase_input: str) -> None:
    padded, _ = resolve_phase(phase_input)
    backup_dir = get_backup_dir(padded)
    if not backup_dir.exists():
        print(f"No backups found for phase {padded}-{PHASE_NAMES[padded]}")
        return
    timestamps = sorted(
        [d.name for d in backup_dir.iterdir() if d.is_dir()], reverse=True
    )
    if not timestamps:
        print(f"No backups found for phase {padded}-{PHASE_NAMES[padded]}")
        return
    print(f"Backups for phase {padded}-{PHASE_NAMES[padded]} ({len(timestamps)} total):")
    for ts in timestamps:
        print(f"  {ts}")


def find_latest_backup(padded: str) -> Path | None:
    backup_dir = get_backup_dir(padded)
    if not backup_dir.exists():
        return None
    timestamps = sorted([d.name for d in backup_dir.iterdir() if d.is_dir()])
    if not timestamps:
        return None
    return backup_dir / timestamps[-1]


def cmd_restore(phase_input: str, timestamp: str | None = None) -> None:
    padded, phase_file = resolve_phase(phase_input)
    if timestamp:
        backup_ts_dir = get_backup_dir(padded) / timestamp
        if not backup_ts_dir.exists():
            print(f"Error: No backup found at timestamp '{timestamp}' for phase {padded}")
            sys.exit(1)
    else:
        backup_ts_dir = find_latest_backup(padded)
        if backup_ts_dir is None:
            print(f"Error: No backups found for phase {padded}-{PHASE_NAMES[padded]}")
            sys.exit(1)
    backup_file = backup_ts_dir / phase_file.name
    if not backup_file.exists():
        print(f"Error: Backup file not found: {backup_file}")
        sys.exit(1)
    shutil.copy2(backup_file, phase_file)
    print(f"Restored phase {padded}-{PHASE_NAMES[padded]} from {backup_ts_dir.name}")
    print(f"  Backup:  {backup_file}")
    print(f"  Restored: {phase_file}")


def cmd_diff(phase_input: str, timestamp: str | None = None) -> None:
    padded, phase_file = resolve_phase(phase_input)
    if timestamp:
        backup_ts_dir = get_backup_dir(padded) / timestamp
        if not backup_ts_dir.exists():
            print(f"Error: No backup found at timestamp '{timestamp}' for phase {padded}")
            sys.exit(1)
    else:
        backup_ts_dir = find_latest_backup(padded)
        if backup_ts_dir is None:
            print(f"Error: No backups found for phase {padded}-{PHASE_NAMES[padded]}")
            sys.exit(1)
    backup_file = backup_ts_dir / phase_file.name
    if not backup_file.exists():
        print(f"Error: Backup file not found: {backup_file}")
        sys.exit(1)

    backup_lines = backup_file.read_text().splitlines(keepends=True)
    current_lines = phase_file.read_text().splitlines(keepends=True)

    diff = difflib.unified_diff(
        backup_lines,
        current_lines,
        fromfile=f"backup ({backup_ts_dir.name})",
        tofile="current",
    )
    diff_text = "".join(diff)
    if not diff_text:
        print(f"No differences between backup ({backup_ts_dir.name}) and current for phase {padded}")
    else:
        print(diff_text)


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: backup_manager.py <command> <phase_number> [timestamp]")
        print("Commands: backup, restore, list, diff")
        print(f"Phases: {', '.join(f'{k} ({v})' for k, v in PHASE_NAMES.items())}")
        sys.exit(1)

    command = sys.argv[1]
    if command not in ("backup", "restore", "list", "diff"):
        print(f"Unknown command: {command}")
        print("Available commands: backup, restore, list, diff")
        sys.exit(1)

    if len(sys.argv) < 3:
        print(f"Error: '{command}' requires a phase number.")
        sys.exit(1)

    phase = sys.argv[2]
    timestamp = sys.argv[3] if len(sys.argv) > 3 else None

    if command == "backup":
        cmd_backup(phase)
    elif command == "restore":
        cmd_restore(phase, timestamp)
    elif command == "list":
        cmd_list(phase)
    elif command == "diff":
        cmd_diff(phase, timestamp)


if __name__ == "__main__":
    main()
