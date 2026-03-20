---
name: paper-architect
description: Design the system or method architecture, mapping components to gaps and identifying what is novel vs adapted.
---

# /paper architect — Phase 3: Design Your Method

Transforms the contribution statement and inspiration into a concrete system or method architecture.

## Variables

```bash
PY=~/.claude/skills/notebooklm-paper/.venv/bin/python3
SKILL=~/.claude/skills/notebooklm-paper
```

## Input

Read from the active project directory (`~/.notebooklm-paper/projects/{name}/`):
- `position.md` — contribution statement, novelty claims, research questions
- `inspiration-map.md` — transferable methods and building blocks from the discover phase

If `position.md` is missing, warn the user and recommend `/paper position`.

## Variable Shortcuts

| Shortcut | Expansion |
|----------|-----------|
| `$PY` | `~/.claude/skills/notebooklm-paper/.venv/bin/python3` |
| `$SKILL` | `~/.claude/skills/notebooklm-paper` |

## Quality Rubric

### Universal Dimensions

- **Specificity** — Each component has concrete inputs, outputs, algorithm description, and connection points. Not "processes the data" but "takes N×D feature matrix, applies self-attention with 8 heads, outputs N×D contextualized embeddings."
- **Traceability** — Every component traces to a gap from position.md. Every adapted technique traces to a source in inspiration-map.md. Component-to-gap mapping is complete.
- **Completeness** — 3-7 components defined, system diagram present, novel vs. adapted clearly separated, assumptions/limitations documented, scorecard updated.

### Phase-Specific Dimensions

- **Ablation readiness** — Each component can be independently evaluated. The architecture supports ablation studies: removing or replacing any single component should be feasible and meaningful.
- **Baseline feasibility** — The architecture implies realistic baselines. Each design choice has an obvious "what if we didn't do this?" alternative that can serve as an ablation baseline.

## Anti-patterns

1. **Hand-wavy components** — DON'T: "The feature extractor processes inputs into useful representations." DO INSTEAD: "The feature extractor is a 6-layer Transformer encoder that takes tokenized input (max 512 tokens) and outputs 768-dimensional hidden states for each position."

2. **Monolithic design** — DON'T: Design a single end-to-end system with no clear component boundaries. DO INSTEAD: Break into 3-7 components with defined interfaces. Each component should be independently testable and replaceable.

3. **All novel, nothing grounded** — DON'T: Claim every component is novel. Reviewers are suspicious when nothing is adapted from existing work. DO INSTEAD: Clearly label what is novel, what is adapted (and how), and what is off-the-shelf. A good paper typically has 1-2 novel components and several adapted/standard ones.

4. **Missing failure modes** — DON'T: Skip the "when does this break?" analysis. DO INSTEAD: For each component, state the conditions under which it degrades or fails. This shows intellectual honesty and helps scope the evaluation.

## Structural Exemplar

```markdown
# Architecture — {Project Name}

## System Overview

**Method name**: {Name}
**Type**: {framework / algorithm / system}
**Core idea**: {One sentence: how it works at the highest level}

### Architecture Diagram
```
Input → [Component A: {purpose}] → [Component B: {purpose}] → Output
              |                            ^
              v                            |
         [Component C: {purpose}] --------+
```

## Components

### {Component 1 Name}
**Purpose**: {what it does in the system}
**Technique**: {specific algorithm/approach}
**Novel or adapted**: {Novel / Adapted from [Paper X], modified by [what]}
**Addresses gap**: {G1: gap description}
**Inputs**: {data format, shape, source}
**Outputs**: {data format, shape, destination}

## Novel vs Adapted

### Novel
- {Component}: {why this is new — what didn't exist before}

### Adapted
- {Component}: from {source}, changed {what and why}

### Standard
- {Component}: uses {standard technique} without modification

## Assumptions and Limitations
- Assumes {X} — fails when {Y}
- Limited to {scope} — does not handle {out-of-scope}
```

## Workflow

### Step 1 — Review position and inspiration

Read `position.md` and `inspiration-map.md`. Summarize back to the user:

```
PROJECT: {name} — Phase 3/8 (Architect)

Contribution: {contribution statement}
Claims: {list claims}
Key building blocks from discover: {list techniques from inspiration-map}

Ready to design the architecture. Any constraints or preferences before we start?
```

Wait for user confirmation or additional constraints (e.g., must run on edge devices, must be differentially private, latency budget).

### Step 2 — Design overall approach

Propose a high-level approach:

- **Method name**: {working name from position or refined}
- **Type**: {e.g., framework, algorithm, system, protocol, model architecture}
- **Core idea in one sentence**: {how it works at the highest level}
- **Why this approach**: {why this design over alternatives}

### Step 3 — Component breakdown

Break the method into 3-7 components. For each component:

| Component | Purpose | Technique | Novel or Adapted | Addresses Gap |
|-----------|---------|-----------|-------------------|---------------|
| {name} | {what it does} | {how it works} | {Novel / Adapted from [paper]} | {gap ID} |

For each component, describe:
1. **What it does** — its role in the overall system
2. **How it works** — the technique or algorithm used
3. **Inputs and outputs** — what data flows in and out
4. **How it connects** to other components

Present the component table and ask the user if the breakdown makes sense before proceeding to details.

### Step 4 — System overview diagram

