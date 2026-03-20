---
name: paper-scout
description: "Phase 3: Scout. Search adjacent fields for methods that partially solve identified gaps. Find transferable techniques and combinable approaches."
phase: 3
---

# /paper scout — Phase 3: Scout

## Input

- `~/.paper-skill/projects/{name}/gaps.md` from Phase 2 (Gap Analysis)
- Top-ranked gaps with importance, feasibility, and novelty scores

## Variable Shortcuts

```bash
PAPER_SKILL=~/project/lab/trust_ai_identity/paper-skill
PY=$PAPER_SKILL/.venv/bin/python3
```

## Workflow

### Step 1 — Select gaps to scout

Read the gap analysis:

```bash
$PY $PAPER_SKILL/scripts/run.py scorecard show
```

Select the top 2-3 gaps by composite score for scouting. Gaps with high importance but low feasibility are especially good candidates — adjacent fields may have solved the feasibility problem in a different context.

### Step 2 — Cross-domain search

For each selected gap, search at least 3 adjacent domains for related methods. The key insight: a problem unsolved in domain A may be routine in domain B.

For each gap, formulate cross-domain queries:

```bash
# Template: "How is [problem X] solved in [domain Z]?"
$PY $PAPER_SKILL/scripts/run.py search --query "robust optimization under distribution shift" --sources arxiv semantic_scholar
$PY $PAPER_SKILL/scripts/run.py search --query "causal inference for fairness" --sources arxiv semantic_scholar
$PY $PAPER_SKILL/scripts/run.py search --query "efficient attention mechanisms in computer vision" --sources arxiv semantic_scholar
```

**Domain selection heuristic**: For each gap, consider:
- The parent field (e.g., if NLP gap, try ML broadly)
- Sibling fields (e.g., if NLP gap, try computer vision or speech)
- Application domains (e.g., if theoretical gap, try systems or HCI)
- Classical methods (e.g., if deep learning gap, try statistics or optimization)
- Distant fields (e.g., if CS gap, try biology, physics, economics)

Try at least 3 different adjacent domains per gap. Cast a wide net.

### Step 3 — Partial method discovery

For each promising method found, assess what percentage of the gap it covers:

- **What piece does it solve?** — Map the method's capability to the gap's requirements
- **What piece is missing?** — Identify the remaining unsolved portion
- **Why does it only partially work?** — Is it a domain mismatch, scale issue, or missing component?

A method that solves 60-70% of a gap is ideal — it gives you a foundation while leaving room for genuine contribution.

### Step 4 — Combinability analysis

After finding partial methods, analyze whether they can be combined:

1. **Complementary coverage** — Do methods A and B cover different pieces of the same gap? If A covers 60% and B covers a different 50%, combining could reach 90%.

2. **Glue logic** — What engineering or theoretical work is needed to combine them?
   - Data format conversion?
   - Loss function modification?
   - Architecture adapter?
   - New theoretical framework unifying both?

3. **Novelty assessment** — What is genuinely new vs assembled from existing parts?
   - If the combination is novel, that IS a contribution
   - If the glue logic requires new theory, that IS a contribution
   - If it's just plugging A into B, that's engineering, not research

### Step 5 — Build inspiration map

Compile all findings into a structured inspiration map.

Save to `~/.paper-skill/projects/{name}/inspiration-map.md` with this format:

```markdown
# Inspiration Map — {project name}

## Summary
{2-3 paragraph overview of cross-domain findings}

## Method-Gap Matrix

| Gap | Partial Fix | From Domain | Coverage | Missing Piece |
|-----|-------------|-------------|----------|---------------|
| {gap title} | {method name} | {source domain} | ~X% | {what's left} |
| ... | ... | ... | ... | ... |

## Detailed Analysis

### Gap: {title}

#### Method 1: {name} from {domain}
- **Source paper**: {citation}
- **What it does**: {description}
- **Coverage**: ~X% of the gap
- **Missing piece**: {what remains}
- **Adaptation needed**: {what changes for your domain}

#### Method 2: ...

### Combinability

#### Combination A: {Method X} + {Method Y}
- **Combined coverage**: ~X%
- **Glue logic needed**: {description}
- **Novelty of combination**: High / Medium / Low
- **Risk level**: High / Medium / Low

## Domains Searched

| Gap | Domains Tried | Productive Domains | Dead Ends |
|-----|---------------|-------------------|-----------|
| ... | ... | ... | ... |

## Key Insights
{What surprised you? What patterns emerged across domains?}
```

## Commands Reference

```bash
# Search (reuses search infrastructure)
$PY $PAPER_SKILL/scripts/run.py search --query "..." --sources arxiv semantic_scholar

# Survey tools (for downloading newly found papers)
$PY $PAPER_SKILL/scripts/run.py survey download

# Cross-cutting
$PY $PAPER_SKILL/scripts/run.py scorecard show
```

## Output

- `~/.paper-skill/projects/{name}/inspiration-map.md` — Cross-domain method analysis with combinability assessment

## Cross-Cutting Updates

No scorecard or claims updates in this phase. The scout phase is exploratory — findings feed into the Position phase where concrete claims and contributions are defined.

## Health Check

Before completing this phase, verify:

- [ ] At least 2 gaps have scouted methods from different domains
- [ ] Each scouted method has coverage percentage and missing piece identified
- [ ] At least 3 adjacent domains were searched per top gap
- [ ] inspiration-map.md exists with the method-gap matrix populated
- [ ] At least 1 combinability analysis was performed

If any check fails, continue working on the phase. Do not transition.

## Phase Transition

When all health checks pass:

```
STATUS: DONE — Scout complete

Scouted {N} methods across {M} domains for {K} gaps.
Most promising lead: {method} from {domain} covers ~X% of "{gap title}".
Combination opportunity: {brief description if found}.

Cross-cutting status:
  Scorecard: X/Y requirements met
  Claims: 0/0 (none yet — claims come in Position phase)
  Matrix: N papers tracked

RECOMMENDATION: /paper position because you have gaps and potential
methods — now define what YOUR specific contribution will be.

A) Continue to /paper position (recommended)
B) Go deeper — scout more domains or investigate promising leads further
C) Backtrack to /paper survey — no usable techniques found, widen survey scope
D) Save progress and stop here

Rate this phase? (1-5, or skip)
```

**Backtrack trigger**: If no scouted method covers more than 30% of any top gap, recommend backtracking to `/paper survey` with a broader scope to discover more related work and potentially redefine the gaps.
