---
name: paper-write
description: "Phase 7: Write. Generate each paper section using accumulated artifacts from all prior phases."
phase: 7
---

# /paper write — Phase 7: Write

## Input

All prior phase outputs:
- `field-map.md` (from survey)
- `gaps.md` (from gap)
- `inspiration-map.md` (from scout)
- `position.md` (from position)
- `architecture.md` (from architect)
- `evaluation.md` (from evaluate)
- `claims.json` (cross-cutting)
- `comparison-matrix.json` (cross-cutting)
- `scorecard.json` (cross-cutting)

## Variable Shortcuts

```bash
PAPER_SKILL=~/project/lab/trust_ai_identity/paper-skill
PY=$PAPER_SKILL/.venv/bin/python3
```

## Workflow

Before starting, read all input artifacts from `~/.paper-skill/projects/{name}/`. Verify they exist. If any are missing, flag which phases need to be completed first.

### Critical Guard — Claim Validation

Before generating EACH section, run:

```bash
$PY $PAPER_SKILL/scripts/run.py claims show
```

If ANY claim referenced in that section has strength "unsupported", **STOP** and flag:

> **Claim [X] is unsupported.** Add evidence before writing this section, or remove the claim.

Do NOT write a section that references unsupported claims. Either:
- A) Go back to `/paper evaluate` to add evidence
- B) Remove the claim from claims.json
- C) Reword the section to avoid the unsupported claim

### Section Generation

Generate each section in order. For each section, read the specified source artifacts and follow the structure below.

#### 1. Abstract

**Source:** position.md

**Structure:**
- Problem statement (1-2 sentences)
- Why it matters / why it's hard (1 sentence)
- Our approach in a nutshell (1-2 sentences)
- Key result (1 sentence, with specific numbers from evaluation.md)
- Implication (1 sentence)

**Target:** 150-250 words. Every sentence must earn its place.

#### 2. Introduction

**Source:** gaps.md + position.md

**Structure:**
1. Open with the problem and why it matters (1-2 paragraphs)
2. Why existing approaches fall short (1 paragraph, referencing gaps.md)
3. Our key insight / approach (1 paragraph, from position.md)
4. Contributions list — numbered, specific, verifiable:
   - "We propose X, which achieves Y"
   - "We show that Z, through experiments on W"
   - "We release [artifact] for reproducibility"
5. Paper organization paragraph (optional, keep brief)

**Guard:** Each contribution listed MUST map to a claim in claims.json with strong/moderate evidence.

#### 3. Related Work

**Source:** field-map.md + comparison-matrix.json

**Structure:**
1. Organize by theme (NOT chronologically, NOT by author)
2. For each theme:
   - Summarize the approach family
   - Cite key papers with brief descriptions
   - State how our work differs
3. End with a comparison table derived from comparison-matrix.json
4. Final paragraph: position our work relative to the closest prior work

**Guard:** Check that all papers in comparison-matrix.json are cited.

#### 4. Method

**Source:** architecture.md

**Structure:**
1. System overview (1 paragraph + figure reference if applicable)
2. Problem formulation / notation (if applicable)
3. Component details — one subsection per major component
4. Key algorithms or procedures (pseudocode if helpful)
5. Design decisions — justify non-obvious choices
6. Complexity analysis or scalability notes (if applicable)

**Guard:** Every design choice should trace back to a gap or insight from prior phases.

#### 5. Evaluation

**Source:** evaluation.md + claims.json

**Structure:**
1. Experimental setup:
   - Datasets with statistics
   - Baselines with brief descriptions and citations
   - Metrics with justification
   - Implementation details (hyperparams, compute, seeds)
2. Results:
   - Main results table
   - Per-claim analysis: "Claim C1 is supported by [Table X, row Y]"
3. Ablation study (if applicable)
4. Analysis:
   - Where the method succeeds and why
   - Where it struggles and why
   - Statistical significance or confidence intervals

**Guard:** Every claim in claims.json must be addressed. Flag any claim not validated by results.

#### 6. Discussion

**Source:** gaps.md + evaluation.md + position.md

**Structure:**
1. Gaps addressed — which gaps from gaps.md does this work close?
2. Limitations — be honest and specific (reviewers will find them anyway)
3. Broader impact (if applicable to the field)
4. Future work — concrete next steps, not vague hand-waving

#### 7. Conclusion

**Source:** position.md + evaluation.md

**Structure:**
1. Restate the contribution (1-2 sentences, different wording from abstract)
2. Key findings with specific numbers
3. Significance — why this matters for the field
4. One-sentence forward-looking statement

**Target:** Half a page or less. No new information.

## Output

Write the complete draft to:

```
~/.paper-skill/projects/{name}/drafts/v1-draft.md
```

Create the `drafts/` subdirectory if it does not exist.

After writing, save the synthesis:

```bash
$PY $PAPER_SKILL/scripts/run.py synthesize save <draft_file> --working-dir <project_dir>
```

## Cross-Cutting Updates

- **Claims**: Verify all claims are referenced in the draft. Flag any orphan claims.
- **Scorecard**: Check if "complete draft" is a scorecard requirement and mark it met.
- **Matrix**: Ensure comparison table in Related Work matches matrix data.

## Health Check

Before completing this phase, verify:

- [ ] All 7 sections are present in v1-draft.md
- [ ] No section references an unsupported claim
- [ ] Abstract is 150-250 words
- [ ] Every contribution in the intro maps to a validated claim
- [ ] Comparison table in Related Work matches comparison-matrix.json
- [ ] All papers from comparison-matrix.json are cited in Related Work
- [ ] Evaluation addresses every claim in claims.json
- [ ] Limitations section is honest (at least 2 acknowledged limitations)

If any check fails, fix it before transitioning.

## Phase Transition

When all health checks pass:

```
STATUS: DONE — Write complete

Draft v1 generated with {N} sections, {W} words.
All {C} claims referenced and supported.
Comparison table covers {P} papers across {D} dimensions.

Cross-cutting status:
  Scorecard: X/Y requirements met (Z% accept probability)
  Claims: S/T supported
  Matrix: N papers tracked, M dimensions

RECOMMENDATION: /paper review because the draft needs simulated
peer review to identify weaknesses before submission.

A) Continue to /paper review (recommended)
B) Go deeper — expand a specific section
C) Backtrack to /paper survey — related work feels thin
D) Backtrack to /paper position — motivation feels weak
E) Save progress and stop here

Rate this phase? (1-5, or skip)
```
