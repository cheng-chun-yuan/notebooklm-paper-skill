#!/usr/bin/env python3
"""
Survey Manager for Academic Paper Surveys
Orchestrates the complete survey workflow: search → download → upload → query → report
"""

import argparse
import json
import sys
import re
from datetime import datetime
from pathlib import Path
from typing import Optional

# Add scripts directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))
from config import DATA_DIR, LIBRARY_FILE, PAPERS_DIR, SURVEYS_DIR


class SurveyManager:
    """Manages academic paper surveys"""

    SURVEYS_FILE = SURVEYS_DIR / "surveys.json"

    def __init__(self):
        self.data = self._load()

    def _load(self) -> dict:
        if self.SURVEYS_FILE.exists():
            with open(self.SURVEYS_FILE) as f:
                return json.load(f)
        return {"surveys": {}, "active_survey_id": None}

    def save(self):
        self.SURVEYS_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(self.SURVEYS_FILE, "w") as f:
            json.dump(self.data, f, indent=2)

    def _generate_id(self, name: str) -> str:
        """Generate survey ID from name"""
        base_id = re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-')
        if base_id not in self.data["surveys"]:
            return base_id

        # Add suffix if exists
        counter = 2
        while f"{base_id}-{counter}" in self.data["surveys"]:
            counter += 1
        return f"{base_id}-{counter}"

    def create(
        self,
        name: str,
        query: str,
        year_from: Optional[int] = None,
        year_to: Optional[int] = None,
        notebook_url: Optional[str] = None,
        description: Optional[str] = None
    ) -> dict:
        """Create a new survey"""
        survey_id = self._generate_id(name)

        survey = {
            "id": survey_id,
            "name": name,
            "description": description or f"Survey on: {query}",
            "query": query,
            "date_range": {
                "from": f"{year_from}-01-01" if year_from else None,
                "to": f"{year_to}-12-31" if year_to else None
            },
            "notebook_url": notebook_url,
            "notebook_id": None,  # From library
            "status": "created",
            "papers": [],
            "papers_file": None,
            "pdfs_dir": None,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "findings_summary": None,
            "steps_completed": []
        }

        self.data["surveys"][survey_id] = survey
        self.data["active_survey_id"] = survey_id
        self.save()

        print(f"Survey created: {survey_id}")
        return survey

    def get(self, survey_id: Optional[str] = None) -> Optional[dict]:
        """Get survey by ID or active survey"""
        sid = survey_id or self.data.get("active_survey_id")
        if not sid:
            return None
        return self.data["surveys"].get(sid)

    def list_surveys(self) -> list[dict]:
        """List all surveys"""
        return list(self.data["surveys"].values())

    def update(self, survey_id: str, updates: dict) -> dict:
        """Update survey data"""
        if survey_id not in self.data["surveys"]:
            raise ValueError(f"Survey not found: {survey_id}")

        survey = self.data["surveys"][survey_id]
        survey.update(updates)
        survey["updated_at"] = datetime.now().isoformat()
        self.save()
        return survey

    def add_step(self, survey_id: str, step: str):
        """Mark a workflow step as completed"""
        survey = self.get(survey_id)
        if survey and step not in survey["steps_completed"]:
            survey["steps_completed"].append(step)
            survey["updated_at"] = datetime.now().isoformat()
            self.save()

    def set_active(self, survey_id: str):
        """Set active survey"""
        if survey_id not in self.data["surveys"]:
            raise ValueError(f"Survey not found: {survey_id}")
        self.data["active_survey_id"] = survey_id
        self.save()
        print(f"Active survey: {survey_id}")

    def delete(self, survey_id: str):
        """Delete a survey"""
        if survey_id in self.data["surveys"]:
            del self.data["surveys"][survey_id]
            if self.data["active_survey_id"] == survey_id:
                self.data["active_survey_id"] = None
            self.save()
            print(f"Survey deleted: {survey_id}")

    def run_search(self, survey_id: Optional[str] = None) -> bool:
        """Run paper search for survey"""
        survey = self.get(survey_id)
        if not survey:
            print("No survey found")
            return False

        print(f"\n{'='*60}")
        print(f"STEP 1: PAPER SEARCH")
        print(f"{'='*60}")
        print(f"Survey: {survey['name']}")
        print(f"Query: {survey['query']}")

        # Import here to avoid circular imports
        try:
            from search.paper_search import UnifiedPaperSearch
        except ImportError:
            print("Error: paper_search module not available")
            return False

        # Parse date range
        year_from = None
        year_to = None
        if survey["date_range"]["from"]:
            year_from = int(survey["date_range"]["from"][:4])
        if survey["date_range"]["to"]:
            year_to = int(survey["date_range"]["to"][:4])

        # Run search
        try:
            search = UnifiedPaperSearch()
            papers = search.search(
                query=survey["query"],
                max_results=30,
                year_from=year_from,
                year_to=year_to
            )

            # Save results
            papers_file = PAPERS_DIR / f"{survey['id']}_papers.json"
            search.save_results(papers, papers_file)

            # Update survey
            self.update(survey["id"], {
                "papers_file": str(papers_file),
                "papers": [p.to_dict() for p in papers],
                "status": "papers_found"
            })
            self.add_step(survey["id"], "search")

            print(f"\nFound {len(papers)} papers")
            return True

        except Exception as e:
            print(f"Search error: {e}")
            return False

    def run_download(self, survey_id: Optional[str] = None) -> bool:
        """Download PDFs for survey papers"""
        survey = self.get(survey_id)
        if not survey:
            print("No survey found")
            return False

        if not survey.get("papers"):
            print("No papers found. Run search first.")
            return False

        print(f"\n{'='*60}")
        print(f"STEP 2: DOWNLOAD PDFS")
        print(f"{'='*60}")

        try:
            from download.paper_downloader import PaperDownloader
        except ImportError:
            print("Error: paper_downloader module not available")
            return False

        # Setup output directory
        pdfs_dir = PAPERS_DIR / survey["id"]
        pdfs_dir.mkdir(parents=True, exist_ok=True)

        try:
            downloader = PaperDownloader(pdfs_dir)
            results = downloader.download_batch(survey["papers"])

            # Update survey
            self.update(survey["id"], {
                "pdfs_dir": str(pdfs_dir),
                "status": "pdfs_downloaded"
            })
            self.add_step(survey["id"], "download")

            print(f"\nDownloaded: {results['successful']}")
            print(f"Failed: {results['failed']}")
            print(f"From cache: {results['skipped']}")
            return True

        except Exception as e:
            print(f"Download error: {e}")
            return False

    def get_upload_instructions(self, survey_id: Optional[str] = None) -> str:
        """Get instructions for uploading PDFs to NotebookLM"""
        survey = self.get(survey_id)
        if not survey:
            return "No survey found"

        pdfs_dir = survey.get("pdfs_dir")
        if not pdfs_dir:
            return "No PDFs downloaded yet. Run download first."

        pdfs_dir = Path(pdfs_dir)
        pdfs = list(pdfs_dir.glob("*.pdf"))

        if not pdfs:
            return "No PDFs found in download directory."

        notebook_url = survey.get("notebook_url", "[YOUR_NOTEBOOK_URL]")

        instructions = f'''
{'='*60}
STEP 3: UPLOAD PDFS TO NOTEBOOKLM
{'='*60}

Survey: {survey['name']}
PDFs directory: {pdfs_dir}
Total PDFs: {len(pdfs)}

Option A: Use upload_pdfs.py script (local browser)
---------------------------------------------------
python scripts/run.py upload_pdfs.py \\
  --notebook-url "{notebook_url}" \\
  --pdf-dir "{pdfs_dir}"

Option B: Use Browserbase MCP (cloud browser)
--------------------------------------------
Claude should use Browserbase MCP tools to:
1. Navigate to: {notebook_url}
2. Click "Add source" button
3. Click "Upload" tab
4. Upload these PDFs:
'''
        for pdf in pdfs[:10]:  # Show first 10
            instructions += f"   - {pdf.name}\n"
        if len(pdfs) > 10:
            instructions += f"   ... and {len(pdfs) - 10} more\n"

        instructions += f'''
After upload, update the survey status:
python scripts/run.py survey_manager.py complete-step \\
  --survey-id {survey['id']} --step upload
'''
        return instructions

    def get_query_suggestions(self, survey_id: Optional[str] = None) -> list[str]:
        """Get suggested questions for the survey"""
        survey = self.get(survey_id)
        if not survey:
            return []

        topic = survey["query"]

        return [
            f"What are the main research themes covered in these papers about {topic}?",
            f"What methodologies or techniques are most commonly used in {topic} research?",
            f"What are the key findings and contributions of each paper?",
            f"What evaluation metrics and benchmarks are used in {topic}?",
            f"What are the limitations and open challenges mentioned in these papers?",
            f"Compare and contrast the different approaches to {topic} in these papers.",
            f"What datasets are used in {topic} research?",
            f"What are the future research directions suggested in these papers?",
            f"Provide a comprehensive summary of the state-of-the-art in {topic}.",
            f"What are the practical applications of {topic} discussed in these papers?"
        ]

    def generate_report_template(self, survey_id: Optional[str] = None) -> str:
        """Generate a report template for the survey"""
        survey = self.get(survey_id)
        if not survey:
            return "No survey found"

        papers_count = len(survey.get("papers", []))

        return f'''
# Survey Report: {survey['name']}

**Generated:** {datetime.now().strftime("%Y-%m-%d")}
**Query:** {survey['query']}
**Papers Analyzed:** {papers_count}

## Executive Summary
[AI-generated summary of key findings]

## Research Themes
[Main research themes and categorization]

## Methodologies
[Common approaches and techniques]

## Key Findings
[Major contributions from each paper]

## Evaluation & Benchmarks
[Datasets, metrics, and comparative results]

## Open Challenges
[Limitations and future work]

## Conclusion
[Synthesis of the survey findings]

## References
[List of papers included in this survey]
'''


