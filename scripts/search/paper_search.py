#!/usr/bin/env python3
"""
Paper Search Module for Survey Agent
Searches academic papers via arXiv and Semantic Scholar APIs
"""

import argparse
import json
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Optional

# Add scripts directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))
from config import DATA_DIR, PAPERS_DIR

try:
    import arxiv
except ImportError:
    arxiv = None

try:
    from semanticscholar import SemanticScholar
except ImportError:
    SemanticScholar = None


class Paper:
    """Unified paper representation"""

    def __init__(
        self,
        title: str,
        authors: list[str],
        abstract: str,
        published: Optional[str] = None,
        arxiv_id: Optional[str] = None,
        doi: Optional[str] = None,
        semantic_scholar_id: Optional[str] = None,
        pdf_url: Optional[str] = None,
        citation_count: int = 0,
        source: str = "unknown"
    ):
        self.title = title
        self.authors = authors
        self.abstract = abstract
        self.published = published
        self.arxiv_id = arxiv_id
        self.doi = doi
        self.semantic_scholar_id = semantic_scholar_id
        self.pdf_url = pdf_url
        self.citation_count = citation_count
        self.source = source

    @property
    def unique_id(self) -> str:
        """Generate unique ID for deduplication"""
        if self.arxiv_id:
            return f"arxiv:{self.arxiv_id}"
        if self.doi:
            return f"doi:{self.doi}"
        if self.semantic_scholar_id:
            return f"s2:{self.semantic_scholar_id}"
        return f"title:{self.title.lower()[:50]}"

    def to_dict(self) -> dict:
        return {
            "title": self.title,
            "authors": self.authors,
            "abstract": self.abstract,
            "published": self.published,
            "arxiv_id": self.arxiv_id,
            "doi": self.doi,
            "semantic_scholar_id": self.semantic_scholar_id,
            "pdf_url": self.pdf_url,
            "citation_count": self.citation_count,
            "source": self.source,
            "unique_id": self.unique_id
        }


class ArxivSearcher:
    """Search papers via arXiv API"""

    def __init__(self):
        if arxiv is None:
            raise ImportError("arxiv package not installed. Run: pip install arxiv")

    def search(
        self,
        query: str,
        max_results: int = 20,
        year_from: Optional[int] = None,
        year_to: Optional[int] = None,
        sort_by: str = "relevance"
    ) -> list[Paper]:
        """Search arXiv for papers"""
        print(f"[arXiv] Searching for: {query}")

        # Build date filter if specified
        date_filter = ""
        if year_from:
            date_filter = f" AND submittedDate:[{year_from}0101 TO "
            if year_to:
                date_filter += f"{year_to}1231]"
            else:
                date_filter += f"{datetime.now().year}1231]"

        search_query = query + date_filter

        sort_criterion = {
            "relevance": arxiv.SortCriterion.Relevance,
            "date": arxiv.SortCriterion.SubmittedDate,
            "citations": arxiv.SortCriterion.Relevance  # arXiv doesn't support citation sort
        }.get(sort_by, arxiv.SortCriterion.Relevance)

        search = arxiv.Search(
            query=search_query,
            max_results=max_results,
            sort_by=sort_criterion
        )

        papers = []
        client = arxiv.Client()

        for result in client.results(search):
            # Respect rate limits
            time.sleep(0.5)

            # Extract arXiv ID from entry_id
            arxiv_id = result.entry_id.split("/abs/")[-1] if result.entry_id else None

            paper = Paper(
                title=result.title,
                authors=[author.name for author in result.authors],
                abstract=result.summary,
                published=result.published.strftime("%Y-%m-%d") if result.published else None,
                arxiv_id=arxiv_id,
                doi=result.doi,
                pdf_url=result.pdf_url,
                source="arxiv"
            )
            papers.append(paper)
            print(f"  Found: {paper.title[:60]}...")

        print(f"[arXiv] Found {len(papers)} papers")
        return papers


class SemanticScholarSearcher:
    """Search papers via Semantic Scholar API"""

    def __init__(self, api_key: Optional[str] = None):
        if SemanticScholar is None:
            raise ImportError("semanticscholar package not installed. Run: pip install semanticscholar")
        self.sch = SemanticScholar(api_key=api_key) if api_key else SemanticScholar()

    def search(
        self,
        query: str,
        max_results: int = 20,
        year_from: Optional[int] = None,
        year_to: Optional[int] = None,
        fields_of_study: Optional[list[str]] = None
    ) -> list[Paper]:
        """Search Semantic Scholar for papers"""
        print(f"[Semantic Scholar] Searching for: {query}")

        # Build year filter
        year_filter = None
        if year_from or year_to:
            start = year_from or 1900
            end = year_to or datetime.now().year
            year_filter = f"{start}-{end}"

        try:
            results = self.sch.search_paper(
                query,
                limit=max_results,
                year=year_filter,
                fields_of_study=fields_of_study,
                fields=[
                    "title", "authors", "abstract", "year",
                    "externalIds", "openAccessPdf", "citationCount"
                ]
            )
        except Exception as e:
            print(f"[Semantic Scholar] Error: {e}")
            return []

        papers = []
        for result in results:
            if not result.title:
                continue

            # Extract IDs
            external_ids = result.externalIds or {}
            arxiv_id = external_ids.get("ArXiv")
            doi = external_ids.get("DOI")
            s2_id = result.paperId

            # Get PDF URL
            pdf_url = None
            if result.openAccessPdf:
                pdf_url = result.openAccessPdf.get("url")

            paper = Paper(
                title=result.title,
                authors=[a.name for a in (result.authors or []) if a.name],
                abstract=result.abstract or "",
                published=str(result.year) if result.year else None,
                arxiv_id=arxiv_id,
                doi=doi,
                semantic_scholar_id=s2_id,
                pdf_url=pdf_url,
                citation_count=result.citationCount or 0,
                source="semantic_scholar"
            )
            papers.append(paper)
            print(f"  Found: {paper.title[:60]}...")

        print(f"[Semantic Scholar] Found {len(papers)} papers")
        return papers


