from __future__ import annotations

import argparse
import sys
from datetime import date
from pathlib import Path

SCRIPTS_ROOT = Path(__file__).resolve().parent
if str(SCRIPTS_ROOT) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_ROOT))

from forecast_ledger import (
    FORECAST_TYPES,
    RESOLUTION_STATUSES,
    VERIFICATION_RE,
    VERIFICATION_REQUIRED_STATUSES,
    ForecastEntry,
    ForecastTriage,
    due_failures,
    parse_entries,
    parse_triage,
    structural_failures,
)


REPO_ROOT = Path(__file__).resolve().parent.parent
LEDGER_PATH = REPO_ROOT / "narrative-geopolitics" / "work" / "forecasts" / "forecast-ledger.md"

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate forecast-ledger triage metadata.")
    parser.add_argument("--as-of", default=date.today().isoformat(), help="Review cutoff in YYYY-MM-DD format.")
    return parser.parse_args()


def validate_triage(
    entries: list[ForecastEntry], triage_rows: list[ForecastTriage], as_of: str
) -> list[str]:
    return [
        *structural_failures(entries, triage_rows),
        *due_failures(entries, triage_rows, as_of),
    ]


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
