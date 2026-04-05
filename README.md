# paper

Your AI research advisor. An 8-phase pipeline from "I have a topic" to "paper submitted" — with an Obsidian knowledge base, NotebookLM integration, acceptance scorecard, and claim-evidence tracking.

## Install

**Requirements:** [Claude Code](https://docs.anthropic.com/en/docs/claude-code) + Python 3.11+ + [Obsidian](https://obsidian.md/) (free)

```bash
# 1. Clone the skill
git clone https://github.com/cheng-chun-yuan/notebooklm-paper.git ~/.claude/skills/paper

# 2. Install dependencies
cd ~/.claude/skills/paper && ./setup

# 3. (Optional) Set up NotebookLM — opens browser for Google login
/paper auth setup
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

1. **Research topic** — "Verifiable credentials for AI agent identity"
2. **Goal** — "Propose a framework binding agent actions to verifiable identity"
3. **Target venue** — Conference/journal name, deadline, page limit (or "not sure yet")
4. **Keywords** — For guiding paper discovery
5. **NotebookLM** — Paste notebook URL (or skip)
6. **Vault path** — Where to store your research (default: `~/.paper/vaults/{project}`)

This creates:
- `.paper` config file in your working directory
- Obsidian vault with 5 research folders

**Next step:** Open the vault folder in Obsidian (`File → Open Vault → Open folder as vault`), then run `/paper discover` to start finding papers.

## Example Workflow

```
Day 1: Start a new research topic
  /paper init                          → set up project
  /paper discover                      → find 10+ papers, auto-ingested to sources/

Day 2: Read and organize
  /paper digest                        → reading pass: notes/ for each paper
                                       → synthesis pass: concepts/ linking ideas across papers

Day 3: Explore and question
  /paper ask "How does X compare to Y?" → answer filed to questions/
  /paper ask log                        → paste a NotebookLM conversation to log it
  /paper check                          → find gaps, get suggestions for new articles

Day 4-5: Write the paper
  /paper position                       → define your angle
  /paper architect                      → design the method
  /paper evaluate                       → validate with experiments
  /paper write                          → generate full draft

Day 6: Polish and submit
  /paper critique                       → simulated peer review
  /paper refine                         → fix all issues
  /paper ship                           → match venue, format, submit
```

## Commands

### Research & Knowledge Base

| Command | What you're thinking | What it does |
|---------|---------------------|-------------|
| `/paper init` | "Starting new research" | Set up project, vault, and NotebookLM in one step |
| `/paper discover` | "I need to find papers" | Search arXiv + Semantic Scholar, download papers, identify gaps. Auto-ingests to vault `sources/` |
| `/paper digest` | "Let me organize what I know" | Two-pass: reads `sources/`, writes per-paper `notes/` (summary, findings, quotes), then synthesizes cross-paper `concepts/` with wikilinks |
| `/paper ask` | "I have a question" | Q&A against your knowledge base. Answers auto-filed to `questions/`. Also logs NotebookLM conversations |
| `/paper check` | "Am I missing anything?" | Health-check: unread sources, broken links, thin articles, suggested new concepts and research questions |

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

### Utility Commands

| Command | What it does |
|---------|-------------|
| `/paper` | Guided menu — shows where you are and what to do next |
| `/paper search` | Search arXiv + Semantic Scholar directly |
| `/paper analyze` | STAR analysis of a single paper |
| `/paper store` | NotebookLM notebook management |
| `/paper auth` | NotebookLM authentication (browser-based Google login) |
| `/paper eval` | Run quality evals on phase outputs |
| `/paper optimize` | Autoresearch-style prompt improvement |

## How It Works

### `.paper` Config

Each research project has a `.paper` file in the working directory — the single source of truth:

```yaml
project: agent-identity
topic: "Verifiable credentials for AI agent identity"
goal: "Propose a framework binding agent actions to verifiable identity"
venue: USENIX Security 2027
venue_type: conference
deadline: 2027-02-01
page_limit: 18
format: usenix
keywords: [verifiable credentials, agent identity, zero-trust]
related_fields: [IAM, decentralized identity]
vault: ~/.paper/vaults/agent-identity
notebook: https://notebooklm.google.com/notebook/abc123
phase: discover
phases_completed: []
created: 2026-04-05
```

Downstream phases read this automatically — `discover` uses keywords for search, `write` uses venue/format for styling, `ship` uses deadline for timeline.

### Obsidian Vault

The vault mirrors how a researcher thinks, viewable in [Obsidian](https://obsidian.md/):

```
vault/
  sources/      ← Original papers (PDFs, web clips)
  notes/        ← Per-paper reading notes (summary, findings, quotes)
  concepts/     ← Cross-paper synthesis articles with wikilinks
  questions/    ← Research Q&A (Claude + NotebookLM conversations)
  insights/     ← Your original ideas and hypotheses
  CATALOG.md    ← AI-readable index (auto-maintained)
```

**Naming conventions:**

| Folder | Pattern | Example |
|--------|---------|---------|
| `sources/` | `{author}-{year}-{title}.{ext}` | `vaswani-2017-attention.pdf` |
| `notes/` | `{author}-{year}-{title}.md` | `vaswani-2017-attention.md` |
| `concepts/` | `{concept-name}.md` | `self-attention.md` |
| `questions/` | `{YYYY-MM-DD}-{slug}.md` | `2026-04-05-why-transformers-scale.md` |
| `insights/` | `{YYYY-MM-DD}-{slug}.md` | `2026-04-05-sparse-attention-meets-moe.md` |

Sources and notes share the same `author-year-title` prefix so you can always find the note for a paper. Concepts have no dates (living documents). Questions and insights are date-prefixed (chronological journey).

**Workflow:** Papers flow into `sources/` via `/paper discover` or manual drop. `/paper digest` does two passes: first creating per-paper `notes/`, then synthesizing cross-paper `concepts/`. `/paper ask` queries everything and files answers to `questions/`. Original ideas go to `insights/`. `/paper check` finds gaps and suggests improvements.

### Architecture

- **Hybrid** — SKILL.md files (Claude's instructions) + Python scripts (data processing)
- **Quality rubrics** — Every phase has standards, anti-patterns, and failure recovery
- **Binary evals** — Automated pass/fail quality checks per phase
- **Self-optimization** — Prompt mutation loops that keep improvements, revert regressions

See [ARCHITECTURE.md](ARCHITECTURE.md) for details.

## License

MIT
