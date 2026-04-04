# TODOS

## Completed

### Pipeline Restructure: 11 → 8 Phases ✓
- Merged Survey + Gap + Scout → Discover (01)
- Merged Review + Audit → Critique (06)
- Renumbered: Position→02, Architect→03, Evaluate→04, Write→05, Refine→07, Ship→08
- Updated SKILL.md routing, progress tracker, guided flow
- Updated README, ARCHITECTURE.md

### Phase Quality Enhancement ✓
- All 8 phases have: Quality Rubric, Anti-patterns, Structural Exemplar, Failure Recovery
- Universal rubric dimensions: Specificity, Traceability, Completeness
- 2-3 phase-specific dimensions per phase

### Eval Infrastructure ✓
- `support/eval.md` — SKILL.md for `/paper eval`
- `scripts/eval/eval_runner.py` — binary eval runner with schema validation
- `scripts/eval/criteria/phase-{01..08}.json` — per-phase criteria (IDs renumbered P01-* through P08-*)
- `scripts/eval/artifacts.json` — artifact manifest for cross-reference validation
- Registered in run.py routing
- JSON schema validation for criteria files (`eval validate` command)
- 26 unit tests in `tests/test_eval_runner.py`

### Self-Optimization ✓
- `support/optimize.md` — SKILL.md for `/paper optimize`
- `scripts/optimize/backup_manager.py` — Python backup/restore for safe mutations
- Autoresearch-style mutation loop design

### Path Fix ✓
- All paths updated to `~/.claude/skills/paper`

### Eng Review Fixes (2026-03-21) ✓
- Eval criteria IDs renumbered from old 11-phase (P4-*, P10-*, P11-*) to new 8-phase (P01-* through P08-*)
- Fixed `create_project()` phase_name: "survey" → "discover" in config.py
- Deduplicated eval_runner.py — imports DATA_DIR, PROJECTS_DIR, get_active_project from config.py
- Added encoding safety (UnicodeDecodeError handling) in file-reading check functions
- Added atomic writes (temp file + os.replace) in save_eval_results
- Capped eval results at 100 entries to prevent unbounded growth
- Old phase files already cleaned (confirmed no remnants of 11-phase files)

## Remaining

### Dogfood test
- Run `/paper` end-to-end on a test topic
- Verify each phase output against rubric dimensions
- Run `/paper eval` to validate eval criteria match actual phase outputs
- Verify artifact manifest matches what phases actually produce
