---
name: paper-check
description: "Health-check the knowledge base vault. Find orphans, broken links, gaps, and suggest improvements."
---

# /paper check — Knowledge Base Health

Diagnose your knowledge base: find unprocessed papers, broken wikilinks, thin articles, and suggest new connections and articles to write.

## Setup

```bash
PAPER_SKILL=~/.claude/skills/paper
PY=$PAPER_SKILL/.venv/bin/python3
VAULT=$($PY -c "from scripts.config import get_vault_dir; print(get_vault_dir())")
```

## Checks

### A. Coverage
- **Uncompiled papers**: raw/ files not in any wiki article's `sources:`
- **Orphan wiki articles**: Articles with no incoming links from other wiki articles
- **Stale Q&A**: qa/ entries referencing deleted wiki articles

### B. Consistency
- **Broken wikilinks**: `[[links]]` pointing to non-existent files
- **Missing frontmatter**: wiki/ or qa/ files without required fields (title, tags)
- **Tag drift**: Similar tags that should merge (e.g., `ml` vs `machine-learning`)
- **Stale articles**: Wiki `updated:` older than raw source modification date

### C. Quality
- **Thin articles**: Wiki articles under 200 words
- **Unlinked articles**: Wiki articles with no `related:` entries
- **Missing concepts**: Topics in 3+ raw papers with no wiki article

### D. Suggestions
- New articles to write (concepts spanning multiple papers)
- Merge candidates (high tag overlap)
- Research questions worth investigating

## Report Format

```
Knowledge Base Health — {date}

Stats: {N} raw | {M} wiki | {K} qa

Healthy:
  {checks that passed}

Warnings:
  {N} uncompiled raw papers
  {N} broken wikilinks
  {details}

Suggestions:
  New article: "{concept}" (in {N} papers, no wiki entry)
  Merge: "{a}" + "{b}" (similar tags)
  Question: "{interesting question from gap}"

Run /paper digest to address uncompiled papers.
```

## Actions

After the report, offer:

**A) Auto-fix** — Fix broken links, normalize tags, update stale dates
**B) Digest missing** — Run `/paper digest` for uncompiled papers
**C) Report only** — No action (default)
