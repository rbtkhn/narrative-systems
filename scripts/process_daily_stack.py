from __future__ import annotations

import argparse
import importlib.util
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_ROOT = REPO_ROOT / "scripts"


def load_module(script_name: str, module_name: str):
    path = SCRIPTS_ROOT / script_name
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load {script_name}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


BOOTSTRAP = load_module("bootstrap_daily_run.py", "bootstrap_daily_run")
VALIDATOR = load_module("validate_daily_run.py", "validate_daily_run")
LEDGER_SYNC = load_module("sync_forecast_ledger.py", "sync_forecast_ledger")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Process the evening Narrative Geopolitics daily synthesis stack for one run date."
    )
    parser.add_argument("--date", required=True, help="Run date in YYYY-MM-DD format.")
    parser.add_argument(
        "--status",
        default="live-intake-first",
        help="Status to write into generated daily files.",
    )
    parser.add_argument(
        "--retro",
        action="store_true",
        help="Mark the day as retrospective when bootstrapping the run folder.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing daily files during bootstrap.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show planned work without writing files.",
    )
    parser.add_argument(
        "--crisis-object",
        default="",
        help="Crisis-object label to use if forecast hooks need to be added to the ledger.",
    )
    parser.add_argument(
        "--skip-ledger-sync",
        action="store_true",
        help="Skip syncing forecast hooks into the ledger.",
    )
    return parser.parse_args()


def run_bootstrap(args: argparse.Namespace) -> dict[str, Any]:
    manifest = BOOTSTRAP.load_manifest()
    rows = [row for row in manifest.get("sources", []) if row.get("date") == args.date]
    rows.sort(key=lambda row: row.get("local_path", ""))
    if not rows:
        raise SystemExit(f"No manifest rows found for {args.date}.")

    run_dir = BOOTSTRAP.DAILY_ROOT / args.date
    actions = [
        BOOTSTRAP.write_text(
            run_dir / "sources.md",
            BOOTSTRAP.build_sources_md(args.date, args.status, rows, args.retro),
            args.force,
            args.dry_run,
        )
    ]
    for name in ("synthesis.md", "forecast.md", "public-brief.md"):
        actions.append(
            BOOTSTRAP.write_text(
                run_dir / name,
                BOOTSTRAP.build_from_template(name, args.date, args.status),
                args.force,
                args.dry_run,
            )
        )
    return {"rows": len(rows), "actions": actions}


def run_validation(run_date: str) -> dict[str, Any]:
    manifest = VALIDATOR.load_manifest()
    rows = VALIDATOR.manifest_rows_for_date(manifest, run_date)
    run_path = VALIDATOR.daily_dir(run_date)

    failures: list[str] = []
    warnings: list[str] = []

    if not run_path.exists():
        failures.append(f"missing daily folder: {run_path.relative_to(REPO_ROOT)}")

    for path in VALIDATOR.expected_files(run_date):
        if not path.exists():
            failures.append(f"missing file: {path.relative_to(REPO_ROOT)}")

    if not rows:
        failures.append(f"no manifest rows for date {run_date}")

    for local_path in VALIDATOR.source_paths_exist(rows):
        failures.append(f"missing archive source file: {local_path}")

    if rows and (run_path / "sources.md").exists():
        sources_text = VALIDATOR.read_text(run_path / "sources.md")
        status = VALIDATOR.extract_status(sources_text)
        linked_paths = {
            VALIDATOR.normalize_daily_archive_link(link)
            for link in VALIDATOR.extract_archive_links(sources_text)
        }
        intake_paths = set(VALIDATOR.extract_intake_paths(sources_text))
        manifest_paths = VALIDATOR.manifest_archive_paths(rows)

        for rel in sorted(linked_paths):
            if not (REPO_ROOT / "narrative-geopolitics" / Path(rel)).exists():
                warnings.append(f"sources.md links missing archive file: {rel}")

        if status != "pilot":
            for rel in sorted(manifest_paths - intake_paths):
                warnings.append(f"intake batch missing manifest day source: {rel}")
            for rel in sorted(intake_paths - manifest_paths):
                warnings.append(f"intake batch includes source outside manifest day batch: {rel}")

    if (run_path / "forecast.md").exists():
        forecast_text = VALIDATOR.read_text(run_path / "forecast.md")
        hook_ids = VALIDATOR.extract_hook_ids(forecast_text)
        ledger_hook_ids = VALIDATOR.extract_ledger_hook_ids()
        if not hook_ids:
            warnings.append("forecast.md has no hook ids")
        for hook_id in hook_ids:
            if hook_id not in ledger_hook_ids:
                warnings.append(f"forecast hook missing from ledger: {hook_id}")

    return {"manifest_rows": len(rows), "failures": failures, "warnings": warnings}


