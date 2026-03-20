---
name: paper-survey
description: "Phase 1: Literature survey. Collect papers via Semantic Scholar/arXiv, analyze acceptance patterns, build field map and acceptance scorecard."
phase: 1
---

# /paper survey — Phase 1: Literature Survey

## Input

- User-provided research topic or query
- Optional: year filter, venue filter, specific paper URLs

## Variable Shortcuts

```bash
PAPER_SKILL=~/project/lab/trust_ai_identity/paper-skill
PY=$PAPER_SKILL/.venv/bin/python3
```

## Workflow

This phase has two parts. Complete Part A before Part B.

### Part A: Paper Collection

#### Step 1 — Create a survey

Ask the user for their research topic. Formulate a precise search query. Create the survey:

```bash
$PY $PAPER_SKILL/scripts/run.py survey create --name "survey-name" --query "search query here" [--year-from 2020]
```

Tips for good queries:
- Use field-specific terminology, not casual language
- Include 2-3 synonyms separated by OR if the field uses multiple terms
- Add year filter to focus on recent work (last 3-5 years unless historical survey)

#### Step 2 — Run the search pipeline

Run the full pipeline (search + download) or run steps individually:

```bash
# Full pipeline (recommended for first run)
$PY $PAPER_SKILL/scripts/run.py survey run

# Or run steps separately for more control
$PY $PAPER_SKILL/scripts/run.py survey search       # Search only
$PY $PAPER_SKILL/scripts/run.py survey download     # Download PDFs only
```

#### Step 3 — Review and refine results

List and inspect what was found:

```bash
$PY $PAPER_SKILL/scripts/run.py survey list          # List all surveys
$PY $PAPER_SKILL/scripts/run.py survey show           # Show current survey details
$PY $PAPER_SKILL/scripts/run.py survey suggest        # Get suggestions for additional queries
```

If coverage is thin (fewer than 10 relevant papers), create additional surveys with refined queries. Use `survey suggest` for query ideas.

#### Step 4 — Upload to NotebookLM (optional but recommended)

If the user wants deep Q&A over papers:

```bash
$PY $PAPER_SKILL/scripts/run.py survey upload --notebook-url "https://notebooklm.google.com/notebook/..."
```

#### Step 5 — Query and report

Ask questions across the collected papers and generate a summary report:

```bash
$PY $PAPER_SKILL/scripts/run.py survey query --question "What are the main approaches to X?"
$PY $PAPER_SKILL/scripts/run.py survey report
```

### Part B: Acceptance Pattern Mining

After collecting at least 10 papers, analyze them for publication patterns. This is where the survey becomes actionable intelligence rather than just a reading list.

#### Step 1 — Identify venues and acceptance rates

For each collected paper, determine:
- Where it was published (conference/journal name, year)
- Acceptance rate of that venue (e.g., NeurIPS ~26%, ICML ~25%, ACL ~25%)
- Tier of the venue (A*, A, B, workshop)

Record this in the field map.

#### Step 2 — Extract success patterns

Read through the papers and calculate what percentage of them include:
- Formal threat model or problem definition
- Comparison against strong baselines (not just ablations)
- Released artifacts (code, datasets, models)
- Theoretical analysis or proofs
- User studies or human evaluation
- Reproducibility details (hyperparams, compute budget, seeds)

These percentages become your "what the field expects" baseline.

#### Step 3 — Extract impact patterns

Identify the most-cited papers in the collection and determine WHY they are impactful:
- Novel formulation?
- New benchmark or dataset?
- Surprising negative result?
- Unified framework replacing fragmented approaches?

#### Step 4 — Extract rejection signals

From the patterns, identify common reviewer complaints in this field:
- "Missing comparison to X" (identify what X is)
- "Evaluation on toy datasets only"
- "No theoretical justification"
- "Incremental over Y"

#### Step 5 — Build acceptance scorecard

For each requirement identified, add it to the scorecard with the observed frequency as the weight:

