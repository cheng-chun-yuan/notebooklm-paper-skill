"""Tests for scripts.core.dotpaper module."""

import pytest

from scripts.core.dotpaper import (
    create_dotpaper,
    find_dotpaper,
    load_dotpaper,
    save_dotpaper,
)


# ---------------------------------------------------------------------------
# 1. create_dotpaper_minimal — only required fields
# ---------------------------------------------------------------------------


class TestCreateDotpaperMinimal:
    def test_create_dotpaper_minimal(self, tmp_path):
        config = create_dotpaper(
            directory=str(tmp_path),
            project="my-project",
            topic="Some topic",
            goal="Some goal",
        )
        assert config["project"] == "my-project"
        assert config["topic"] == "Some topic"
        assert config["goal"] == "Some goal"
        assert config["venue"] == ""
        assert config["phase"] == "init"
        assert config["phases_completed"] == []
        assert (tmp_path / ".paper").exists()


# ---------------------------------------------------------------------------
# 2. create_dotpaper_full — all fields
# ---------------------------------------------------------------------------


class TestCreateDotpaperFull:
    def test_create_dotpaper_full(self, tmp_path):
        config = create_dotpaper(
            directory=str(tmp_path),
            project="behavioral-vcs",
            topic="Verifiable credentials for AI agent identity",
            goal="Propose a framework binding agent actions to verifiable identity",
            venue="USENIX Security 2027",
            venue_type="conference",
            deadline="2027-02-01",
            page_limit=18,
            format="usenix",
            notebook="https://notebooklm.google.com/notebook/abc123",
            vault="/custom/vault/path",
            keywords=["verifiable credentials", "agent identity"],
            related_fields=["IAM", "decentralized identity"],
        )
        assert config["project"] == "behavioral-vcs"
        assert config["venue"] == "USENIX Security 2027"
        assert config["venue_type"] == "conference"
        assert config["deadline"] == "2027-02-01"
        assert config["page_limit"] == 18
        assert config["format"] == "usenix"
        assert config["notebook"] == "https://notebooklm.google.com/notebook/abc123"
        assert config["vault"] == "/custom/vault/path"
        assert config["keywords"] == ["verifiable credentials", "agent identity"]
        assert config["related_fields"] == ["IAM", "decentralized identity"]


# ---------------------------------------------------------------------------
# 3. load_dotpaper — reads back correctly
# ---------------------------------------------------------------------------


class TestLoadDotpaper:
    def test_load_dotpaper(self, tmp_path):
        create_dotpaper(
            directory=str(tmp_path),
            project="load-test",
            topic="Testing load",
            goal="Verify round-trip",
        )
        loaded = load_dotpaper(str(tmp_path))
        assert loaded is not None
        assert loaded["project"] == "load-test"
        assert loaded["topic"] == "Testing load"
        assert loaded["goal"] == "Verify round-trip"


# ---------------------------------------------------------------------------
# 4. load_dotpaper_missing — returns None
# ---------------------------------------------------------------------------


class TestLoadDotpaperMissing:
    def test_load_dotpaper_missing(self, tmp_path):
        result = load_dotpaper(str(tmp_path))
        assert result is None


# ---------------------------------------------------------------------------
# 5. save_dotpaper_updates — preserves existing, updates changed
# ---------------------------------------------------------------------------


class TestSaveDotpaperUpdates:
    def test_save_dotpaper_updates(self, tmp_path):
        config = create_dotpaper(
            directory=str(tmp_path),
            project="update-test",
            topic="Original topic",
            goal="Original goal",
        )
        config["topic"] = "Updated topic"
        config["phase"] = "discover"
        save_dotpaper(str(tmp_path), config)

        reloaded = load_dotpaper(str(tmp_path))
        assert reloaded["topic"] == "Updated topic"
        assert reloaded["phase"] == "discover"
        # Preserved fields
        assert reloaded["project"] == "update-test"
        assert reloaded["goal"] == "Original goal"


# ---------------------------------------------------------------------------
# 6. find_dotpaper_walks_up — finds .paper in parent directory
# ---------------------------------------------------------------------------


class TestFindDotpaperWalksUp:
    def test_find_dotpaper_walks_up(self, tmp_path):
        create_dotpaper(
            directory=str(tmp_path),
            project="walk-test",
            topic="Walk up",
            goal="Find parent",
        )
        child = tmp_path / "sub" / "deep"
        child.mkdir(parents=True)

        found = find_dotpaper(str(child))
        assert found is not None
        assert found == tmp_path / ".paper"


# ---------------------------------------------------------------------------
# 7. find_dotpaper_none — returns None when no .paper
# ---------------------------------------------------------------------------


class TestFindDotpaperNone:
    def test_find_dotpaper_none(self, tmp_path):
        result = find_dotpaper(str(tmp_path))
        assert result is None


# ---------------------------------------------------------------------------
# 8. dotpaper_vault_default — defaults to ~/.paper/vaults/{project}
# ---------------------------------------------------------------------------


class TestDotpaperVaultDefault:
    def test_dotpaper_vault_default(self, tmp_path):
        config = create_dotpaper(
            directory=str(tmp_path),
            project="default-vault",
            topic="Test",
            goal="Test",
        )
        from pathlib import Path

        expected = str(Path.home() / ".paper" / "vaults" / "default-vault")
        assert config["vault"] == expected


# ---------------------------------------------------------------------------
# 9. dotpaper_vault_custom — respects custom vault path
# ---------------------------------------------------------------------------


class TestDotpaperVaultCustom:
    def test_dotpaper_vault_custom(self, tmp_path):
        config = create_dotpaper(
            directory=str(tmp_path),
            project="custom-vault",
            topic="Test",
            goal="Test",
            vault="/my/custom/vault",
        )
        assert config["vault"] == "/my/custom/vault"