Create an ASCII diagram showing how components connect:

```
Input -> [Component A] -> [Component B] -> Output
              |                ^
              v                |
         [Component C] -------+
```

Or describe the architecture clearly enough that the user could draw it. Include:
- Data flow direction
- Component interactions
- External dependencies (datasets, APIs, models)
- Feedback loops if any

### Step 5 — Component-to-gap mapping

Verify that every gap identified in `position.md` is addressed by at least one component:

```
Gap G1: "{gap description}" -> Component A + Component C
Gap G2: "{gap description}" -> Component B
Gap G3: "{gap description}" -> Component A
```

If any gap is unmapped, either:
- Design a new component to address it
- Explain why it is out of scope (and update claims accordingly)

### Step 6 — Novel vs adapted inventory

Clearly separate what is new from what is borrowed:

**Novel contributions:**
- {component or technique}: {why it is new}

**Adapted from existing work:**
- {component}: adapted from {paper/method}, modified by {what changed and why}

**Standard/off-the-shelf:**
- {component}: uses {standard technique} without modification

This inventory feeds directly into the "Related Work" and "Our Approach" sections of the paper.

### Step 7 — Threat model and assumptions (if applicable)

For security, systems, or protocol papers, document:
- **Threat model**: What adversary capabilities are assumed
- **Trust assumptions**: What entities or components are trusted
- **Out-of-scope threats**: What is explicitly not defended against

For non-security papers, document:
- **Assumptions**: What must be true for the method to work
- **Limitations by design**: What the architecture intentionally does not handle
- **Failure modes**: When/how the system degrades

### Step 8 — Scorecard update

Update the scorecard for architecture-related requirements:

```bash
$PY $SKILL/scripts/run.py scorecard show
```

For any met requirements, update:

```bash
$PY $SKILL/scripts/run.py scorecard update "Formal threat model" met architect
$PY $SKILL/scripts/run.py scorecard update "Clear method description" met architect
$PY $SKILL/scripts/run.py scorecard update "Component justification" met architect
```

## Output

Write `~/.notebooklm-paper/projects/{name}/architecture.md` with this structure:

```markdown
# Architecture — {Project Name}

## System Overview

**Method name**: {name}
**Type**: {framework / algorithm / system / protocol / model}
**Core idea**: {one-sentence description}

### Architecture Diagram

{ASCII diagram or structured description}

## Components

### {Component 1 Name}

**Purpose**: {what it does}
**Technique**: {how it works}
**Novel or adapted**: {Novel / Adapted from [source]}
**Addresses gap**: {gap ID and description}
**Inputs**: {what data it receives}
**Outputs**: {what it produces}
**Details**: {2-5 sentences on implementation approach}

### {Component 2 Name}
{same structure}

### {Component N Name}
{same structure}

## Component-to-Gap Mapping

| Gap | Description | Components |
|-----|-------------|------------|
| G1 | {description} | {Component A, Component C} |
| G2 | {description} | {Component B} |

## Novel vs Adapted

### Novel
- {item}: {explanation}

### Adapted
- {item}: from {source}, changed {what and why}

### Standard
- {item}: {standard technique used}

## Assumptions and Constraints

{Threat model for security papers, or assumptions/limitations for others}

### Assumptions
- {assumption 1}
- {assumption 2}

### Limitations by Design
- {limitation 1}
- {limitation 2}

### Failure Modes
- {condition}: {what happens}
```

## Health Check

Before completing this phase, verify:

1. Every gap from `position.md` is mapped to at least one component:
   - Read position.md gaps, cross-reference with Component-to-Gap Mapping
   - If any gap is unmapped, flag it
2. Every claim from position has a plausible path to evidence through the architecture
3. Novel vs adapted is clearly separated (no ambiguity about what is new)
4. Scorecard updated for architecture-related requirements:
   ```bash
   $PY $SKILL/scripts/run.py scorecard show
   ```

If the health check reveals unmapped gaps, iterate on the architecture before proceeding.

## Failure Recovery

1. **Architecture can't address a key gap** — If a gap from position.md has no component mapped to it: Either design a new component specifically for that gap, or revisit position.md to remove claims about that gap. Don't leave unmapped gaps — they become unsupported claims.

2. **Too many components (>7)** — The architecture is overengineered. Merge components that always operate together. Ask: "Can these two components be described as one with a clear interface?" If yes, merge.

3. **No clear novel contribution in the architecture** — If everything is adapted or standard, the novelty must be in the combination or the application domain. Explicitly state: "The novelty is not in individual components but in their combination to address {gap}." If even the combination isn't novel, backtrack to `/paper position`.

## Phase Transition

Use the standard phase transition template from the root SKILL.md.

```
RECOMMENDATION: /paper evaluate because the architecture is designed and needs experimental validation.

A) Continue to /paper evaluate (recommended)
B) Go deeper — refine component details or add formal specifications
C) Backtrack to /paper discover — "Design doesn't hold, need better building blocks"
D) Backtrack to /paper position — "Architecture reveals the contribution needs rethinking"
E) Save progress and stop here
```

Backtrack triggers:
- Architecture cannot address a key gap -> `/paper discover` (find better building blocks)
- Design reveals the contribution is not feasible -> `/paper position` (redefine contribution)
- Too many components are adapted with no novelty -> `/paper discover` or `/paper position`
