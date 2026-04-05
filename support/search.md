---
name: paper-search
description: Search for academic papers across multiple sources (arXiv, Semantic Scholar).
---

# /paper search

Searches for academic papers across arXiv and Semantic Scholar.

## Command

```bash
PY=~/.claude/skills/paper/.venv/bin/python3
PAPER_SKILL=~/.claude/skills/paper

$PY $PAPER_SKILL/scripts/run.py search --query "..." [--year-from Y] [--year-to Y] [--sources arxiv semantic_scholar] [--sort relevance] [--max-results 20]
```

### Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `--query` | (required) | Search query string |
| `--year-from` | none | Filter papers published from this year |
| `--year-to` | none | Filter papers published up to this year |
| `--sources` | `arxiv semantic_scholar` | Space-separated list of sources |
| `--sort` | `relevance` | Sort order: `relevance` or `date` |
| `--max-results` | `20` | Maximum number of results to return |

## Search Strategy Guidance

### Finding recent papers
- `"[topic] 2025"` — recent work on a topic
- `"[topic] arXiv 2025"` — preprints from this year
- Use `--year-from 2024 --sort date` for the latest work

### Finding foundational papers
- `"[topic] survey"` — survey and review papers
- `"[topic] benchmark"` — benchmark and evaluation papers
- `"[topic] tutorial"` — introductory or tutorial papers

### Narrowing results
- Add method names or author names to the query
- Combine with year filters for a specific time window
- Use `--sources arxiv` or `--sources semantic_scholar` to search one source at a time

## Workflow

1. Run the search command with user's query
2. Present results as a numbered table with columns: #, Title, Authors, Year, Source, Citations
3. Ask the user which papers to download or analyze further
4. For selected papers, hand off to `/paper analyze` or `/paper store upload`
