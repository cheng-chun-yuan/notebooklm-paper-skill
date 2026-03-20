# TODOS

## In Progress

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
- `scripts/eval/eval_runner.py` — binary eval runner
- `scripts/eval/criteria/phase-{01..08}.json` — per-phase criteria
- Registered in run.py routing

### Self-Optimization ✓
- `support/optimize.md` — SKILL.md for `/paper optimize`
- Autoresearch-style mutation loop design

### Path Fix ✓
- All paths updated to `~/.claude/skills/notebooklm-paper-skill`

## Remaining

### Cleanup old phase files
- Delete old files: 01-survey.md, 02-gap.md, 03-scout.md, 04-position.md, 05-architect.md, 06-evaluate.md, 07-write.md, 08-review.md, 09-audit.md, 10-refine.md, 11-venue.md
- After verifying new files are complete

### Dogfood test
- Run `/paper` end-to-end on a test topic
- Verify each phase output against rubric dimensions
- Run `/paper eval` to validate eval criteria
