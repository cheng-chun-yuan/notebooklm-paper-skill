#!/usr/bin/env python3
"""
Paper Downloader Module for Survey Agent
Downloads PDFs from arXiv and open-access sources
"""

import argparse
import json
import sys
import time
import re
from datetime import datetime
from pathlib import Path
from typing import Optional
from concurrent.futures import ThreadPoolExecutor, as_completed

# Add scripts directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))
from config import DATA_DIR, PAPERS_DIR, DOWNLOADS_FILE

try:
    import httpx
except ImportError:
    httpx = None

try:
    import arxiv
except ImportError:
    arxiv = None


class DownloadTracker:
    """Track download status for papers"""

    def __init__(self, tracker_file: Optional[Path] = None):
        self.tracker_file = tracker_file or DOWNLOADS_FILE
        self.data = self._load()

    def _load(self) -> dict:
        if self.tracker_file.exists():
            with open(self.tracker_file) as f:
                return json.load(f)
        return {"downloads": {}}

    def save(self):
        self.tracker_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.tracker_file, "w") as f:
            json.dump(self.data, f, indent=2)

    def is_downloaded(self, unique_id: str) -> bool:
        return unique_id in self.data["downloads"]

    def mark_downloaded(self, unique_id: str, file_path: str, metadata: dict):
        self.data["downloads"][unique_id] = {
            "file_path": file_path,
            "downloaded_at": datetime.now().isoformat(),
            "metadata": metadata
        }
        self.save()

    def get_downloaded_path(self, unique_id: str) -> Optional[str]:
        if unique_id in self.data["downloads"]:
            return self.data["downloads"][unique_id].get("file_path")
        return None


class PaperDownloader:
    """Download papers from various sources"""

    ARXIV_DELAY = 3.0  # Respect arXiv rate limits

    def __init__(self, output_dir: Path, tracker: Optional[DownloadTracker] = None):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.tracker = tracker or DownloadTracker()

        if httpx is None:
            raise ImportError("httpx package not installed. Run: pip install httpx")

    def sanitize_filename(self, title: str, max_length: int = 100) -> str:
        """Create safe filename from paper title"""
        # Remove/replace unsafe characters
        safe = re.sub(r'[<>:"/\\|?*]', '', title)
        safe = re.sub(r'\s+', '_', safe)
        safe = safe.strip('._')

        # Truncate if needed
        if len(safe) > max_length:
            safe = safe[:max_length].rsplit('_', 1)[0]

        return safe or "paper"

    def download_from_arxiv(self, arxiv_id: str, title: str) -> Optional[Path]:
        """Download PDF directly from arXiv using arxiv.py"""
        if arxiv is None:
            return self.download_from_url(
                f"https://arxiv.org/pdf/{arxiv_id}.pdf",
                title
            )

        print(f"  Downloading from arXiv: {arxiv_id}")

        try:
            search = arxiv.Search(id_list=[arxiv_id])
            client = arxiv.Client()
            paper = next(client.results(search))

            filename = f"{self.sanitize_filename(title)}_{arxiv_id.replace('/', '_')}.pdf"
            file_path = self.output_dir / filename

            paper.download_pdf(dirpath=str(self.output_dir), filename=filename)
            time.sleep(self.ARXIV_DELAY)  # Rate limit

            if file_path.exists():
                return file_path

        except Exception as e:
            print(f"  Error downloading from arXiv: {e}")

        return None

    def download_from_url(self, url: str, title: str) -> Optional[Path]:
        """Download PDF from direct URL"""
        if not url:
            return None

        print(f"  Downloading from URL: {url[:60]}...")

        try:
            filename = f"{self.sanitize_filename(title)}.pdf"
            file_path = self.output_dir / filename

            with httpx.Client(follow_redirects=True, timeout=60) as client:
                response = client.get(url, headers={
                    "User-Agent": "Mozilla/5.0 (compatible; AcademicSurveyBot/1.0)"
                })

                if response.status_code == 200:
                    content_type = response.headers.get("content-type", "")
                    if "pdf" in content_type or url.endswith(".pdf"):
                        file_path.write_bytes(response.content)
                        return file_path
                    else:
                        print(f"  Warning: Not a PDF (content-type: {content_type})")

        except Exception as e:
            print(f"  Error downloading from URL: {e}")

        return None

    def download_paper(self, paper: dict) -> dict:
        """Download a single paper, trying multiple sources"""
        unique_id = paper.get("unique_id", paper.get("title", "unknown"))
        title = paper.get("title", "Unknown Paper")

        # Check if already downloaded
        if self.tracker.is_downloaded(unique_id):
            existing_path = self.tracker.get_downloaded_path(unique_id)
            if existing_path and Path(existing_path).exists():
                print(f"  Already downloaded: {title[:50]}...")
                return {
                    "success": True,
                    "file_path": existing_path,
                    "source": "cache"
                }

        print(f"\nDownloading: {title[:60]}...")

        file_path = None
        source = None

        # Try arXiv first (most reliable for CS papers)
        arxiv_id = paper.get("arxiv_id")
        if arxiv_id:
            file_path = self.download_from_arxiv(arxiv_id, title)
            if file_path:
                source = "arxiv"

        # Try direct PDF URL
        if not file_path:
            pdf_url = paper.get("pdf_url")
            if pdf_url:
                file_path = self.download_from_url(pdf_url, title)
                if file_path:
                    source = "direct_url"

        # Try DOI-based URL (via Unpaywall or direct)
        if not file_path:
            doi = paper.get("doi")
            if doi:
                # Try sci-hub alternatives or unpaywall
                unpaywall_url = f"https://api.unpaywall.org/v2/{doi}?email=survey@example.com"
                try:
                    with httpx.Client(timeout=10) as client:
                        resp = client.get(unpaywall_url)
                        if resp.status_code == 200:
                            data = resp.json()
                            oa_location = data.get("best_oa_location", {})
                            if oa_location:
                                pdf_url = oa_location.get("url_for_pdf")
                                if pdf_url:
                                    file_path = self.download_from_url(pdf_url, title)
                                    if file_path:
                                        source = "unpaywall"
                except Exception:
                    pass

        # Record result
        if file_path:
            self.tracker.mark_downloaded(unique_id, str(file_path), {
                "title": title,
                "arxiv_id": arxiv_id,
                "doi": paper.get("doi")
            })
            return {
                "success": True,
                "file_path": str(file_path),
                "source": source
            }

        return {
            "success": False,
            "file_path": None,
            "error": "No downloadable PDF found"
        }

    def download_batch(
        self,
        papers: list[dict],
        max_concurrent: int = 1,  # Default to 1 to respect rate limits
        skip_existing: bool = True
    ) -> dict:
        """Download multiple papers"""
        results = {
            "total": len(papers),
            "successful": 0,
            "failed": 0,
            "skipped": 0,
            "downloads": []
        }

        # Filter out already downloaded if requested
        to_download = []
        for paper in papers:
            unique_id = paper.get("unique_id", paper.get("title", ""))
            if skip_existing and self.tracker.is_downloaded(unique_id):
                existing = self.tracker.get_downloaded_path(unique_id)
                if existing and Path(existing).exists():
                    results["skipped"] += 1
                    results["downloads"].append({
                        "title": paper.get("title"),
                        "success": True,
                        "file_path": existing,
                        "source": "cache"
                    })
                    continue
            to_download.append(paper)

        print(f"\nDownloading {len(to_download)} papers ({results['skipped']} skipped from cache)")

        # Download sequentially for rate limiting
        if max_concurrent == 1:
            for paper in to_download:
                result = self.download_paper(paper)
                result["title"] = paper.get("title")
                results["downloads"].append(result)

                if result["success"]:
                    results["successful"] += 1
                else:
                    results["failed"] += 1
        else:
            # Parallel download (use carefully with rate limits)
            with ThreadPoolExecutor(max_workers=max_concurrent) as executor:
                future_to_paper = {
                    executor.submit(self.download_paper, paper): paper
                    for paper in to_download
                }

                for future in as_completed(future_to_paper):
                    paper = future_to_paper[future]
                    result = future.result()
                    result["title"] = paper.get("title")
                    results["downloads"].append(result)

                    if result["success"]:
                        results["successful"] += 1
                    else:
                        results["failed"] += 1

        return results


