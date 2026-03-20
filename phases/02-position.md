---
name: paper-position
description: Define your research contribution, novelty claims, and differentiation from closest related work.
---

# /paper position — Phase 2: Define Your Contribution

Transforms gap analysis and scouted inspiration into a clear contribution statement with novelty claims.

## Variables

```bash
PY=~/.claude/skills/notebooklm-paper-skill/.venv/bin/python3
SKILL=~/.claude/skills/notebooklm-paper-skill
```

## Input

Read from the active project directory (`~/.notebooklm-paper-skill/projects/{name}/`):
- `gaps.md` — prioritized research gaps from the discover phase
- `inspiration-map.md` — transferable methods and ideas from the discover phase

If either file is missing, warn the user and recommend the corresponding phase (`/paper discover`).

## Quality Rubric

### Universal dimensions

- **Specificity** — Contribution statement names the exact technique, the exact gap, and the exact benefit. Not "We improve X" but "We combine [technique A] with [technique B] to address [gap G], reducing [metric] by [amount] on [benchmark]."
- **Traceability** — Every claim traces to a specific gap from gaps.md. Every differentiation point traces to a specific paper from field-map.md or inspiration-map.md.
- **Completeness** — 2-5 numbered claims added to claims.json. Comparison matrix initialized with 3+ papers. Research questions formulated for architect/evaluate phases.

### Phase-specific dimensions

- **Falsifiability** — Every claim is testable. "Our method is better" is not falsifiable. "Our method achieves >=15% improvement on [specific metric] over [specific baseline] on [specific dataset]" is falsifiable.
- **Differentiation clarity** — For each of the top-3 closest papers, the differentiation is stated in one sentence that a non-expert could understand. Not "We use a different architecture" but "Unlike [Paper X] which requires labeled data, our approach learns from unlabeled examples."

## Anti-patterns

1. **Category-level positioning** — DON'T: "We address the problem of NLP for healthcare." DO INSTEAD: "We address medication extraction from unstructured clinical notes where existing NER models miss multi-word drug names."

2. **Incremental-disguised-as-novel** — DON'T: Claim novelty for combining two existing techniques in an obvious way. EXAMPLE: "We propose using BERT with attention for classification." DO INSTEAD: Articulate what the combination enables that neither technique alone could achieve. If you can't, the contribution may be incremental.

3. **Unfalsifiable claims** — DON'T: "Our framework provides a comprehensive solution." DO INSTEAD: "Our framework handles [specific cases A, B, C] that [baseline] cannot, as demonstrated in Section 4.2, Table 3."

4. **Missing closest competitor** — DON'T: Differentiate against strawman baselines from 5+ years ago. DO INSTEAD: Identify the strongest recent work (last 2 years) and articulate the specific delta. If you can't beat the closest competitor, reframe the contribution.

## Structural Exemplar

```markdown
# Position — {Project Name}

## Contribution Statement

We propose **{Method Name}**, which combines {technique A from inspiration} with
{technique B} to solve {specific gap from gaps.md}. This enables {concrete benefit
that wasn't possible before}, achieving {metric improvement} on {benchmark}.

## Novelty Claims

1. C1: {Method Name} achieves {specific metric} on {benchmark}, outperforming
   {strongest baseline} by {amount} [Testable in Phase 4]
2. C2: Combining {A} with {B} enables {new capability} that neither achieves alone
   [Testable via ablation in Phase 4]
3. C3: {Specific measurable property} under conditions {X, Y, Z}
   [Testable in Phase 4]

## Differentiation from Closest Work

| Aspect | {Paper 1} | {Paper 2} | {Paper 3} | Ours |
|--------|-----------|-----------|-----------|------|
| {Key dimension from gap} | No | Partial | No | Yes |
| {Another dimension} | {detail} | {detail} | {detail} | {detail} |

## Research Questions

- RQ1: Does {method} achieve {claimed benefit} vs {baselines}?
- RQ2: How does {component} contribute to overall performance? [ablation]
- RQ3: Under what conditions does {method} fail or degrade?
```

## Workflow

### Step 1 — Select the target gap

Read `gaps.md` and present the high-priority gaps to the user.

If there are multiple high-priority gaps, ask:

```
PROJECT: {name} — Phase 2/8 (Position)

Your gap analysis found these high-priority gaps:

1. {gap 1 summary}
2. {gap 2 summary}
3. {gap 3 summary}

RECOMMENDATION: Choose [{N}] because {reason — e.g., most scouted inspiration aligns with it}

A) Gap 1 — {one-line description}
B) Gap 2 — {one-line description}
C) Gap N — {one-line description}
D) Combine gaps — address multiple in one contribution
```

If only one high-priority gap exists, confirm it with the user and proceed.

### Step 2 — Draft contribution statement

Using the selected gap and inspiration-map.md, draft a contribution statement in this format:

> We propose **X** that combines **A** + **B** to solve **gap G**, enabling **benefit**.

Where:
- **X** = the proposed method/system/framework name (suggest a working name)
- **A**, **B** = key techniques from scouted inspiration
- **G** = the specific gap being addressed
- **benefit** = what becomes possible that wasn't before

Present to user for refinement. Iterate until they approve.

### Step 3 — Novelty differentiation

Identify the top-3 closest existing papers (from gaps.md, inspiration-map.md, or project paper store). For each, articulate:

- What they do
- What they miss (the gap)
- How the proposed contribution differs

Present as a comparison table:

