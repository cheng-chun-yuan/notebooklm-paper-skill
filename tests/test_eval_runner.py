"""Tests for scripts.eval.eval_runner module."""

import json

import pytest

from scripts.eval.eval_runner import (
    check_file_contains,
    check_file_exists,
    check_file_nonempty,
    check_file_section_count,
    check_json_field,
    check_word_count,
    run_criterion,
    run_phase_eval,
    save_eval_results,
)


# ---------------------------------------------------------------------------
# Check functions (tests 1-12)
# ---------------------------------------------------------------------------


class TestCheckFileExists:
    def test_check_file_exists_present(self, tmp_project_dir):
        (tmp_project_dir / "paper.md").write_text("hello")
        assert check_file_exists(tmp_project_dir, "paper.md") is True

    def test_check_file_exists_missing(self, tmp_project_dir):
        assert check_file_exists(tmp_project_dir, "nonexistent.md") is False


class TestCheckFileNonempty:
    def test_check_file_nonempty_has_content(self, tmp_project_dir):
        (tmp_project_dir / "paper.md").write_text("some content")
        assert check_file_nonempty(tmp_project_dir, "paper.md") is True

    def test_check_file_nonempty_empty(self, tmp_project_dir):
        (tmp_project_dir / "empty.md").write_text("")
        assert check_file_nonempty(tmp_project_dir, "empty.md") is False

    def test_check_file_nonempty_missing(self, tmp_project_dir):
        assert check_file_nonempty(tmp_project_dir, "missing.md") is False


class TestCheckFileContains:
    def test_check_file_contains_match(self, tmp_project_dir):
        (tmp_project_dir / "paper.md").write_text("# Introduction\nThis paper discusses AI.")
        assert check_file_contains(tmp_project_dir, "paper.md", "introduction") is True

    def test_check_file_contains_no_match(self, tmp_project_dir):
        (tmp_project_dir / "paper.md").write_text("# Introduction\nThis paper discusses AI.")
        assert check_file_contains(tmp_project_dir, "paper.md", "conclusion") is False

    def test_check_file_contains_case_insensitive(self, tmp_project_dir):
        (tmp_project_dir / "paper.md").write_text("Research Methodology is KEY")
        assert check_file_contains(tmp_project_dir, "paper.md", "research methodology") is True

    def test_check_file_contains_binary_file(self, tmp_project_dir):
        (tmp_project_dir / "binary.bin").write_bytes(b"\x80\x81\x82\xff\xfe")
        assert check_file_contains(tmp_project_dir, "binary.bin", "hello") is False


class TestCheckFileSectionCount:
    def test_check_file_section_count_enough(self, tmp_project_dir):
        content = "## Section 1\ntext\n## Section 2\ntext\n## Section 3\ntext\n"
        (tmp_project_dir / "paper.md").write_text(content)
        assert check_file_section_count(tmp_project_dir, "paper.md", "## ", 3) is True

    def test_check_file_section_count_too_few(self, tmp_project_dir):
        content = "## Section 1\ntext\n"
        (tmp_project_dir / "paper.md").write_text(content)
        assert check_file_section_count(tmp_project_dir, "paper.md", "## ", 3) is False


class TestCheckWordCount:
    def test_check_word_count_above_min(self, tmp_project_dir):
        (tmp_project_dir / "paper.md").write_text("word " * 100)
        assert check_word_count(tmp_project_dir, "paper.md", min_words=50) is True


# ---------------------------------------------------------------------------
# JSON field checks (tests 13-16)
# ---------------------------------------------------------------------------


class TestCheckJsonField:
    def test_check_json_field_list_enough(self, tmp_project_dir):
        data = {"references": ["ref1", "ref2", "ref3"]}
        (tmp_project_dir / "data.json").write_text(json.dumps(data))
        assert check_json_field(tmp_project_dir, "data.json", "references", min_items=3) is True

    def test_check_json_field_list_too_few(self, tmp_project_dir):
        data = {"references": ["ref1"]}
        (tmp_project_dir / "data.json").write_text(json.dumps(data))
        assert check_json_field(tmp_project_dir, "data.json", "references", min_items=5) is False

    def test_check_json_field_missing_file(self, tmp_project_dir):
        assert check_json_field(tmp_project_dir, "nonexistent.json", "key") is False

    def test_check_json_field_malformed_json(self, tmp_project_dir):
        (tmp_project_dir / "bad.json").write_text("{not valid json")
        assert check_json_field(tmp_project_dir, "bad.json", "key") is False


# ---------------------------------------------------------------------------
# Criterion runner (tests 17-19)
# ---------------------------------------------------------------------------


