---
name: paper-review
description: "Phase 8: Review. Simulate 3 adversarial reviewer personas to identify weaknesses in the draft."
phase: 8
---

# /paper review — Phase 8: Review

## Input

- `drafts/v1-draft.md` (or latest draft)
- `scorecard.json` (cross-cutting)
- `claims.json` (cross-cutting)
- `field-map.md` (for Reviewer A)
- `comparison-matrix.json` (for Reviewer A)
- `evaluation.md` (for Reviewer B)

## Variable Shortcuts

```bash
PAPER_SKILL=~/project/lab/trust_ai_identity/paper-skill
PY=$PAPER_SKILL/.venv/bin/python3
```

## Workflow

Read the draft and all supporting artifacts from `~/.paper-skill/projects/{name}/`. Then simulate 3 adversarial reviewer personas. Each reviewer operates independently — do NOT let one reviewer's assessment influence another.

### Reviewer A — Domain Expert

**Reads:** field-map.md, comparison-matrix.json, Related Work section of draft

**Checks:**
1. Are ALL relevant baselines cited? Cross-reference comparison-matrix.json against the Related Work section. Flag any missing paper.
2. Is the contribution truly novel vs existing work? Identify the closest prior work and articulate the specific delta.
3. Is the comparison fair and complete? Check that baselines are recent and strong (not strawmen).
4. Are field-specific conventions followed? (e.g., standard benchmarks, expected metrics)
5. Does the paper demonstrate awareness of the broader research landscape?

**Output format:**
```
## Reviewer A — Domain Expert

Verdict: [Strong Accept / Accept / Weak Accept / Weak Reject / Reject]
Confidence: [High / Medium / Low]

### Strengths
1. ...
2. ...

### Weaknesses
1. ...
2. ...

### Questions for Authors
1. ...

### Missing References
- [paper title or description] — why it should be cited
```

### Reviewer B — Methodology Hawk

**Reads:** claims.json, evaluation.md, Method and Evaluation sections of draft

**Checks:**
1. Does the evaluation support EVERY claim? Run:
   ```bash
   $PY $PAPER_SKILL/scripts/run.py claims show
   ```
   For each claim, verify there is a specific table/figure/result that validates it.
2. Are metrics appropriate for this field and task?
3. Is the experiment reproducible? Are hyperparameters, compute budget, random seeds, and dataset splits specified?
4. Missing ablation studies? Each major design decision should have an ablation.
5. Statistical rigor: Are results averaged over multiple runs? Confidence intervals or significance tests?
6. Are baselines run under the same conditions (same hardware, same data splits)?

**Output format:**
```
## Reviewer B — Methodology Hawk

Verdict: [Strong Accept / Accept / Weak Accept / Weak Reject / Reject]
Confidence: [High / Medium / Low]

### Strengths
1. ...
2. ...

### Weaknesses
1. ...
2. ...

### Claim Validation
- C1: [Supported / Partially Supported / Unsupported] — [specific evidence reference]
- C2: ...

### Missing Experiments
1. ...

### Reproducibility Concerns
1. ...
```

### Reviewer C — Clarity Critic

**Reads:** drafts/v1-draft.md (full draft)

**Checks:**
1. Is the writing clear and concise? Flag jargon-heavy sentences, overly long paragraphs, passive voice overuse.
2. Do figures and tables match surrounding text? Every figure/table must be referenced and explained.
3. Is the story arc coherent? Trace: abstract promise -> intro motivation -> method delivery -> evaluation proof -> conclusion summary. Flag logical gaps.
4. Abstract accuracy: Does the abstract accurately represent what the paper delivers?
5. Section balance: Are sections appropriately weighted? (e.g., method not too short, related work not too long)
6. Are transitions between sections smooth?

**Output format:**
```
## Reviewer C — Clarity Critic

Verdict: [Strong Accept / Accept / Weak Accept / Weak Reject / Reject]
Confidence: [High / Medium / Low]

### Strengths
1. ...
2. ...

### Weaknesses
1. ...
2. ...

### Specific Line-Level Feedback
1. Section [X], paragraph [Y]: [issue and suggestion]
2. ...

### Structural Suggestions
1. ...
```

### Meta-Review

After all 3 reviews, synthesize:

```
## Meta-Review

### Overall Recommendation: [Accept / Revise / Reject]

### Verdict Summary
| Reviewer | Verdict | Confidence |
|----------|---------|------------|
| A — Domain Expert | ... | ... |
| B — Methodology Hawk | ... | ... |
| C — Clarity Critic | ... | ... |

### Priority-Ranked Issues
1. [CRITICAL] ... (from Reviewer X, point Y)
2. [HIGH] ... (from Reviewer X, point Y)
3. [MEDIUM] ... (from Reviewer X, point Y)
4. [LOW] ... (from Reviewer X, point Y)

### Consensus Strengths
1. ...

### Path to Acceptance
- Fix issues #1-3 to move from Revise to Accept
- Address issues #4-6 to strengthen the paper further
```

## Output

Write the complete review to:

```
~/.paper-skill/projects/{name}/review-report.md
```

## Cross-Cutting Updates

- **Claims**: If Reviewer B flags unsupported claims, note them for the refine phase.
- **Scorecard**: Run `$PY $PAPER_SKILL/scripts/run.py scorecard show` and include current acceptance probability in the meta-review.

## Health Check

Before completing this phase, verify:

- [ ] All 3 reviewer sections are present with verdicts
- [ ] Each reviewer has at least 2 strengths and 2 weaknesses
- [ ] Reviewer B validated every claim in claims.json
- [ ] Meta-review has a priority-ranked issue list
- [ ] Overall recommendation is provided (Accept / Revise / Reject)
- [ ] Path to acceptance is specific and actionable

If any check fails, complete the missing review content before transitioning.

## Phase Transition

When all health checks pass:

```
STATUS: DONE — Review complete

Simulated 3 reviewers. Overall: {recommendation}.
{N} issues identified: {critical} critical, {high} high, {medium} medium, {low} low.
Top issue: {description of #1 priority issue}.

Cross-cutting status:
  Scorecard: X/Y requirements met (Z% accept probability)
  Claims: S/T supported (Reviewer B flagged {F} issues)
  Matrix: N papers tracked, M dimensions

RECOMMENDATION: /paper audit because the review identified issues
that need systematic assessment before fixing.

A) Continue to /paper audit (recommended)
B) Go deeper — address critical issues immediately before audit
C) Backtrack to {phase} — fundamental flaw identified
D) Save progress and stop here

Rate this phase? (1-5, or skip)
```
