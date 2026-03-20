# paper-skill

Your AI research advisor. An 11-phase pipeline that guides you from "I have a topic" to "paper submitted" — with acceptance scorecard, claim-evidence tracking, and simulated peer review.

```
Survey → Gap → Scout → Position → Architect → Evaluate → Write → Review → Audit → Refine → Venue
```

**What it does:**
- **Survey** — search arXiv + Semantic Scholar, download PDFs, upload to NotebookLM, mine acceptance patterns
- **Gap** — find what no one has solved, rank by novelty potential
- **Scout** — hunt for transferable methods across different domains
- **Position** — define your contribution and novelty claims
- **Architect** — design your method with component-to-gap mapping
- **Evaluate** — design experiments, validate claims with evidence
- **Write** — generate full paper draft with claim-evidence guard (refuses unsupported claims)
- **Review** — 3 adversarial reviewer personas simulate peer review
- **Audit** — pre-submission advisory with readiness score and acceptance probability
- **Refine** — fix everything flagged by review + audit
- **Venue** — match your paper to the right conference/journal

**3 cross-cutting systems track quality across all phases:**
- **Acceptance Scorecard** — built from surveyed papers, audits every phase
- **Claim-Evidence Chain** — catches unsupported claims before you write
- **Comparison Matrix** — auto-builds the comparison table for your paper

## Install — takes 30 seconds

**Requirements:** [Claude Code](https://docs.anthropic.com/en/docs/claude-code), Python 3.11+

### One-prompt install

Open Claude Code and paste this:

> Install paper-skill: run **`git clone https://github.com/cheng-chun-yuan/notebooklm-paper-skill.git ~/.claude/skills/paper-skill && ~/.claude/skills/paper-skill/setup`** then add a "paper-skill" section to CLAUDE.md that lists the available skills: /paper, /paper survey, /paper gap, /paper scout, /paper position, /paper architect, /paper evaluate, /paper write, /paper review, /paper audit, /paper refine, /paper venue, /paper auth, /paper store, /paper search, /paper analyze, /paper feedback, /paper update.

### Manual install

```bash
git clone https://github.com/cheng-chun-yuan/notebooklm-paper-skill.git ~/.claude/skills/paper-skill
cd ~/.claude/skills/paper-skill && ./setup
```

Then add to your `~/.claude/CLAUDE.md`:

```markdown
## paper-skill

- Available skills: /paper, /paper survey, /paper gap, /paper scout, /paper position, /paper architect, /paper evaluate, /paper write, /paper review, /paper audit, /paper refine, /paper venue, /paper auth, /paper store, /paper search, /paper analyze, /paper feedback, /paper update
```

### NotebookLM setup (optional, for survey/store features)

```
/paper auth setup
```

## Quick start: your first 5 minutes

1. Run `/paper` — see where you are in your research
2. Pick **A) Starting fresh** — give it your topic
3. It creates a project, starts surveying papers, builds your acceptance scorecard
4. Follow the guided flow through each phase
5. At any point, backtrack or skip ahead — the skill adapts

## How it works

```
You:  /paper

Paper Skill — Research Paper Generation Pipeline

Where are you in your research?

A) Starting fresh — "I have a topic but haven't read any papers yet"
B) I've read papers — "I know the field but need to find my angle"
C) I found gaps — "I know what's unsolved, need inspiration"
D) I have my angle — "I know my contribution, need to position it"
E) I've positioned — "Contribution is clear, need to design it"
F) I have results — "Method is done, need to write it up"
G) Draft exists — "Paper is written, needs review"
H) Continue previous project
```

Each phase shows a progress tracker:

```
[■■■□□□□□□□□] Phase 3/11 — Scout

  ✓ Survey    — 23 papers analyzed, acceptance scorecard built
  ✓ Gap       — 4 gaps identified, 2 high-priority
  ► Scout     — Hunting transferable methods across domains...

  Scorecard: 2/9 met | Claims: 0/0 | Matrix: 5 papers tracked
```

## Commands

| Command | Phase | What it does |
|---------|-------|-------------|
| `/paper` | — | Guided flow entry point |
| `/paper survey` | 1 | Search, download, analyze papers + build acceptance scorecard |
| `/paper gap` | 2 | Find unsolved problems across surveyed papers |
| `/paper scout` | 3 | Hunt transferable methods from other domains |
| `/paper position` | 4 | Define your contribution + novelty claims |
| `/paper architect` | 5 | Design your method/system architecture |
| `/paper evaluate` | 6 | Design experiments, analyze results, validate claims |
| `/paper write` | 7 | Generate full paper draft (section by section) |
| `/paper review` | 8 | Simulated peer review (3 adversarial reviewers) |
| `/paper audit` | 9 | Pre-submission advisory with readiness score |
| `/paper refine` | 10 | Fix everything flagged by review + audit |
| `/paper venue` | 11 | Match paper to target conference/journal |
| `/paper auth` | — | NotebookLM authentication |
| `/paper store` | — | Save to NotebookLM (extensible) |
| `/paper search` | — | Standalone paper search |
| `/paper analyze` | — | STAR framework analysis of a single paper |
| `/paper feedback` | — | Rate phases, suggest improvements |
| `/paper update` | — | Pull latest version |

## Storage

```
~/.paper-skill/              # Global research database
├── papers/                  # Downloaded PDFs (shared across projects)
├── analyses/                # STAR analyses
├── gaps/                    # Gap analyses
├── projects/                # Per-project state
│   └── {name}/
│       ├── project.json     # Current phase, progress
│       ├── scorecard.json   # Acceptance requirements
│       ├── claims.json      # Claim-evidence chain
│       ├── field-map.md     # Survey output
│       ├── gaps.md          # Gap analysis
│       ├── position.md      # Contribution statement
│       ├── architecture.md  # Method design
│       └── drafts/          # Paper versions
└── feedback/                # Phase ratings for skill improvement
```

## Design

Inspired by [gstack](https://github.com/garrytan/gstack)'s architecture:
- **Sub-skill pattern** — each phase is its own SKILL.md
- **Preamble** — version check, session tracking, project detection
- **Structured UX** — AskUserQuestion format, completion status protocol
- **Feedback loop** — phase ratings drive skill improvements via git updates

See [ARCHITECTURE.md](ARCHITECTURE.md) for design decisions.

## License

MIT
