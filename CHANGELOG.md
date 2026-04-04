# Changelog

## 0.2.1 (2026-03-21)

### Eval infrastructure hardening
- Renumbered eval criteria IDs from old 11-phase (P4-*, P10-*, P11-*) to new 8-phase (P01-* through P08-*)
- Added JSON schema validation for criteria files (`eval validate` command)
- Added artifact manifest (`scripts/eval/artifacts.json`) for cross-reference validation
- Added encoding safety (UnicodeDecodeError handling) in file-reading check functions
- Added atomic writes (temp file + os.replace) in save_eval_results
- Capped eval results at 100 entries to prevent unbounded growth
- Deduplicated eval_runner.py — imports shared code from config.py

### Self-optimization safety
- Added Python backup/restore script (`scripts/optimize/backup_manager.py`) for safe prompt mutations
- Registered optimize command in run.py routing

### Testing
- Added 26 unit tests for eval_runner.py covering all check functions, edge cases, and results management

### Fixes
- Fixed `create_project()` phase_name: "survey" → "discover" to match 8-phase naming

## 0.2.0 (2026-03-21)

### Pipeline restructure: 11 → 8 phases
- Merged Survey + Gap + Scout → **Discover** (Phase 1)
- Merged Review + Audit → **Critique** (Phase 6)
- Renamed Venue → **Ship** (Phase 8)
- Pipeline: Discover → Position → Architect → Evaluate → Write → Critique → Refine → Ship

### Phase quality enhancement
- Added Quality Rubric to all phases (3 universal + 2-3 phase-specific dimensions)
- Added Anti-patterns with DON'T/DO INSTEAD examples
- Added Structural Exemplars (domain-agnostic output skeletons)
- Added Failure Recovery scenarios

### Self-optimization infrastructure
- New `/paper eval` command — binary eval criteria per phase (pass/fail quality checks)
- New `/paper optimize` command — autoresearch-style prompt mutation loops
- Eval criteria JSON files for all 8 phases
- Python eval runner (`scripts/eval/eval_runner.py`)

### Fixes
- All paths updated from `paper-skill` to `notebooklm-paper` (later renamed to `paper`)
- Data directory moved to `~/.paper/` (was `~/.notebooklm-paper/`)

## 0.1.0 (2026-03-20)

- Initial release
- 11-phase paper generation pipeline
- Absorbs notebooklm-skill, paper-star-analyzer, academic-paper-search, paper-gap-analyzer
- Cross-cutting systems: acceptance scorecard, claim-evidence chain, comparison matrix
- gstack-style patterns: preamble, guided flow, structured questions, completion status
- Feedback-driven evolution system
