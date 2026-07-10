# Narrative Geopolitics Work Surface

This folder holds internal working files for daily Narrative Geopolitics runs.

Each run is operator-triggered by `daily-geopolitics` and should live at:

```text
work/daily/YYYY-MM-DD/
```

Each run should contain:

- `sources.md`
- `synthesis.md`
- `daily-brief.md`
- `forecast.md`

For the normal evening synthesis session after the day's `best-intake` work is
done, use the single `geopolitical-synthesis` command:

```text
C:\Users\rober\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe scripts/geopolitical_synthesis.py --date YYYY-MM-DD
```

This command now opens a guided work session first. It summarizes the current
day state and presents a bounded multiple-choice menu so the evening pass can be
navigated deliberately rather than always jumping straight into automation.

Each guided invocation also writes a lightweight session receipt to:

```text
work/daily/YYYY-MM-DD/geopolitical-synthesis-session.json
```

The receipt records manifest-row count, validation state, whether a real sourced
daily run exists, whether a placeholder scaffold exists, the recommended menu
letter, the latest selected choice if one was provided, and a small choice
history for that day.

Menu shape:

- `A` bootstrap or refresh the day run
- `B` reconcile intake coverage and routing
- `C` deepen synthesis around the owning object
- `D` sharpen forecast hooks and review logic
- `E` execute the full daily stack immediately

If you want the old one-shot automation behavior directly, use:

```text
C:\Users\rober\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe scripts/geopolitical_synthesis.py --date YYYY-MM-DD --execute
```

Direct execute mode:

- bootstraps the daily run folder from the manifest day batch
- carries forward due forecast reviews into `forecast.md`
- validates the daily run against archive and ledger state
- syncs any missing forecast hooks into the ledger

If you want to scaffold a full month or date range, including placeholder days
that are still awaiting intake, use:

```text
C:\Users\rober\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe scripts/geopolitical_synthesis.py --month 2026-07 --scaffold-empty
```

Or:

```text
C:\Users\rober\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe scripts/geopolitical_synthesis.py --start-date YYYY-MM-DD --end-date YYYY-MM-DD --scaffold-empty
```

This creates canonical `sources.md`, `synthesis.md`, `forecast.md`,
`daily-brief.md`, and a session receipt for empty days without pretending a
real sourced run already exists.

Implementation note: `scripts/geopolitical_synthesis.py` is the operator-facing
entrypoint and delegates to the underlying orchestration helper. The older
`scripts/geo_synthesis.py` name remains as a compatibility shim.

## Skill Sync

The repo drafts for reusable Codex skills live under:

- `docs/skill-drafts/best-intake/SKILL.md`
- `docs/skill-drafts/geopolitical-synthesis/SKILL.md`

To deploy those repo-owned drafts into the live user-level Codex skill
directory, run:

```text
C:\Users\rober\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe scripts/sync_codex_skills.py
```

To check for drift without rewriting anything, run:

```text
C:\Users\rober\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe scripts/check_codex_skills_sync.py
```

To audit the full repo-vs-Codex skill picture, including skills that exist only
in the repo or only in the live Codex install, run:

```text
C:\Users\rober\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe scripts/audit_codex_skills_sync.py
```

Short rule:

```text
edit in repo, sync to codex, check for drift before relying on the live skill
```

To bootstrap a new daily run from the manifest day batch, use:

```text
py scripts/bootstrap_daily_run.py --date YYYY-MM-DD
```

This creates the day folder and pre-populates `sources.md` from the central
archive rows for that date, while also scaffolding the other three daily files
from templates.

The generated `forecast.md` also carries forward any open ledger hooks whose
`Review Date` is due on or before the new run date, so review work is surfaced
inside the daily run rather than left to memory.

Before trusting a real daily run for synthesis or review, validate it against the
archive and forecast ledger:

```text
C:\Users\rober\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe scripts/validate_daily_run.py --date YYYY-MM-DD --stage synthesis
```

Stage behavior is deliberate:

- `--stage intake` reports `stale-after-intake` plus a refresh instruction
  without blocking source landing.
- `--stage synthesis`, `forecast`, or `publication` blocks when the Intake
  Batch does not exactly cover the manifest day rows.
- The Run Source Set may remain a documented analytical subset of the complete
  Intake Batch.

The validator checks:

- the daily folder and expected files exist
- the manifest has rows for the date
- the referenced archive source files exist
- `sources.md` links cover the manifest day batch
- `forecast.md` hook ids are present in the forecast ledger

For placeholder days that are still awaiting intake, the validator reports a
non-fatal placeholder warning rather than treating the day as a completed run.

## Forecast Accountability Triage

The central Markdown ledger preserves every historical row, but only
timing-reviewed `ex_ante` entries marked `Accountable: yes` belong in later
calibration. Validate that separation with:

```text
C:\Users\rober\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe scripts/triage_forecast_ledger.py --as-of YYYY-MM-DD
```

Retrospective hypotheses, indicators, falsifiers, and unscorable hooks remain
visible without being counted as forecast performance. When the authorized
archive cannot resolve an observable, use
`unresolvable_with_authorized_evidence` rather than forcing a hit or miss.

To sync a day's forecast hooks into the central ledger without duplicate manual
copying, use:

```text
C:\Users\rober\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe scripts/sync_forecast_ledger.py --date YYYY-MM-DD --crisis-object "Your crisis object"
```

Use `--dry-run` first when checking what new ledger rows would be added.

## Daily Cadence

Daily runs begin with intake. Before synthesis, land the day's transcripts,
articles, essays, reports, or posts in the central archive and update the
manifest:

- `archive/sources/YYYY-MM-DD/source-*.md`
- `archive/source-manifest.json`

Then route each source through the relevant continuity layers:

- `voices/` for whole-source-person continuity
- `channels/` for host, show, or channel conditioning
- `work/daily/YYYY-MM-DD/` for the day's judgment run

The daily run should use the newly imported day sources first, then add older
archive sources only when they sharpen the crisis object or pressure-test the
judgment.

## Operating Rule

Daily runs are internal-first judgment work. They should intake the day's
source material, identify the crisis object, route primary and pressure voices,
make a bounded judgment, and create at least one reviewable forecast hook.

Use coarse probability bands for v1:

- `low`: roughly 10-30%
- `plausible`: roughly 30-45%
- `likely`: roughly 55-70%
- `high`: roughly 70-85%

Do not publish a draft brief to `public/` until it is intentionally promoted.

Placeholder run folders are allowed when they are explicitly scaffolded as
awaiting intake. Do not treat those placeholders as real synthesis runs until
the archive day batch exists.