class TestRunCriterion:
    def test_run_criterion_pass(self, tmp_project_dir):
        (tmp_project_dir / "paper.md").write_text("content")
        criterion = {
            "id": "C01",
            "description": "Paper file exists",
            "check": "file_exists",
            "params": {"filepath": "paper.md"},
        }
        result = run_criterion(tmp_project_dir, criterion)
        assert result["pass"] is True
        assert result["detail"] is None

    def test_run_criterion_fail(self, tmp_project_dir):
        criterion = {
            "id": "C02",
            "description": "Paper file exists",
            "check": "file_exists",
            "params": {"filepath": "missing.md"},
        }
        result = run_criterion(tmp_project_dir, criterion)
        assert result["pass"] is False
        assert result["detail"] is not None

    def test_run_criterion_unknown_check(self, tmp_project_dir):
        criterion = {
            "id": "C03",
            "description": "Unknown check",
            "check": "nonexistent_check",
            "params": {},
        }
        result = run_criterion(tmp_project_dir, criterion)
        assert result["pass"] is False
        assert "Unknown check type" in result["detail"]


# ---------------------------------------------------------------------------
# Phase eval (tests 20-21)
# ---------------------------------------------------------------------------


class TestRunPhaseEval:
    def test_run_phase_eval_all_pass(self, tmp_project_dir, monkeypatch):
        criteria = [
            {"id": "C01", "description": "File exists", "check": "file_exists",
             "params": {"filepath": "paper.md"}},
            {"id": "C02", "description": "File nonempty", "check": "file_nonempty",
             "params": {"filepath": "paper.md"}},
        ]
        (tmp_project_dir / "paper.md").write_text("content here")
        monkeypatch.setattr(
            "scripts.eval.eval_runner.load_criteria", lambda phase: criteria
        )
        result = run_phase_eval("01", tmp_project_dir)
        assert result["pass_rate"] == 100.0
        assert result["score"] == "2/2"

    def test_run_phase_eval_partial(self, tmp_project_dir, monkeypatch):
        criteria = [
            {"id": "C01", "description": "File exists", "check": "file_exists",
             "params": {"filepath": "paper.md"}},
            {"id": "C02", "description": "Other exists", "check": "file_exists",
             "params": {"filepath": "missing.md"}},
        ]
        (tmp_project_dir / "paper.md").write_text("content")
        monkeypatch.setattr(
            "scripts.eval.eval_runner.load_criteria", lambda phase: criteria
        )
        result = run_phase_eval("01", tmp_project_dir)
        assert result["pass_rate"] == 50.0
        assert result["score"] == "1/2"


# ---------------------------------------------------------------------------
# Results management (tests 22-24)
# ---------------------------------------------------------------------------


class TestSaveEvalResults:
    def test_save_eval_results_creates_file(self, tmp_project_dir):
        eval_result = {"phase": "discover", "score": "3/3", "pass_rate": 100.0}
        save_eval_results(tmp_project_dir, eval_result)
        results_file = tmp_project_dir / "eval-results.json"
        assert results_file.exists()
        data = json.loads(results_file.read_text())
        assert len(data) == 1
        assert data[0]["phase"] == "discover"

    def test_save_eval_results_appends(self, tmp_project_dir):
        existing = [{"phase": "discover", "score": "2/3"}]
        (tmp_project_dir / "eval-results.json").write_text(json.dumps(existing))
        new_result = {"phase": "position", "score": "1/1"}
        save_eval_results(tmp_project_dir, new_result)
        data = json.loads((tmp_project_dir / "eval-results.json").read_text())
        assert len(data) == 2
        assert data[0]["phase"] == "discover"
        assert data[1]["phase"] == "position"

    def test_save_eval_results_caps_at_100(self, tmp_project_dir):
        existing = [{"phase": f"entry-{i}"} for i in range(100)]
        (tmp_project_dir / "eval-results.json").write_text(json.dumps(existing))
        save_eval_results(tmp_project_dir, {"phase": "overflow"})
        data = json.loads((tmp_project_dir / "eval-results.json").read_text())
        assert len(data) == 100
        # The oldest entry should have been dropped; the newest is last.
        assert data[-1]["phase"] == "overflow"
        assert data[0]["phase"] == "entry-1"


# ---------------------------------------------------------------------------
# Word count extras (tests 25-26)
# ---------------------------------------------------------------------------


class TestCheckWordCountExtra:
    def test_check_word_count_below_min(self, tmp_project_dir):
        (tmp_project_dir / "short.md").write_text("just a few words")
        assert check_word_count(tmp_project_dir, "short.md", min_words=100) is False

    def test_check_word_count_with_max(self, tmp_project_dir):
        (tmp_project_dir / "paper.md").write_text("word " * 50)
        # 50 words, within range 10-60
        assert check_word_count(tmp_project_dir, "paper.md", min_words=10, max_words=60) is True
        # 50 words, above max of 30
        assert check_word_count(tmp_project_dir, "paper.md", min_words=10, max_words=30) is False
