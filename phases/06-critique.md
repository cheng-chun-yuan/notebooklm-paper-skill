---
name: paper-critique
description: "Phase 6: Critique. Simulate peer review (3 adversarial personas) then run a pre-submission audit — find every weakness before real reviewers do."
phase: 6
---

# /paper critique — Phase 6: Stress-Test Your Draft

## Variable Shortcuts

```bash
PAPER_SKILL=~/.claude/skills/paper
PY=$PAPER_SKILL/.venv/bin/python3
```

## Input

All artifacts from `~/.paper/projects/{name}/`:
- `drafts/v1-draft.md` (or latest draft)
- `field-map.md`
- `gaps.md`
- `position.md`
- `architecture.md`
- `evaluation.md`
- `claims.json`
- `comparison-matrix.json`
- `scorecard.json`

## Quality Rubric

**Universal dimensions:**

- **Specificity** — Every review point references a specific section/paragraph. Every audit finding has a concrete action. Not "the evaluation is weak" but "Claim C2 in Section 4 lacks evidence — Table 3 shows no statistically significant difference."
- **Traceability** — Reviewer A cross-references field-map.md. Reviewer B cross-references claims.json. Audit cross-references scorecard.json. Everything connects back to artifacts.
- **Completeness** — All 3 reviewers report with verdicts. All 6 audit categories covered. Priority-ranked issue list produced. Path to acceptance is specific.

**Phase-specific dimensions:**

- **Calibrated severity** — Issues distributed across severity levels. Not all "critical." A paper with 10 critical issues and 0 medium/low has uncalibrated reviewers.
- **Actionable feedback** — Every weakness has a fix suggestion. "Add comparison against [baseline] on [dataset] to support C2" not "the evaluation could be stronger."
- **Honest assessment** — Readiness score is calibrated: 30-50 for papers with fundamental issues, 60-75 for papers needing significant revision, 80-90 for near-ready, 90+ only if genuinely polished.

## Anti-patterns

1. **Severity inflation** — DON'T: Mark every issue as "critical" or "major." A typo in Section 3.1 and an unsupported core claim are not the same severity. DO INSTEAD: Reserve "critical" for issues that would cause rejection (unsupported claims, missing baselines, fundamental flaws). Use "medium" and "low" for presentation issues.

2. **Vague criticism** — DON'T: "The evaluation could be stronger." "More experiments needed." DO INSTEAD: "Claim C2 lacks direct evidence. Add experiment comparing [method] vs [baseline] on [dataset] measuring [metric]."

3. **Reviewer persona leakage** — DON'T: Let all 3 reviewers make the same points. All reviewers comment on missing baselines. DO INSTEAD: Reviewer A checks baselines (domain expertise). Reviewer B checks methodology rigor. Reviewer C checks writing clarity. Overlap should be minimal.

4. **Everything is BROKEN** — DON'T: Flag every audit finding as critical. A typo and an unsupported core claim are not the same severity. DO INSTEAD: Use STRONG for things that work, NEEDS_FIX for real but non-fatal issues, BROKEN only for things that would cause rejection on their own.

5. **Missing positive signal** — DON'T: Only list weaknesses. A review with 0 strengths and 12 weaknesses, or an audit with no STRONG findings. DO INSTEAD: Identify genuine strengths first. A balanced review is more credible and more useful than pure criticism.

## Structural Exemplar

The complete output combines 3 reviewer reports, a meta-review, a 6-category audit, and a readiness score:

