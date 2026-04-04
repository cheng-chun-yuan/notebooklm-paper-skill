---
name: paper-analyze
description: Analyze a paper using the STAR framework (Situation, Task, Action, Result, Reflexion).
---

# /paper analyze

Performs structured analysis of a research paper using the STAR framework.

## Save Command

```bash
PY=~/.claude/skills/paper/.venv/bin/python3
SKILL=~/.claude/skills/paper

$PY $SKILL/scripts/run.py analyze save <paper_id> <file>
```

## STAR Framework

### 1. Situation — Field Context

Identify:
- **Key terms and definitions**: Core concepts the paper builds on
- **Prior techniques**: What methods existed before this work
- **Relationships**: How this work connects to the broader field
- **Research landscape**: Active debates, open questions, recent trends

### 2. Task — Problem Definition

Identify:
- **Problem statement**: What specific problem does the paper address
- **Limitations of prior work**: Why existing approaches are insufficient
- **Application scenarios**: Where the solution would be applied
- **Success criteria**: How the authors define success

### 3. Action — Method and Approach

Identify:
- **Method architecture**: Overall design and components
- **Core technical value**: The key innovation or insight
- **Algorithm or procedure**: Step-by-step description of the approach
- **Design decisions**: Why specific choices were made over alternatives

### 4. Result — Evidence and Outcomes

Identify:
- **Datasets**: What data was used for evaluation
- **Quantitative results**: Numbers, tables, metrics
- **Claim validation**: Does the evidence support each claim
- **Comparisons**: How results compare to baselines and prior work

### 5. Reflexion — Critical Assessment

Identify:
- **Areas for improvement**: Weaknesses, limitations, missing experiments
- **Research connections**: Links to related work not cited by the authors
- **QA items**: Questions that remain unanswered
- **Extension opportunities**: How this work could be built upon

## Output Template

After analyzing a paper, produce the following markdown document:

```markdown
# STAR Analysis: [Paper Title]

**Paper ID**: [id]
**Authors**: [authors]
**Year**: [year]
**Source**: [venue/arxiv]

---

## 1. Situation — Field Context

**Key terms**: [term1, term2, ...]
**Prior techniques**: [technique1, technique2, ...]
**Field relationships**: [description of how this work fits in the field]

## 2. Task — Problem Definition

**Problem**: [1-2 sentence problem statement]
**Prior limitations**: [what existing approaches fail to do]
**Application scenarios**: [where this would be used]

## 3. Action — Method and Approach

**Architecture**: [high-level method description]
**Core value**: [the key innovation in 1-2 sentences]
**Procedure**:
1. [step 1]
2. [step 2]
3. [step N]

## 4. Result — Evidence and Outcomes

**Datasets**: [dataset1, dataset2, ...]
**Key results**:
| Metric | This Work | Best Baseline | Delta |
|--------|-----------|---------------|-------|
| ...    | ...       | ...           | ...   |

**Claim validation**:
- Claim 1: [supported/partially/unsupported] — [evidence reference]
- Claim N: [supported/partially/unsupported] — [evidence reference]

## 5. Reflexion — Critical Assessment

**Strengths**: [what the paper does well]
**Weaknesses**: [limitations and gaps]
**Open questions**: [unanswered questions]
**Extension ideas**: [how to build on this work]
```

## Workflow

1. Read the paper (from PDF, NotebookLM, or provided text)
2. Work through each STAR section systematically
3. Fill in the output template
4. Save the analysis using `$PY $SKILL/scripts/run.py analyze save <paper_id> <file>`
5. If the analysis is part of a survey phase, feed results into the comparison matrix
