#!/usr/bin/env python3
"""
NotebookLM PDF Upload Script
Uses notebooklm-py library for direct API upload (no browser needed)
"""

import argparse
import asyncio
import re
import sys
from pathlib import Path
from typing import List

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.auth_manager import AuthManager
from notebook.notebook_manager import NotebookLibrary


def extract_notebook_id(url: str) -> str:
    """Extract notebook UUID from NotebookLM URL"""
    match = re.search(r'notebook/([a-f0-9-]{36})', url)
    if match:
        return match.group(1)
    if re.match(r'^[a-f0-9-]{36}$', url):
        return url
    raise ValueError(f"Cannot extract notebook ID from: {url}")


async def _upload(notebook_id: str, pdf_paths: List[Path]) -> dict:
    from notebooklm import NotebookLMClient

    results = {"success": True, "uploaded": [], "failed": [], "errors": []}

    async with await NotebookLMClient.from_storage() as client:
        for i, pdf_path in enumerate(pdf_paths, 1):
            print(f"  [{i}/{len(pdf_paths)}] Uploading: {pdf_path.name}...", end=" ", flush=True)
            try:
                src = await client.sources.add_file(notebook_id, pdf_path, wait=True, wait_timeout=180)
                results["uploaded"].append(str(pdf_path))
                print(f"OK (status={src.status})")
            except Exception as e:
                results["failed"].append(str(pdf_path))
                results["errors"].append(f"{pdf_path.name}: {e}")
                print(f"FAILED: {e}")

    if results["failed"]:
        results["success"] = False
    return results


def upload_pdfs_to_notebook(notebook_id: str, pdf_paths: List[Path]) -> dict:
    """Upload PDFs to NotebookLM via API"""
    auth = AuthManager()
    if not auth.is_authenticated():
        print("Not authenticated. Run: python scripts/run.py auth setup")
        return {"success": False, "error": "Not authenticated"}

    print(f"Uploading {len(pdf_paths)} PDFs to NotebookLM...")
    print(f"Notebook: {notebook_id}")

    try:
        results = asyncio.run(_upload(notebook_id, pdf_paths))

        print(f"\n{'='*50}")
        print(f"Upload Complete!")
        print(f"  Uploaded: {len(results['uploaded'])}")
        print(f"  Failed: {len(results['failed'])}")
        if results["failed"]:
            print(f"\nFailed files:")
            for f in results["failed"]:
                print(f"  - {f}")
        return results

    except Exception as e:
        print(f"Error: {e}")
        return {"success": False, "errors": [str(e)]}


def main():
    parser = argparse.ArgumentParser(description='Upload PDFs to NotebookLM')
    parser.add_argument('--notebook-url', help='NotebookLM notebook URL or UUID')
    parser.add_argument('--notebook-id', help='Notebook ID from library')
    parser.add_argument('--pdf', help='Single PDF file to upload')
    parser.add_argument('--pdf-dir', help='Directory containing PDFs to upload')

    args = parser.parse_args()

    # Resolve notebook ID
    notebook_id = None
    if args.notebook_url:
        notebook_id = extract_notebook_id(args.notebook_url)
    elif args.notebook_id:
        library = NotebookLibrary()
        notebook = library.get_notebook(args.notebook_id)
        if notebook:
            notebook_id = extract_notebook_id(notebook['url'])
        else:
            print(f"Notebook '{args.notebook_id}' not found")
            return 1
    else:
        library = NotebookLibrary()
        active = library.get_active_notebook()
        if active:
            notebook_id = extract_notebook_id(active['url'])
            print(f"Using active notebook: {active['name']}")
        else:
            print("No notebook specified. Use --notebook-url or --notebook-id")
            return 1

    # Collect PDFs
    pdf_paths = []
    if args.pdf:
        pdf_path = Path(args.pdf)
        if pdf_path.exists() and pdf_path.suffix.lower() == '.pdf':
            pdf_paths.append(pdf_path)
        else:
            print(f"PDF not found or invalid: {args.pdf}")
            return 1

    if args.pdf_dir:
        pdf_dir = Path(args.pdf_dir)
        if pdf_dir.is_dir():
            pdf_paths.extend(sorted(pdf_dir.glob("*.pdf")))
        else:
            print(f"Directory not found: {args.pdf_dir}")
            return 1

    if not pdf_paths:
        print("No PDF files specified. Use --pdf or --pdf-dir")
        return 1

    print(f"Found {len(pdf_paths)} PDF(s) to upload:")
    for p in pdf_paths:
        print(f"  - {p.name}")
    print()

    results = upload_pdfs_to_notebook(notebook_id=notebook_id, pdf_paths=pdf_paths)
    return 0 if results["success"] else 1


if __name__ == "__main__":
    sys.exit(main())
