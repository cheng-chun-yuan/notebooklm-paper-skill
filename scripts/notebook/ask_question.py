#!/usr/bin/env python3
"""
NotebookLM Question Interface
Uses notebooklm-py library for direct API access (no browser needed)
"""

import argparse
import asyncio
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.auth_manager import AuthManager
from notebook.notebook_manager import NotebookLibrary

FOLLOW_UP_REMINDER = (
    "\n\nEXTREMELY IMPORTANT: Is that ALL you need to know? "
    "You can always ask another question! Think about it carefully: "
    "before you reply to the user, review their original request and this answer. "
    "If anything is still unclear or missing, ask me another comprehensive question."
)


def extract_notebook_id(url: str) -> str:
    """Extract notebook UUID from NotebookLM URL"""
    match = re.search(r'notebook/([a-f0-9-]{36})', url)
    if match:
        return match.group(1)
    # Maybe it's already a UUID
    if re.match(r'^[a-f0-9-]{36}$', url):
        return url
    raise ValueError(f"Cannot extract notebook ID from: {url}")


async def _ask(notebook_id: str, question: str) -> str:
    from notebooklm import NotebookLMClient

    async with await NotebookLMClient.from_storage() as client:
        result = await client.chat.ask(notebook_id, question)
        answer = result.answer
        if result.references:
            answer += "\n\n--- Sources ---"
            for ref in result.references:
                answer += f"\n  [{ref.source_id[:8]}] {ref}"
        return answer


def ask_notebooklm(question: str, notebook_id: str) -> str:
    """Ask a question to NotebookLM via API"""
    auth = AuthManager()
    if not auth.is_authenticated():
        print("⚠️ Not authenticated. Run: python scripts/run.py auth setup")
        return None

    print(f"💬 Asking: {question[:80]}...")
    print(f"📚 Notebook: {notebook_id}")

    try:
        answer = asyncio.run(_ask(notebook_id, question))
        print("  ✅ Got answer!")
        return answer + FOLLOW_UP_REMINDER
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return None


def resolve_notebook_id(args) -> str:
    """Resolve notebook ID from args (URL, ID, or active notebook)"""
    if args.notebook_url:
        return extract_notebook_id(args.notebook_url)

    if args.notebook_id:
        library = NotebookLibrary()
        notebook = library.get_notebook(args.notebook_id)
        if notebook:
            return extract_notebook_id(notebook['url'])
        print(f"❌ Notebook '{args.notebook_id}' not found in library")
        return None

    library = NotebookLibrary()
    active = library.get_active_notebook()
    if active:
        print(f"📚 Using active notebook: {active['name']}")
        return extract_notebook_id(active['url'])

    notebooks = library.list_notebooks()
    if notebooks:
        print("\n📚 Available notebooks:")
        for nb in notebooks:
            mark = " [ACTIVE]" if nb.get('id') == library.active_notebook_id else ""
            print(f"  {nb['id']}: {nb['name']}{mark}")
        print("\nSpecify with --notebook-url or --notebook-id")
    else:
        print("❌ No notebooks in library. Use --notebook-url with a NotebookLM URL")
    return None


def main():
    parser = argparse.ArgumentParser(description='Ask NotebookLM a question')
    parser.add_argument('--question', required=True, help='Question to ask')
    parser.add_argument('--notebook-url', help='NotebookLM notebook URL or UUID')
    parser.add_argument('--notebook-id', help='Notebook ID from library')

    args = parser.parse_args()

    notebook_id = resolve_notebook_id(args)
    if not notebook_id:
        return 1

    answer = ask_notebooklm(question=args.question, notebook_id=notebook_id)

    if answer:
        print("\n" + "=" * 60)
        print(f"Question: {args.question}")
        print("=" * 60)
        print()
        print(answer)
        print()
        print("=" * 60)
        return 0
    else:
        print("\n❌ Failed to get answer")
        return 1


if __name__ == "__main__":
    sys.exit(main())
