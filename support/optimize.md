---
name: paper-optimize
description: "Autoresearch-style self-optimization. Mutates a phase's SKILL.md one change at a time, scores against binary eval criteria, keeps improvements, reverts regressions."
---

# /paper optimize — Self-Optimize Phase Prompts

Adapted from the autoresearch pattern: autonomously improve a phase's SKILL.md through binary eval loops.

## Variable Shortcuts

```bash
PAPER_SKILL=~/.claude/skills/paper
PY=$PAPER_SKILL/.venv/bin/python3
```

## Prerequisites

Before running optimize:
1. The target phase must have binary eval criteria in `scripts/eval/criteria/phase-{NN}.json`
2. You need a test topic to run the phase against (the optimizer runs the phase, evaluates output, mutates, repeats)
3. An active project must exist (to store test outputs)

## Workflow

### Step 1 — Gather inputs

Ask the user:

```
/paper optimize — Self-Optimization Loop

Which phase do you want to optimize?
A) Position (04)
B) Architect (05)
C) Write (07)
D) Review (08)
E) Audit (09)
F) Refine (10)
G) Venue (11)

How many experiments? (default: 5, max: 20)
What research topic to test against? (e.g., "federated learning for medical imaging")
```

### Step 2 — Establish baseline

1. Back up the current phase SKILL.md:
   ```bash
   cp $PAPER_SKILL/phases/{NN}-{name}.md $PAPER_SKILL/phases/{NN}-{name}.md.baseline
   ```

2. Run the phase on the test topic (this requires simulating the phase execution)

3. Run eval against the output:
   ```bash
   $PY $PAPER_SKILL/scripts/run.py eval run {NN}
   ```

4. Record the baseline score as Experiment #0

### Step 3 — Mutation loop

For each experiment (1 to N):

1. **Analyze failures** — Read the eval results. Identify which criteria failed.

2. **Propose ONE mutation** — Change exactly one thing in the phase's SKILL.md that addresses a failing criterion. Examples of good mutations:
   - Add a specific instruction for a missing output element
   - Add an anti-pattern that addresses a common failure mode
   - Strengthen a quality gate with more specific language
   - Add a structural exemplar for a section that's often weak

   **Bad mutations (DO NOT):**
   - Rewrite the entire file
   - Add 10 rules at once
   - Make vague instructions ("be more specific")
   - Remove existing functionality

3. **Apply the mutation** — Edit the phase SKILL.md

4. **Run the phase** on the same test topic

5. **Evaluate** — Run eval:
   ```bash
   $PY $PAPER_SKILL/scripts/run.py eval run {NN}
   ```

6. **Keep or revert:**
   - If score IMPROVED → keep the mutation, log it as successful
   - If score UNCHANGED → revert (avoid complexity creep)
   - If score DECREASED → revert immediately

7. **Log the experiment:**
   ```
   Experiment #{N}:
   - Mutation: {what changed}
   - Reason: {why — which failing criterion}
   - Before: {score}
   - After: {score}
   - Decision: KEEP / REVERT
   ```

### Step 4 — Stop conditions

Stop the loop when ANY of:
- Budget exhausted (N experiments reached)
- Score reaches 95%+ for 3 consecutive experiments
- User interrupts
- No failing criteria left to address

### Step 5 — Report results

```
Optimization Complete — Phase {NN} ({name})

Baseline: {X}/{Y} ({Z}%)
Final:    {X}/{Y} ({Z}%)
Experiments: {N} run, {K} mutations kept, {R} reverted

Mutations kept:
1. {mutation description} — improved {criterion} (+{delta})
2. {mutation description} — improved {criterion} (+{delta})

Still failing:
- {criterion}: {reason it's hard to fix}

Changelog saved to: {path}
```

## Output

Save the optimization log to:
```
~/.paper/optimize/{phase}-{timestamp}/
├── changelog.md        # Detailed mutation log
├── baseline.md         # Original SKILL.md backup
├── results.json        # Per-experiment scores
└── summary.md          # Human-readable summary
```

## Guard Rails

1. **Backup first** — Always backup the original SKILL.md before starting
2. **One mutation at a time** — Scientific method: change one variable so you know what caused the effect
3. **Revert on regression** — Never keep a change that makes things worse
4. **Revert on neutral** — Don't add complexity without improvement
5. **Budget cap** — Default 5 experiments, max 20. Don't run forever.
6. **Preserve functionality** — Mutations can ADD instructions, STRENGTHEN language, or REFINE structure. They must NOT remove existing workflow steps, health checks, or phase transitions.

## Feedback Integration

If the project has feedback data (`~/.paper/feedback/`), read it before starting:
- Low ratings (1-3) on a phase suggest specific areas to target
- Comments from users provide qualitative signal about what's weak
- Weight mutations toward addressing feedback themes

## Important Notes

- This command modifies SKILL.md files in the paper-skill installation directory
- Changes are tracked in git — you can always `git diff` to see what changed
- The optimizer is NOT fully autonomous — it runs within a Claude Code session and uses Claude's judgment for mutations
- For best results, use 3-5 diverse test topics across different domains to avoid overfitting prompts to one field
