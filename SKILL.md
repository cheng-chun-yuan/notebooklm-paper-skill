---
name: paper
description: "Research paper pipeline in 8 phases: Discover → Position → Architect → Evaluate → Write → Critique → Refine → Ship. Acceptance scorecard, claim-evidence tracking, comparison matrix."
---

# Paper Skill — Research Paper Pipeline

## Preamble (run first)

```bash
PAPER_SKILL=~/.claude/skills/paper
VENV=$PAPER_SKILL/.venv
PY="$VENV/bin/python3"
if [ ! -d "$VENV" ] || [ ! -x "$PY" ]; then
  echo "NEEDS_SETUP"
else
  echo "READY"
fi

_VERSION=$(cat "$PAPER_SKILL/VERSION" 2>/dev/null || echo "0.0.0")
_UPD=$("$PAPER_SKILL/bin/paper-update-check" 2>/dev/null || true)
echo "VERSION: $_VERSION"
[ -n "$_UPD" ] && echo "$_UPD"

mkdir -p ~/.paper/sessions ~/.paper/projects
touch ~/.paper/sessions/"$PPID"
find ~/.paper/sessions -mmin +120 -type f -delete 2>/dev/null || true
_AUTH=$("$PY" "$PAPER_SKILL/scripts/run.py" auth status --quiet 2>/dev/null || echo "NO_AUTH")
echo "AUTH: $_AUTH"

# Read .paper if present
if [ -f .paper ]; then
  _PROJ_NAME=$(grep '^project:' .paper | awk '{print $2}')
  _PHASE=$(grep '^phase:' .paper | awk '{print $2}')
  _VAULT=$(grep '^vault:' .paper | awk '{print $2}')
  _NOTEBOOK=$(grep '^notebook:' .paper | awk '{$1=""; print substr($0,2)}')
  echo "PROJECT: $_PROJ_NAME — Phase: $_PHASE"
  [ -n "$_VAULT" ] && echo "VAULT: $_VAULT"
  [ -n "$_NOTEBOOK" ] && echo "NOTEBOOK: $_NOTEBOOK"
else
  # Fallback to legacy project.json
  _PROJECT=$("$PY" -c "
import pathlib, json
projects_dir = pathlib.Path.home() / '.paper' / 'projects'
if not projects_dir.exists():
    print('none'); exit()
for pf in projects_dir.glob('*/project.json'):
    try:
        p = json.loads(pf.read_text())
        if p.get('active'):
            print(f\"{p['name']} — Phase {p['current_phase']}/8 ({p['phase_name']})\"); exit()
    except: pass
print('none')
" 2>/dev/null || echo "none")
  echo "PROJECT: $_PROJECT"
fi

_FEEDBACK=$("$PAPER_SKILL/bin/paper-config" get feedback_mode 2>/dev/null || echo "on")
echo "FEEDBACK: $_FEEDBACK"
```

If `NEEDS_SETUP`: tell user "paper-skill needs one-time setup (~30s). OK?" then run the setup script.
If `NO_AUTH`: tell user "NotebookLM auth not configured. Run `/paper auth setup` when you need NotebookLM features."
If `UPGRADE_AVAILABLE`: tell user about the available update and offer `/paper update`.

## Guided Flow

When user invokes `/paper` with no sub-command, show:

```
Paper Skill — Research Paper Pipeline

Where are you in your research?

A) Starting fresh — "I have a topic but haven't started"
   → /paper init

B) Finding papers — "I need to survey the field"
   → /paper discover

C) Organizing notes — "I have papers, need to digest them"
   → /paper digest

D) Have a question — "I want to ask something about my research"
   → /paper ask

E) Check my progress — "How's my knowledge base looking?"
   → /paper check

F) Ready to write — "I know my angle, time to write the paper"
   → /paper position → architect → evaluate → write → critique → refine → ship

G) Continue previous project
   → list .paper files or projects from ~/.paper/projects/
```

When user picks an option:
1. If no active project, create one: ask for project name, then run `$PY -c "from scripts.config import create_project; create_project('{name}', working_directory='$(pwd)')"`
2. Each entry point runs a health check on prior phases. If jumping ahead (e.g., `/paper write` without discover), flag it but don't block.
3. Read the corresponding sub-skill SKILL.md and follow its instructions.

