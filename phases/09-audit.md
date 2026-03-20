---
name: paper-audit
description: "Phase 9: Audit. Pre-submission advisory with 6 audit categories covering structure, claims, blind spots, positioning, presentation, and strategy."
phase: 9
---

# /paper audit — Phase 9: Audit

## Input

All artifacts from `~/.paper-skill/projects/{name}/`:
- `drafts/v1-draft.md` (or latest draft)
- `review-report.md`
- `field-map.md`
- `gaps.md`
- `position.md`
- `architecture.md`
- `evaluation.md`
- `claims.json`
- `comparison-matrix.json`
- `scorecard.json`

## Variable Shortcuts

```bash
PAPER_SKILL=~/project/lab/trust_ai_identity/paper-skill
PY=$PAPER_SKILL/.venv/bin/python3
```

## Workflow

Read all artifacts and the review report. Then perform 6 independent audit categories. Be brutally honest — the goal is to catch problems BEFORE a real reviewer does.

### 1. Structural Audit

**Check:**
- Does the abstract match what the paper actually delivers? Compare abstract promises to evaluation results.
- Does the intro promise what the evaluation proves? List each intro contribution and find its proof in the evaluation.
- Is the story arc coherent? Trace: problem -> why hard -> insight -> method -> proof. Flag any logical jumps.
- Are there logical gaps between sections? Does each section flow naturally to the next?
- Does the conclusion introduce new information? (It should not.)

**Output:** List of structural issues, each tagged [STRONG / NEEDS_FIX / BROKEN].

### 2. Claims vs Reality

**Check:**
Run:
```bash
$PY $PAPER_SKILL/scripts/run.py claims show
```

For every claim:
- **Strong evidence**: Claim is well-supported. Mark as OK.
- **Moderate evidence**: Claim is supported but could be stronger. Mark as MODERATE.
- **Unsupported**: No evidence. Mark as UNSUPPORTED — must be fixed or removed.
- **Overclaimed**: Evidence exists but the claim overstates it. Mark as OVERCLAIMED.
- **Underclaimed**: Evidence is stronger than the claim suggests. Mark as UNDERCLAIMED.
- **Contradictory**: Evidence contradicts the claim. Mark as CONTRADICTORY.

**Output:** Table of claims with status and recommended action.

### 3. Blind Spot Detection

**Check:**
- What obvious question would a reviewer ask that the paper DOESN'T answer?
- What related work is NOT cited that should be? (Cross-reference field-map.md against Related Work.)
- What experiment was NOT run that the field expects? (Check scorecard requirements.)
- What limitation is NOT acknowledged that a reviewer will notice?
- What failure case is NOT discussed?

**Output:** Numbered list of blind spots, each with suggested fix.

### 4. Positioning Strength

**Check:**
Run:
```bash
$PY $PAPER_SKILL/scripts/run.py scorecard show
```

- Re-check novelty overlap with the closest 3 papers from comparison-matrix.json.
- Is the contribution clear in ONE sentence? If not, the positioning needs work.
- Is the contribution defensible? Could a reviewer argue it's incremental?
- Does the comparison matrix show clear differentiation on at least 2 dimensions?

**Output:** Positioning strength assessment: [STRONG / ADEQUATE / WEAK] with justification.

### 5. Presentation Quality

**Check:**
- Figures: Readable at print size? Captions present and descriptive? Referenced in text?
- Tables: Support the claims in surrounding text? Properly formatted? All columns explained?
- Jargon density: Flag paragraphs with excessive undefined terminology.
- Sentence length: Flag sentences over 40 words.
- Passive voice: Flag excessive use (some is fine, paragraphs of it are not).
- Page budget: Which sections are over-weight or under-weight relative to norms?
  - Related work: ~15% of paper
  - Method: ~25-30%
  - Evaluation: ~25-30%
  - Introduction: ~10-15%

**Output:** Numbered presentation issues with severity.

### 6. Strategic Advice

**Check:**
- What is the paper's strongest differentiator? Is it emphasized enough?
- What key insights are buried? Should they be promoted to intro or abstract?
- What running examples or case studies would make the paper more concrete?
- What would make this paper memorable (a strong hook, a surprising finding, a useful tool)?
- What is the one thing that would most improve acceptance probability?

**Output:** Numbered strategic recommendations, prioritized by impact.

## Output

Write the complete audit to:

```
~/.paper-skill/projects/{name}/audit-report.md
```

Use this format:

```markdown
# Audit Report — {project name}

**Date:** {date}
**Draft:** v1-draft.md
**Overall Readiness:** XX/100

---

## 1. Structural Audit
[findings]

## 2. Claims vs Reality
[claim status table]

## 3. Blind Spot Detection
[numbered blind spots]

## 4. Positioning Strength
[assessment]

## 5. Presentation Quality
[numbered issues]

## 6. Strategic Advice
[numbered recommendations]

---

## Summary

OVERALL READINESS: XX/100

Strengths (keep):
- ...

Fix before submit (high impact):
1. ...
2. ...

Strategic advice:
1. ...
2. ...

Nice to have (if time):
1. ...
2. ...

ACCEPTANCE PROBABILITY: ~XX%
PATH TO 85%: Fix items 1, 2, 3 from "Fix before submit"
```

## Cross-Cutting Updates

- **Scorecard**: Run `$PY $PAPER_SKILL/scripts/run.py scorecard show` and report current status in the summary.
- **Claims**: Report claim health in the summary (X strong, Y moderate, Z unsupported).

## Health Check

Before completing this phase, verify:

- [ ] All 6 audit categories are covered
- [ ] Every claim in claims.json has a status in the Claims vs Reality section
- [ ] At least 3 blind spots identified (if fewer, the audit was not thorough enough)
- [ ] Positioning strength has a clear verdict
- [ ] Overall readiness score and acceptance probability are provided
- [ ] Path to 85% acceptance is specific and actionable
- [ ] Summary section is complete with all 4 categories

If any check fails, complete the missing audit content before transitioning.

## Phase Transition

When all health checks pass:

```
STATUS: DONE — Audit complete

Overall readiness: {XX}/100. Acceptance probability: ~{YY}%.
{N} items to fix before submit, {M} strategic recommendations.
Path to 85%: {summary of top fixes}.

Cross-cutting status:
  Scorecard: X/Y requirements met (Z% accept probability)
  Claims: S strong, T moderate, U unsupported
  Matrix: N papers tracked, M dimensions

RECOMMENDATION: /paper refine because the audit identified
specific issues to fix that will improve acceptance probability.

A) Continue to /paper refine (recommended)
B) Go deeper — investigate a specific audit finding
C) Backtrack to {specific phase flagged} — not ready, needs more work
D) Save progress and stop here

Rate this phase? (1-5, or skip)
```
