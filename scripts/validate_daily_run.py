from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parent.parent
NG_ROOT = REPO_ROOT / "narrative-geopolitics"
MANIFEST_PATH = NG_ROOT / "archive" / "source-manifest.json"
DAILY_ROOT = NG_ROOT / "work" / "daily"
LEDGER_PATH = NG_ROOT / "work" / "forecasts" / "forecast-ledger.md"


HOOK_RE = re.compile(r"`(NG-\d{8}-F\d{2})`")
ARCHIVE_LINK_RE = re.compile(r"\((\.\./\.\./\.\./archive/sources/[^)]+\.md)\)")
INTAKE_ROW_RE = re.compile(r"\|\s*`(archive/sources/[^`]+\.md)`\s*\|")
STATUS_RE = re.compile(r"Status:\s*`([^`]+)`")
PLACEHOLDER_RE = re.compile(r"awaiting intake", re.IGNORECASE)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate a Narrative Geopolitics daily run against archive and forecast surfaces."
    )
    parser.add_argument("--date", required=True, help="Run date in YYYY-MM-DD format.")
    return parser.parse_args()


def load_manifest() -> dict[str, Any]:
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8-sig"))


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def daily_dir(run_date: str) -> Path:
    return DAILY_ROOT / run_date


def expected_files(run_date: str) -> list[Path]:
    base = daily_dir(run_date)
    return [
        base / "sources.md",
        base / "synthesis.md",
        base / "forecast.md",
        base / "daily-brief.md",
    ]


def manifest_rows_for_date(manifest: dict[str, Any], run_date: str) -> list[dict[str, Any]]:
    rows = [row for row in manifest.get("sources", []) if row.get("date") == run_date]
    rows.sort(key=lambda row: row.get("local_path", ""))
    return rows


def source_paths_exist(rows: list[dict[str, Any]]) -> list[str]:
    missing: list[str] = []
    for row in rows:
        local_path = row.get("local_path", "")
        target = REPO_ROOT / Path(local_path)
        if not target.exists():
            missing.append(local_path)
    return missing


def extract_archive_links(sources_text: str) -> list[str]:
    return ARCHIVE_LINK_RE.findall(sources_text)


def extract_intake_paths(sources_text: str) -> list[str]:
    return INTAKE_ROW_RE.findall(sources_text)


def extract_status(text: str) -> str:
    match = STATUS_RE.search(text)
    return match.group(1) if match else ""


def is_placeholder_day(run_path: Path) -> bool:
    sources_path = run_path / "sources.md"
    if not sources_path.exists():
        return False
    return bool(PLACEHOLDER_RE.search(read_text(sources_path)))


def normalize_daily_archive_link(link: str) -> str:
    return link.removeprefix("../../../")


def manifest_archive_paths(rows: list[dict[str, Any]]) -> set[str]:
    return {row.get("local_path", "").split("narrative-geopolitics/", 1)[-1] for row in rows}


def extract_hook_ids(text: str) -> list[str]:
    seen: list[str] = []
    for hook in HOOK_RE.findall(text):
        if hook not in seen:
            seen.append(hook)
    return seen


def extract_ledger_hook_ids() -> set[str]:
    return set(HOOK_RE.findall(read_text(LEDGER_PATH)))


def main() -> None:
    args = parse_args()
    run_date = args.date
    manifest = load_manifest()
    rows = manifest_rows_for_date(manifest, run_date)
    run_path = daily_dir(run_date)
    placeholder_day = is_placeholder_day(run_path)

    failures: list[str] = []
    warnings: list[str] = []

    if not run_path.exists():
        failures.append(f"missing daily folder: {run_path.relative_to(REPO_ROOT)}")

    for path in expected_files(run_date):
        if not path.exists():
            failures.append(f"missing file: {path.relative_to(REPO_ROOT)}")

    if not rows and not placeholder_day:
        failures.append(f"no manifest rows for date {run_date}")
    if not rows and placeholder_day:
        warnings.append(f"placeholder day awaiting intake for date {run_date}")

    missing_sources = source_paths_exist(rows)
    for local_path in missing_sources:
        failures.append(f"missing archive source file: {local_path}")

    if rows and (run_path / "sources.md").exists():
        sources_text = read_text(run_path / "sources.md")
        status = extract_status(sources_text)
        linked_paths = {normalize_daily_archive_link(link) for link in extract_archive_links(sources_text)}
        intake_paths = set(extract_intake_paths(sources_text))
        manifest_paths = manifest_archive_paths(rows)

        for rel in sorted(linked_paths):
            if not (REPO_ROOT / "narrative-geopolitics" / Path(rel)).exists():
                warnings.append(f"sources.md links missing archive file: {rel}")

        if status != "pilot":
            missing_intake = sorted(manifest_paths - intake_paths)
            extra_intake = sorted(intake_paths - manifest_paths)
            for rel in missing_intake:
                warnings.append(f"intake batch missing manifest day source: {rel}")
            for rel in extra_intake:
                warnings.append(f"intake batch includes source outside manifest day batch: {rel}")

    if (run_path / "forecast.md").exists():
        forecast_text = read_text(run_path / "forecast.md")
        hook_ids = extract_hook_ids(forecast_text)
        ledger_hook_ids = extract_ledger_hook_ids()
        if not hook_ids and not placeholder_day:
            warnings.append("forecast.md has no hook ids")
        for hook_id in hook_ids:
            if hook_id not in ledger_hook_ids:
                warnings.append(f"forecast hook missing from ledger: {hook_id}")

    print(f"date={run_date}")
    print(f"manifest_rows={len(rows)}")
    print(f"failures={len(failures)}")
    print(f"warnings={len(warnings)}")
    for item in failures:
        print(f"FAIL {item}")
    for item in warnings:
        print(f"WARN {item}")

    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
