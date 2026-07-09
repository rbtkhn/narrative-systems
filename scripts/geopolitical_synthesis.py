from __future__ import annotations

import argparse
from datetime import date, timedelta
import json
from pathlib import Path

import process_daily_stack as stack


REPO_ROOT = Path(__file__).resolve().parent.parent


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Start a guided Narrative Geopolitics synthesis session, scaffold "
            "placeholder daily files, or execute the full daily stack directly."
        )
    )
    parser.add_argument("--date", help="Run date in YYYY-MM-DD format.")
    parser.add_argument("--month", help="Optional month selector in YYYY-MM format.")
    parser.add_argument("--start-date", help="Optional inclusive start date in YYYY-MM-DD format.")
    parser.add_argument("--end-date", help="Optional inclusive end date in YYYY-MM-DD format.")
    parser.add_argument(
        "--choice",
        choices=("A", "B", "C", "D", "E"),
        help="Optional menu choice to display for the current session.",
    )
    parser.add_argument(
        "--execute",
        action="store_true",
        help="Run the full existing daily-stack processor instead of opening the guided session menu.",
    )
    parser.add_argument(
        "--status",
        default="live-intake-first",
        help="Status to use if execute mode or scaffold work writes daily files.",
    )
    parser.add_argument(
        "--retro",
        action="store_true",
        help="Mark the day as retrospective when execute mode bootstraps the run folder.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing daily files during execute or scaffold work.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show planned execute-mode or scaffold work without writing files.",
    )
    parser.add_argument(
        "--crisis-object",
        default="",
        help="Crisis-object label to use if execute mode syncs forecast hooks into the ledger.",
    )
    parser.add_argument(
        "--skip-ledger-sync",
        action="store_true",
        help="Skip syncing forecast hooks into the ledger during execute mode.",
    )
    parser.add_argument(
        "--scaffold-empty",
        action="store_true",
        help="Create or normalize placeholder daily files for days without manifest rows.",
    )
    args = parser.parse_args()
    if not args.date and not args.month and not (args.start_date and args.end_date):
        raise SystemExit("Provide --date, --month, or both --start-date and --end-date.")
    return args


def build_execute_args(args: argparse.Namespace) -> argparse.Namespace:
    return argparse.Namespace(
        date=args.date,
        status=args.status,
        retro=args.retro,
        force=args.force,
        dry_run=args.dry_run,
        crisis_object=args.crisis_object,
        skip_ledger_sync=args.skip_ledger_sync,
    )


def parse_iso_date(value: str) -> date:
    return date.fromisoformat(value)


def iter_dates(args: argparse.Namespace) -> list[str]:
    if args.month:
        start = parse_iso_date(f"{args.month}-01")
        if start.month == 12:
            end = date(start.year + 1, 1, 1) - timedelta(days=1)
        else:
            end = date(start.year, start.month + 1, 1) - timedelta(days=1)
    elif args.start_date and args.end_date:
        start = parse_iso_date(args.start_date)
        end = parse_iso_date(args.end_date)
        if end < start:
            raise SystemExit("--end-date must be on or after --start-date")
    else:
        return [args.date]

    current = start
    dates: list[str] = []
    while current <= end:
        dates.append(current.isoformat())
        current += timedelta(days=1)
    return dates


def gather_context(run_date: str) -> dict[str, object]:
    manifest = stack.BOOTSTRAP.load_manifest()
    rows = [row for row in manifest.get("sources", []) if row.get("date") == run_date]
    rows.sort(key=lambda row: row.get("local_path", ""))

    run_dir = stack.BOOTSTRAP.DAILY_ROOT / run_date
    required_files = ("sources.md", "synthesis.md", "forecast.md", "daily-brief.md")
    scaffold_exists = all((run_dir / name).exists() for name in required_files)
    run_exists = scaffold_exists and bool(rows)

    validation: dict[str, object] = {
        "manifest_rows": len(rows),
        "failures": [],
        "warnings": [],
    }
    if run_exists:
        validation = stack.run_validation(run_date)

    return {
        "rows": rows,
        "run_dir": run_dir,
        "run_exists": run_exists,
        "scaffold_exists": scaffold_exists,
        "awaiting_intake": len(rows) == 0,
        "validation": validation,
    }


def session_receipt_path(run_date: str) -> Path:
    return stack.BOOTSTRAP.DAILY_ROOT / run_date / "geopolitical-synthesis-session.json"


