---
name: paper-evaluate
description: Design experiments, analyze results, validate claims with evidence, and update the comparison matrix and scorecard.
phase: 4
---

# /paper evaluate — Phase 4: Experiments and Results

Designs the evaluation plan, then analyzes results to validate each claim from the position phase.

## Variables

```bash
PY=~/.claude/skills/paper/.venv/bin/python3
SKILL=~/.claude/skills/paper
```

## Input

Read from the active project directory (`~/.paper/projects/{name}/`):
- `architecture.md` — system design with components and gap mappings
- `position.md` — claims and research questions

Also read cross-cutting state:

```bash
$PY $SKILL/scripts/run.py scorecard show
$PY $SKILL/scripts/run.py claims show
$PY $SKILL/scripts/run.py matrix show
```

If `architecture.md` is missing, warn the user and recommend `/paper architect`.

## Workflow

### Step 1 — Review claims and scorecard requirements

Summarize to the user:

```
PROJECT: {name} — Phase 4/8 (Evaluate)

Claims to validate:
  C1: {claim text}
  C2: {claim text}
  CN: {claim text}

Research questions:
  RQ1: {question}
  RQ2: {question}

Scorecard evaluation requirements:
  {list any scorecard items related to evaluation, e.g., ">=3 baselines", "ablation study", "statistical significance"}

Ready to design the evaluation. Have you already run experiments, or do we need to plan them first?
```

Branch based on user response:
- **"Plan experiments"** -> proceed to Step 2
- **"I have results"** -> skip to Step 4

### Step 2 — Design experiments

For each research question, design an experiment:

#### Metrics

Check the scorecard for what metrics the field trusts. Propose:

| Metric | What it measures | Why it matters | RQ |
|--------|-----------------|----------------|----|
| {metric 1} | {description} | {field standard / scorecard requirement} | RQ1 |
| {metric 2} | {description} | {reason} | RQ1, RQ2 |

#### Baselines

Check the scorecard for baseline requirements (e.g., ">=3 baselines"). Select baselines from the comparison matrix and position.md:

| Baseline | Why included | Source |
|----------|-------------|--------|
| {baseline 1} | {closest prior work} | {paper reference} |
| {baseline 2} | {state-of-the-art on target task} | {paper reference} |
| {baseline 3} | {ablation — our method minus key component} | Internal |

Ensure at least as many baselines as the scorecard requires.

#### Datasets

| Dataset | Size | Why chosen | Availability |
|---------|------|------------|-------------|
| {dataset 1} | {stats} | {standard benchmark / real-world} | {public / needs access} |
| {dataset 2} | {stats} | {reason} | {availability} |

#### Experiment plan

For each RQ, specify:
1. **Setup**: what is configured, trained, or deployed
2. **Procedure**: what is run and measured
3. **Expected outcome**: what would support the claim (and what would refute it)

### Step 3 — Ablation study design (if applicable)

If the architecture has multiple novel components, design ablations:

| Variant | What is removed/changed | Tests |
|---------|------------------------|-------|
| Full method | Nothing — complete system | Baseline for ablation |
| w/o Component A | Remove component A | Is A necessary? |
| w/o Component B | Remove component B | Is B necessary? |
| Replace C with standard | Swap novel C for off-the-shelf | Is the novel version of C better? |

### Step 4 — Analyze results

When the user provides results (tables, figures, raw numbers, or descriptions):

1. **Parse results** into structured tables
2. **Map each result to a claim**: does this evidence support, partially support, or refute the claim?
3. **Identify surprises**: results that are better or worse than expected

Present the analysis:

```
Results Analysis:

Claim C1: "{claim text}"
  Evidence: {Table/Figure reference}, {metric} = {value} vs baseline {value}
  Verdict: STRONG / MODERATE / WEAK / UNSUPPORTED
  Notes: {interpretation}

Claim C2: "{claim text}"
  Evidence: {reference}
  Verdict: {verdict}
  Notes: {interpretation}
```

### Step 5 — Update claims with evidence

For each claim, record the evidence:

```bash
$PY $SKILL/scripts/run.py claims validate C1 "Table 2, row 3: X outperforms Y by Z%" strong evaluate
$PY $SKILL/scripts/run.py claims validate C2 "Figure 4: consistent improvement across datasets" moderate evaluate
$PY $SKILL/scripts/run.py claims validate C3 "Table 3: ablation shows component A contributes +N%" strong evaluate
```

Use evidence strength levels:
- **strong** — clear quantitative evidence, statistically significant
- **moderate** — evidence supports claim but with caveats (e.g., not on all datasets)
- **weak** — marginal or mixed evidence
- **unsupported** — evidence does not support the claim

