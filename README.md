# notebooklm-paper

Your AI research advisor. An 8-phase pipeline that guides you from "I have a topic" to "paper submitted" — with acceptance scorecard, claim-evidence tracking, and simulated peer review.

```
Discover → Position → Architect → Evaluate → Write → Critique → Refine → Ship
```

## What it does

### 8-Phase Research Pipeline

| # | Phase | Command | What it does |
|---|-------|---------|-------------|
| 1 | **Discover** | `/paper discover` | Survey literature (arXiv + Semantic Scholar), analyze gaps with 6-question framework, scout cross-domain methods, build field map + acceptance scorecard |
| 2 | **Position** | `/paper position` | Define contribution statement, novelty claims, and differentiation from closest papers |
| 3 | **Architect** | `/paper architect` | Design method/system architecture with component-to-gap mapping |
| 4 | **Evaluate** | `/paper evaluate` | Design experiments, analyze results, validate every claim with evidence strength |
| 5 | **Write** | `/paper write` | Generate full paper draft with claim-evidence guard (refuses unsupported claims) |
| 6 | **Critique** | `/paper critique` | 3 adversarial reviewer personas + 6-category pre-submission audit with readiness score |
| 7 | **Refine** | `/paper refine` | Fix everything flagged by critique, produce v2 draft with changelog |
| 8 | **Ship** | `/paper ship` | Match paper to target venue, extract formatting requirements, submission timeline |

### 3 Cross-Cutting Quality Systems

- **Acceptance Scorecard** (`scorecard.json`) — Built from surveyed papers in Phase 1. Lists venue requirements with frequency weights (0.0–1.0). Calculates acceptance probability.
- **Claim-Evidence Chain** (`claims.json`) — Introduced in Phase 2. Tracks each claim with evidence strength: strong / moderate / weak / unsupported. Write phase refuses unsupported claims.
- **Comparison Matrix** (`matrix.json`) — Tracks papers vs. dimensions. Auto-generates the comparison table for Related Work.

### Self-Optimization

- **`/paper eval`** — Binary eval criteria against phase outputs. Pass/fail quality checks.
- **`/paper optimize`** — Autoresearch-style prompt mutation loops. Keeps improvements, reverts regressions.

### Support Commands

| Command | What it does |
|---------|-------------|
| `/paper` | Guided flow — shows progress and options |
| `/paper search` | Paper search (arXiv + Semantic Scholar) |
| `/paper analyze` | STAR framework analysis of a single paper |
| `/paper store` | NotebookLM notebook management |
| `/paper auth` | NotebookLM authentication setup |
| `/paper eval` | Run quality evals on phase outputs |
| `/paper optimize` | Self-optimize phase prompts |

## Install

**Requirements:** [Claude Code](https://docs.anthropic.com/en/docs/claude-code) + Python 3.11+

```bash
git clone https://github.com/cheng-chun-yuan/notebooklm-paper.git ~/.claude/skills/notebooklm-paper
cd ~/.claude/skills/notebooklm-paper && ./setup
```

Then add to `~/.claude/CLAUDE.md`:

```markdown
## notebooklm-paper

- Available skills: /paper, /paper discover, /paper position, /paper architect, /paper evaluate, /paper write, /paper critique, /paper refine, /paper ship, /paper auth, /paper store, /paper search, /paper analyze, /paper eval, /paper optimize
```

## Quick start

```
/paper
→ Pick "Starting fresh"
→ Give your research topic
→ Follow the guided flow through each phase
```

```
[■■□□□□□□] Phase 2/8 — Position

  ✓ Discover  — 23 papers, 4 gaps, 2 methods scouted
  ► Position  — Defining contribution...
  ○ Architect — Design your method
  ○ Evaluate  — Experiments & results
  ○ Write     — Generate paper draft
  ○ Critique  — Peer review + audit
  ○ Refine    — Fix & polish
  ○ Ship      — Target venue & submit
```

## Design

- **Hybrid architecture** — SKILL.md (brain) + Python scripts (hands)
- **Quality rubrics** — every phase has explicit standards + anti-patterns
- **Binary evals** — automated pass/fail quality measurement
- **Self-optimization** — autoresearch-style prompt improvement loops
- **Backtracking** — non-destructive, all artifacts preserved

Inspired by [gstack](https://github.com/garrytan/gstack) and [autoresearch-skill](https://github.com/olelehmann100kMRR/autoresearch-skill).

See [ARCHITECTURE.md](ARCHITECTURE.md) for details.

## License

MIT
