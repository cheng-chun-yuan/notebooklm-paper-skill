---
name: paper-gap
description: "Phase 2: Gap analysis. Apply 6-question framework to each surveyed paper, then aggregate to find gaps no paper addresses."
phase: 2
---

# /paper gap — Phase 2: Gap Analysis

## Input

- `~/.paper-skill/projects/{name}/field-map.md` from Phase 1 (Survey)
- Surveyed papers from the collection

## Variable Shortcuts

```bash
PAPER_SKILL=~/project/lab/trust_ai_identity/paper-skill
PY=$PAPER_SKILL/.venv/bin/python3
```

## Workflow

### Step 1 — Load survey artifacts

Read the field map and paper collection:

```bash
$PY $PAPER_SKILL/scripts/run.py scorecard show
$PY $PAPER_SKILL/scripts/run.py survey show
```

Confirm that at least 10 papers were analyzed in the survey phase. If fewer, warn the user and recommend going back to `/paper survey`.

### Step 2 — Per-paper 6-question analysis

Apply the following 6-question framework to EACH surveyed paper. This is the core of gap analysis — do not skip or batch papers superficially.

For each paper, answer:

1. **What does it CLAIM to solve?**
   Read the abstract and introduction. What problem statement does the paper present? What does it promise?

2. **What does it ACTUALLY solve?**
   Look at the evaluation section, not the abstract. What do the experiments actually demonstrate? Is there a gap between the claim and the evidence?

3. **What does it FAIL to solve?**
   Read the limitations section (if present) and the conclusion's future work. What do the authors themselves acknowledge as unsolved?

4. **What does it IGNORE?**
   This is the most valuable question. What limitations are NOT stated? Examples:
   - Assumes clean data but real data is noisy
   - Tests on English only but claims "language understanding"
   - Evaluates on synthetic benchmarks but targets real-world use
   - Ignores computational cost
   - Ignores adversarial settings

5. **Why do these gaps exist?**
   Classify each gap as:
   - **Fundamental** — inherent limitation of the approach (e.g., attention is O(n^2))
   - **Engineering** — could be solved with more effort (e.g., scaling to larger datasets)
   - **Scope** — intentionally out of scope for that paper (e.g., privacy not considered)
   - **Blind spot** — the field has not noticed this gap

6. **How does this relate to YOUR work?**
   If the user's research context is known, connect this paper's gaps to potential contributions. If not yet known, note promising directions.

Save each per-paper analysis:

```bash
$PY $PAPER_SKILL/scripts/run.py gap save <paper_id> <file>
```

### Step 3 — Aggregate gaps across all papers

After analyzing all papers individually, aggregate the findings:

1. **Gaps that NO paper addresses** — These are the most valuable. List problems mentioned in multiple papers' limitations that nobody has solved.

2. **Gaps that SOME papers address partially** — Problems where existing solutions are incomplete. Note what percentage of the gap is covered and what remains.

3. **Gaps only ONE paper addresses** — Potentially novel but unvalidated. Could be opportunities or dead ends.

### Step 4 — Rank gaps

Rank each aggregated gap by three dimensions:

| Dimension | Question | Scale |
|-----------|----------|-------|
| **Importance** | How much does the field care? | 1-5 (5 = frequently mentioned as future work) |
| **Feasibility** | Can this realistically be solved? | 1-5 (5 = clear path forward) |
| **Novelty** | How original would a solution be? | 1-5 (5 = nobody has tried this angle) |

Compute a composite score: `importance * 0.4 + feasibility * 0.3 + novelty * 0.3`

### Step 5 — Write gaps.md

Save the aggregated analysis to `~/.paper-skill/projects/{name}/gaps.md` with this structure:

```markdown
# Gap Analysis — {project name}

## Summary
{2-3 paragraph overview of the gap landscape}

## Top Gaps (Ranked)

### Gap 1: {title} — Score: X.X
- **Description**: {what is missing}
- **Evidence**: {which papers mention this, how}
- **Type**: Fundamental / Engineering / Scope / Blind spot
- **Importance**: X/5 — {why}
- **Feasibility**: X/5 — {why}
- **Novelty**: X/5 — {why}
- **Potential direction**: {brief sketch of how this could be addressed}

### Gap 2: ...
(repeat for all identified gaps)

## Per-Paper Analysis Summary

| Paper | Claims | Actually Solves | Key Gap | Gap Type |
|-------|--------|-----------------|---------|----------|
| ... | ... | ... | ... | ... |

## Field Blind Spots
{Gaps categorized as "blind spot" — the field hasn't noticed these yet}
```

## Commands Reference

```bash
# Gap analysis
$PY $PAPER_SKILL/scripts/run.py gap save <paper_id> <file>

# Cross-cutting
$PY $PAPER_SKILL/scripts/run.py scorecard show
$PY $PAPER_SKILL/scripts/run.py scorecard update "requirement" met gap
```

## Output

- `~/.paper-skill/projects/{name}/gaps.md` — Ranked gap list with per-paper analysis
- Per-paper gap analysis files saved via `gap save`

## Cross-Cutting Updates

- **Scorecard**: Update with the question "Are you targeting a gap the field cares about?" Check this by verifying the top gap has importance >= 3/5.

```bash
$PY $PAPER_SKILL/scripts/run.py scorecard add "Targets field-relevant gap" 0.85
$PY $PAPER_SKILL/scripts/run.py scorecard update "Targets field-relevant gap" met gap
```

## Health Check

Before completing this phase, verify:

- [ ] At least 3 gaps identified with severity ratings
- [ ] Each gap has importance, feasibility, and novelty scores
- [ ] gaps.md exists with all required sections
- [ ] Per-paper analysis covers the majority of surveyed papers (not just 2-3)
- [ ] At least 1 gap classified as "blind spot" or "fundamental" (if none exist, state why)

If any check fails, continue working on the phase. Do not transition.

## Phase Transition

When all health checks pass:

```
STATUS: DONE — Gap analysis complete

Analyzed {N} papers. Found {M} gaps, top 3:
1. {Gap 1 title} (score: X.X) — {one line}
2. {Gap 2 title} (score: X.X) — {one line}
3. {Gap 3 title} (score: X.X) — {one line}

Field blind spots: {count} identified

Cross-cutting status:
  Scorecard: X/Y requirements met
  Claims: 0/0 (none yet)
  Matrix: N papers tracked

RECOMMENDATION: /paper scout because you have ranked gaps and need to
find methods from adjacent fields that could address them.

A) Continue to /paper scout (recommended)
B) Go deeper — analyze more papers or refine gap rankings
C) Backtrack to /paper survey — field too crowded, survey adjacent field
D) Save progress and stop here

Rate this phase? (1-5, or skip)
```

**Backtrack trigger**: If ALL top gaps have novelty <= 2/5 ("field too crowded"), recommend backtracking to `/paper survey` with a query targeting an adjacent or emerging subfield.
