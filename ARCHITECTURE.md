# Architecture

## Why hybrid stack

SKILL.md files are the "brain" — Claude reads them as instructions for how to guide the user through each phase. Python scripts are the "hands" — they handle data processing (API calls, file I/O, JSON state management).

Phases that require creative reasoning (Position, Architect, Write, Review, Audit, Refine, Venue) are SKILL.md-only — Claude IS the engine. Phases that need external data (Survey, Gap, Scout, Evaluate) have Python scripts backing them.

## Why global storage with project linking

Papers are reusable across projects. A paper analyzed for project A might be relevant to project B. `~/.paper-skill/` is the research database. Each project gets its own directory under `~/.paper-skill/projects/{name}/` with phase artifacts, cross-cutting JSON files, and drafts.

Project-local linking: when working in a project directory, `RESEARCH_SYNTHESIS.md` is generated there (committed to git), and `.paper-skill/project.json` links back to the global project (gitignored).

## Why 11 phases

Maps to the real doctoral research lifecycle:
1. Survey — understand what exists
2. Gap — find what's missing
3. Scout — find transferable methods from other domains
4. Position — define your contribution
5. Architect — design your method
6. Evaluate — prove it works
7. Write — put it on paper
8. Review — simulate peer review
9. Audit — advisor's honest check
10. Refine — fix everything
11. Venue — pick where to submit

Fewer phases = skipping critical steps (researchers who skip gap analysis write incremental papers). More = unnecessary granularity.

## Why cross-cutting systems

- **Acceptance Scorecard**: Built from surveyed papers. Prevents "write the paper then discover it won't be accepted." Every phase checks against it.
- **Claim-Evidence Chain**: Top rejection reason is unsupported claims. Tracking claims from Position through Write prevents this.
- **Comparison Matrix**: The most tedious table in any paper. Auto-built from survey/gap/scout phases.

## Why feedback loop

Skills improve through usage. Tracking which phases get low ratings or cause backtracks reveals where the guidance is weakest. This feeds into version updates via git.
