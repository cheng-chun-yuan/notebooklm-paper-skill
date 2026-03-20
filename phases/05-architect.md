---
name: paper-architect
description: Design the system or method architecture, mapping components to gaps and identifying what is novel vs adapted.
---

# /paper architect — Phase 5: Design Your Method

Transforms the contribution statement and inspiration into a concrete system or method architecture.

## Variables

```bash
PY=~/project/lab/trust_ai_identity/paper-skill/.venv/bin/python3
SKILL=~/project/lab/trust_ai_identity/paper-skill
```

## Input

Read from the active project directory (`~/.paper-skill/projects/{name}/`):
- `position.md` — contribution statement, novelty claims, research questions
- `inspiration-map.md` — transferable methods and building blocks from the scout phase

If `position.md` is missing, warn the user and recommend `/paper position`.

## Workflow

### Step 1 — Review position and inspiration

Read `position.md` and `inspiration-map.md`. Summarize back to the user:

```
PROJECT: {name} — Phase 5/11 (Architect)

Contribution: {contribution statement}
Claims: {list claims}
Key building blocks from scout: {list techniques from inspiration-map}

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

Write `~/.paper-skill/projects/{name}/architecture.md` with this structure:

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

## Phase Transition

Use the standard phase transition template from the root SKILL.md.

```
RECOMMENDATION: /paper evaluate because the architecture is designed and needs experimental validation.

A) Continue to /paper evaluate (recommended)
B) Go deeper — refine component details or add formal specifications
C) Backtrack to /paper scout — "Design doesn't hold, need better building blocks"
D) Backtrack to /paper position — "Architecture reveals the contribution needs rethinking"
E) Save progress and stop here
```

Backtrack triggers:
- Architecture cannot address a key gap -> `/paper scout` (find better building blocks)
- Design reveals the contribution is not feasible -> `/paper position` (redefine contribution)
- Too many components are adapted with no novelty -> `/paper scout` or `/paper position`
