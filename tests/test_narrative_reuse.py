from __future__ import annotations

import importlib.util
import sys
from datetime import date
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPT = REPO_ROOT / "scripts" / "report_narrative_reuse.py"


def load_module():
    spec = importlib.util.spec_from_file_location("narrative_reuse_tests", SCRIPT)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


reuse = load_module()


def write_day(root: Path, run_date: str, paragraph: str) -> None:
    run = root / run_date
    run.mkdir(parents=True)
    (run / "synthesis.md").write_text(
        f"# Synthesis\n\n{paragraph}\n", encoding="utf-8"
    )
    (run / "daily-brief.md").write_text(
        "# Brief\n\nA distinct paragraph that is deliberately long enough to qualify "
        f"for the report and belongs only to {run_date}.\n",
        encoding="utf-8",
    )
    (run / "issue.md").write_text(f"# Issue\n\n{paragraph}\n", encoding="utf-8")


def test_report_detects_cross_date_reuse_and_excludes_generated_issue(tmp_path: Path) -> None:
    paragraph = (
        "This repeated analytical paragraph is intentionally longer than one hundred "
        "and twenty characters so the exact cross-date reuse detector includes it."
    )
    write_day(tmp_path, "2026-07-01", paragraph)
    write_day(tmp_path, "2026-07-02", paragraph)

    payload = reuse.report_payload(
        reuse.collect(date(2026, 7, 1), date(2026, 7, 2), tmp_path)
    )

    assert payload["repeated_instances"] == 2
    assert payload["groups"][0]["count"] == 2
    assert all("issue.md" not in item for item in payload["groups"][0]["artifacts"])


def test_report_rejects_reversed_range(tmp_path: Path) -> None:
    try:
        reuse.collect(date(2026, 7, 2), date(2026, 7, 1), tmp_path)
    except ValueError as error:
        assert "must not be later" in str(error)
    else:
        raise AssertionError("reversed range was accepted")
