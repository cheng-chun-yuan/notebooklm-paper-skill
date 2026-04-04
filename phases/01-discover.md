---
name: paper-discover
description: "Phase 1: Discover. Survey literature, analyze gaps, and scout cross-domain methods — all in one phase."
phase: 1
---

# /paper discover — Phase 1: Discover the Landscape

## Input

- User-provided research topic or query
- Optional: year filter, venue filter, specific paper URLs

## Variable Shortcuts

```bash
PAPER_SKILL=~/.claude/skills/paper
PY=$PAPER_SKILL/.venv/bin/python3
```

## Quality Rubric

### Universal Dimensions

- **Specificity** — Field map has concrete percentages for success patterns (e.g., "85% of accepted papers include ablation studies"), gap rankings use numeric scores (importance/feasibility/novelty on 1-5 scales), and scouted methods have coverage percentages (e.g., "covers ~60% of the gap").
- **Traceability** — Every gap traces to specific papers ("Papers [3], [7], [12] all assume clean data"). Every scouted method traces to a specific gap ("Method X from domain Y addresses Gap 2"). Scorecard requirements trace to field observations ("90% of surveyed papers include formal problem definitions").
- **Completeness** — At least 10 papers surveyed with the 6-question framework applied, 3+ gaps ranked with composite scores, 2+ gaps have scouted cross-domain methods (if scout stage is run), and the scorecard has 5+ requirements with weights.

### Phase-Specific Dimensions

- **Field coverage** — Papers span multiple venues (not just one conference) and multiple years (not just 2025). Multiple research groups and methodological approaches are represented. If the entire survey comes from one lab or one venue, the field map is biased.
- **Gap depth** — Gaps go beyond what papers state in their "limitations" and "future work" sections. Include at least one **blind spot** — something no paper in the field has noticed or questioned. The most valuable gaps are the ones nobody is talking about.

## Anti-Patterns

### Shallow survey
- **DON'T**: Collect 20 papers but only read abstracts.
- **DO**: Apply the 6-question framework to each paper. A survey of 10 deeply analyzed papers beats 30 skimmed ones.

### Echo chamber gaps
- **DON'T**: Only find gaps mentioned in papers' "future work" sections.
- **DO**: Also look for blind spots — assumptions the entire field shares that could be wrong. Ask: "What does every paper in this field take for granted?"

### Narrow scouting
- **DON'T**: Only search within your own field for solutions to gaps.
- **DO**: Search at least 3 adjacent domains. The most impactful methods often come from unexpected places (e.g., attention mechanisms from NLP transforming computer vision).

## Structural Exemplar

Below is the skeleton of what this phase produces. Your actual files will have real content, but the structure should match.

### field-map.md (Stage A output)

```markdown
# Field Map — {project name}

## Field Overview
{2-3 paragraphs: what this research area is about, how big it is, where it's heading}

## Key Papers
| # | Paper | Venue | Year | Citations | One-Line Contribution |
|---|-------|-------|------|-----------|-----------------------|
| 1 | ...   | ...   | ...  | ...       | ...                   |

## Methodological Trends
{What approaches are gaining traction? What's fading?}

## Success Patterns
- Formal problem definition: 90% of accepted papers
- Strong baselines comparison: 85%
- Released code/artifacts: 70%
- ...

## Impact Patterns
{Why are the most-cited papers impactful? Novel formulation? New benchmark?}

## Rejection Signals
{Common reviewer complaints: "missing comparison to X", "toy datasets only", etc.}

## Scorecard Summary
| Requirement | Weight | Rationale |
|-------------|--------|-----------|
| ...         | 0.XX   | ...       |
```

### gaps.md (Stage B output)

```markdown
# Gap Analysis — {project name}

## Summary
{2-3 paragraphs: what the gap landscape looks like}

## Top Gaps (Ranked)
### Gap 1: {title} — Score: X.X
- **Description**: ...
- **Evidence**: Papers [3], [7], [12] mention this
- **Type**: Blind spot
- **Importance**: X/5 — ...
- **Feasibility**: X/5 — ...
- **Novelty**: X/5 — ...
- **Potential direction**: ...

## Per-Paper Analysis Summary
| Paper | Claims | Actually Solves | Key Gap | Gap Type |
|-------|--------|-----------------|---------|----------|

## Field Blind Spots
{Things no paper in this field has noticed}
```

### inspiration-map.md (Stage C output, optional)