def run_ledger_sync(args: argparse.Namespace) -> dict[str, Any]:
    forecast_path = LEDGER_SYNC.DAILY_ROOT / args.date / "forecast.md"
    if not forecast_path.exists():
        raise SystemExit(f"Missing forecast file: {forecast_path.relative_to(REPO_ROOT)}")

    forecast_text = LEDGER_SYNC.read_text(forecast_path)
    run_date = LEDGER_SYNC.extract_run_date(forecast_text)
    hooks = LEDGER_SYNC.extract_hook_rows(forecast_text)
    if not hooks:
        return {"hooks": 0, "new_rows": 0, "rows": []}

    ledger_text = LEDGER_SYNC.read_text(LEDGER_SYNC.LEDGER_PATH)
    existing = LEDGER_SYNC.existing_hook_ids(ledger_text)
    crisis_object = LEDGER_SYNC.infer_crisis_object(forecast_text, args.crisis_object)

    new_rows = [
        LEDGER_SYNC.build_ledger_row(run_date, crisis_object, hook)
        for hook in hooks
        if hook["hook_id"] not in existing
    ]

    if not args.dry_run and new_rows:
        updated = LEDGER_SYNC.insert_rows(ledger_text, new_rows)
        LEDGER_SYNC.LEDGER_PATH.write_text(updated, encoding="utf-8", newline="\n")

    return {"hooks": len(hooks), "new_rows": len(new_rows), "rows": new_rows}


def main() -> None:
    args = parse_args()

    bootstrap = run_bootstrap(args)
    run_dir = BOOTSTRAP.DAILY_ROOT / args.date
    forecast_exists = (run_dir / "forecast.md").exists()
    can_validate = (not args.dry_run) or run_dir.exists()
    can_sync_ledger = (not args.skip_ledger_sync) and ((not args.dry_run) or forecast_exists)

    validation = {"failures": [], "warnings": [], "manifest_rows": bootstrap["rows"]}
    if can_validate:
        validation = run_validation(args.date)

    ledger_sync = {"hooks": 0, "new_rows": 0, "rows": []}
    if can_sync_ledger:
        ledger_sync = run_ledger_sync(args)
        if can_validate:
            validation = run_validation(args.date)

    print(f"date={args.date}")
    print(f"bootstrap_rows={bootstrap['rows']}")
    for action in bootstrap["actions"]:
        print(action)
    if args.dry_run and not forecast_exists:
        print("INFO dry-run on fresh date: validation and ledger sync are deferred until files exist")
    print(f"validation_failures={len(validation['failures'])}")
    print(f"validation_warnings={len(validation['warnings'])}")
    for item in validation["failures"]:
        print(f"FAIL {item}")
    for item in validation["warnings"]:
        print(f"WARN {item}")
    print(f"ledger_hooks={ledger_sync['hooks']}")
    print(f"ledger_new_rows={ledger_sync['new_rows']}")
    for row in ledger_sync["rows"]:
        print(row)

    if validation["failures"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