## /paper init — First-Time Setup

Walk the user through project setup conversationally:

1. **"What's your research topic?"**
   → topic field

2. **"What's your goal? (one sentence)"**
   → goal field

3. **"Targeting a venue?"**
   A) Conference — ask name + deadline
   B) Journal — ask name
   C) Workshop — ask name + deadline
   D) Not sure yet / preprint
   → venue, venue_type, deadline fields

4. **"Any keywords to guide paper discovery? (comma-separated)"**
   → keywords field

5. **"Do you have a NotebookLM notebook? (paste URL or skip)"**
   → notebook field. If no auth: suggest `/paper auth setup` first.

6. **"Custom vault path? (default: ~/.paper/vaults/{project-name})"**
   → vault field

Create .paper:
```bash
$PY -c "
from scripts.core.dotpaper import create_dotpaper
from pathlib import Path
create_dotpaper(
    Path('.'),
    project='{project}',
    topic='{topic}',
    goal='{goal}',
    venue='{venue}',
    venue_type='{venue_type}',
    deadline='{deadline}',
    notebook='{notebook}',
    keywords={keywords},
    vault='{vault}',
)
"
```

Initialize vault:
```bash
$PY $PAPER_SKILL/scripts/run.py vault init "$VAULT"
```

Show:
```
Project "{project}" initialized!

.paper created in current directory
Vault at {vault} — open in Obsidian
{NotebookLM linked / NotebookLM skipped}

Ready! Run /paper discover to start surveying the field.
```

## Progress Tracker

Show at the start of each phase:

```
[■■□□□□□□] Phase 2/8 — Position

  ✓ Discover  — {summary from project artifacts}
  ► Position  — {current action}
  ○ Architect — Design your method
  ○ Evaluate  — Experiments & results
  ○ Write     — Generate paper draft
  ○ Critique  — Peer review + audit
  ○ Refine    — Fix & polish
  ○ Ship      — Target venue & submit

  Scorecard: X/Y met | Claims: S/T supported | Matrix: N papers
```

Read progress from project.json. Read cross-cutting status by running:
```bash
$PY $PAPER_SKILL/scripts/run.py scorecard show 2>/dev/null
$PY $PAPER_SKILL/scripts/run.py claims show 2>/dev/null
$PY $PAPER_SKILL/scripts/run.py matrix show 2>/dev/null
```

## Sub-skill Routing

| Command | Reads from | Type |
|---------|------------|------|
| `/paper discover` | `phases/01-discover.md` | Script-backed |
| `/paper position` | `phases/02-position.md` | SKILL.md-only |
| `/paper architect` | `phases/03-architect.md` | SKILL.md-only |
| `/paper evaluate` | `phases/04-evaluate.md` | Script-backed |
| `/paper write` | `phases/05-write.md` | SKILL.md-only |
| `/paper critique` | `phases/06-critique.md` | SKILL.md-only |
| `/paper refine` | `phases/07-refine.md` | SKILL.md-only |
| `/paper ship` | `phases/08-ship.md` | SKILL.md-only |
| `/paper auth` | `support/auth.md` | Script-backed |
| `/paper store` | `support/store.md` | Script-backed |
| `/paper search` | `support/search.md` | Script-backed |
| `/paper analyze` | `support/analyze.md` | SKILL.md-only + persistence |
| `/paper feedback` | `support/feedback.md` | Utility |
| `/paper update` | `support/update.md` | Utility |
| `/paper eval` | `support/eval.md` | Script-backed |
| `/paper optimize` | `support/optimize.md` | SKILL.md-only (autoresearch) |
| `/paper init` | `SKILL.md` (inline) | Conversational setup |
| `/paper digest` | `support/digest.md` | SKILL.md-only |
| `/paper ask` | `support/ask.md` | SKILL.md-only |
| `/paper check` | `support/check.md` | SKILL.md-only |

All paths are relative to the paper-skill root directory.

## Phase Transition Template

After completing each phase, use this template:

