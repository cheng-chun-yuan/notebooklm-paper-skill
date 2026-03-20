---
name: paper-ship
description: "Phase 8: Ship. Select target venues, match contribution to venue scope, check deadlines and formatting requirements."
phase: 8
---

# /paper ship — Phase 8: Ship

## Input

- `position.md` (contribution summary and field)
- Latest draft (`drafts/v2-refined.md` or `drafts/v1-draft.md`)
- `scorecard.json` (cross-cutting)
- `field-map.md` (for venue context)

## Variable Shortcuts

```bash
PAPER_SKILL=~/.claude/skills/notebooklm-paper
PY=$PAPER_SKILL/.venv/bin/python3
```

## Quality Rubric

Every venue recommendation is evaluated on these dimensions:

| Dimension | Excellent | Acceptable | Poor |
|-----------|-----------|------------|------|
| **Specificity** | Each venue entry has exact deadline (with timezone), page limit, format, acceptance rate, and submission system. Match reasons reference specific paper contributions: "Your efficiency analysis (Section 5.3) aligns with {venue}'s systems track." | Venues have deadlines and page limits. Match reasons are reasonable but generic ("good fit for ML papers"). | Venues listed by name only. No deadlines, no page limits, no match justification. |
| **Traceability** | Match scores reference position.md contribution type, scorecard.json acceptance probability, and specific draft sections. Tier assignments connect to paper quality assessment. | Match scores exist and are reasonable. Some connection to prior artifacts. | Match scores appear arbitrary. No connection to paper's actual strengths or weaknesses. |
| **Completeness** | At least 3 venues across at least 2 tiers. Formatting notes for top venue. Realistic timeline. Strategic recommendations. | 3 venues identified. Basic formatting notes. Timeline present. | Fewer than 3 venues. No formatting notes. No timeline. |
| **Data recency** | Venue deadlines, acceptance rates, and page limits are from the current year (2026). Sources cited. "Deadline TBD" used when no current CFP exists rather than guessing. | Most data is current. One or two items may be from previous year but noted as approximate. | Deadlines from 2024 or earlier presented as current. Acceptance rates from 3+ years ago. |
| **Match justification** | Each venue's match score is justified with 2-3 specific reasons referencing the paper's contribution type, field, and strength. "85% match: (1) your systems contribution aligns with {venue}'s systems track, (2) your 8-page paper fits the 10-page limit, (3) your evaluation depth matches recent accepted papers." | Match scores have at least 1 specific reason. | Match scores are just numbers with no explanation. |

## Anti-patterns

1. **Targeting unrealistic venues** — DON'T: Recommend NeurIPS for a paper with weak evaluation and a scorecard showing 35% acceptance probability. DO: Calibrate venue tier to paper quality. A solid paper at a B-tier venue is better than a desk rejection at A*. If the scorecard shows <50% acceptance probability, the Tier A list should include a caveat: "stretch target — consider only if P0 fixes are completed."

2. **Stale deadline data** — DON'T: Report deadlines from last year's conference as if they are current. "ICML 2025 deadline: January 2025" when the user needs 2026/2027 dates. DO: Use WebSearch to find the current year's CFP. If no current CFP exists, write "Deadline: TBD (2025 was {date}, typically {month} each year)" rather than guessing.

3. **Ignoring page limits** — DON'T: Recommend a venue with an 8-page limit for a 15-page paper without flagging the mismatch. DO: Compare current word count (from the draft) to venue page limits. If the paper is >20% over the limit, flag it explicitly: "Paper is ~15 pages. {Venue} limit is 8 pages. Requires significant cutting (~7 pages). Consider whether core content fits."

4. **One-size-fits-all recommendations** — DON'T: Recommend the same top-5 ML conferences for every paper regardless of subfield or contribution type. DO: Match venues to the paper's specific contribution type (empirical vs. theoretical vs. systems vs. benchmark) and subfield. A benchmark paper has different ideal venues than a theoretical paper in the same field.

## Structural Exemplar

The venue recommendation follows this shape (content is illustrative, not prescriptive):

