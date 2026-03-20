# Architecture

## Why hybrid stack

SKILL.md files are the "brain" — Claude reads them as instructions for how to guide the user through each phase. Python scripts are the "hands" — they handle data processing (API calls, file I/O, JSON state management).

Phases that require creative reasoning (Position, Architect, Write, Critique, Refine, Ship) are SKILL.md-only — Claude IS the engine. Phases that need external data (Discover, Evaluate) have Python scripts backing them.

## Why global storage with project linking

Papers are reusable across projects. A paper analyzed for project A might be relevant to project B. `~/.notebooklm-paper/` is the research database. Each project gets its own directory under `~/.notebooklm-paper/projects/{name}/` with phase artifacts, cross-cutting JSON files, and drafts.

Project-local linking: when working in a project directory, `RESEARCH_SYNTHESIS.md` is generated there (committed to git), and `.notebooklm-paper/project.json` links back to the global project (gitignored).

## Why 8 phases

Maps to how PhD students actually think about research:

1. **Discover** — understand what exists, find what's missing, scout methods (Survey + Gap + Scout merged — all are "understanding the landscape")
2. **Position** — define your contribution
3. **Architect** — design your method
4. **Evaluate** — prove it works
5. **Write** — put it on paper
6. **Critique** — stress-test the draft (Review + Audit merged — both assess draft quality from different angles)
7. **Refine** — fix everything
8. **Ship** — pick where to submit

Previously 11 phases. Merged Survey+Gap+Scout→Discover and Review+Audit→Critique because these always ran sequentially and represent the same cognitive task from the researcher's perspective.

## Why cross-cutting systems

- **Acceptance Scorecard**: Built from surveyed papers. Prevents "write the paper then discover it won't be accepted." Every phase checks against it.
- **Claim-Evidence Chain**: Top rejection reason is unsupported claims. Tracking claims from Position through Write prevents this.
- **Comparison Matrix**: The most tedious table in any paper. Auto-built from discover/position phases.

## Why self-optimization

Each phase has:
- **Quality Rubric** — dimensions of excellence (specificity, traceability, completeness + phase-specific)
- **Anti-patterns** — common failure modes with DON'T/DO INSTEAD examples
- **Structural Exemplar** — domain-agnostic output skeleton
- **Failure Recovery** — what to do when output is weak

Binary eval criteria (`/paper eval`) measure phase output quality. `/paper optimize` runs autoresearch-style mutation loops to improve phase prompts automatically.

## Why feedback loop

Skills improve through usage. Tracking which phases get low ratings or cause backtracks reveals where the guidance is weakest. This feeds into version updates via git and into the self-optimization loop.