```markdown
# Inspiration Map — {project name}

## Summary
{2-3 paragraphs: cross-domain findings overview}

## Method-Gap Matrix
| Gap | Partial Fix | From Domain | Coverage | Missing Piece |
|-----|-------------|-------------|----------|---------------|

## Detailed Analysis
### Gap: {title}
#### Method 1: {name} from {domain}
- **Source paper**: ...
- **Coverage**: ~X%
- **Missing piece**: ...
- **Adaptation needed**: ...

## Combinability
### Combination A: {Method X} + {Method Y}
- **Combined coverage**: ~X%
- **Glue logic needed**: ...
- **Novelty of combination**: High / Medium / Low

## Domains Searched
| Gap | Domains Tried | Productive Domains | Dead Ends |
```

---

## Workflow

This phase has three stages. Complete them in order: A, then B, then C (optional).

---

### Stage A: Survey — Find and Analyze Papers

Collect papers, analyze acceptance patterns, build the field map, and create the acceptance scorecard.

#### A1 — Create a survey

Ask the user for their research topic. Formulate a precise search query. Create the survey:

```bash
$PY $PAPER_SKILL/scripts/run.py survey create --name "survey-name" --query "search query here" [--year-from 2020]
```

Tips for good queries:
- Use field-specific terminology, not casual language
- Include 2-3 synonyms separated by OR if the field uses multiple terms
- Add year filter to focus on recent work (last 3-5 years unless historical survey)

#### A2 — Run the search pipeline

Run the full pipeline (search + download) or run steps individually:

```bash
# Full pipeline (recommended for first run)
$PY $PAPER_SKILL/scripts/run.py survey run

# Or run steps separately for more control
$PY $PAPER_SKILL/scripts/run.py survey search       # Search only
$PY $PAPER_SKILL/scripts/run.py survey download     # Download PDFs only
```

#### A3 — Review and refine results

List and inspect what was found:

```bash
$PY $PAPER_SKILL/scripts/run.py survey list          # List all surveys
$PY $PAPER_SKILL/scripts/run.py survey show           # Show current survey details
$PY $PAPER_SKILL/scripts/run.py survey suggest        # Get suggestions for additional queries
```

If coverage is thin (fewer than 10 relevant papers), create additional surveys with refined queries. Use `survey suggest` for query ideas.

#### A4 — Upload to NotebookLM (optional but recommended)

If the user wants deep Q&A over papers:

```bash
$PY $PAPER_SKILL/scripts/run.py survey upload --notebook-url "https://notebooklm.google.com/notebook/..."
```

#### A5 — Query and report

Ask questions across the collected papers and generate a summary report:

```bash
$PY $PAPER_SKILL/scripts/run.py survey query --question "What are the main approaches to X?"
$PY $PAPER_SKILL/scripts/run.py survey report
```

#### A6 — Mine acceptance patterns

After collecting at least 10 papers, analyze them for publication patterns. This is where the survey becomes actionable intelligence rather than just a reading list.

**Identify venues and acceptance rates.** For each collected paper, determine:
- Where it was published (conference/journal name, year)
- Acceptance rate of that venue (e.g., NeurIPS ~26%, ICML ~25%, ACL ~25%)
- Tier of the venue (A*, A, B, workshop)

Record this in the field map.

**Extract success patterns.** Read through the papers and calculate what percentage of them include:
- Formal threat model or problem definition
- Comparison against strong baselines (not just ablations)
- Released artifacts (code, datasets, models)
- Theoretical analysis or proofs
- User studies or human evaluation
- Reproducibility details (hyperparams, compute budget, seeds)

These percentages become your "what the field expects" baseline.

**Extract impact patterns.** Identify the most-cited papers in the collection and determine WHY they are impactful:
- Novel formulation?
- New benchmark or dataset?
- Surprising negative result?
- Unified framework replacing fragmented approaches?

**Extract rejection signals.** From the patterns, identify common reviewer complaints in this field:
- "Missing comparison to X" (identify what X is)
- "Evaluation on toy datasets only"
- "No theoretical justification"
- "Incremental over Y"

#### A7 — Build acceptance scorecard

For each requirement identified, add it to the scorecard with the observed frequency as the weight:

```bash
$PY $PAPER_SKILL/scripts/run.py scorecard add "Strong baselines comparison" 0.85
$PY $PAPER_SKILL/scripts/run.py scorecard add "Released code/artifacts" 0.70
$PY $PAPER_SKILL/scripts/run.py scorecard add "Formal problem definition" 0.90
$PY $PAPER_SKILL/scripts/run.py scorecard add "Ablation study" 0.75
$PY $PAPER_SKILL/scripts/run.py scorecard add "Reproducibility details" 0.65
```

The weight (0.00-1.00) represents how critical this requirement is based on the field norm. 0.90 means 90% of accepted papers in this field include it.

#### A8 — Save field map

Write `field-map.md` to the project directory. It must contain:

1. **Field Overview** — 2-3 paragraph summary of the research landscape
2. **Key Papers** — Table of top papers with venue, year, citation count, one-line contribution
3. **Methodological Trends** — What approaches are gaining/losing traction
4. **Success Patterns** — The percentages from A6
5. **Impact Patterns** — What makes papers influential in this field
6. **Rejection Signals** — Common reviewer complaints
7. **Scorecard Summary** — List of requirements and weights

Save location: `~/.paper/projects/{name}/field-map.md`

---

### Stage B: Gap Analysis — Find What's Missing

Apply the 6-question framework to each surveyed paper, then aggregate to find gaps no paper addresses.

#### B1 — Load survey artifacts

Read the field map and paper collection:

```bash
$PY $PAPER_SKILL/scripts/run.py scorecard show
$PY $PAPER_SKILL/scripts/run.py survey show
```

Confirm that at least 10 papers were analyzed in Stage A. If fewer, go back and collect more.

#### B2 — Per-paper 6-question analysis

Apply the following framework to EACH surveyed paper. This is the core of gap analysis — do not skip or batch papers superficially.

For each paper, answer:

1. **What does it CLAIM to solve?**
   Read the abstract and introduction. What problem statement does the paper present? What does it promise?

2. **What does it ACTUALLY solve?**
   Look at the evaluation section, not the abstract. What do the experiments actually demonstrate? Is there a gap between the claim and the evidence?

3. **What does it FAIL to solve?**
   Read the limitations section (if present) and the conclusion's future work. What do the authors themselves acknowledge as unsolved?

4. **What does it IGNORE?**
   This is the most valuable question. What limitations are NOT stated? Examples:
   - Assumes clean data but real data is noisy
   - Tests on English only but claims "language understanding"
   - Evaluates on synthetic benchmarks but targets real-world use
   - Ignores computational cost
   - Ignores adversarial settings

5. **Why do these gaps exist?**
   Classify each gap as:
   - **Fundamental** — inherent limitation of the approach (e.g., attention is O(n^2))
   - **Engineering** — could be solved with more effort (e.g., scaling to larger datasets)
   - **Scope** — intentionally out of scope for that paper (e.g., privacy not considered)
   - **Blind spot** — the field has not noticed this gap

6. **How does this relate to YOUR work?**
   If the user's research context is known, connect this paper's gaps to potential contributions. If not yet known, note promising directions.

Save each per-paper analysis:

```bash
$PY $PAPER_SKILL/scripts/run.py gap save <paper_id> <file>
```

#### B3 — Aggregate gaps across all papers

After analyzing all papers individually, aggregate the findings:

1. **Gaps that NO paper addresses** — These are the most valuable. List problems mentioned in multiple papers' limitations that nobody has solved.

2. **Gaps that SOME papers address partially** — Problems where existing solutions are incomplete. Note what percentage of the gap is covered and what remains.

3. **Gaps only ONE paper addresses** — Potentially novel but unvalidated. Could be opportunities or dead ends.

#### B4 — Rank gaps

Rank each aggregated gap by three dimensions:

| Dimension | Question | Scale |
|-----------|----------|-------|
| **Importance** | How much does the field care? | 1-5 (5 = frequently mentioned as future work) |
| **Feasibility** | Can this realistically be solved? | 1-5 (5 = clear path forward) |
| **Novelty** | How original would a solution be? | 1-5 (5 = nobody has tried this angle) |

Compute a composite score: `importance * 0.4 + feasibility * 0.3 + novelty * 0.3`

#### B5 — Write gaps.md

Save the aggregated analysis to `~/.paper/projects/{name}/gaps.md`. Follow the structure shown in the Structural Exemplar above.

---

### Stage C: Scout — Find Methods from Other Domains (OPTIONAL)

> **When to skip this stage:** If your top gaps are addressable with methods already known within your field, skip Stage C and proceed directly to Phase 2: Position. Stage C is most valuable when your gaps require techniques that your field hasn't adopted yet.

