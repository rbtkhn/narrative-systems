from __future__ import annotations

import argparse
import re
from collections import Counter
from dataclasses import dataclass
from datetime import date
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
LEDGER_PATH = REPO_ROOT / "narrative-geopolitics" / "work" / "forecasts" / "forecast-ledger.md"

FORECAST_TYPES = {
    "ex_ante",
    "retrospective_hypothesis",
    "indicator",
    "falsifier",
    "unscorable",
}
RESOLUTION_STATUSES = {
    "open",
    "hit",
    "miss",
    "mixed",
    "unresolved",
    "unresolvable_with_authorized_evidence",
    "excluded_retrospective",
    "excluded_unscorable",
}

ENTRY_RE = re.compile(
    r"^\|\s*`(NG-\d{8}-F\d{2})`\s*\|\s*`([^`]+)`\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|"
    r"\s*`(low|plausible|likely|high)`\s*\|\s*`([^`]+)`\s*\|.*?\|\s*`([^`]+)`\s*\|$"
)
TRIAGE_RE = re.compile(
    r"^\|\s*`(NG-\d{8}-F\d{2})`\s*\|\s*`([^`]+)`\s*\|\s*`([^`]+)`\s*\|"
    r"\s*`([^`]+)`\s*\|\s*`([^`]+)`\s*\|\s*`(yes|no)`\s*\|\s*(.*?)\s*\|$"
)


@dataclass(frozen=True)
class ForecastEntry:
    hook_id: str
    run_date: str
    crisis_object: str
    claim: str
    probability_band: str
    review_date: str
    status: str


@dataclass(frozen=True)
class ForecastTriage:
    hook_id: str
    authorship_bound: str
    timing_provenance: str
    forecast_type: str
    resolution_status: str
    accountable: bool
    review_note: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate forecast-ledger triage metadata.")
    parser.add_argument("--as-of", default=date.today().isoformat(), help="Review cutoff in YYYY-MM-DD format.")
    return parser.parse_args()


def parse_entries(text: str) -> list[ForecastEntry]:
    entries: list[ForecastEntry] = []
    for line in text.splitlines():
        match = ENTRY_RE.match(line.strip())
        if not match:
            continue
        entries.append(ForecastEntry(*match.groups()))
    return entries


def parse_triage(text: str) -> list[ForecastTriage]:
    rows: list[ForecastTriage] = []
    for line in text.splitlines():
        match = TRIAGE_RE.match(line.strip())
        if not match:
            continue
        hook_id, bound, provenance, forecast_type, resolution, accountable, note = match.groups()
        rows.append(
            ForecastTriage(
                hook_id=hook_id,
                authorship_bound=bound,
                timing_provenance=provenance,
                forecast_type=forecast_type,
                resolution_status=resolution,
                accountable=accountable == "yes",
                review_note=note,
            )
        )
    return rows


def validate_triage(
    entries: list[ForecastEntry], triage_rows: list[ForecastTriage], as_of: str
) -> list[str]:
    failures: list[str] = []
    entry_ids = [entry.hook_id for entry in entries]
    triage_ids = [row.hook_id for row in triage_rows]

    for hook_id, count in Counter(triage_ids).items():
        if count > 1:
            failures.append(f"duplicate triage row: {hook_id}")
    for hook_id in sorted(set(entry_ids) - set(triage_ids)):
        failures.append(f"missing triage row: {hook_id}")
    for hook_id in sorted(set(triage_ids) - set(entry_ids)):
        failures.append(f"triage row has no ledger entry: {hook_id}")

    entries_by_id = {entry.hook_id: entry for entry in entries}
    for row in triage_rows:
        if row.forecast_type not in FORECAST_TYPES:
            failures.append(f"invalid forecast type for {row.hook_id}: {row.forecast_type}")
        if row.resolution_status not in RESOLUTION_STATUSES:
            failures.append(f"invalid resolution status for {row.hook_id}: {row.resolution_status}")
        if row.accountable and row.forecast_type != "ex_ante":
            failures.append(f"only ex_ante forecasts may be accountable: {row.hook_id}")
        if row.accountable and row.resolution_status.startswith("excluded_"):
            failures.append(f"accountable forecast cannot be excluded: {row.hook_id}")
        entry = entries_by_id.get(row.hook_id)
        if entry and row.accountable and entry.review_date <= as_of and row.resolution_status == "open":
            failures.append(f"overdue accountable forecast remains open: {row.hook_id}")
    return failures


def accountable_open_hook_ids(text: str, as_of: str | None = None) -> set[str]:
    entries = {entry.hook_id: entry for entry in parse_entries(text)}
    result: set[str] = set()
    for row in parse_triage(text):
        entry = entries.get(row.hook_id)
        if not entry or not row.accountable or row.resolution_status != "open":
            continue
        if as_of is None or entry.review_date <= as_of:
            result.add(row.hook_id)
    return result


def main() -> None:
    args = parse_args()
    text = LEDGER_PATH.read_text(encoding="utf-8")
    entries = parse_entries(text)
    triage_rows = parse_triage(text)
    failures = validate_triage(entries, triage_rows, args.as_of)
    print(f"entries={len(entries)}")
    print(f"triage_rows={len(triage_rows)}")
    print(f"accountable={sum(row.accountable for row in triage_rows)}")
    print(f"failures={len(failures)}")
    for failure in failures:
        print(f"FAIL {failure}")
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
