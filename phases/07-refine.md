---
name: paper-refine
description: "Phase 7: Refine. Address review and audit findings point-by-point, producing a polished v2 draft."
phase: 7
---

# /paper refine — Phase 7: Refine

## Input

- `review-report.md` (from critique phase)
- `audit-report.md` (from critique phase)
- `drafts/v1-draft.md` (or latest draft)
- All prior artifacts for reference

## Variable Shortcuts

```bash
PAPER_SKILL=~/.claude/skills/paper
PY=$PAPER_SKILL/.venv/bin/python3
```

## Quality Rubric

Every refine output is evaluated on these dimensions:

| Dimension | Excellent | Acceptable | Poor |
|-----------|-----------|------------|------|
| **Specificity** | Each fix references exact section, paragraph, and the original issue ID from triage. Changelog entries say "Changed Section 3.2, paragraph 1: replaced 'significantly outperforms' with 'achieves comparable performance (within 1.2%)' per Reviewer B Point 2." | Fixes reference sections but not exact paragraphs. Changelog entries are brief but identifiable. | Vague changelog. "Improved evaluation section." No way to verify what changed. |
| **Traceability** | Every change in v2-changelog.md maps to a specific issue from review-report.md or audit-report.md by ID. No orphan changes. | Most changes are traced. A few fixes lack clear origin. | Changes appear without connection to any reported issue. |
| **Completeness** | All P0 and P1 issues addressed. P2 issues mostly addressed. Remaining issues explicitly listed with rationale for deferral. | All P0 addressed. Most P1 addressed. Some P2 addressed. | P0 issues left unaddressed without explanation. |
| **Issue coverage** | All P0 and P1 issues from triage are addressed. P2 issues are mostly addressed. Remaining issues are explicitly listed in "Remaining Issues" with a reason for deferral and a suggested next step. | P0 fully addressed. P1 mostly addressed. Remaining list exists but reasons are thin. | P0 or P1 issues silently dropped. No remaining issues list. |
| **Regression safety** | After fixes, re-check shows no new unsupported claims, scorecard shows improvement (not regression), and no section contradicts another. Explicitly confirms: "Re-check found no regressions." | Re-check performed. Minor new issues noted and flagged. | No re-check performed. Fixes introduce new contradictions or unsupported claims. |

## Anti-patterns

1. **Surface-level fixes** — DON'T: Fix wording without fixing the underlying issue. EXAMPLE: Reviewer says "evaluation is weak" and the fix is rewording the evaluation section to sound more confident. DO: Add the missing experiment or baseline, then rewrite the section to reflect the new evidence. If new experiments are not feasible, present the trade-off to the user explicitly.

2. **Fix-induced regressions** — DON'T: Fix a claim in Section 5.1 but leave the old version of that claim in the abstract, introduction, and conclusion. DO: After every substantive fix, grep the draft for related references and update all of them. Check: abstract, intro contributions list, conclusion, and any cross-references.

3. **Skipping P2 issues** — DON'T: Only fix critical issues and ignore presentation and clarity problems. P2 issues (jargon, sentence length, figure captions, section balance) are often the difference between "Weak Accept" and "Accept." DO: Address P2 issues after P0 and P1 are resolved. If time is limited, at least fix the P2 issues in the introduction and evaluation (highest reviewer attention).

4. **Silent deferral** — DON'T: Quietly skip an issue without documenting why. DO: Every deferred issue appears in the "Remaining Issues" section of v2-changelog.md with a reason ("requires new experiments — user decision needed") and a suggested action.

## Structural Exemplar

The v2-changelog.md follows this shape (content is illustrative, not prescriptive):

```markdown
# v2 Changelog

## Summary
- 14 issues addressed out of 18 total
- P0: 3/3 fixed | P1: 6/6 fixed | P2: 5/7 fixed | P3: 0/2 fixed

## Changes by Reviewer Concern

### Reviewer A
- Point 1 (P0): [FIXED] — Added missing baseline comparison against {method} in Table 2. New row shows our method achieves 3.2% improvement. Updated abstract and intro claims accordingly.
- Point 2 (P1): [FIXED] — Added ablation study for component X in new Table 4. Shows component contributes 40% of total improvement.
- Point 3 (P2): [FIXED] — Reduced related work from 2.5 pages to 1.8 pages. Moved 3 less-relevant paragraphs to appendix.

### Reviewer B
- Point 1 (P0): [FIXED] — Replaced "significantly outperforms" with "achieves competitive performance" in 4 locations (abstract, intro, Section 5.1, conclusion) to match Table 2 evidence.
- Point 2 (P1): [DEFERRED] — Requires cross-domain experiment on {dataset}. Estimated effort: 2 weeks. Recommend either running experiment or weakening generalization claim. User decision needed.
- Point 3 (P2): [FIXED] — Added concrete running example in Section 3.1, carried through to Section 3.3.

### Reviewer C
- Point 1 (P1): [FIXED] — Added failure case discussion after Section 5.2 covering 3 known limitations.
- Point 2 (P2): [FIXED] — Fixed Figure 2 caption to match actual results shown.

## Changes by Audit Finding
- Structural: Added experimental setup section (new Section 4.1) between method and results.
- Claims: 2 overclaimed claims weakened to match evidence. 1 unsupported claim removed.
- Blind spots: Added 2 missing citations. Added limitations paragraph.
- Positioning: Sharpened contribution statement in abstract (now 1 sentence, 22 words).
- Presentation: Fixed 3 long sentences (>40 words). Reduced jargon in Section 3.
- Strategic: Promoted scaling result to abstract and introduction hook.

## Remaining Issues
1. Cross-domain experiment (Reviewer B, Point 2, P1) — requires new experiments, ~2 weeks effort — recommend `/paper evaluate` or weaken claim
2. Additional dataset evaluation (P2) — would strengthen paper but not blocking — target for camera-ready
3. Improved Figure 1 visualization (P3) — cosmetic, low priority
4. Extended related work on {subtopic} (P3) — nice to have, not required by reviewers
```