class UnifiedPaperSearch:
    """Unified search across multiple sources with deduplication"""

    def __init__(self, semantic_scholar_api_key: Optional[str] = None):
        self.searchers = {}

        # Initialize available searchers
        if arxiv is not None:
            try:
                self.searchers["arxiv"] = ArxivSearcher()
            except ImportError as e:
                print(f"Warning: {e}")

        if SemanticScholar is not None:
            try:
                self.searchers["semantic_scholar"] = SemanticScholarSearcher(semantic_scholar_api_key)
            except ImportError as e:
                print(f"Warning: {e}")

        if not self.searchers:
            raise RuntimeError("No search backends available. Install arxiv or semanticscholar packages.")

    def search(
        self,
        query: str,
        max_results: int = 20,
        year_from: Optional[int] = None,
        year_to: Optional[int] = None,
        sources: Optional[list[str]] = None,
        sort_by: str = "relevance"
    ) -> list[Paper]:
        """Search across all sources and deduplicate"""

        if sources is None:
            sources = list(self.searchers.keys())

        all_papers = []
        results_per_source = max_results // len(sources) + 5  # Get extra for dedup

        for source in sources:
            if source not in self.searchers:
                print(f"Warning: Source '{source}' not available")
                continue

            searcher = self.searchers[source]

            if source == "arxiv":
                papers = searcher.search(
                    query=query,
                    max_results=results_per_source,
                    year_from=year_from,
                    year_to=year_to,
                    sort_by=sort_by
                )
            else:  # semantic_scholar
                papers = searcher.search(
                    query=query,
                    max_results=results_per_source,
                    year_from=year_from,
                    year_to=year_to
                )

            all_papers.extend(papers)
            time.sleep(1)  # Rate limit between sources

        # Deduplicate
        seen = {}
        unique_papers = []

        for paper in all_papers:
            uid = paper.unique_id
            if uid not in seen:
                seen[uid] = paper
                unique_papers.append(paper)
            else:
                # Merge info from duplicate (prefer more complete records)
                existing = seen[uid]
                if not existing.pdf_url and paper.pdf_url:
                    existing.pdf_url = paper.pdf_url
                if not existing.citation_count and paper.citation_count:
                    existing.citation_count = paper.citation_count

        # Sort results
        if sort_by == "citations":
            unique_papers.sort(key=lambda p: p.citation_count, reverse=True)
        elif sort_by == "date":
            unique_papers.sort(key=lambda p: p.published or "", reverse=True)

        # Limit to max_results
        unique_papers = unique_papers[:max_results]

        print(f"\n[Total] {len(unique_papers)} unique papers after deduplication")
        return unique_papers

    def save_results(self, papers: list[Paper], output_file: Path):
        """Save search results to JSON"""
        data = {
            "search_time": datetime.now().isoformat(),
            "total_papers": len(papers),
            "papers": [p.to_dict() for p in papers]
        }

        output_file.parent.mkdir(parents=True, exist_ok=True)
        with open(output_file, "w") as f:
            json.dump(data, f, indent=2)

        print(f"\nResults saved to: {output_file}")


def main():
    parser = argparse.ArgumentParser(description="Search academic papers via arXiv and Semantic Scholar")
    parser.add_argument("--query", "-q", required=True, help="Search query")
    parser.add_argument("--max-results", "-n", type=int, default=20, help="Maximum results (default: 20)")
    parser.add_argument("--year-from", type=int, help="Start year filter")
    parser.add_argument("--year-to", type=int, help="End year filter")
    parser.add_argument("--sources", nargs="+", choices=["arxiv", "semantic_scholar"],
                        help="Search sources (default: both)")
    parser.add_argument("--sort", choices=["relevance", "date", "citations"],
                        default="relevance", help="Sort order")
    parser.add_argument("--output", "-o", type=Path, help="Output JSON file")
    parser.add_argument("--s2-api-key", help="Semantic Scholar API key for higher rate limits")

    args = parser.parse_args()

    # Initialize search
    search = UnifiedPaperSearch(semantic_scholar_api_key=args.s2_api_key)

    # Perform search
    papers = search.search(
        query=args.query,
        max_results=args.max_results,
        year_from=args.year_from,
        year_to=args.year_to,
        sources=args.sources,
        sort_by=args.sort
    )

    # Output results
    if args.output:
        search.save_results(papers, args.output)
    else:
        # Default output location
        output_file = PAPERS_DIR / "search_results.json"
        search.save_results(papers, output_file)

    # Print summary
    print("\n" + "="*60)
    print("SEARCH RESULTS SUMMARY")
    print("="*60)
    for i, paper in enumerate(papers, 1):
        print(f"\n{i}. {paper.title}")
        print(f"   Authors: {', '.join(paper.authors[:3])}{'...' if len(paper.authors) > 3 else ''}")
        print(f"   Published: {paper.published or 'N/A'}")
        print(f"   Citations: {paper.citation_count}")
        print(f"   PDF: {'Available' if paper.pdf_url else 'Not available'}")
        print(f"   Source: {paper.source}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
