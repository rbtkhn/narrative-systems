from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from datetime import date
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parent.parent
NG_ROOT = REPO_ROOT / "narrative-geopolitics"
TRACKER_ROOT = NG_ROOT / "work" / "voice-accountability"
LEDGER_MD_PATH = TRACKER_ROOT / "voice-revision-ledger.md"
LEDGER_JSON_PATH = TRACKER_ROOT / "voice-revision-ledger.json"
NEAR_MISSES_PATH = TRACKER_ROOT / "voice-revision-near-misses.md"
CANDIDATE_SCRIPT = (
    REPO_ROOT
    / "docs"
    / "skill-drafts"
    / "voice-accountability"
    / "scripts"
    / "find_revision_candidates.py"
)

REVISION_ID_RE = re.compile(r"\bVR-\d{8}-\d{2}\b")
NEAR_MISS_ID_RE = re.compile(r"\bNM-\d{8}-\d{2}\b")
MARKDOWN_TABLE_ID_RE = re.compile(r"^\|\s*`(?P<id>VR-\d{8}-\d{2})`\s*\|", re.MULTILINE)

ALLOWED_CLASSES = {
    "explicit-personal-admission",
    "personal-position-revision",
    "personal-prediction-revision",
    "qualified-collective-revision",
}
ALLOWED_STATUSES = {"active", "superseded", "withdrawn"}
REQUIRED_FIELDS = {
    "id",
    "date",
    "voice_slug",
    "host_slug",
    "source_title",
    "source_path",
    "line",
    "class",
    "status",
    "prior_view",
    "revised_view",
    "excerpt",
    "adjudication_note",
}


def relative(path: Path) -> str:
    return path.relative_to(REPO_ROOT).as_posix()


def load_ledger(path: Path = LEDGER_JSON_PATH) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def markdown_entry_ids(text: str) -> list[str]:
    return MARKDOWN_TABLE_ID_RE.findall(text)


def duplicate_values(values: list[str]) -> list[str]:
    seen: set[str] = set()
    duplicates: set[str] = set()
    for value in values:
        if value in seen:
            duplicates.add(value)
        seen.add(value)
    return sorted(duplicates)


