from __future__ import annotations

import argparse
import re
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
NG_ROOT = REPO_ROOT / "narrative-geopolitics"
DAILY_ROOT = NG_ROOT / "work" / "daily"
LEDGER_PATH = NG_ROOT / "work" / "forecasts" / "forecast-ledger.md"


DATE_RE = re.compile(r"Date:\s*`([^`]+)`")
CRISIS_OBJECT_RE = re.compile(r"## Crisis Object\s+(.+?)(?:\n## |\Z)", re.DOTALL)
TABLE_ROW_RE = re.compile(
    r"^\|\s*`(NG-\d{8}-F\d{2})`\s*\|\s*(.*?)\s*\|\s*`?(low|plausible|likely|high)`?\s*\|\s*`([^`]+)`\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|$"
)
LEDGER_HOOK_RE = re.compile(r"`(NG-\d{8}-F\d{2})`")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Sync forecast hooks from a daily run into the central forecast ledger."
    )
    parser.add_argument("--date", required=True, help="Run date in YYYY-MM-DD format.")
    parser.add_argument("--crisis-object", default="", help="Crisis-object label to use in new ledger rows.")
    parser.add_argument("--dry-run", action="store_true", help="Print planned ledger additions without writing.")
    return parser.parse_args()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def extract_run_date(text: str) -> str:
    match = DATE_RE.search(text)
    if not match:
        raise SystemExit("Could not find run date in forecast.md")
    return match.group(1)


def extract_hook_rows(text: str) -> list[dict[str, str]]:
    hooks: list[dict[str, str]] = []
    for line in text.splitlines():
        match = TABLE_ROW_RE.match(line.strip())
        if not match:
            continue
        hook_id, claim, band, review_date, strengthening, weakening = match.groups()
        hooks.append(
            {
                "hook_id": hook_id,
                "claim": claim,
                "band": band,
                "review_date": review_date,
                "strengthening": strengthening,
                "weakening": weakening,
            }
        )
    return hooks


def existing_hook_ids(text: str) -> set[str]:
    return set(LEDGER_HOOK_RE.findall(text))


def infer_crisis_object(forecast_text: str, fallback: str) -> str:
    if fallback:
        return fallback
    run_date = extract_run_date(forecast_text)
    synthesis_path = DAILY_ROOT / run_date / "synthesis.md"
    if synthesis_path.exists():
        synthesis_text = read_text(synthesis_path)
        match = CRISIS_OBJECT_RE.search(synthesis_text)
        if match:
            crisis_object = " ".join(match.group(1).strip().splitlines()).strip()
            if crisis_object:
                return crisis_object
    return f"{run_date} daily judgment"


def build_ledger_row(run_date: str, crisis_object: str, hook: dict[str, str]) -> str:
    source_run = f"[{run_date}](../daily/{run_date}/forecast.md)"
    return (
        f"| `{hook['hook_id']}` | `{run_date}` | {crisis_object} | {hook['claim']} | "
        f"`{hook['band']}` | `{hook['review_date']}` | {source_run} | `open` |"
    )


def insert_rows(ledger_text: str, rows: list[str]) -> str:
    if not rows:
        return ledger_text
    lines = ledger_text.rstrip().splitlines()
    insertion_index = len(lines)
    for index, line in enumerate(lines):
        if line.startswith("| `NG-"):
            insertion_index = index
    if insertion_index == len(lines):
        insertion_index = len(lines)
    lines.extend(rows)
    return "\n".join(lines) + "\n"


def main() -> None:
    args = parse_args()
    forecast_path = DAILY_ROOT / args.date / "forecast.md"
    if not forecast_path.exists():
        raise SystemExit(f"Missing forecast file: {forecast_path.relative_to(REPO_ROOT)}")

    forecast_text = read_text(forecast_path)
    run_date = extract_run_date(forecast_text)
    hooks = extract_hook_rows(forecast_text)
    if not hooks:
        raise SystemExit("No hook rows found in forecast.md")

    ledger_text = read_text(LEDGER_PATH)
    existing = existing_hook_ids(ledger_text)
    crisis_object = infer_crisis_object(forecast_text, args.crisis_object)

    new_rows = [
        build_ledger_row(run_date, crisis_object, hook)
        for hook in hooks
        if hook["hook_id"] not in existing
    ]

    print(f"date={run_date}")
    print(f"hooks={len(hooks)}")
    print(f"new_rows={len(new_rows)}")
    for row in new_rows:
        print(row)

    if args.dry_run or not new_rows:
        return

    updated = insert_rows(ledger_text, new_rows)
    LEDGER_PATH.write_text(updated, encoding="utf-8", newline="\n")


if __name__ == "__main__":
    main()
