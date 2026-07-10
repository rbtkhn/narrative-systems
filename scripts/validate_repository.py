from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path

from codex_skill_registry import DEPLOYABLE_SKILL_NAMES, discover_repo_skill_names


REPO_ROOT = Path(__file__).resolve().parent.parent
NG_ROOT = REPO_ROOT / "narrative-geopolitics"
ARCHIVE_SOURCES = NG_ROOT / "archive" / "sources"
MANIFEST_PATH = NG_ROOT / "archive" / "source-manifest.json"
DAILY_ROOT = NG_ROOT / "work" / "daily"
LEDGER_PATH = NG_ROOT / "work" / "forecasts" / "forecast-ledger.md"
LOCAL_SKILLS = {"coffee", "dream"}
LOCAL_ROUTER_PATH = REPO_ROOT / "AGENTS.md"
REQUIRED_DAILY_FILES = {"sources.md", "synthesis.md", "forecast.md", "daily-brief.md"}

MARKDOWN_LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
HOOK_ID_RE = re.compile(r"`(NG-\d{8}-F\d{2})`")


def load_manifest() -> dict:
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8-sig"))


def relative(path: Path) -> str:
    return path.relative_to(REPO_ROOT).as_posix()


def archive_manifest_failures() -> list[str]:
    manifest = load_manifest()
    rows = manifest.get("sources", [])
    row_paths = [row.get("local_path", "") for row in rows]
    file_paths = sorted(relative(path) for path in ARCHIVE_SOURCES.rglob("*.md"))
    failures: list[str] = []

    if manifest.get("source_count") != len(rows):
        failures.append(
            f"manifest source_count={manifest.get('source_count')} but rows={len(rows)}"
        )
    if len(row_paths) != len(set(row_paths)):
        failures.append("manifest contains duplicate local_path rows")
    if sorted(row_paths) != file_paths:
        missing = sorted(set(row_paths) - set(file_paths))
        extra = sorted(set(file_paths) - set(row_paths))
        failures.extend(f"manifest path missing file: {path}" for path in missing)
        failures.extend(f"archive file missing manifest row: {path}" for path in extra)
    return failures


def daily_run_failures() -> list[str]:
    manifest = load_manifest()
    dates = {row.get("date") for row in manifest.get("sources", [])}
    failures: list[str] = []
    for run_dir in sorted(path for path in DAILY_ROOT.iterdir() if path.is_dir()):
        files = {path.name for path in run_dir.iterdir() if path.is_file()}
        if not files:
            failures.append(f"empty daily directory: {relative(run_dir)}")
            continue
        if run_dir.name not in dates:
            failures.append(f"daily directory has no manifest rows: {relative(run_dir)}")
        missing = REQUIRED_DAILY_FILES - files
        failures.extend(
            f"daily run missing {name}: {relative(run_dir)}" for name in sorted(missing)
        )
        if "geopolitical-synthesis-session.json" in files:
            failures.append(f"tracked session receipt: {relative(run_dir)}")
        sources_path = run_dir / "sources.md"
        if sources_path.exists() and "awaiting intake" in sources_path.read_text(
            encoding="utf-8"
        ).lower():
            failures.append(f"placeholder daily run: {relative(run_dir)}")
    return failures


def forecast_ledger_failures() -> list[str]:
    text = LEDGER_PATH.read_text(encoding="utf-8")
    entry_text, separator, triage_text = text.partition("## Accountability Triage")
    failures: list[str] = []
    if not separator:
        return ["forecast ledger missing Accountability Triage section"]

    entry_ids = HOOK_ID_RE.findall(entry_text)
    triage_ids = HOOK_ID_RE.findall(triage_text)
    if len(entry_ids) != len(set(entry_ids)):
        failures.append("forecast ledger contains duplicate entry hook IDs")
    if len(triage_ids) != len(set(triage_ids)):
        failures.append("forecast triage contains duplicate hook IDs")
    failures.extend(
        f"forecast entry missing triage row: {hook_id}"
        for hook_id in sorted(set(entry_ids) - set(triage_ids))
    )
    failures.extend(
        f"forecast triage row missing entry: {hook_id}"
        for hook_id in sorted(set(triage_ids) - set(entry_ids))
    )
    return failures


def markdown_files() -> list[Path]:
    roots = (REPO_ROOT / "docs", NG_ROOT, REPO_ROOT / "predictive-history")
    files: list[Path] = []
    for root in roots:
        if not root.exists():
            continue
        for path in root.rglob("*.md"):
            if ARCHIVE_SOURCES in path.parents:
                continue
            files.append(path)
    return sorted(files)


def markdown_link_failures() -> list[str]:
    failures: list[str] = []
    for path in markdown_files():
        text = path.read_text(encoding="utf-8")
        for match in MARKDOWN_LINK_RE.finditer(text):
            raw_target = match.group(1).strip().strip("<>")
            target = raw_target.split("#", 1)[0]
            if not target or target.startswith(("http://", "https://", "mailto:")):
                continue
            resolved = path.parent / target
            if not resolved.exists():
                failures.append(f"broken Markdown link: {relative(path)} -> {raw_target}")
    return failures


def skill_sync_failures() -> list[str]:
    failures: list[str] = []
    deployable = set(DEPLOYABLE_SKILL_NAMES)
    if deployable != {"best-intake", "geopolitical-synthesis"}:
        failures.append(f"unexpected deployable skill allowlist: {sorted(deployable)}")
    repo_skills = set(discover_repo_skill_names())
    if not LOCAL_SKILLS <= repo_skills:
        failures.append("coffee/dream local skill drafts are missing")
    if deployable & LOCAL_SKILLS:
        failures.append("local coffee/dream skills must not be globally deployable")
    if not LOCAL_ROUTER_PATH.exists():
        failures.append("repository-local coffee/dream trigger router is missing")
    else:
        router = LOCAL_ROUTER_PATH.read_text(encoding="utf-8")
        for name in sorted(LOCAL_SKILLS):
            expected = f"docs/skill-drafts/{name}/SKILL.md"
            if expected not in router:
                failures.append(f"local cadence trigger missing route: {expected}")
    return failures


def tracked_artifact_failures() -> list[str]:
    result = subprocess.run(
        ["git", "ls-files"],
        cwd=REPO_ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    tracked = set(result.stdout.splitlines())
    forbidden = {
        "narrative-geopolitics/work/cadence/last-dream.json",
    }
    return [f"tracked derived cadence artifact: {path}" for path in sorted(forbidden & tracked)]


def validate_repository() -> list[str]:
    failures: list[str] = []
    for check in (
        archive_manifest_failures,
        daily_run_failures,
        forecast_ledger_failures,
        markdown_link_failures,
        skill_sync_failures,
        tracked_artifact_failures,
    ):
        failures.extend(check())
    return failures


def main() -> None:
    failures = validate_repository()
    print(f"repository_integrity_failures={len(failures)}")
    for item in failures:
        print(f"FAIL {item}")
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
