#!/usr/bin/env python3
"""
Authentication Manager for NotebookLM
Uses notebooklm-py library for auth via `notebooklm login`
"""

import json
import time
import argparse
import subprocess
import sys
from pathlib import Path
from typing import Dict, Any

sys.path.insert(0, str(Path(__file__).parent.parent))

from config import AUTH_INFO_FILE, DATA_DIR, NOTEBOOKLM_STORAGE_PATH


class AuthManager:
    """Manages authentication for NotebookLM via notebooklm-py"""

    def __init__(self):
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        self.storage_path = NOTEBOOKLM_STORAGE_PATH
        self.auth_info_file = AUTH_INFO_FILE

    def is_authenticated(self) -> bool:
        """Check if valid authentication exists"""
        if not self.storage_path.exists():
            return False

        age_days = (time.time() - self.storage_path.stat().st_mtime) / 86400
        if age_days > 7:
            print(f"⚠️ Auth state is {age_days:.1f} days old, may need re-authentication")

        return True

    def get_auth_info(self) -> Dict[str, Any]:
        """Get authentication information"""
        info = {
            'authenticated': self.is_authenticated(),
            'state_file': str(self.storage_path),
            'state_exists': self.storage_path.exists()
        }

        if self.auth_info_file.exists():
            try:
                with open(self.auth_info_file, 'r') as f:
                    info.update(json.load(f))
            except Exception:
                pass

        if info['state_exists']:
            info['state_age_hours'] = (time.time() - self.storage_path.stat().st_mtime) / 3600

        return info

    def setup_auth(self) -> bool:
        """Run `notebooklm login` to authenticate"""
        print("🔐 Starting authentication via notebooklm login...")
        try:
            result = subprocess.run(
                [sys.executable, "-m", "notebooklm", "login"],
                check=False
            )
            if result.returncode == 0 and self.storage_path.exists():
                self._save_auth_info()
                return True
            # Also check if storage exists even if return code is non-zero
            if self.storage_path.exists():
                self._save_auth_info()
                return True
            print("❌ Authentication failed")
            return False
        except FileNotFoundError:
            print("❌ notebooklm-py not installed. Run: pip install notebooklm-py[browser]")
            return False

    def _save_auth_info(self):
        try:
            info = {
                'authenticated_at': time.time(),
                'authenticated_at_iso': time.strftime('%Y-%m-%d %H:%M:%S')
            }
            with open(self.auth_info_file, 'w') as f:
                json.dump(info, f, indent=2)
        except Exception:
            pass

    def clear_auth(self) -> bool:
        """Clear authentication data"""
        print("🗑️ Clearing authentication data...")
        try:
            if self.storage_path.exists():
                self.storage_path.unlink()
                print("  ✅ Removed auth storage")
            if self.auth_info_file.exists():
                self.auth_info_file.unlink()
                print("  ✅ Removed auth info")
            return True
        except Exception as e:
            print(f"  ❌ Error clearing auth: {e}")
            return False

    def re_auth(self) -> bool:
        """Clear and re-authenticate"""
        print("🔄 Starting re-authentication...")
        self.clear_auth()
        return self.setup_auth()

    def validate_auth(self) -> bool:
        """Validate auth by attempting to list notebooks"""
        if not self.is_authenticated():
            return False

        print("🔍 Validating authentication...")
        try:
            import asyncio
            from notebooklm import NotebookLMClient

            async def _validate():
                async with await NotebookLMClient.from_storage() as client:
                    await client.notebooks.list()
                    return True

            result = asyncio.run(_validate())
            print("  ✅ Authentication is valid")
            return result
        except Exception as e:
            print(f"  ❌ Validation failed: {e}")
            return False


def main():
    parser = argparse.ArgumentParser(description='Manage NotebookLM authentication')
    subparsers = parser.add_subparsers(dest='command', help='Commands')

    subparsers.add_parser('setup', help='Setup authentication')
    subparsers.add_parser('status', help='Check authentication status')
    subparsers.add_parser('validate', help='Validate authentication')
    subparsers.add_parser('clear', help='Clear authentication')
    subparsers.add_parser('reauth', help='Re-authenticate')

    args = parser.parse_args()
    auth = AuthManager()

    if args.command == 'setup':
        if auth.setup_auth():
            print("\n✅ Authentication setup complete!")
        else:
            print("\n❌ Authentication setup failed")
            exit(1)
    elif args.command == 'status':
        info = auth.get_auth_info()
        print("\n🔐 Authentication Status:")
        print(f"  Authenticated: {'Yes' if info['authenticated'] else 'No'}")
        if info.get('state_age_hours'):
            print(f"  State age: {info['state_age_hours']:.1f} hours")
        if info.get('authenticated_at_iso'):
            print(f"  Last auth: {info['authenticated_at_iso']}")
        print(f"  State file: {info['state_file']}")
    elif args.command == 'validate':
        if auth.validate_auth():
            print("Authentication is valid and working")
        else:
            print("Authentication is invalid. Run: auth setup")
    elif args.command == 'clear':
        auth.clear_auth()
    elif args.command == 'reauth':
        if auth.re_auth():
            print("\n✅ Re-authentication complete!")
        else:
            print("\n❌ Re-authentication failed")
            exit(1)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