```bash
$PY $PAPER_SKILL/scripts/run.py scorecard add "Strong baselines comparison" 0.85
$PY $PAPER_SKILL/scripts/run.py scorecard add "Released code/artifacts" 0.70
$PY $PAPER_SKILL/scripts/run.py scorecard add "Formal problem definition" 0.90
$PY $PAPER_SKILL/scripts/run.py scorecard add "Ablation study" 0.75
$PY $PAPER_SKILL/scripts/run.py scorecard add "Reproducibility details" 0.65
```

The weight (0.00-1.00) represents how critical this requirement is based on the field norm. 0.90 means 90% of accepted papers in this field include it.

#### Step 6 — Save field map

Write `field-map.md` to the project directory. It must contain:

1. **Field Overview** — 2-3 paragraph summary of the research landscape
2. **Key Papers** — Table of top papers with venue, year, citation count, one-line contribution
3. **Methodological Trends** — What approaches are gaining/losing traction
4. **Success Patterns** — The percentages from Step 2
5. **Impact Patterns** — What makes papers influential in this field
6. **Rejection Signals** — Common reviewer complaints
7. **Scorecard Summary** — List of requirements and weights

Save location: `~/.paper-skill/projects/{name}/field-map.md`

## Commands Reference

```bash
# Survey management
$PY $PAPER_SKILL/scripts/run.py survey create --name "..." --query "..." [--year-from Y]
$PY $PAPER_SKILL/scripts/run.py survey run
$PY $PAPER_SKILL/scripts/run.py survey search
$PY $PAPER_SKILL/scripts/run.py survey download
$PY $PAPER_SKILL/scripts/run.py survey upload --notebook-url "..."
$PY $PAPER_SKILL/scripts/run.py survey query --question "..."
$PY $PAPER_SKILL/scripts/run.py survey report
$PY $PAPER_SKILL/scripts/run.py survey list
$PY $PAPER_SKILL/scripts/run.py survey show
$PY $PAPER_SKILL/scripts/run.py survey suggest

# Scorecard (cross-cutting)
$PY $PAPER_SKILL/scripts/run.py scorecard add "requirement name" 0.XX
$PY $PAPER_SKILL/scripts/run.py scorecard show
```

## Output

- `~/.paper-skill/projects/{name}/field-map.md` — Comprehensive field analysis
- `~/.paper-skill/projects/{name}/scorecard.json` — Acceptance requirements with weights

## Cross-Cutting Updates

- **Scorecard**: Initialize the acceptance scorecard with 5+ requirements extracted from field analysis. Each requirement has a weight (0.00-1.00) based on how frequently accepted papers in this field include it.
- **Matrix**: Optionally begin populating the comparison matrix with surveyed papers and key dimensions.

## Health Check

Before completing this phase, verify:

- [ ] At least 10 papers analyzed (not just downloaded — actually read/summarized)
- [ ] Scorecard has 5+ requirements with meaningful weights
- [ ] field-map.md exists and contains all 7 sections
- [ ] At least 2 different venues represented in the collection
- [ ] Success patterns have concrete percentages, not vague statements

If any check fails, continue working on the phase. Do not transition.

## Phase Transition

When all health checks pass:

```
STATUS: DONE — Survey complete

Surveyed {N} papers across {M} venues. Field map covers {topic summary}.
Top acceptance requirements: {top 3 from scorecard}.
Key insight: {one-sentence finding about the field}.

Cross-cutting status:
  Scorecard: {X} requirements initialized
  Claims: 0/0 (none yet — claims come in Position phase)
  Matrix: {N} papers tracked

RECOMMENDATION: /paper gap because the field landscape is mapped and
you need to identify where the gaps are before choosing your angle.

A) Continue to /paper gap (recommended)
B) Go deeper — run additional surveys with broader/narrower queries
C) Save progress and stop here

Rate this phase? (1-5, or skip)
```