def main():
    parser = argparse.ArgumentParser(description="Download academic papers as PDFs")
    parser.add_argument("--input", "-i", type=Path, required=True,
                        help="Input JSON file with paper search results")
    parser.add_argument("--output-dir", "-o", type=Path,
                        help="Output directory for PDFs (default: data/papers/pdfs)")
    parser.add_argument("--max-concurrent", type=int, default=1,
                        help="Max concurrent downloads (default: 1 for rate limits)")
    parser.add_argument("--skip-existing", action="store_true", default=True,
                        help="Skip already downloaded papers")
    parser.add_argument("--no-skip-existing", action="store_false", dest="skip_existing",
                        help="Re-download all papers")

    args = parser.parse_args()

    # Load paper list
    if not args.input.exists():
        print(f"Error: Input file not found: {args.input}")
        return 1

    with open(args.input) as f:
        data = json.load(f)

    papers = data.get("papers", [])
    if not papers:
        print("No papers found in input file")
        return 1

    print(f"Found {len(papers)} papers to download")

    # Set up output directory
    output_dir = args.output_dir or PAPERS_DIR / "pdfs"

    # Download
    downloader = PaperDownloader(output_dir)
    results = downloader.download_batch(
        papers,
        max_concurrent=args.max_concurrent,
        skip_existing=args.skip_existing
    )

    # Summary
    print("\n" + "="*60)
    print("DOWNLOAD SUMMARY")
    print("="*60)
    print(f"Total papers: {results['total']}")
    print(f"Successfully downloaded: {results['successful']}")
    print(f"From cache: {results['skipped']}")
    print(f"Failed: {results['failed']}")
    print(f"\nPDFs saved to: {output_dir}")

    if results["failed"] > 0:
        print("\nFailed downloads:")
        for dl in results["downloads"]:
            if not dl["success"]:
                print(f"  - {dl.get('title', 'Unknown')[:60]}...")
                print(f"    Error: {dl.get('error', 'Unknown error')}")

    # Save results summary
    summary_file = output_dir / "download_summary.json"
    with open(summary_file, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nSummary saved to: {summary_file}")

    return 0 if results["failed"] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
