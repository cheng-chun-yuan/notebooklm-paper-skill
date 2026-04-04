---
name: paper-eval
description: "Run binary eval criteria against phase outputs to measure quality. Reports pass/fail per criterion with scores."
---

# /paper eval — Evaluate Phase Output Quality

Run binary eval criteria against your phase outputs to measure quality objectively.

## Variable Shortcuts

```bash
PAPER_SKILL=~/.claude/skills/paper
PY=$PAPER_SKILL/.venv/bin/python3
```

## Workflow

### Step 1 — Determine scope

If the user specifies a phase (e.g., `/paper eval write`), evaluate that phase only.
If no phase specified, evaluate all phases that have artifacts.

Map phase names to numbers:
- position → 04
- architect → 05
- write → 07
- review → 08
- audit → 09
- refine → 10
- venue → 11

### Step 2 — Run eval

```bash
# Single phase
$PY $PAPER_SKILL/scripts/run.py eval run {phase_number}

# All phases with artifacts
$PY $PAPER_SKILL/scripts/run.py eval run
```

### Step 3 — Present results

Show results in a clear table:

```
Eval Results — {project name}

Phase 07 (write): 8/10 (80.0%)
  [PASS] P7-01: v1-draft.md exists and is non-empty
  [PASS] P7-02: Abstract section present
  [FAIL] P7-03: Introduction section present
         Check 'file_contains' failed with params {...}
  ...

Overall: {total_passed}/{total_criteria} ({percentage}%)
```

### Step 4 — Recommendations

Based on results:
- If a phase scores < 60%: recommend re-running that phase
- If a phase scores 60-80%: list the specific failing criteria as improvement targets
- If a phase scores > 80%: phase is healthy, note any remaining gaps

## Other Commands

### Show criteria

```bash
$PY $PAPER_SKILL/scripts/run.py eval show [phase_number]
```

Shows the binary criteria defined for each phase without running them.

### View history

```bash
$PY $PAPER_SKILL/scripts/run.py eval results [phase_number]
```

Shows past eval runs with timestamps and scores. Useful for tracking improvement over time.

## Eval Criteria Design

Each phase has 5-10 binary (pass/fail) criteria stored as JSON in `scripts/eval/criteria/phase-{NN}.json`.

**Universal dimensions checked across all phases:**
- **Specificity** — output contains concrete details, not vague generalities
- **Traceability** — output references prior phase artifacts
- **Completeness** — all required sections/elements are present

**Criteria types:**
- `file_exists` — artifact file was created
- `file_nonempty` — artifact has content
- `file_contains` — artifact contains expected section/keyword
- `file_section_count` — artifact has minimum number of sections
- `json_field` — JSON artifact has expected field with minimum items
- `word_count` — artifact meets minimum word count

## Adding Custom Criteria

To add criteria for a phase, edit `scripts/eval/criteria/phase-{NN}.json`:

```json
{
  "id": "P7-11",
  "description": "Abstract is under 300 words",
  "check": "word_count",
  "params": {"filepath": "drafts/v1-draft.md", "min_words": 100, "max_words": 300}
}
```

## Phase Transition

This is a utility command — no phase transition. After running eval, recommend:

```
Eval complete. {passed}/{total} criteria passed ({percentage}%).

A) Fix failing criteria — address specific issues listed above
B) Continue to next phase — if score is acceptable
C) Re-run phase — if score is below 60%
```
