---
name: paper-refine
description: "Phase 10: Refine. Address review and audit findings point-by-point, producing a polished v2 draft."
phase: 10
---

# /paper refine — Phase 10: Refine

## Input

- `review-report.md` (from review phase)
- `audit-report.md` (from audit phase)
- `drafts/v1-draft.md` (or latest draft)
- All prior artifacts for reference

## Variable Shortcuts

```bash
PAPER_SKILL=~/project/lab/trust_ai_identity/paper-skill
PY=$PAPER_SKILL/.venv/bin/python3
```

## Workflow

### Step 1 — Triage Issues

Read `review-report.md` and `audit-report.md`. Build a unified issue list:

1. Extract all issues from the review (priority-ranked list from meta-review)
2. Extract all issues from the audit ("Fix before submit" items first, then strategic advice)
3. Deduplicate — many review and audit issues will overlap
4. Prioritize by acceptance probability impact:
   - **P0 (Critical)**: Issues that would cause rejection (unsupported claims, missing baselines, fundamental flaws)
   - **P1 (High)**: Issues that would lower score significantly (weak motivation, poor clarity, missing ablations)
   - **P2 (Medium)**: Issues that would cause minor deductions (presentation, missing citations, wording)
   - **P3 (Low)**: Nice-to-have improvements

Present the triaged list to the user before proceeding. Ask: "Does this prioritization look right? Any items to add or reorder?"

### Step 2 — Address Review Concerns

For each reviewer concern from review-report.md, address it point-by-point:

**Format for each fix:**
```
### Reviewer [A/B/C], Point [N]: [summary]

**Issue:** [what the reviewer said]
**Action:** [what we changed]
**Location:** [which section/paragraph was modified]
**Rationale:** [why this addresses the concern]
```

Work through concerns in priority order (P0 first).

### Step 3 — Address Audit Findings

For each audit finding from audit-report.md:

1. **Structural issues**: Restructure sections, fix logical gaps, align abstract with evaluation
2. **Claims vs Reality**: Fix overclaimed/unsupported claims — either add evidence or weaken the claim
3. **Blind spots**: Add missing citations, acknowledge missing experiments, add limitation discussion
4. **Positioning**: Sharpen the contribution statement if flagged as weak
5. **Presentation**: Fix jargon, sentence length, passive voice, section balance
6. **Strategic**: Promote buried insights, add running examples, strengthen the hook

### Step 4 — Re-check Claims

After all fixes, verify claims are healthy:

```bash
$PY $PAPER_SKILL/scripts/run.py claims show
```

All claims should have strong or moderate evidence. If any remain unsupported:
- Either add evidence (may require going back to `/paper evaluate`)
- Or remove/weaken the claim in the draft

### Step 5 — Re-check Scorecard

```bash
$PY $PAPER_SKILL/scripts/run.py scorecard show
```

Review each unmet requirement. For each:
- Can it be addressed in the draft? (e.g., add reproducibility details)
- Does it require new experiments? (flag for user decision)
- Is it a venue-specific requirement that can wait?

### Step 6 — Generate Refined Draft

Apply all changes to produce `v2-refined.md`. The refined draft should:
- Address every P0 and P1 issue
- Address most P2 issues
- Note any P3 issues left for later

## Output

Write the refined draft to:

```
~/.paper-skill/projects/{name}/drafts/v2-refined.md
```

Also write a change log:

```
~/.paper-skill/projects/{name}/drafts/v2-changelog.md
```

The changelog format:

```markdown
# v2 Changelog

## Summary
- {N} issues addressed out of {M} total
- P0: {X}/{Y} fixed | P1: {X}/{Y} fixed | P2: {X}/{Y} fixed

## Changes by Reviewer Concern

### Reviewer A
- Point 1: [FIXED] — [brief description of change]
- Point 2: [FIXED] — [brief description of change]

### Reviewer B
- Point 1: [FIXED] — [brief description of change]
- Point 2: [DEFERRED] — requires new experiments

### Reviewer C
- Point 1: [FIXED] — [brief description of change]

## Changes by Audit Finding
- Structural: [changes made]
- Claims: [changes made]
- Blind spots: [changes made]
- Positioning: [changes made]
- Presentation: [changes made]
- Strategic: [changes made]

## Remaining Issues
1. [issue] — [reason not addressed] — [suggested action]
```

## Cross-Cutting Updates

- **Claims**: Re-validate any claims that were modified. Update evidence references if needed.
- **Scorecard**: Mark any newly met requirements (e.g., "ablation study" if one was added).

## Health Check

Before completing this phase, verify:

- [ ] All P0 (critical) issues are addressed
- [ ] All P1 (high) issues are addressed
- [ ] v2-refined.md exists with all 7 paper sections
- [ ] v2-changelog.md documents all changes
- [ ] Claims re-check shows no unsupported claims
- [ ] Scorecard re-check shows improvement over pre-refine state
- [ ] No new unsupported claims were introduced

If any check fails, continue fixing before transitioning.

## Phase Transition

When all health checks pass:

```
STATUS: DONE — Refine complete

Addressed {N}/{M} issues. All P0 and P1 issues resolved.
Claims: all strong/moderate. Scorecard: {improvement summary}.
Draft v2 is {W} words ({delta} from v1).

Cross-cutting status:
  Scorecard: X/Y requirements met (Z% accept probability)
  Claims: S/T supported
  Matrix: N papers tracked, M dimensions

RECOMMENDATION: /paper venue because the paper is polished
and ready for venue selection and formatting.

A) Continue to /paper venue (recommended)
B) Go deeper — another round of refinement
C) Backtrack to /paper evaluate — needs more evidence
D) Save progress and stop here

Rate this phase? (1-5, or skip)
```