```markdown
# Venue Recommendation — {project name}

**Date:** 2026-03-20
**Field:** Natural Language Processing
**Contribution type:** Empirical (new method + evaluation)
**Paper length:** ~10 pages (7,200 words)

---

## Recommended Venues

### Tier A (Best fit, high impact)
1. **Annual Meeting of the ACL** (ACL 2026)
   - Deadline: 2026-01-15 (11:59 PM UTC-12)
   - Pages: 8 + unlimited references (double column, ACL format)
   - Acceptance rate: ~23% (2025)
   - Match: 82% — Strong empirical NLP contribution. Evaluation depth matches recent accepted papers. Paper is 2 pages over limit; trimming related work (-1 page) and compressing tables (-1 page) should suffice.
   - Submission system: OpenReview

2. **EMNLP 2026**
   - Deadline: 2026-06-01 (estimated, 2025 was 2025-06-01)
   - Pages: 8 + unlimited references (double column, ACL format)
   - Acceptance rate: ~24% (2025)
   - Match: 80% — Same format as ACL. Later deadline gives more time for revisions. Good fallback if ACL deadline is missed.

### Tier B (Good fit, moderate impact or tight deadline)
1. **NAACL 2027**
   - Deadline: TBD (2025 was 2025-10-15, typically October)
   - Pages: 8 + references
   - Acceptance rate: ~26% (2025)
   - Match: 75% — Good regional venue. Higher acceptance rate. Consider if ACL/EMNLP are rejected.

### Tier C (Backup / workshops)
1. **Workshop on {Specific Topic}** @ ACL 2026
   - Deadline: 2026-04-01 (estimated)
   - Pages: 4-8 (extended abstract or short paper)
   - Match: 70% — Lower bar, good for getting early feedback. Could submit a condensed version while targeting main conference.

## Formatting Notes for Top Venue (ACL 2026)

- **Template:** acl2023.sty (check ACL 2026 website for updates)
- **Page limit:** 8 pages content + unlimited references and appendix
- **Citation style:** Numbered, ACL style
- **Anonymization:** Yes — double-blind. Remove author names, acknowledgments, and self-citations that reveal identity.
- **Supplementary:** Allowed (appendix after references, + separate supplementary PDF)
- **Submission system:** OpenReview (softconf for some tracks)

## Timeline

| Milestone | Date | Notes |
|-----------|------|-------|
| ACL Deadline | 2026-01-15 | -67 days from now (PASSED) |
| EMNLP Deadline | 2026-06-01 | ~73 days from now |
| EMNLP Notification | 2026-08-15 | estimated |
| EMNLP Camera-ready | 2026-09-01 | estimated |

## Recommendations

Target EMNLP 2026 as the primary venue. The ACL 2026 deadline has passed, but EMNLP uses the same format and has a comparable acceptance rate. The ~73 days until deadline provides adequate time to address the remaining P2 issues from the refine phase and trim the paper to 8 pages.

Consider submitting to the {Specific Topic} Workshop @ ACL 2026 in parallel (4-page version) to get early community feedback. Workshop and main conference submissions are typically not considered dual submissions if the workshop paper is a condensed/extended abstract version.
```

## Failure Recovery

| Scenario | Detection | Recovery |
|----------|-----------|----------|
| **No venue with feasible deadline** | All identified venues have deadlines that have passed or are <2 weeks away, and the paper still needs revisions. | Recommend preprint first: post to arXiv to establish priority and get informal feedback. Then target the next conference cycle (typically 6-12 months). Identify the specific next deadline and create a timeline working backwards from it. |
| **Paper doesn't match any venue well (<60% match)** | No venue scores above 60% match. The contribution may be too niche, too interdisciplinary, or misaligned with standard venues. | Suggest: (1) workshop venues or special tracks that welcome interdisciplinary work, (2) journal submission (longer format, no deadline pressure, broader scope), (3) re-evaluate the positioning — if no venue fits, the contribution framing may need adjustment (backtrack to `/paper position`). |
| **WebSearch returns no results for current deadlines** | Search queries return outdated or no results for {current_year} CFPs. | Fall back to known conference databases: WikiCFP, conference-rankings.org, the venue's official website from the previous year. Use previous year's dates as estimates and clearly mark them: "Deadline: TBD (estimated {month} based on 2025 cycle)." Never present estimated dates as confirmed. |
| **Paper length significantly exceeds all venue limits** | Current draft is 15+ pages and all target venues have 8-10 page limits. | Flag explicitly. Estimate cutting effort: "Need to cut ~7 pages. Recommend: (1) move detailed proofs to appendix (-2 pages), (2) compress related work (-1.5 pages), (3) merge Tables 2-3 (-1 page), (4) tighten method section prose (-2.5 pages)." If cutting is not feasible, recommend journal venues with no page limit (e.g., JMLR, TACL). |

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
~/.notebooklm-paper/projects/{name}/venue-recommendation.md
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

## Failure Recovery

If a health check fails:

1. **Fewer than 3 venues identified** — Broaden the search. Try adjacent fields, interdisciplinary venues, and workshops. If the contribution is very niche, include journal options (no page limit, rolling deadlines) to reach the 3-venue minimum.
2. **Missing deadline or acceptance rate for a venue** — Search the venue's official website directly. If the current year's CFP is not yet published, use previous year's data with a clear "estimated" label. Never leave these fields blank — at minimum write "TBD (estimated {month})."
3. **No feasible deadline (all passed or <2 weeks away)** — Do not force a recommendation. Instead: (a) recommend arXiv preprint for priority, (b) identify the next cycle deadline for each venue, (c) create a 6-month timeline showing when to target each venue.
4. **Match scores lack justification** — For each score, require at minimum: (1) scope fit reason, (2) paper quality vs. venue bar assessment, (3) length compatibility note. If any of these is missing, add it before transitioning.

## Phase Transition

This is the final phase of the pipeline.

```
STATUS: DONE — Ship complete

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
C) Start a new paper project — /paper discover
D) Export to LaTeX — format the draft for submission

Rate this phase? (1-5, or skip)
```