Search adjacent fields for methods that partially solve identified gaps. Find transferable techniques and combinable approaches.

#### C1 — Select gaps to scout

Read the gap analysis:

```bash
$PY $PAPER_SKILL/scripts/run.py scorecard show
```

Select the top 2-3 gaps by composite score for scouting. Gaps with high importance but low feasibility are especially good candidates — adjacent fields may have solved the feasibility problem in a different context.

#### C2 — Cross-domain search

For each selected gap, search at least 3 adjacent domains for related methods. The key insight: a problem unsolved in domain A may be routine in domain B.

For each gap, formulate cross-domain queries:

```bash
# Template: "How is [problem X] solved in [domain Z]?"
$PY $PAPER_SKILL/scripts/run.py search --query "robust optimization under distribution shift" --sources arxiv semantic_scholar
$PY $PAPER_SKILL/scripts/run.py search --query "causal inference for fairness" --sources arxiv semantic_scholar
$PY $PAPER_SKILL/scripts/run.py search --query "efficient attention mechanisms in computer vision" --sources arxiv semantic_scholar
```

**Domain selection heuristic** — for each gap, consider:
- The parent field (e.g., if NLP gap, try ML broadly)
- Sibling fields (e.g., if NLP gap, try computer vision or speech)
- Application domains (e.g., if theoretical gap, try systems or HCI)
- Classical methods (e.g., if deep learning gap, try statistics or optimization)
- Distant fields (e.g., if CS gap, try biology, physics, economics)

Try at least 3 different adjacent domains per gap. Cast a wide net.

#### C3 — Partial method discovery

For each promising method found, assess what percentage of the gap it covers:

- **What piece does it solve?** — Map the method's capability to the gap's requirements
- **What piece is missing?** — Identify the remaining unsolved portion
- **Why does it only partially work?** — Is it a domain mismatch, scale issue, or missing component?

A method that solves 60-70% of a gap is ideal — it gives you a foundation while leaving room for genuine contribution.

#### C4 — Combinability analysis

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

#### C5 — Build inspiration map

Compile all findings into `~/.paper/projects/{name}/inspiration-map.md`. Follow the structure shown in the Structural Exemplar above.

---

## Output

This phase produces the following artifacts in `~/.paper/projects/{name}/`:

| File | Stage | Required? | Description |
|------|-------|-----------|-------------|
| `field-map.md` | A | Yes | Comprehensive field analysis with success patterns, impact patterns, and rejection signals |
| `scorecard.json` | A | Yes | Acceptance requirements with weights (0.00-1.00) based on field norms |
| `gaps.md` | B | Yes | Ranked gap list with per-paper 6-question analysis and blind spots |
| `inspiration-map.md` | C | Only if Stage C was run | Cross-domain method analysis with coverage percentages and combinability assessment |

## Commands Reference

```bash
# Survey management
$PY $PAPER_SKILL/scripts/run.py survey create --name "..." --query "..." [--year-from Y]
$PY $PAPER_SKILL/scripts/run.py survey run
$PY $PAPER_SKILL/scripts/run.py survey search
$PY $PAPER_SKILL/scripts/run.py survey download
$PY $PAPER_SKILL/scripts/run.py survey upload --notebook-url "..."
$PY $PAPER_SKILL/scripts/run.py survey query --question "..."
$PY $PAPER_SKILL/scripts/run.py survey report
$PY $PAPER_SKILL/scripts/run.py survey list
$PY $PAPER_SKILL/scripts/run.py survey show
$PY $PAPER_SKILL/scripts/run.py survey suggest

# Scorecard
$PY $PAPER_SKILL/scripts/run.py scorecard add "requirement name" 0.XX
$PY $PAPER_SKILL/scripts/run.py scorecard show
$PY $PAPER_SKILL/scripts/run.py scorecard update "requirement" met gap

# Gap analysis
$PY $PAPER_SKILL/scripts/run.py gap save <paper_id> <file>

# Cross-domain search (Stage C)
$PY $PAPER_SKILL/scripts/run.py search --query "..." --sources arxiv semantic_scholar
```

## Cross-Cutting Updates

- **Scorecard**: Initialize the acceptance scorecard with 5+ requirements extracted from field analysis. Each requirement has a weight (0.00-1.00) based on how frequently accepted papers in this field include it. During gap analysis, add "Targets field-relevant gap" as a requirement.
- **Matrix**: Optionally begin populating the comparison matrix with surveyed papers and key dimensions.

