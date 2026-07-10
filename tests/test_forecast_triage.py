from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


triage = load_module("forecast_triage_tests", REPO_ROOT / "scripts" / "triage_forecast_ledger.py")
bootstrap = load_module("forecast_bootstrap_tests", REPO_ROOT / "scripts" / "bootstrap_daily_run.py")


def ledger_text(review_date: str = "2026-07-10", accountable: str = "yes") -> str:
    return f"""# Ledger

| Hook ID | Date | Crisis Object | Claim | Probability Band | Review Date | Source Run | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `NG-20260707-F01` | `2026-07-07` | Object | Bounded claim | `likely` | `{review_date}` | [run](x) | `open` |

| Hook ID | Authored No Later Than | Timing Provenance | Forecast Type | Resolution Status | Accountable | Review Note |
| --- | --- | --- | --- | --- | --- | --- |
| `NG-20260707-F01` | `2026-07-08` | `git_commit_upper_bound` | `ex_ante` | `open` | `{accountable}` | Prospective review. |
"""


def test_accountable_ex_ante_forecast_passes_before_due_date() -> None:
    text = ledger_text()
    failures = triage.validate_triage(
        triage.parse_entries(text), triage.parse_triage(text), "2026-07-09"
    )
    assert failures == []


def test_overdue_accountable_forecast_fails() -> None:
    text = ledger_text(review_date="2026-07-09")
    failures = triage.validate_triage(
        triage.parse_entries(text), triage.parse_triage(text), "2026-07-09"
    )
    assert failures == ["overdue accountable forecast remains open: NG-20260707-F01"]


def test_non_ex_ante_row_cannot_be_accountable() -> None:
    text = ledger_text().replace("`ex_ante`", "`retrospective_hypothesis`")
    failures = triage.validate_triage(
        triage.parse_entries(text), triage.parse_triage(text), "2026-07-09"
    )
    assert "only ex_ante forecasts may be accountable: NG-20260707-F01" in failures


def test_unresolvable_is_allowed_without_forcing_outcome() -> None:
    text = ledger_text(accountable="no").replace(
        "`open` | `no`", "`unresolvable_with_authorized_evidence` | `no`"
    )
    failures = triage.validate_triage(
        triage.parse_entries(text), triage.parse_triage(text), "2026-07-20"
    )
    assert failures == []


def test_due_review_carry_forward_excludes_non_accountable_rows(monkeypatch) -> None:
    text = """# Ledger
| Hook ID | Date | Crisis Object | Claim | Probability Band | Review Date | Source Run | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `NG-20260707-F01` | `2026-07-07` | Object | Accountable claim | `likely` | `2026-07-10` | [run](x) | `open` |
| `NG-20260630-F01` | `2026-06-30` | Object | Retrospective claim | `likely` | `2026-07-10` | [run](x) | `open` |
| `NG-20260707-F01` | `2026-07-08` | `git_commit_upper_bound` | `ex_ante` | `open` | `yes` | Prospective. |
| `NG-20260630-F01` | `2026-07-07` | `git_commit_upper_bound` | `retrospective_hypothesis` | `excluded_retrospective` | `no` | Retrospective. |
"""
    monkeypatch.setattr(bootstrap, "load_ledger_text", lambda: text)

    hooks = bootstrap.extract_due_review_hooks("2026-07-20")

    assert [hook["hook_id"] for hook in hooks] == ["NG-20260707-F01"]


def test_due_review_link_is_rebased_for_daily_forecast() -> None:
    text = "# Forecast\n\n## Hooks\n"
    hooks = [
        {
            "hook_id": "NG-20260707-F01",
            "hook_date": "2026-07-07",
            "crisis_object": "Object",
            "claim": "Claim",
            "band": "likely",
            "review_date": "2026-07-10",
            "source_label": "2026-07-07",
            "source_link": "../daily/2026-07-07/forecast.md",
        }
    ]

    updated = bootstrap.inject_due_review_hooks(text, hooks)

    assert "[2026-07-07](../2026-07-07/forecast.md)" in updated
    assert "../daily/2026-07-07/forecast.md" not in updated