```markdown
# Critique Report — {project name}

**Date:** {date}
**Draft:** v1-draft.md

---

# Stage A: Simulated Peer Review

## Reviewer A — Domain Expert

Verdict: [Weak Accept]
Confidence: [High]

### Strengths
1. {Specific strength with reference to a paper section}
2. {Another strength, mentioning what surprised or impressed}

### Weaknesses
1. {Specific issue referencing a section + comparison to a specific prior paper}
2. {Gap in coverage — names the missing related work}

### Questions for Authors
1. {Genuine question about a design choice, not a rhetorical attack}

### Missing References
- {Paper title} — {why it should be cited and where}

---

## Reviewer B — Methodology Hawk

Verdict: [Weak Reject]
Confidence: [High]

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

---

## Reviewer C — Clarity Critic

Verdict: [Accept]
Confidence: [Medium]

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

---

## Meta-Review

### Overall Recommendation: [Revise]

### Verdict Summary
| Reviewer | Verdict | Confidence |
|----------|---------|------------|
| A — Domain Expert | ... | ... |
| B — Methodology Hawk | ... | ... |
| C — Clarity Critic | ... | ... |

### Priority-Ranked Issues
1. [CRITICAL] {Issue from Reviewer X, point Y — 1 sentence}
2. [HIGH] {Issue — 1 sentence}
3. [MEDIUM] {Issue — 1 sentence}
4. [LOW] {Issue — 1 sentence}

### Consensus Strengths
1. ...

### Path to Acceptance
- Fix issues #1-2 to move from Revise → Accept
- Address #3-5 to strengthen further

---

# Stage B: Pre-Submission Audit

**Overall Readiness:** 62/100

## 1. Structural Audit

- [STRONG] Abstract-to-evaluation alignment: Abstract promises X, Y, Z → all three validated in Section 5.
- [NEEDS_FIX] Introduction claims "first to..." but Section 2.3 cites {paper} doing similar work.
- [BROKEN] Section 4 jumps from method to results with no experimental setup.

## 2. Claims vs Reality

| Claim ID | Claim | Status | Action |
|----------|-------|--------|--------|
| C1 | "State-of-the-art performance" | OVERCLAIMED | Table 2 shows 2nd best. Change to "competitive" or add missing baseline. |
| C2 | "Generalizes to new domains" | UNSUPPORTED | No cross-domain experiment. Add experiment or remove claim. |
| C3 | "Efficient at scale" | STRONG | Figure 3 clearly shows linear scaling. |

## 3. Blind Spot Detection

1. **Missing ablation for component X** — Add ablation to Table 3. (Est: 1 paragraph + 1 table row)
2. **No failure case discussion** — Add a limitations paragraph after Section 5.2.
3. **Uncited related work: {Author2024}** — Directly relevant. Add to Section 2.

## 4. Positioning Strength

**Verdict: ADEQUATE**
Contribution is clear but differentiation from {closest paper} is thin.

## 5. Presentation Quality

1. [NEEDS_FIX] Figure 2 caption says "outperforms" but the figure shows a tie.
2. [NEEDS_FIX] Section 3.2, paragraph 3: 52-word sentence. Split.
3. [MINOR] Related work is 22% of paper (target ~15%). Trim.

## 6. Strategic Advice

1. **Promote the scaling result** — Buried in Section 5.3. Mention in abstract and intro. (High impact, low effort)
2. **Add a running example** — Method section is abstract. A concrete example would help. (Medium impact, medium effort)

---

## Summary

OVERALL READINESS: 62/100

Strengths (keep):
- Clear scaling results (Figure 3)
- Well-structured evaluation protocol

Fix before submit (high impact):
1. Add experimental setup section (~2 hours)
2. Fix overclaimed SOTA result (~30 min)
3. Add cross-domain experiment or weaken claim (~4 hours or 30 min)

Strategic advice:
1. Promote scaling finding to abstract and introduction
2. Add running example through method section

Nice to have (if time):
1. Trim related work by ~1 page
2. Fix 52-word sentence in Section 3.2

ACCEPTANCE PROBABILITY: ~45%
PATH TO 85%: Fix items 1, 2, 3 from "Fix before submit" (+20%), promote scaling finding (+10%), add running example (+8%)
```

## Workflow

Read all artifacts from `~/.paper/projects/{name}/`. This phase has two stages — run them in order.

---

### Stage A: Simulated Peer Review

Simulate 3 adversarial reviewer personas. Each reviewer operates independently — do NOT let one reviewer's assessment influence another.

#### Reviewer A — Domain Expert

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

#### Reviewer B — Methodology Hawk

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

#### Reviewer C — Clarity Critic

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

#### Meta-Review

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

---

### Stage B: Pre-Submission Audit

Using the review from Stage A plus all prior artifacts, perform 6 independent audit categories. Be brutally honest — the goal is to catch problems BEFORE a real reviewer does. Explicitly mark findings as "also flagged in review" vs "new finding."

#### 1. Structural Audit

**Check:**
- Does the abstract match what the paper actually delivers? Compare abstract promises to evaluation results.
- Does the intro promise what the evaluation proves? List each intro contribution and find its proof in the evaluation.
- Is the story arc coherent? Trace: problem -> why hard -> insight -> method -> proof. Flag any logical jumps.
- Are there logical gaps between sections? Does each section flow naturally to the next?
- Does the conclusion introduce new information? (It should not.)

**Output:** List of structural issues, each tagged [STRONG / NEEDS_FIX / BROKEN].

#### 2. Claims vs Reality

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

#### 3. Blind Spot Detection