```bash
$PY $PAPER_SKILL/scripts/run.py scorecard add "Targets field-relevant gap" 0.85
$PY $PAPER_SKILL/scripts/run.py scorecard update "Targets field-relevant gap" met gap
```

## Health Check

Before completing this phase, verify all applicable checks.

### Stage A checks
- [ ] At least 10 papers analyzed (not just downloaded — actually read/summarized)
- [ ] Scorecard has 5+ requirements with meaningful weights
- [ ] `field-map.md` exists and contains all 7 sections
- [ ] At least 2 different venues represented in the collection
- [ ] Success patterns have concrete percentages, not vague statements

### Stage B checks
- [ ] At least 3 gaps identified and ranked with composite scores
- [ ] Each gap has importance, feasibility, and novelty scores
- [ ] `gaps.md` exists with all required sections
- [ ] Per-paper analysis covers the majority of surveyed papers (not just 2-3)
- [ ] At least 1 gap classified as "blind spot" (if none exist, state why)

### Stage C checks (only if Stage C was run)
- [ ] At least 2 gaps have scouted methods from different domains
- [ ] Each scouted method has coverage percentage and missing piece identified
- [ ] At least 3 adjacent domains were searched per top gap
- [ ] `inspiration-map.md` exists with the method-gap matrix populated
- [ ] At least 1 combinability analysis was performed

If any applicable check fails, continue working on the phase. Do not transition.

## Failure Recovery

If you get stuck at any stage, use these recovery strategies:

- **Survey finds <10 papers**: Broaden search terms, add synonyms, try both arXiv and Semantic Scholar. If the field is genuinely small, lower the threshold to 7 papers but note this in the field map.
- **All gaps are low-novelty (novelty <= 2/5 for every gap)**: Survey an adjacent subfield, or look for blind spots the entire field shares. Ask: "What assumption does every paper make that might be wrong?"
- **No useful cross-domain methods found**: Skip Stage C entirely and proceed to Phase 2: Position with within-field methods. Not every project needs cross-domain scouting — some gaps are best addressed with deeper work within the field.
- **Papers are behind paywalls**: Use arXiv preprints, check authors' personal pages, or use Semantic Scholar's open access filter. If a key paper is inaccessible, note it in the field map and rely on citing papers for context.

## Phase Transition

When all applicable health checks pass:

```
STATUS: DONE — Discover phase complete

Surveyed {N} papers across {M} venues. Found {K} gaps, top 3:
1. {Gap 1 title} (score: X.X) — {one line}
2. {Gap 2 title} (score: X.X) — {one line}
3. {Gap 3 title} (score: X.X) — {one line}

Field blind spots: {count} identified
Scout status: {completed / skipped}
{If scouted: Most promising lead: {method} from {domain} covers ~X% of "{gap title}"}

Cross-cutting status:
  Scorecard: {X} requirements initialized
  Claims: 0/0 (none yet — claims come in Position phase)
  Matrix: {N} papers tracked

RECOMMENDATION: /paper position because the landscape is mapped and
you know where the gaps are. Time to define YOUR contribution.

A) Continue to /paper position (recommended)
B) Go deeper — survey more papers, refine gaps, or scout more domains
C) Save progress and stop here

Rate this phase? (1-5, or skip)
```

**Backtrack triggers:**
- If ALL top gaps have novelty <= 2/5 ("field too crowded"), broaden the survey to an adjacent or emerging subfield before proceeding.
- If Stage C was run but no scouted method covers more than 30% of any top gap, consider redefining the gaps or widening the survey scope.

### The 8-Phase Pipeline

You are here: **Phase 1: Discover** (this phase). The full pipeline is:

| Phase | Name | What Happens |
|-------|------|--------------|
| **1** | **Discover** | Survey literature, analyze gaps, scout cross-domain methods |
| 2 | Position | Define your contribution, claims, and novelty angle |
| 3 | Architect | Design experiments, system architecture, evaluation plan |
| 4 | Evaluate | Run experiments, collect results, validate claims |
| 5 | Write | Draft the paper end-to-end |
| 6 | Critique | Simulate peer review, identify weaknesses |
| 7 | Refine | Address critique, strengthen arguments, polish |
| 8 | Ship | Final formatting, submission checklist, camera-ready |