```
STATUS: DONE — {phase} complete

{2-3 line summary of what was produced}

Cross-cutting status:
  Scorecard: X/Y requirements met (Z% accept probability)
  Claims: S/T supported
  Matrix: N papers tracked, M dimensions

{Any health check warnings from scorecard or claim-evidence chain}

RECOMMENDATION: /paper {next} because {reason}

A) Continue to /paper {next} (recommended)
B) Go deeper — {specific deeper action}
C) Backtrack to /paper {earlier} — {reason you might}
D) Save progress and stop here

Rate this phase? (1-5, or skip)
```

If user rates < 4: ask "What would make it better?" and save via `$PAPER_SKILL/bin/paper-feedback {phase} {rating} "{comment}"`.
If user rates 5: ask "What worked well?" and save positive feedback too.

After transition, update project state:
```bash
# Update .paper if present, fallback to project.json
if [ -f .paper ]; then
  $PY -c "
from pathlib import Path
from scripts.core.dotpaper import find_dotpaper, load_dotpaper, save_dotpaper
dp_dir = find_dotpaper(Path('.'))
if dp_dir:
    dp = load_dotpaper(dp_dir)
    dp['phases_completed'].append('{current_phase}')
    dp['phase'] = '{next_phase_name}'
    save_dotpaper(dp_dir, dp)
"
else
  $PY -c "
from scripts.config import load_project, save_project, get_active_project
p = get_active_project()
p['phases_completed'].append('{current_phase}')
p['current_phase'] = {next_phase_number}
p['phase_name'] = '{next_phase_name}'
save_project(p)
"
fi
```

## Backtrack Triggers

| Phase | Trigger | Goes to |
|-------|---------|---------|
| Discover | Field too crowded, all gaps low-novelty | Discover (adjacent field) |
| Position | Can't differentiate | Discover (find different gap) |
| Architect | Design doesn't hold | Discover (need better building blocks) |
| Evaluate | Results don't support claims | Architect or Position |
| Write | Related work thin / weak motivation | Discover or Position |
| Critique | Fundamental flaw | Any earlier phase |
| Refine | Needs more evidence | Evaluate |

When backtracking: do NOT reset completed phases. Keep all artifacts. User can re-run a phase with broader scope.

## AskUserQuestion Format

Every question to the user follows:
1. **Re-ground**: Project name, current phase (1-2 sentences)
2. **Simplify**: Plain English a smart 16-year-old could follow
3. **Recommend**: `RECOMMENDATION: Choose [X] because [reason]`
4. **Options**: Lettered A) B) C)

## Completion Status Protocol

Every phase exits with one of:
- **DONE** — Phase completed. Evidence provided. Scorecard updated.
- **DONE_WITH_CONCERNS** — Completed with issues. List each.
- **BLOCKED** — Cannot proceed. State blocker.
- **NEEDS_CONTEXT** — Missing information. State exactly what's needed.

## Escalation

3 failures on the same step → stop and escalate to user. Bad work is worse than no work.

## Cross-Cutting Commands Reference

```bash
PY=~/.claude/skills/paper/.venv/bin/python3
SKILL=~/.claude/skills/paper

# Scorecard
$PY $SKILL/scripts/run.py scorecard show
$PY $SKILL/scripts/run.py scorecard add "requirement name" 0.91
$PY $SKILL/scripts/run.py scorecard update "requirement name" met discover

# Claims
$PY $SKILL/scripts/run.py claims show
$PY $SKILL/scripts/run.py claims add "claim text" phase_name
$PY $SKILL/scripts/run.py claims validate C1 "Table 2, row 3" strong evaluate

# Matrix
$PY $SKILL/scripts/run.py matrix show
$PY $SKILL/scripts/run.py matrix add-dim "dimension name"
$PY $SKILL/scripts/run.py matrix add-paper "paper name"
$PY $SKILL/scripts/run.py matrix set "paper" "dimension" true

# Eval
$PY $SKILL/scripts/run.py eval run [phase_number]
$PY $SKILL/scripts/run.py eval show [phase_number]
$PY $SKILL/scripts/run.py eval results [phase_number]
```