**Check:**
- What obvious question would a reviewer ask that the paper DOESN'T answer?
- What related work is NOT cited that should be? (Cross-reference field-map.md against Related Work.)
- What experiment was NOT run that the field expects? (Check scorecard requirements.)
- What limitation is NOT acknowledged that a reviewer will notice?
- What failure case is NOT discussed?

**Output:** Numbered list of blind spots, each with suggested fix.

#### 4. Positioning Strength

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

#### 5. Presentation Quality

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

#### 6. Strategic Advice

**Check:**
- What is the paper's strongest differentiator? Is it emphasized enough?
- What key insights are buried? Should they be promoted to intro or abstract?
- What running examples or case studies would make the paper more concrete?
- What would make this paper memorable (a strong hook, a surprising finding, a useful tool)?
- What is the one thing that would most improve acceptance probability?

**Output:** Numbered strategic recommendations, prioritized by impact.

## Output

Write the complete critique report (both stages combined) to:

```
~/.paper/projects/{name}/critique-report.md
```

Use the structure shown in the Structural Exemplar above: Stage A (3 reviewer reports + meta-review) followed by Stage B (6 audit categories + summary with readiness score and acceptance probability).

## Cross-Cutting Updates

- **Claims**: If Reviewer B flags unsupported claims, note them for the refine phase. Report claim health in the summary (X strong, Y moderate, Z unsupported).
- **Scorecard**: Run `$PY $PAPER_SKILL/scripts/run.py scorecard show` and include current acceptance probability in both the meta-review and audit summary.
- **Matrix**: Report current state (N papers tracked, M dimensions).

## Health Check

Before completing this phase, verify:

**Stage A:**
- [ ] All 3 reviewer sections are present with verdicts
- [ ] Each reviewer has at least 2 strengths and 2 weaknesses
- [ ] Reviewer B validated every claim in claims.json
- [ ] Meta-review has a priority-ranked issue list
- [ ] Overall recommendation is provided (Accept / Revise / Reject)
- [ ] Path to acceptance is specific and actionable

**Stage B:**
- [ ] All 6 audit categories are covered
- [ ] Every claim in claims.json has a status in the Claims vs Reality section
- [ ] At least 3 blind spots identified
- [ ] Positioning strength has a clear verdict
- [ ] Overall readiness score and acceptance probability are provided
- [ ] Path to 85% acceptance is specific and actionable

If any check fails, complete the missing content before transitioning.

## Failure Recovery

1. **All reviewers give the same verdict** — If all 3 say "Reject" or all say "Accept," the review lacks diversity. Re-read each reviewer's persona description. Force Reviewer C to find at least one thing to disagree with from Reviewers A and B. Real peer review always has divergent opinions.

2. **Claims can't be validated** — If claims.json shows unsupported claims that the draft references, don't fake validation. Flag them explicitly: "Claim C3 is referenced in Section 4 but has no evidence in evaluation.md. This is a CRITICAL issue." Recommend backtrack to `/paper evaluate` (Phase 4).

3. **Readiness score < 50** — Too many fundamental issues for refinement alone. Recommend specific backtrack: if claims are unsupported, backtrack to `/paper evaluate` (Phase 4); if structure is broken, backtrack to `/paper write` (Phase 5); if positioning is weak, backtrack to `/paper position` (Phase 2). State which phase and why.

4. **Review feels shallow (< 3 specific points per reviewer)** — Re-read the draft section by section. For Reviewer A: check every citation against field-map.md. For Reviewer B: check every number against evaluation.md. For Reviewer C: read every paragraph transition. Shallow reviews mean the reviewer didn't actually read the artifacts.

## Phase Transition

When all health checks pass:

```
STATUS: DONE — Critique complete (review + audit)

Simulated 3 reviewers. Overall: {recommendation}.
{N} issues identified: {critical} critical, {high} high, {medium} medium, {low} low.
Top issue: {description of #1 priority issue}.

Overall readiness: {XX}/100. Acceptance probability: ~{YY}%.
{N} items to fix before submit, {M} strategic recommendations.
Path to 85%: {summary of top fixes}.

Cross-cutting status:
  Scorecard: X/Y requirements met (Z% accept probability)
  Claims: S strong, T moderate, U unsupported
  Matrix: N papers tracked, M dimensions

RECOMMENDATION: /paper refine because the critique identified
specific issues to fix.

A) Continue to /paper refine (recommended)
B) Go deeper — investigate a specific finding
C) Backtrack to {specific phase} — fundamental flaw identified
D) Save progress and stop here

Rate this phase? (1-5, or skip)
```