### Step 6 — Update comparison matrix

Fill in the "Ours" column with actual results:

```bash
$PY $SKILL/scripts/run.py matrix set "Ours" "Handles [gap aspect]" true
$PY $SKILL/scripts/run.py matrix set "Ours" "Scalable" true
$PY $SKILL/scripts/run.py matrix set "Ours" "[Metric] > threshold" true
```

Also fill in baseline results if known:

```bash
$PY $SKILL/scripts/run.py matrix set "[baseline paper]" "[dimension]" false
```

Show the updated matrix:

```bash
$PY $SKILL/scripts/run.py matrix show
```

### Step 7 — Update scorecard

Mark evaluation-related requirements as met or unmet:

```bash
$PY $SKILL/scripts/run.py scorecard update ">=3 baselines" met evaluate
$PY $SKILL/scripts/run.py scorecard update "Ablation study" met evaluate
$PY $SKILL/scripts/run.py scorecard update "Statistical significance" met evaluate
$PY $SKILL/scripts/run.py scorecard update "Open-source artifact" planned evaluate
```

Show updated scorecard:

```bash
$PY $SKILL/scripts/run.py scorecard show
```

### Step 8 — Identify limitations

Document limitations discovered during evaluation:
- Where the method underperforms
- Datasets or conditions where results are weaker
- Scalability concerns
- Threats to validity

These feed directly into the paper's Limitations section.

## Output

Write `~/.paper/projects/{name}/evaluation.md` with this structure:

```markdown
# Evaluation — {Project Name}

## Experiment Design

### Metrics

| Metric | Description | RQ |
|--------|-------------|----|
| ... | ... | ... |

### Baselines

| Baseline | Description | Source |
|----------|-------------|--------|
| ... | ... | ... |

### Datasets

| Dataset | Size | Description |
|---------|------|-------------|
| ... | ... | ... |

## Results

### Main Results

| Method | {Metric 1} | {Metric 2} | {Metric N} |
|--------|------------|------------|------------|
| {Baseline 1} | ... | ... | ... |
| {Baseline 2} | ... | ... | ... |
| {Baseline 3} | ... | ... | ... |
| **Ours** | ... | ... | ... |

### Ablation Study (if applicable)

| Variant | {Metric 1} | {Metric 2} | Delta |
|---------|------------|------------|-------|
| Full method | ... | ... | — |
| w/o Component A | ... | ... | ... |
| w/o Component B | ... | ... | ... |

## Claim-Evidence Mapping

| Claim | Evidence | Strength | Notes |
|-------|----------|----------|-------|
| C1: {text} | {reference} | Strong | {interpretation} |
| C2: {text} | {reference} | Moderate | {interpretation} |
| CN: {text} | {reference} | {level} | {interpretation} |

## Research Question Answers

- **RQ1**: {answer with evidence reference}
- **RQ2**: {answer with evidence reference}
- **RQN**: {answer}

## Limitations

- {limitation 1}: {description and impact}
- {limitation 2}: {description and impact}
- {limitation N}: {description and impact}
```

## Health Check

Before completing this phase, verify:

1. All claims from position phase have evidence (strong or moderate):
   ```bash
   $PY $SKILL/scripts/run.py claims show
   ```
   If any claim is weak or unsupported, flag it and discuss with user.

2. Scorecard evaluation requirements are updated:
   ```bash
   $PY $SKILL/scripts/run.py scorecard show
   ```

3. Comparison matrix "Ours" column is filled:
   ```bash
   $PY $SKILL/scripts/run.py matrix show
   ```

4. Each research question has an answer supported by evidence.

If claims are unsupported, discuss with user:
- Can the claim be weakened to match the evidence?
- Is more experimentation needed?
- Should the claim be dropped?

## Phase Transition

Use the standard phase transition template from the root SKILL.md.

```
RECOMMENDATION: /paper write because claims are validated and the evaluation is complete.

A) Continue to /paper write (recommended)
B) Go deeper — run additional experiments or ablations
C) Backtrack to /paper architect — "Results don't support claims, need to redesign"
D) Backtrack to /paper position — "Evidence suggests a different contribution than claimed"
E) Save progress and stop here
```

Backtrack triggers:
- Majority of claims unsupported -> `/paper architect` (redesign method) or `/paper position` (redefine contribution)
- Results show the method is not better than baselines -> `/paper architect` (improve design)
- Missing a critical baseline or metric -> stay in evaluate and extend experiments
- Unexpected negative result reveals a flaw -> `/paper architect`
