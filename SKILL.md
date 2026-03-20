---
name: paper-skill
description: Full research paper generation pipeline. 11 phases from literature survey to venue submission. Acceptance scorecard, claim-evidence tracking, comparison matrix. Use when user wants to research a topic, analyze papers, write a paper, or any academic research workflow.
---

# Paper Skill — Research Paper Generation Pipeline

## Preamble (run first)

```bash
PAPER_SKILL=~/project/lab/trust_ai_identity/paper-skill
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

mkdir -p ~/.paper-skill/sessions ~/.paper-skill/projects
touch ~/.paper-skill/sessions/"$PPID"
find ~/.paper-skill/sessions -mmin +120 -type f -delete 2>/dev/null || true
_AUTH=$("$PY" "$PAPER_SKILL/scripts/run.py" auth status --quiet 2>/dev/null || echo "NO_AUTH")
echo "AUTH: $_AUTH"

_PROJECT=$("$PY" -c "
import pathlib, json
projects_dir = pathlib.Path.home() / '.paper-skill' / 'projects'
if not projects_dir.exists():
    print('none'); exit()
for pf in projects_dir.glob('*/project.json'):
    try:
        p = json.loads(pf.read_text())
        if p.get('active'):
            print(f\"{p['name']} — Phase {p['current_phase']}/11 ({p['phase_name']})\"); exit()
    except: pass
print('none')
" 2>/dev/null || echo "none")
echo "PROJECT: $_PROJECT"

_FEEDBACK=$("$PAPER_SKILL/bin/paper-config" get feedback_mode 2>/dev/null || echo "on")
echo "FEEDBACK: $_FEEDBACK"
```

If `NEEDS_SETUP`: tell user "paper-skill needs one-time setup (~30s). OK?" then run the setup script.
If `NO_AUTH`: tell user "NotebookLM auth not configured. Run `/paper auth setup` when you need NotebookLM features."
If `UPGRADE_AVAILABLE`: tell user about the available update and offer `/paper update`.

## Guided Flow

When user invokes `/paper` with no sub-command, show:

```
Paper Skill — Research Paper Generation Pipeline

Where are you in your research?

A) Starting fresh — "I have a topic but haven't read any papers yet"
   → /paper survey

B) I've read papers — "I know the field but need to find my angle"
   → /paper gap

C) I found gaps — "I know what's unsolved, need inspiration"
   → /paper scout

D) I have my angle — "I know my contribution, need to position it"
   → /paper position

E) I've positioned — "Contribution is clear, need to design it"
   → /paper architect

F) I have results — "Method is done, need to write it up"
   → /paper write

G) Draft exists — "Paper is written, needs review"
   → /paper review

H) Continue previous project
   → list projects from ~/.paper-skill/projects/
```

When user picks an option:
1. If no active project, create one: ask for project name, then run `$PY -c "from scripts.config import create_project; create_project('{name}', working_directory='$(pwd)')"`
2. Each entry point runs a health check on prior phases. If jumping ahead (e.g., `/paper write` without gap analysis), flag it but don't block.
3. Read the corresponding sub-skill SKILL.md and follow its instructions.

## Progress Tracker

Show at the start of each phase:

```
[■■■□□□□□□□□] Phase 3/11 — Scout

  ✓ Survey    — {summary from project artifacts}
  ✓ Gap       — {summary}
  ► Scout     — {current action}
  ○ Position  — Define your contribution
  ○ Architect — Design your method
  ○ Evaluate  — Experiments & results
  ○ Write     — Generate paper draft
  ○ Review    — Simulated peer review
  ○ Audit     — Pre-submission advisory
  ○ Refine    — Fix & polish
  ○ Venue     — Target venue selection

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
| `/paper survey` | `phases/01-survey.md` | Script-backed |
| `/paper gap` | `phases/02-gap.md` | Script-backed |
| `/paper scout` | `phases/03-scout.md` | Script-backed (reuses search) |
| `/paper position` | `phases/04-position.md` | SKILL.md-only |
| `/paper architect` | `phases/05-architect.md` | SKILL.md-only |
| `/paper evaluate` | `phases/06-evaluate.md` | Script-backed |
| `/paper write` | `phases/07-write.md` | SKILL.md-only |
| `/paper review` | `phases/08-review.md` | SKILL.md-only |
| `/paper audit` | `phases/09-audit.md` | SKILL.md-only |
| `/paper refine` | `phases/10-refine.md` | SKILL.md-only |
| `/paper venue` | `phases/11-venue.md` | SKILL.md-only |
| `/paper auth` | `support/auth.md` | Script-backed |
| `/paper store` | `support/store.md` | Script-backed |
| `/paper search` | `support/search.md` | Script-backed |
| `/paper analyze` | `support/analyze.md` | SKILL.md-only + persistence |
| `/paper feedback` | `support/feedback.md` | Utility |
| `/paper update` | `support/update.md` | Utility |

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

After transition, update project.json:
```bash
$PY -c "
from scripts.config import load_project, save_project, get_active_project
p = get_active_project()
p['phases_completed'].append('{current_phase}')
p['current_phase'] = {next_phase_number}
p['phase_name'] = '{next_phase_name}'
save_project(p)
"
```

## Backtrack Triggers

| Phase | Trigger | Goes to |
|-------|---------|---------|
| Gap | Field too crowded | Survey (adjacent field) |
| Scout | No usable techniques | Survey (widen scope) |
| Position | Can't differentiate | Gap or Scout |
| Architect | Design doesn't hold | Scout |
| Evaluate | Results don't support claims | Architect or Position |
| Write | Related work thin / weak motivation | Survey or Position |
| Review | Fundamental flaw | Any earlier phase |
| Audit | Not ready | Specific phase flagged |
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
PY=~/project/lab/trust_ai_identity/paper-skill/.venv/bin/python3
SKILL=~/project/lab/trust_ai_identity/paper-skill

# Scorecard
$PY $SKILL/scripts/run.py scorecard show
$PY $SKILL/scripts/run.py scorecard add "requirement name" 0.91
$PY $SKILL/scripts/run.py scorecard update "requirement name" met survey

# Claims
$PY $SKILL/scripts/run.py claims show
$PY $SKILL/scripts/run.py claims add "claim text" phase_name
$PY $SKILL/scripts/run.py claims validate C1 "Table 2, row 3" strong evaluate

# Matrix
$PY $SKILL/scripts/run.py matrix show
$PY $SKILL/scripts/run.py matrix add-dim "dimension name"
$PY $SKILL/scripts/run.py matrix add-paper "paper name"
$PY $SKILL/scripts/run.py matrix set "paper" "dimension" true
```