def load_existing_receipt(run_date: str) -> dict[str, object] | None:
    path = session_receipt_path(run_date)
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def write_session_receipt(
    run_date: str,
    context: dict[str, object],
    recommended: str,
    choice: str | None,
) -> Path:
    run_dir = context["run_dir"]
    run_dir.mkdir(parents=True, exist_ok=True)
    path = session_receipt_path(run_date)
    validation = context["validation"]
    prior = load_existing_receipt(run_date)
    history = []
    if prior and isinstance(prior.get("choice_history"), list):
        history = list(prior["choice_history"])
    if choice:
        history.append(choice)

    payload = {
        "run_date": run_date,
        "status": "guided-session",
        "awaiting_intake": context["awaiting_intake"],
        "manifest_day_rows": len(context["rows"]),
        "daily_run_exists": context["run_exists"],
        "daily_scaffold_exists": context["scaffold_exists"],
        "validation_failures": len(validation["failures"]),
        "validation_warnings": len(validation["warnings"]),
        "recommended_choice": recommended,
        "selected_choice": choice,
        "choice_history": history,
        "session_menu": {
            "A": "Bootstrap / refresh the day run from the manifest batch.",
            "B": "Reconcile intake coverage and source routing against the full day batch.",
            "C": "Deepen the internal synthesis around the owning crisis object.",
            "D": "Sharpen forecast hooks, falsifiers, and review questions.",
            "E": "Execute the full daily stack immediately.",
        },
        "execute_command": (
            "C:\\Users\\rober\\.cache\\codex-runtimes\\codex-primary-runtime\\dependencies\\python\\python.exe "
            f"scripts/geopolitical_synthesis.py --date {run_date} --execute"
        ),
    }
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8", newline="\n")
    return path


def recommend_choice(context: dict[str, object]) -> str:
    validation = context["validation"]
    if context["awaiting_intake"] or not context["run_exists"]:
        return "A"
    if validation["failures"] or validation["warnings"]:
        return "B"
    return "C"


def build_placeholder_sources_md(run_date: str, status: str) -> str:
    return f"""# Sources

Date: `{run_date}`

Status: `{status}`

## Source Basis

Primary source basis:

- `narrative-geopolitics/archive/source-manifest.json`
- `narrative-geopolitics/archive/sources/{run_date}/`

## Intake Batch

This day is scaffolded and awaiting intake. No manifest day rows currently exist for `{run_date}`.

| Source File | Source Type | Intake Status | Manifest Row | Voice Route | Channel Route | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| `none yet` | `pending` | `awaiting-intake` | `no` | `pending` | `pending` | Archive intake must land before synthesis. |

## Run Source Set

No run source set is authorized until intake lands for this date.

| Source ID | Voice | Host / Channel | Modality | Archive Path | Why It Matters |
| --- | --- | --- | --- | --- | --- |
| `pending` |  |  |  |  | Await archive intake before selecting sources. |

## Load-Bearing Quotes

No quotes should be carried forward before intake.

| Source ID | Quote | Why It Matters |
| --- | --- | --- |
| `pending` |  | Await archive intake. |

## Initial Claims

No claims should be promoted before intake.

| Claim ID | Source IDs | Claim | Voice / Channel Note | Initial Status |
| --- | --- | --- | --- | --- |
| `pending` | `pending` | Await archive intake. | No synthesis yet. | `blocked-awaiting-intake` |

## Source Hygiene

- Confirm archive intake lands first.
- Confirm manifest rows exist before any real synthesis.
- Do not infer a run source set for this date until source bodies are imported.
"""


def build_placeholder_synthesis_md(run_date: str, status: str) -> str:
    return f"""# Synthesis

Date: `{run_date}`

Status: `{status}`

## Lead Judgment

No lead judgment is authorized yet. This day is scaffolded only and remains blocked on archive intake.

## Crisis Object

Do not assign a crisis object until the day's source batch exists.

## Primary Voices

Await intake before assigning voice roles.

| Voice | Role In This Run | What It Adds | Main Risk |
| --- | --- | --- | --- |
| `pending` | Await intake | Await intake | Premature synthesis |

## Orthogonal Pressure Test

Do not complete pressure testing until source grounding exists.

| Axis | Voice | Pressure Question | Effect On Judgment |
| --- | --- | --- | --- |
| `pending` | `pending` | What does the day intake actually support? | Await intake |

## Actor Map

| Actor | Interest | Constraint | Narrative / Legitimacy Claim |
| --- | --- | --- | --- |
| `pending` |  |  | Await intake |

## Draft Judgment

- Await archive intake before writing synthesis.

## Uncertainty

The governing uncertainty is missing day intake, not analytical disagreement.

## Forecast Candidates

No day-specific forecast candidates are authorized until intake lands.

| Hook ID | Claim | Probability Band | Review Date |
| --- | --- | --- | --- |
| `pending` | Await archive intake before proposing hooks. |  |  |
"""


