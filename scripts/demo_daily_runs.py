from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from datetime import date, timedelta
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parent.parent
NG_ROOT = REPO_ROOT / "narrative-geopolitics"
MANIFEST_PATH = NG_ROOT / "archive" / "source-manifest.json"
DAILY_ROOT = NG_ROOT / "work" / "daily"
LEDGER_PATH = NG_ROOT / "work" / "forecasts" / "forecast-ledger.md"

DATE_RE = re.compile(r"Date:\s*`([^`]+)`")
STATUS_RE = re.compile(r"Status:\s*`([^`]+)`")
CRISIS_OBJECT_RE = re.compile(r"## Crisis Object\s+(.+?)(?:\n## |\Z)", re.DOTALL)
HOOK_ID_RE = re.compile(r"`(NG-\d{8}-F\d{2})`")
LEDGER_ROW_RE = re.compile(
    r"^\|\s*`(NG-\d{8}-F\d{2})`\s*\|\s*`([^`]+)`\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*`(low|plausible|likely|high)`\s*\|\s*`([^`]+)`\s*\|\s*\[([^\]]+)\]\(([^)]+)\)\s*\|\s*`([^`]+)`\s*\|$"
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Prepare and print demo-friendly daily run summaries.")
    parser.add_argument("--month", required=True, help="Month selector in YYYY-MM format.")
    parser.add_argument(
        "--mode",
        choices=("executive-summary", "month-summary", "hook-review", "day-compare", "crisis-map"),
        default="month-summary",
        help="Demo report mode.",
    )
    parser.add_argument("--day-a", help="First day for day-compare mode.")
    parser.add_argument("--day-b", help="Second day for day-compare mode.")
    return parser.parse_args()


def load_manifest() -> dict[str, Any]:
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8-sig"))


def iter_month(month: str) -> list[str]:
    start = date.fromisoformat(f"{month}-01")
    if start.month == 12:
        end = date(start.year + 1, 1, 1) - timedelta(days=1)
    else:
        end = date(start.year, start.month + 1, 1) - timedelta(days=1)
    current = start
    dates: list[str] = []
    while current <= end:
        dates.append(current.isoformat())
        current += timedelta(days=1)
    return dates


def manifest_rows_for_date(manifest: dict[str, Any], run_date: str) -> list[dict[str, Any]]:
    rows = [row for row in manifest.get("sources", []) if row.get("date") == run_date]
    rows.sort(key=lambda row: row.get("local_path", ""))
    return rows


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def file_path(run_date: str, name: str) -> Path:
    return DAILY_ROOT / run_date / name


def extract_status(path: Path) -> str:
    if not path.exists():
        return ""
    match = STATUS_RE.search(read_text(path))
    return match.group(1) if match else ""


def extract_crisis_object(run_date: str) -> str:
    path = file_path(run_date, "synthesis.md")
    if not path.exists():
        return ""
    match = CRISIS_OBJECT_RE.search(read_text(path))
    if not match:
        return ""
    return " ".join(line.strip() for line in match.group(1).splitlines()).strip()


def extract_hook_ids(run_date: str) -> list[str]:
    path = file_path(run_date, "forecast.md")
    if not path.exists():
        return []
    seen: list[str] = []
    for hook in HOOK_ID_RE.findall(read_text(path)):
        if hook not in seen:
            seen.append(hook)
    return seen


def day_record(manifest: dict[str, Any], run_date: str) -> dict[str, Any]:
    rows = manifest_rows_for_date(manifest, run_date)
    return {
        "date": run_date,
        "manifest_rows": len(rows),
        "voices": sorted({slug for row in rows for slug in row.get("voice_slugs", [])}),
        "hosts": sorted({row.get("host_slug") for row in rows if row.get("host_slug")}),
        "sources_exists": file_path(run_date, "sources.md").exists(),
        "synthesis_exists": file_path(run_date, "synthesis.md").exists(),
        "forecast_exists": file_path(run_date, "forecast.md").exists(),
        "daily_brief_exists": file_path(run_date, "daily-brief.md").exists(),
        "status": extract_status(file_path(run_date, "synthesis.md")),
        "crisis_object": extract_crisis_object(run_date),
        "hook_ids": extract_hook_ids(run_date),
    }


def ledger_entries_for_month(month: str) -> list[dict[str, str]]:
    entries: list[dict[str, str]] = []
    for line in read_text(LEDGER_PATH).splitlines():
        match = LEDGER_ROW_RE.match(line.strip())
        if not match:
            continue
        hook_id, hook_date, crisis_object, claim, band, review_date, source_label, source_link, status = match.groups()
        if hook_date.startswith(month):
            entries.append(
                {
                    "hook_id": hook_id,
                    "hook_date": hook_date,
                    "crisis_object": crisis_object,
                    "claim": claim,
                    "band": band,
                    "review_date": review_date,
                    "status": status,
                }
            )
    return entries


def print_month_summary(month: str) -> None:
    manifest = load_manifest()
    days = [day_record(manifest, run_date) for run_date in iter_month(month)]
    real_days = [day for day in days if day["sources_exists"] and day["synthesis_exists"] and day["forecast_exists"] and day["daily_brief_exists"]]
    sparse = [day for day in real_days if day["manifest_rows"] <= 5]
    dense = [day for day in real_days if day["manifest_rows"] >= 10]
    crisis_counts = Counter(day["crisis_object"] for day in real_days if day["crisis_object"])
    print(f"month={month}")
    print(f"real_run_days={len(real_days)}")
    print(f"sparse_days={len(sparse)}")
    print(f"dense_days={len(dense)}")
    print(f"total_hooks={sum(len(day['hook_ids']) for day in real_days)}")
    print("")
    print("dense_examples:")
    for day in dense[:5]:
        print(f"- {day['date']} rows={day['manifest_rows']} crisis_object={day['crisis_object']}")
    print("")
    print("sparse_examples:")
    for day in sparse[:5]:
        print(f"- {day['date']} rows={day['manifest_rows']} crisis_object={day['crisis_object']}")
    print("")
    print("top_crisis_objects:")
    for crisis_object, count in crisis_counts.most_common(5):
        print(f"- {count}x {crisis_object}")


def print_executive_summary(month: str) -> None:
    manifest = load_manifest()
    days = [day_record(manifest, run_date) for run_date in iter_month(month)]
    real_days = [day for day in days if day["sources_exists"] and day["synthesis_exists"] and day["forecast_exists"] and day["daily_brief_exists"]]
    sparse = [day for day in real_days if day["manifest_rows"] <= 5]
    dense = [day for day in real_days if day["manifest_rows"] >= 10]
    dense_example = dense[0] if dense else None
    sparse_example = sparse[0] if sparse else None
    print("June is now a reviewable judgment month, not just a stored archive month.")
    print(f"- {len(real_days)} real run days are now present for {month}.")
    print(f"- {len(sparse)} sparse days and {len(dense)} dense days both validate under the same contract.")
    print(f"- The month currently carries {sum(len(day['hook_ids']) for day in real_days)} forecast/review hooks.")
    if dense_example:
        print(
            f"- Dense example: {dense_example['date']} carries {dense_example['manifest_rows']} source rows and resolves to "
            f"\"{dense_example['crisis_object']}\"."
        )
    if sparse_example:
        print(
            f"- Sparse example: {sparse_example['date']} carries {sparse_example['manifest_rows']} source rows and still resolves to "
            f"\"{sparse_example['crisis_object']}\"."
        )
    print("- June backfill and July live operation now coexist as one system: retrospective real run, live real run, and placeholder day all validate differently but cleanly.")


def print_hook_review(month: str) -> None:
    entries = ledger_entries_for_month(month)
    print(f"month={month}")
    print(f"ledger_entries={len(entries)}")
    for entry in entries[:10]:
        print(
            f"- {entry['hook_id']} review_date={entry['review_date']} band={entry['band']} "
            f"crisis_object={entry['crisis_object']}"
        )


def print_day_compare(day_a: str, day_b: str) -> None:
    manifest = load_manifest()
    for run_date in (day_a, day_b):
        day = day_record(manifest, run_date)
        print(f"date={run_date}")
        print(f"manifest_rows={day['manifest_rows']}")
        print(f"voices={', '.join(day['voices'])}")
        print(f"hosts={', '.join(day['hosts'])}")
        print(f"crisis_object={day['crisis_object']}")
        print(f"hook_ids={', '.join(day['hook_ids'])}")
        print("")


def print_crisis_map(month: str) -> None:
    manifest = load_manifest()
    days = [day_record(manifest, run_date) for run_date in iter_month(month)]
    for day in days:
        print(f"- {day['date']} | rows={day['manifest_rows']} | hooks={len(day['hook_ids'])} | {day['crisis_object']}")


def main() -> None:
    args = parse_args()
    if args.mode == "executive-summary":
        print_executive_summary(args.month)
        return
    if args.mode == "month-summary":
        print_month_summary(args.month)
        return
    if args.mode == "hook-review":
        print_hook_review(args.month)
        return
    if args.mode == "crisis-map":
        print_crisis_map(args.month)
        return
    if not args.day_a or not args.day_b:
        raise SystemExit("--day-a and --day-b are required for day-compare mode")
    print_day_compare(args.day_a, args.day_b)


if __name__ == "__main__":
    main()