```
| Aspect | [Paper 1] | [Paper 2] | [Paper 3] | Ours |
|--------|-----------|-----------|-----------|------|
| Approach | ... | ... | ... | ... |
| Handles [gap aspect] | No | Partial | No | Yes |
| [Key differentiator] | ... | ... | ... | ... |
```

### Step 4 — Initialize comparison matrix

Add the closest papers and key dimensions to the comparison matrix:

```bash
# Add dimensions based on gap aspects and differentiators
$PY $SKILL/scripts/run.py matrix add-dim "Handles [gap aspect 1]"
$PY $SKILL/scripts/run.py matrix add-dim "Handles [gap aspect 2]"
$PY $SKILL/scripts/run.py matrix add-dim "[Key differentiator]"

# Add papers
$PY $SKILL/scripts/run.py matrix add-paper "Ours"
$PY $SKILL/scripts/run.py matrix add-paper "[closest paper 1]"
$PY $SKILL/scripts/run.py matrix add-paper "[closest paper 2]"
$PY $SKILL/scripts/run.py matrix add-paper "[closest paper 3]"

# Fill known values for existing papers
$PY $SKILL/scripts/run.py matrix set "[paper 1]" "[dimension]" false
# ... repeat for known cells

# Fill "Ours" with claimed values
$PY $SKILL/scripts/run.py matrix set "Ours" "[dimension]" true
```

### Step 5 — Define novelty claims

Formulate 2-5 numbered claims. Each claim should be:
- Specific and falsifiable
- Tied to a gap or differentiator
- Testable in the evaluate phase

Add each claim:

```bash
$PY $SKILL/scripts/run.py claims add "Our method [does X] better than [baseline approach]" position
$PY $SKILL/scripts/run.py claims add "Combining [A] with [B] enables [new capability]" position
$PY $SKILL/scripts/run.py claims add "[Specific measurable improvement]" position
```

### Step 6 — Formulate research questions

Derive 2-4 research questions from the claims. These guide the architect and evaluate phases:

- RQ1: Does [proposed method] achieve [claimed benefit] compared to [baselines]?
- RQ2: How does [component A] contribute to [overall performance]?
- RQ3: Under what conditions does [method] fail or degrade?

### Step 7 — Scorecard check

```bash
$PY $SKILL/scripts/run.py scorecard show
```

Check: is the novelty strong enough based on field expectations? If the scorecard has requirements like "novel contribution" or "clear differentiation," assess whether the current position meets them.

## Output

Write `~/.notebooklm-paper-skill/projects/{name}/position.md` with this structure:

```markdown
# Position — {Project Name}

## Contribution Statement

{The approved contribution statement from Step 2}

## Novelty Claims

1. {Claim C1}: {claim text}
2. {Claim C2}: {claim text}
3. {Claim CN}: {claim text}

## Differentiation from Closest Work

| Aspect | [Paper 1] | [Paper 2] | [Paper 3] | Ours |
|--------|-----------|-----------|-----------|------|
| ... | ... | ... | ... | ... |

### [Paper 1] — {title}
- What it does: {summary}
- What it misses: {gap}
- How we differ: {differentiation}

### [Paper 2] — {title}
{same structure}

### [Paper 3] — {title}
{same structure}

## Research Questions

- RQ1: {question}
- RQ2: {question}
- RQ3: {question}

## Target Gap

{Selected gap from gaps.md with full context}

## Inspiration Sources

{Key techniques from inspiration-map.md being combined}
```

## Health Check

Before completing this phase, verify:

1. At least 2 claims added to the claim-evidence chain:
   ```bash
   $PY $SKILL/scripts/run.py claims show
   ```
2. Comparison matrix has 3+ papers (including "Ours"):
   ```bash
   $PY $SKILL/scripts/run.py matrix show
   ```
3. Contribution statement is specific (not vague like "we improve X")
4. Each claim is falsifiable and testable

If any check fails, address it before proceeding.

## Failure Recovery

1. **Can't differentiate from top-3 papers** — If the closest papers already do something very similar: (a) Look for a different gap in gaps.md that's more unique, (b) Check inspiration-map.md for a cross-domain technique that creates a novel combination, (c) If no differentiation exists, backtrack to `/paper discover`.

2. **Claims feel incremental** — If claims are small improvements on existing work: Ask "What becomes POSSIBLE with this that was IMPOSSIBLE before?" If the answer is "nothing, it's just faster/better," the positioning needs work. Consider reframing: instead of "X% improvement," frame as "enables [new use case] for the first time."

3. **Too many claims (>5)** — Focus. Pick the 2-3 strongest claims that form a coherent story. Extra claims dilute the message and create more obligations for the evaluation phase.

## Phase Transition

Use the standard phase transition template from the root SKILL.md.

```
RECOMMENDATION: /paper architect because your contribution is defined and needs a concrete design.

A) Continue to /paper architect (recommended)
B) Go deeper — add more claims or refine differentiation
C) Backtrack to /paper discover — "Can't differentiate from existing work"
D) Backtrack to /paper discover — "Need better building blocks for the contribution"
E) Save progress and stop here
```

Backtrack triggers:
- Cannot clearly differentiate from top-3 papers -> `/paper discover` (find different gap) or `/paper discover` (find different inspiration)
- Contribution feels incremental -> `/paper discover` (look for bigger gaps)
- No testable claims can be formulated -> `/paper discover` (need more concrete methods)