def validate_ledger(
    *,
    repo_root: Path = REPO_ROOT,
    markdown_path: Path = LEDGER_MD_PATH,
    json_path: Path = LEDGER_JSON_PATH,
    near_misses_path: Path = NEAR_MISSES_PATH,
) -> list[str]:
    failures: list[str] = []
    for path in (markdown_path, json_path, near_misses_path):
        if not path.exists():
            failures.append(f"voice accountability tracker missing: {relative(path)}")
    if failures:
        return failures

    markdown_text = markdown_path.read_text(encoding="utf-8")
    near_misses_text = near_misses_path.read_text(encoding="utf-8")
    try:
        ledger = json.loads(json_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        return [f"voice accountability JSON is invalid: {relative(json_path)}:{error.lineno}"]

    entries = ledger.get("entries")
    if not isinstance(entries, list):
        return ["voice accountability JSON missing entries list"]

    markdown_ids = markdown_entry_ids(markdown_text)
    json_ids = [str(entry.get("id", "")) for entry in entries if isinstance(entry, dict)]
    for revision_id in duplicate_values(json_ids):
        failures.append(f"duplicate voice-revision ID: {revision_id}")
    for revision_id in duplicate_values(markdown_ids):
        failures.append(f"duplicate voice-revision Markdown row: {revision_id}")
    if set(markdown_ids) != set(json_ids):
        failures.append(
            "voice-revision Markdown/JSON ID mismatch: "
            f"markdown={sorted(set(markdown_ids))} json={sorted(set(json_ids))}"
        )

    if NEAR_MISS_ID_RE.search(markdown_text) or NEAR_MISS_ID_RE.search(json.dumps(ledger)):
        failures.append("near-miss entry leaked into main voice-revision ledger")

    near_miss_ids = set(NEAR_MISS_ID_RE.findall(near_misses_text))
    if near_miss_ids & set(json_ids):
        failures.append("near-miss ID overlaps a main voice-revision ID")

    for index, entry in enumerate(entries, start=1):
        if not isinstance(entry, dict):
            failures.append(f"voice accountability entry #{index} is not an object")
            continue
        label = str(entry.get("id") or f"entry #{index}")
        missing = sorted(field for field in REQUIRED_FIELDS if not entry.get(field))
        failures.extend(f"voice accountability entry missing {field}: {label}" for field in missing)
        revision_id = str(entry.get("id", ""))
        if not REVISION_ID_RE.fullmatch(revision_id):
            failures.append(f"invalid voice-revision ID: {label}")
        entry_date = str(entry.get("date", ""))
        try:
            parsed_date = date.fromisoformat(entry_date)
        except ValueError:
            failures.append(f"invalid voice-revision date: {label} -> {entry_date}")
        else:
            if revision_id and revision_id[3:11] != parsed_date.strftime("%Y%m%d"):
                failures.append(f"voice-revision ID/date mismatch: {label}")
        if entry.get("class") not in ALLOWED_CLASSES:
            failures.append(f"invalid voice-revision class: {label} -> {entry.get('class')}")
        if entry.get("status") not in ALLOWED_STATUSES:
            failures.append(f"invalid voice-revision status: {label} -> {entry.get('status')}")

        source_value = entry.get("source_path")
        if not isinstance(source_value, str) or not source_value:
            continue
        source_path = repo_root / source_value
        if not source_path.is_file():
            failures.append(f"voice-revision source path missing: {label} -> {source_value}")
            continue
        line = entry.get("line")
        if not isinstance(line, int) or line < 1:
            failures.append(f"voice-revision line reference invalid: {label} -> {line}")
            continue
        line_count = len(source_path.read_text(encoding="utf-8-sig", errors="replace").splitlines())
        if line > line_count:
            failures.append(
                f"voice-revision line reference out of range: {label} -> {source_value}:{line}"
            )

    return failures


def run_candidates(args: argparse.Namespace) -> int:
    if args.date_from > args.date_to:
        print("--from must not be later than --to", file=sys.stderr)
        return 2
    command = [
        sys.executable,
        str(CANDIDATE_SCRIPT),
        "--repo-root",
        str(REPO_ROOT),
        "--from",
        args.date_from.isoformat(),
        "--to",
        args.date_to.isoformat(),
    ]
    if args.voice:
        command.extend(["--voice", args.voice])
    result = subprocess.run(command, check=False, capture_output=True, text=True)
    if result.returncode != 0:
        sys.stderr.write(result.stderr)
        return result.returncode
    payload = json.loads(result.stdout)
    payload["mode"] = args.mode
    payload["ledger_mutation"] = "none"
    payload["review_note"] = (
        "Candidates require curated transcript review before any ledger entry is added."
    )
    if not args.dry_run:
        payload["mutation_guard"] = (
            "Non-dry-run candidate generation is still read-only until a curated "
            "entry path is added."
        )
    print(json.dumps(payload, ensure_ascii=True, indent=2))
    return 0


def run_validate(_: argparse.Namespace) -> int:
    failures = validate_ledger()
    print(f"voice_accountability_failures={len(failures)}")
    for failure in failures:
        print(f"FAIL {failure}")
    return 1 if failures else 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Voice accountability tracker tooling")
    subparsers = parser.add_subparsers(dest="command", required=True)
    for name in ("audit", "backfill"):
        sub = subparsers.add_parser(name, help="Generate read-only candidate proposals")
        sub.set_defaults(func=run_candidates, mode=name)
        sub.add_argument("--from", dest="date_from", required=True, type=date.fromisoformat)
        sub.add_argument("--to", dest="date_to", required=True, type=date.fromisoformat)
        sub.add_argument("--voice")
        sub.add_argument("--dry-run", action="store_true")
    validate = subparsers.add_parser("validate", help="Validate canonical tracker files")
    validate.set_defaults(func=run_validate)
    return parser


def main(arguments: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(arguments)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
