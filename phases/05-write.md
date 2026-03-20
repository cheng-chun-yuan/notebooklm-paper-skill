---
name: paper-write
description: "Phase 5: Write. Generate each paper section using accumulated artifacts from all prior phases."
phase: 5
---

# /paper write — Phase 5: Write

## Input

All prior phase outputs:
- `field-map.md` (from discover)
- `gaps.md` (from discover)
- `inspiration-map.md` (from discover)
- `position.md` (from position)
- `architecture.md` (from architect)
- `evaluation.md` (from evaluate)
- `claims.json` (cross-cutting)
- `comparison-matrix.json` (cross-cutting)
- `scorecard.json` (cross-cutting)

## Variable Shortcuts

```bash
PAPER_SKILL=~/.claude/skills/notebooklm-paper-skill
PY=$PAPER_SKILL/.venv/bin/python3
```

## Quality Rubric

**Universal dimensions:**

- **Specificity** — Every claim uses concrete numbers, specific paper names, and precise comparisons rather than vague qualifiers ("significantly better" → "12.3% improvement over baseline X on dataset Y").
- **Traceability** — Every section traces back to a specific prior phase artifact (abstract → position.md, intro → gaps.md, method → architecture.md, eval → evaluation.md).
- **Completeness** — All 7 paper sections present, all claims addressed, all matrix papers cited.

**Phase-specific dimensions:**

- **Narrative coherence** — The paper tells one story: problem → why hard → insight → method → proof → impact. No logical jumps between sections. A reader can follow the thread from abstract to conclusion without confusion.
- **Claim-evidence alignment** — Every claim in the introduction maps to a specific table/figure in evaluation. Every result in evaluation maps back to a claim. No orphan claims, no orphan results.
- **Academic voice** — Precise, measured language. No overselling ("groundbreaking", "revolutionary"). Limitations acknowledged honestly. Related work treated fairly, not dismissed.

## Anti-patterns

**DON'T:** Make vague contribution claims like "We improve performance."
**Example:** "Our method significantly outperforms prior work across all tasks."
**DO INSTEAD:** "We reduce inference latency by 34% on the GLUE benchmark while maintaining 98.2% of BERT-base accuracy."

---

**DON'T:** List related work chronologically without synthesis — "X did A. Y did B. Z did C."
**Example:** "Smith (2020) proposed attention pooling. Jones (2021) used graph networks. Lee (2022) tried contrastive learning."
**DO INSTEAD:** Organize by theme, show how each family of approaches fails at the specific gap you address. "Attention-based methods (Smith 2020; Park 2021) improve token-level representation but fail to capture document-level structure, which is the gap our method targets."

---

**DON'T:** Present evaluation results without connecting them to specific claims.
**Example:** A results table followed by "Our method achieves the best results on most benchmarks."
**DO INSTEAD:** After each results table, explicitly state the claim-evidence link: "This supports Claim C1 because our method outperforms the strongest baseline (RoBERTa-large) by 2.1 F1 points on SQuAD 2.0 (Table 1, row 3)."

---

**DON'T:** Write a passive, vague limitation section — "There are some limitations to our approach."
**Example:** "Our method has limitations that could be addressed in future work."
**DO INSTEAD:** Name specific failure modes with conditions: "Our method degrades when input sequences exceed 2048 tokens because the attention mechanism scales quadratically (O(n²)), resulting in 3× slower inference compared to linear alternatives."

---

**DON'T:** Promise results in the abstract that don't appear in evaluation.
**Example:** Abstract claims "state-of-the-art on 5 benchmarks" but evaluation only covers 3.
**DO INSTEAD:** Write the abstract LAST, after evaluation is complete, using exact numbers from results. Cross-check every metric in the abstract against evaluation tables.

## Structural Exemplar

A domain-agnostic skeleton showing the shape of good output:

```markdown
# {Paper Title}

## Abstract
{Problem: 1-2 sentences stating the gap} {Why hard: 1 sentence on challenges}
{Approach: 1-2 sentences on method} {Result: 1 sentence with specific metric from evaluation}
{Implication: 1 sentence on broader impact}

[Target: 150-250 words]

## 1. Introduction
[Para 1: Problem + why it matters — hook the reader]
[Para 2: Why existing approaches fall short — reference gaps.md]
[Para 3: Our key insight — the "aha" moment]
[Para 4: Contributions list]
  1. We propose {method}, which {achieves what}
  2. We demonstrate {result} through {experiments}
  3. We release {artifact} for reproducibility

## 2. Related Work
### {Theme A}: {Approach Family}
[2-3 papers, how they relate, what they miss]
### {Theme B}: {Approach Family}
[2-3 papers, how they relate, what they miss]
[Comparison table from matrix.json]
[Positioning paragraph: how we differ from closest work]

## 3. Method
### 3.1 Overview
[System overview + figure reference]
### 3.2 {Component 1}
[From architecture.md — inputs, algorithm, outputs]
### 3.3 {Component 2}
[Design decisions with justification tracing to gaps]

## 4. Evaluation
### 4.1 Setup
[Datasets | Baselines | Metrics | Implementation details]
### 4.2 Main Results
[Results table + per-claim analysis: "C1 is supported by Table 1, row 3"]
### 4.3 Ablation Study
[One table per design decision]
### 4.4 Analysis
[Where it works, where it fails, why]

## 5. Discussion
[Gaps closed | Honest limitations | Future work]

## 6. Conclusion
[Restate contribution | Key numbers | Significance | Forward look]
```

## Workflow

Before starting, read all input artifacts from `~/.notebooklm-paper-skill/projects/{name}/`. Verify they exist. If any are missing, flag which phases need to be completed first.

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
~/.notebooklm-paper-skill/projects/{name}/drafts/v1-draft.md
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

## Failure Recovery

### Weak motivation / thin introduction

If the intro feels generic or doesn't compellingly explain why the problem matters: Go back to `gaps.md` and `position.md`. Find the most surprising or counterintuitive finding from the gap analysis. Lead with that. If gaps.md itself is thin, backtrack to `/paper discover`.

### Evaluation doesn't support claims

If results are weak or claims are overclaimed: Run `$PY $PAPER_SKILL/scripts/run.py claims show` and identify which claims have weak/no evidence. Options:
- (a) Weaken the claim language
- (b) Add qualifying conditions
- (c) Backtrack to `/paper evaluate` for additional experiments
- (d) Remove the claim entirely

### Related work section feels like a list

If related work reads as "X did A. Y did B. Z did C." without synthesis: Restructure by theme, not by paper. For each theme, explain the approach family's strengths and limitations, then position your work. Use the comparison matrix to identify the key differentiating dimensions.

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

RECOMMENDATION: /paper critique because the draft needs simulated
peer review to identify weaknesses before submission.

A) Continue to /paper critique (recommended)
B) Go deeper — expand a specific section
C) Backtrack to /paper discover — related work feels thin
D) Backtrack to /paper position — motivation feels weak
E) Save progress and stop here

Rate this phase? (1-5, or skip)
```
