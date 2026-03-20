# Changelog

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
- All paths updated from `paper-skill` to `notebooklm-paper-skill`
- Data directory moved to `~/.notebooklm-paper-skill/`

## 0.1.0 (2026-03-20)

- Initial release
- 11-phase paper generation pipeline
- Absorbs notebooklm-skill, paper-star-analyzer, academic-paper-search, paper-gap-analyzer
- Cross-cutting systems: acceptance scorecard, claim-evidence chain, comparison matrix
- gstack-style patterns: preamble, guided flow, structured questions, completion status
- Feedback-driven evolution system