def build_placeholder_forecast_md(run_date: str, status: str) -> str:
    text = stack.BOOTSTRAP.build_from_template("forecast.md", run_date, status)
    replacement = (
        "## Hooks\n\n"
        "No new day-specific forecast hooks are authorized because this day is awaiting intake.\n\n"
        "| Hook ID | Claim | Probability Band | Review Date | Strengthening Evidence | Weakening Evidence |\n"
        "| --- | --- | --- | --- | --- | --- |\n"
        "| `pending` | Await archive intake before making a new probability-bearing claim. |  |  |  |  |\n\n"
    )
    return text.replace("## Hooks\n", replacement, 1)


def build_placeholder_daily_brief_md(run_date: str) -> str:
    return f"""# Narrative Geopolitics Daily Brief: {run_date}

Status: `not-promoted`

## Lead Judgment

No daily brief is publishable for this date because the day remains awaiting intake.

## Source Grounding

No archive-grounded source batch exists yet for this date.

## Crisis Object

Do not assign a public crisis object before intake.

## Actor And Narrative Map

Public narration is blocked until the internal archive day batch exists.

## Voice Pressure Test

No voice pressure test should be published before intake and internal synthesis.

## What To Watch

The next required action is archive intake, not publication.

## Forecast / Review Hooks

Only previously due review hooks may be consulted internally. No new outward-facing hook should be promoted from this placeholder day.
"""


def scaffold_placeholder_day(run_date: str, args: argparse.Namespace) -> list[str]:
    run_dir = stack.BOOTSTRAP.DAILY_ROOT / run_date
    return [
        stack.BOOTSTRAP.write_text(
            run_dir / "sources.md",
            build_placeholder_sources_md(run_date, args.status),
            args.force,
            args.dry_run,
        ),
        stack.BOOTSTRAP.write_text(
            run_dir / "synthesis.md",
            build_placeholder_synthesis_md(run_date, args.status),
            args.force,
            args.dry_run,
        ),
        stack.BOOTSTRAP.write_text(
            run_dir / "forecast.md",
            build_placeholder_forecast_md(run_date, args.status),
            args.force,
            args.dry_run,
        ),
        stack.BOOTSTRAP.write_text(
            run_dir / "daily-brief.md",
            build_placeholder_daily_brief_md(run_date),
            args.force,
            args.dry_run,
        ),
    ]


def handle_scaffold(run_date: str, args: argparse.Namespace) -> dict[str, object]:
    context = gather_context(run_date)
    actions: list[str] = []
    if context["awaiting_intake"] and args.scaffold_empty:
        actions = scaffold_placeholder_day(run_date, args)
        context = gather_context(run_date)
    recommended = recommend_choice(context)
    receipt_path = write_session_receipt(run_date, context, recommended, args.choice)
    return {"context": context, "actions": actions, "receipt_path": receipt_path}


def print_menu(run_date: str, context: dict[str, object], choice: str | None) -> None:
    rows = context["rows"]
    run_exists = context["run_exists"]
    scaffold_exists = context["scaffold_exists"]
    validation = context["validation"]
    failures = validation["failures"]
    warnings = validation["warnings"]
    awaiting_intake = context["awaiting_intake"]
    recommended = recommend_choice(context)
    prior_receipt = load_existing_receipt(run_date)
    prior_selected = None
    prior_history: list[str] = []
    if prior_receipt:
        prior_selected = prior_receipt.get("selected_choice")
        history = prior_receipt.get("choice_history")
        if isinstance(history, list):
            prior_history = [item for item in history if isinstance(item, str)]
    receipt_path = session_receipt_path(run_date)

    print(f"geopolitical-synthesis session: {run_date}")
    print(f"manifest_day_rows={len(rows)}")
    print(f"daily_run_exists={'yes' if run_exists else 'no'}")
    print(f"daily_scaffold_exists={'yes' if scaffold_exists else 'no'}")
    print(f"awaiting_intake={'yes' if awaiting_intake else 'no'}")
    print(f"validation_failures={len(failures)}")
    print(f"validation_warnings={len(warnings)}")
    print(f"session_receipt={receipt_path.relative_to(REPO_ROOT).as_posix()}")
    if prior_selected:
        print(f"resume_last_choice={prior_selected}")
    if prior_history:
        print(f"choice_history={' -> '.join(prior_history)}")
    if failures:
        for item in failures:
            print(f"FAIL {item}")
    if warnings:
        for item in warnings:
            print(f"WARN {item}")
    if awaiting_intake:
        print("INFO no manifest day rows yet; this date is awaiting intake before a real synthesis run can begin")

    print("")
    print("Session Menu - reply with A-E")
    menu = [
        ("A", "Bootstrap / refresh the day run from the manifest batch."),
        ("B", "Reconcile intake coverage and source routing against the full day batch."),
        ("C", "Deepen the internal synthesis around the owning crisis object."),
        ("D", "Sharpen forecast hooks, falsifiers, and review questions."),
        ("E", "Execute the full daily stack immediately."),
    ]
    for key, text in menu:
        suffix = " (recommended)" if key == recommended else ""
        print(f"{key}. {text}{suffix}")

    if choice:
        print("")
        print(f"selected={choice}")
        guidance = {
            "A": (
                "Bootstrap focus: make sure sources.md, synthesis.md, forecast.md, "
                "and daily-brief.md reflect the current manifest day batch."
            ),
            "B": (
                "Reconciliation focus: compare Intake Batch and Run Source Set to all "
                "manifest rows for the day, then decide which new sources belong in the run."
            ),
            "C": (
                "Synthesis focus: tighten the lead judgment, crisis object, and "
                "speaker-by-function roles without widening the day."
            ),
            "D": (
                "Forecast focus: convert today's judgment into cleaner observable tests, "
                "review dates, and falsifiers."
            ),
            "E": (
                "Execute focus: run the existing automation path now using "
                "`--execute` with the same date."
            ),
        }
        print(guidance[choice])