## Failure Recovery

| Scenario | Detection | Recovery |
|----------|-----------|----------|
| **P0 issue requires new experiments** | A critical issue (e.g., missing baseline, unsupported core claim) cannot be fixed with text changes alone. | Cannot fix in the refine phase alone. Present to user with two options: (a) backtrack to `/paper evaluate` to run the experiment (estimate effort), or (b) weaken the claim to match existing evidence. Do not silently weaken claims — get user approval. |
| **Too many changes destabilize the draft** | v2 diverges significantly from v1 (>30% of paragraphs changed, or structural reorganization). | Re-run the health check from Phase 5 (Write) on the v2 draft. Specifically: verify story arc coherence, check that all sections still connect logically, and confirm no orphan references or broken cross-references. |
| **Scorecard shows regression after fixes** | After re-check in Step 5, one or more scorecard items that were previously met are now unmet. | A fix broke something. Identify which specific fix caused the regression by comparing the changed sections against the regressed scorecard item. Revert that fix and find an alternative approach that addresses the original issue without the regression. |
| **Conflicting reviewer advice** | Reviewer A says "add more detail" and Reviewer B says "paper is too long" for the same section. | Do not try to satisfy both literally. Identify the underlying concern (usually: the section has low information density). Fix the root cause: tighten prose, move details to appendix, or restructure. Document the conflict and resolution in the changelog. |

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

### Step 4.5 — Reverse Outline Verification

After claim re-check, verify narrative coherence at the paragraph level:

1. **Extract topic sentences** — For each paragraph in v2, identify its single main point (usually the first sentence).
2. **Build reverse outline** — List the topic sentences in order. Read only the outline — does it tell a coherent story from problem → method → evidence → impact?
3. **Check paragraph-to-thesis mapping** — Every paragraph's topic sentence must support the section's thesis. Flag any paragraph that cannot be mapped → candidate for deletion or rewrite.
4. **Check inter-paragraph flow** — Between consecutive paragraphs, there should be a logical connector (cause/contrast/consequence/refinement/example). Flag any abrupt transitions where the reader would ask "why is this here now?"
5. **Fix issues found:**
   - Unmappable paragraphs → delete, merge into adjacent paragraph, or rewrite with clear connection
   - Missing transitions → add a linking sentence or connective phrase
   - Topic sentence buried mid-paragraph → promote it to the opening position

Document any changes in v2-changelog.md under a "Narrative Coherence" subsection.

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
~/.paper/projects/{name}/drafts/v2-refined.md
```

Also write a change log:

```
~/.paper/projects/{name}/drafts/v2-changelog.md
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
- [ ] Reverse outline verification passed — no unmappable paragraphs, no abrupt transitions

If any check fails, continue fixing before transitioning.

## Failure Recovery

If a health check fails:

1. **P0/P1 issues remain unaddressed** — Do not transition. If the issue requires user input (e.g., new experiments), present the blocker explicitly and wait for a decision. If the issue is fixable with text changes, fix it now.
2. **v2-changelog.md is incomplete** — Review every change made to the draft and ensure each is documented. Cross-reference against the triaged issue list — every issue should appear in the changelog as either FIXED or DEFERRED with rationale.
3. **Claims re-check shows new unsupported claims** — A fix introduced a new problem. Identify which fix caused it (check recently modified sections), and either revert or add supporting evidence.
4. **Scorecard shows regression** — Compare pre-refine and post-refine scorecard side by side. Identify the regressed item, find the responsible change, and fix without re-introducing the original issue.

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

RECOMMENDATION: /paper ship because the paper is polished
and ready for venue selection and formatting.

A) Continue to /paper ship (recommended)
B) Go deeper — another round of refinement
C) Backtrack to /paper evaluate — needs more evidence
D) Save progress and stop here

Rate this phase? (1-5, or skip)
```
