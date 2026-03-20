---
name: paper-venue
description: "Phase 11: Venue. Select target venues, match contribution to venue scope, check deadlines and formatting requirements."
phase: 11
---

# /paper venue — Phase 11: Venue

## Input

- `position.md` (contribution summary and field)
- Latest draft (`drafts/v2-refined.md` or `drafts/v1-draft.md`)
- `scorecard.json` (cross-cutting)
- `field-map.md` (for venue context)

## Variable Shortcuts

```bash
PAPER_SKILL=~/project/lab/trust_ai_identity/paper-skill
PY=$PAPER_SKILL/.venv/bin/python3
```

## Workflow

### Step 1 — Extract Contribution Profile

Read `position.md` and the latest draft. Identify:
- **Field**: Primary research area (e.g., NLP, computer vision, security, HCI)
- **Contribution type**: Empirical, theoretical, systems, benchmark, survey, position
- **Contribution strength**: Based on scorecard and claim validation
- **Paper length**: Current word count and estimated page count
- **Key topics/keywords**: For venue matching

### Step 2 — Search for Venues

Use WebSearch to find relevant venues. Search for:
- "top {field} conferences {current_year}"
- "{field} conference deadlines {current_year} {next_year}"
- "best venues for {contribution type} papers in {field}"
- "{specific topic} workshop call for papers"

For each candidate venue, gather:
- Full name and abbreviation
- Submission deadline (with timezone)
- Notification date
- Acceptance rate (recent years)
- Page limit and format (single/double column)
- Topics of interest
- Tier ranking (A*, A, B, workshop)

### Step 3 — Match Contribution to Venue

For each candidate venue, assess:

1. **Scope match**: Does the venue publish this type of work?
   - Check recent proceedings for similar topics
   - Check call for papers for relevant tracks/areas
2. **Rigor match**: Does the paper meet the venue's typical quality bar?
   - Compare scorecard completion to venue's expected standards
   - Compare evaluation depth to similar accepted papers
3. **Length match**: Does the paper fit the page limit?
   - Flag if paper is significantly over/under limit
4. **Timing match**: Is the deadline realistic given current paper state?
   - At least 2 weeks away for a polished paper
   - At least 4 weeks away if significant revisions remain

Score each venue: **Match: XX%** with a one-line reason.

### Step 4 — Rank and Recommend

Rank venues by:
1. Match score (highest first)
2. Deadline proximity (soonest feasible first)
3. Acceptance rate (consider realistic chances)
4. Impact factor / prestige

Categorize into tiers:
- **Tier A**: Best match, high impact, realistic deadline
- **Tier B**: Good match, moderate impact, or tight deadline
- **Tier C**: Backup options (workshops, lower-tier venues)

### Step 5 — Formatting Notes

For the top recommended venue:
- Page limit and what counts (references, appendix)
- Citation style (numbered, author-year, etc.)
- Template (LaTeX class, Word template)
- Special formatting rules (anonymization, supplementary material)
- Submission system (OpenReview, CMT, EasyChair, etc.)

## Output

Write the venue recommendation to:

```
~/.paper-skill/projects/{name}/venue-recommendation.md
```

Use this format:

```markdown
# Venue Recommendation — {project name}

**Date:** {date}
**Field:** {field}
**Contribution type:** {type}
**Paper length:** ~{N} pages ({W} words)

---

## Recommended Venues

### Tier A
1. **{Venue Name}** ({abbreviation})
   - Deadline: {YYYY-MM-DD} ({timezone})
   - Pages: {N} ({format})
   - Acceptance rate: ~{XX}%
   - Match: {XX}% — {reason}

2. ...

### Tier B
1. **{Venue Name}** ({abbreviation})
   - Deadline: {YYYY-MM-DD}
   - Pages: {N} ({format})
   - Acceptance rate: ~{XX}%
   - Match: {XX}% — {reason}

### Tier C (Backup)
1. **{Venue Name}** ({abbreviation})
   - Deadline: {YYYY-MM-DD}
   - Match: {XX}% — {reason}

## Formatting Notes for Top Venue

- **Template:** {LaTeX class / link}
- **Page limit:** {N} pages ({what counts})
- **Citation style:** {style}
- **Anonymization:** {Yes/No — double-blind/single-blind}
- **Supplementary:** {allowed/required/not allowed}
- **Submission system:** {system name}

## Timeline

| Milestone | Date | Notes |
|-----------|------|-------|
| Deadline | {date} | {days from now} |
| Notification | {date} | |
| Camera-ready | {date} | |

## Recommendations

{1-2 paragraphs of strategic advice: which venue to target first,
whether to consider dual submission, workshop vs main conference, etc.}
```

## Cross-Cutting Updates

- **Scorecard**: Check if venue-specific requirements need to be added (e.g., page limit compliance, anonymization).

## Health Check

Before completing this phase, verify:

- [ ] At least 3 venues identified across at least 2 tiers
- [ ] Each venue has deadline, acceptance rate, and page limit
- [ ] Match scores are justified with specific reasons
- [ ] Formatting notes are provided for the top venue
- [ ] Timeline is realistic (deadline is at least 2 weeks away)

If no suitable venue is found with a feasible deadline, recommend the user either:
- Target a later deadline
- Consider a workshop or preprint (arXiv) first

## Phase Transition

This is the final phase of the pipeline.

```
STATUS: DONE — Venue selection complete

Top venue: {venue} (deadline: {date}, match: {XX}%).
{N} venues identified across {T} tiers.
Formatting notes ready for {top venue}.

Cross-cutting status:
  Scorecard: X/Y requirements met (Z% accept probability)
  Claims: S/T supported
  Matrix: N papers tracked, M dimensions

The paper pipeline is complete! What would you like to do next?

A) Paper is ready — save final state and celebrate
B) Back to /paper refine — final polish for {top venue}
C) Start a new paper project — /paper survey
D) Export to LaTeX — format the draft for submission

Rate this phase? (1-5, or skip)
```