def run_batch(args: argparse.Namespace) -> None:
    for run_date in iter_dates(args):
        if args.execute:
            single_args = build_execute_args(args)
            single_args.date = run_date
            context = gather_context(run_date)
            if context["awaiting_intake"]:
                result = handle_scaffold(run_date, args)
                context = result["context"]
                print(f"date={run_date}")
                print(f"manifest_day_rows={len(context['rows'])}")
                print(f"daily_run_exists={'yes' if context['run_exists'] else 'no'}")
                print(f"daily_scaffold_exists={'yes' if context['scaffold_exists'] else 'no'}")
                print(f"awaiting_intake={'yes' if context['awaiting_intake'] else 'no'}")
                for action in result["actions"]:
                    print(action)
                print(f"session_receipt={result['receipt_path'].relative_to(REPO_ROOT).as_posix()}")
                print("")
                continue

            bootstrap = stack.run_bootstrap(single_args)
            validation = stack.run_validation(run_date)
            ledger_sync = {"hooks": 0, "new_rows": 0, "rows": []}
            if not args.skip_ledger_sync:
                ledger_sync = stack.run_ledger_sync(single_args)
                validation = stack.run_validation(run_date)

            result = handle_scaffold(run_date, args)
            context = result["context"]
            print(f"date={run_date}")
            print(f"bootstrap_rows={bootstrap['rows']}")
            for action in bootstrap["actions"]:
                print(action)
            print(f"validation_failures={len(validation['failures'])}")
            print(f"validation_warnings={len(validation['warnings'])}")
            print(f"ledger_hooks={ledger_sync['hooks']}")
            print(f"ledger_new_rows={ledger_sync['new_rows']}")
            print(f"session_receipt={result['receipt_path'].relative_to(REPO_ROOT).as_posix()}")
            print("")
            continue

        result = handle_scaffold(run_date, args)
        context = result["context"]
        print(f"date={run_date}")
        print(f"manifest_day_rows={len(context['rows'])}")
        print(f"daily_run_exists={'yes' if context['run_exists'] else 'no'}")
        print(f"daily_scaffold_exists={'yes' if context['scaffold_exists'] else 'no'}")
        print(f"awaiting_intake={'yes' if context['awaiting_intake'] else 'no'}")
        for action in result["actions"]:
            print(action)
        print(f"session_receipt={result['receipt_path'].relative_to(REPO_ROOT).as_posix()}")
        print("")


def main() -> None:
    args = parse_args()
    if args.month or (args.start_date and args.end_date):
        run_batch(args)
        return

    if args.execute:
        context = gather_context(args.date)
        if context["awaiting_intake"]:
            raise SystemExit(
                f"Cannot execute full daily stack for {args.date}: no manifest rows found. Land intake first."
            )
        stack_args = build_execute_args(args)
        bootstrap = stack.run_bootstrap(stack_args)
        run_dir = stack.BOOTSTRAP.DAILY_ROOT / args.date
        forecast_exists = (run_dir / "forecast.md").exists()
        can_validate = (not args.dry_run) or run_dir.exists()
        can_sync_ledger = (not args.skip_ledger_sync) and ((not args.dry_run) or forecast_exists)

        validation = {"failures": [], "warnings": [], "manifest_rows": bootstrap["rows"]}
        if can_validate:
            validation = stack.run_validation(args.date)

        ledger_sync = {"hooks": 0, "new_rows": 0, "rows": []}
        if can_sync_ledger:
            ledger_sync = stack.run_ledger_sync(stack_args)
            if can_validate:
                validation = stack.run_validation(args.date)

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
        return

    result = handle_scaffold(args.date, args)
    print_menu(args.date, result["context"], args.choice)


if __name__ == "__main__":
    main()