def main():
    parser = argparse.ArgumentParser(description="Survey Manager for academic paper surveys")
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # Create command
    create_parser = subparsers.add_parser("create", help="Create a new survey")
    create_parser.add_argument("--name", "-n", required=True, help="Survey name")
    create_parser.add_argument("--query", "-q", required=True, help="Search query")
    create_parser.add_argument("--year-from", type=int, help="Start year")
    create_parser.add_argument("--year-to", type=int, help="End year")
    create_parser.add_argument("--notebook-url", help="NotebookLM URL (optional)")
    create_parser.add_argument("--description", help="Survey description")

    # List command
    list_parser = subparsers.add_parser("list", help="List all surveys")

    # Show command
    show_parser = subparsers.add_parser("show", help="Show survey details")
    show_parser.add_argument("--survey-id", "-s", help="Survey ID (default: active)")

    # Search command
    search_parser = subparsers.add_parser("search", help="Run paper search")
    search_parser.add_argument("--survey-id", "-s", help="Survey ID (default: active)")

    # Download command
    download_parser = subparsers.add_parser("download", help="Download PDFs")
    download_parser.add_argument("--survey-id", "-s", help="Survey ID (default: active)")

    # Upload instructions command
    upload_parser = subparsers.add_parser("upload", help="Show upload instructions")
    upload_parser.add_argument("--survey-id", "-s", help="Survey ID (default: active)")

    # Suggestions command
    suggest_parser = subparsers.add_parser("suggest", help="Get query suggestions")
    suggest_parser.add_argument("--survey-id", "-s", help="Survey ID (default: active)")

    # Report template command
    report_parser = subparsers.add_parser("report", help="Generate report template")
    report_parser.add_argument("--survey-id", "-s", help="Survey ID (default: active)")

    # Complete step command
    step_parser = subparsers.add_parser("complete-step", help="Mark step as complete")
    step_parser.add_argument("--survey-id", "-s", required=True, help="Survey ID")
    step_parser.add_argument("--step", required=True,
                             choices=["search", "download", "upload", "query", "report"])

    # Set notebook command
    notebook_parser = subparsers.add_parser("set-notebook", help="Set notebook URL")
    notebook_parser.add_argument("--survey-id", "-s", help="Survey ID (default: active)")
    notebook_parser.add_argument("--url", required=True, help="NotebookLM URL")

    # Delete command
    delete_parser = subparsers.add_parser("delete", help="Delete a survey")
    delete_parser.add_argument("--survey-id", "-s", required=True, help="Survey ID")

    # Run all command
    run_parser = subparsers.add_parser("run", help="Run complete pipeline (search + download)")
    run_parser.add_argument("--survey-id", "-s", help="Survey ID (default: active)")

    args = parser.parse_args()

    manager = SurveyManager()

    if args.command == "create":
        survey = manager.create(
            name=args.name,
            query=args.query,
            year_from=args.year_from,
            year_to=args.year_to,
            notebook_url=args.notebook_url,
            description=args.description
        )
        print(f"\nSurvey ID: {survey['id']}")
        print(f"\nNext steps:")
        print(f"1. Run search: python scripts/run.py survey_manager.py search")
        print(f"2. Download PDFs: python scripts/run.py survey_manager.py download")
        print(f"3. Upload to NotebookLM: python scripts/run.py survey_manager.py upload")

    elif args.command == "list":
        surveys = manager.list_surveys()
        if not surveys:
            print("No surveys found")
        else:
            active = manager.data.get("active_survey_id")
            print(f"\n{'ID':<30} {'Name':<30} {'Status':<15} {'Papers':<10}")
            print("-" * 85)
            for s in surveys:
                marker = "* " if s["id"] == active else "  "
                papers = len(s.get("papers", []))
                print(f"{marker}{s['id']:<28} {s['name'][:28]:<30} {s['status']:<15} {papers:<10}")

    elif args.command == "show":
        survey = manager.get(args.survey_id)
        if not survey:
            print("Survey not found")
        else:
            print(json.dumps(survey, indent=2))

    elif args.command == "search":
        manager.run_search(args.survey_id)

    elif args.command == "download":
        manager.run_download(args.survey_id)

    elif args.command == "upload":
        print(manager.get_upload_instructions(args.survey_id))

    elif args.command == "suggest":
        suggestions = manager.get_query_suggestions(args.survey_id)
        print("\nSuggested questions for NotebookLM:\n")
        for i, q in enumerate(suggestions, 1):
            print(f"{i}. {q}\n")

    elif args.command == "report":
        print(manager.generate_report_template(args.survey_id))

    elif args.command == "complete-step":
        manager.add_step(args.survey_id, args.step)
        print(f"Step '{args.step}' marked as complete")

    elif args.command == "set-notebook":
        survey_id = args.survey_id or manager.data.get("active_survey_id")
        if survey_id:
            manager.update(survey_id, {"notebook_url": args.url})
            print(f"Notebook URL set for survey: {survey_id}")

    elif args.command == "delete":
        manager.delete(args.survey_id)

    elif args.command == "run":
        survey_id = args.survey_id or manager.data.get("active_survey_id")
        if not survey_id:
            print("No survey specified. Create one first.")
            return 1

        print(f"\nRunning complete pipeline for survey: {survey_id}\n")

        if manager.run_search(survey_id):
            if manager.run_download(survey_id):
                print(manager.get_upload_instructions(survey_id))
                print("\n" + "="*60)
                print("NEXT: Upload PDFs to NotebookLM, then query!")
                print("="*60)

    else:
        parser.print_help()

    return 0


if __name__ == "__main__":
    sys.exit(main())
