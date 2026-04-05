# paper

Your AI research advisor. An 8-phase pipeline from "I have a topic" to "paper submitted" — with an Obsidian knowledge base, NotebookLM integration, acceptance scorecard, and claim-evidence tracking.

## Install

**Requirements:** [Claude Code](https://docs.anthropic.com/en/docs/claude-code) + Python 3.11+

```bash
git clone https://github.com/cheng-chun-yuan/notebooklm-paper.git ~/.claude/skills/paper
cd ~/.claude/skills/paper && ./setup
```

Add to `~/.claude/CLAUDE.md`:

```markdown
## paper skill

- Available skills: /paper, /paper init, /paper discover, /paper digest, /paper ask, /paper check, /paper position, /paper architect, /paper evaluate, /paper write, /paper critique, /paper refine, /paper ship, /paper auth, /paper store, /paper search, /paper analyze, /paper eval, /paper optimize
```

## Quick Start

```
/paper init
```

Walks you through setup:
1. Research topic and goal
2. Target venue, deadline, page limit
3. Keywords for paper discovery
4. NotebookLM notebook URL (optional)
5. Obsidian vault path (default: `~/.paper/vaults/{project}`)

Creates a `.paper` config file in your working directory and initializes an Obsidian vault with `sources/`, `notes/`, `concepts/`, `questions/`, and `insights/` folders.

**Open the vault folder in Obsidian** to browse your research.

## Usage

### Research & Knowledge Base

| Command | What you're thinking | What it does |
|---------|---------------------|-------------|
| `/paper discover` | "I need to find papers" | Search arXiv + Semantic Scholar, download papers, identify gaps. Auto-ingests to vault `sources/` |
| `/paper digest` | "Let me organize what I know" | Two-pass: reads `sources/`, writes per-paper `notes/` (summary, findings, quotes), then synthesizes cross-paper `concepts/` with wikilinks |
| `/paper ask` | "I have a question" | Q&A against your wiki. Answers auto-filed to `questions/` so explorations accumulate. Also logs NotebookLM conversations |
| `/paper check` | "Am I missing anything?" | Health-check: uncompiled papers, broken links, thin articles, suggested new articles and research questions |

### Paper Writing Pipeline

```
Discover → Position → Architect → Evaluate → Write → Critique → Refine → Ship
```

| # | Phase | Command | What it does |
|---|-------|---------|-------------|
| 1 | **Discover** | `/paper discover` | Survey literature, analyze gaps, scout cross-domain methods, build field map + scorecard |
| 2 | **Position** | `/paper position` | Define contribution, novelty claims, differentiation from closest papers |
| 3 | **Architect** | `/paper architect` | Design method/system with component-to-gap mapping |
| 4 | **Evaluate** | `/paper evaluate` | Design experiments, validate every claim with evidence |
| 5 | **Write** | `/paper write` | Generate full draft with claim-evidence guard (refuses unsupported claims) |
| 6 | **Critique** | `/paper critique` | 3 adversarial reviewers + 6-category audit with readiness score |
| 7 | **Refine** | `/paper refine` | Fix all flagged issues, produce v2 with changelog |
| 8 | **Ship** | `/paper ship` | Match to venue, formatting requirements, submission timeline |

### Quality Systems

- **Acceptance Scorecard** — Venue requirements with frequency weights. Calculates acceptance probability.
- **Claim-Evidence Chain** — Tracks claims with strength ratings. Write phase refuses unsupported claims.
- **Comparison Matrix** — Papers vs. dimensions. Auto-generates Related Work table.

### Other Commands

| Command | What it does |
|---------|-------------|
| `/paper` | Guided menu — shows where you are and what to do next |
| `/paper search` | Search arXiv + Semantic Scholar |
| `/paper analyze` | STAR analysis of a single paper |
| `/paper store` | NotebookLM notebook management |
| `/paper auth` | NotebookLM authentication |
| `/paper eval` | Quality evals on phase outputs |
| `/paper optimize` | Autoresearch-style prompt improvement |

## How It Works

### `.paper` Config

Each research project has a `.paper` file in the working directory:

```yaml
project: agent-identity
topic: "Verifiable credentials for AI agent identity"
goal: "Propose a framework binding agent actions to verifiable identity"
venue: USENIX Security 2027
deadline: 2027-02-01
keywords: [verifiable credentials, agent identity, zero-trust]
vault: ~/.paper/vaults/agent-identity
notebook: https://notebooklm.google.com/notebook/abc123
phase: discover
```

### Obsidian Vault

The vault is your research knowledge base, viewable in Obsidian:

```
vault/
  sources/      ← Original papers (PDFs, web clips)
  notes/        ← Per-paper reading notes (summary, findings, quotes)
  concepts/     ← Cross-paper synthesis articles with wikilinks
  questions/    ← Research Q&A (Claude + NotebookLM conversations)
  insights/     ← Your original ideas and hypotheses
  CATALOG.md    ← AI-readable index (auto-maintained)
  .obsidian/    ← Obsidian config with bookmarks
```

**Workflow:** Papers flow into `sources/` via `/paper discover` or manual drop. `/paper digest` does two passes: first creating per-paper `notes/`, then synthesizing cross-paper `concepts/`. `/paper ask` queries everything and files answers to `questions/`. Original ideas go to `insights/`. `/paper check` finds gaps and suggests improvements.

### Architecture

- **Hybrid** — SKILL.md files (Claude's instructions) + Python scripts (data processing)
- **Quality rubrics** — Every phase has standards, anti-patterns, and failure recovery
- **Binary evals** — Automated pass/fail quality checks per phase
- **Self-optimization** — Prompt mutation loops that keep improvements, revert regressions

See [ARCHITECTURE.md](ARCHITECTURE.md) for details.

## License

MIT
