# Narrative Geopolitics Work Surface

This folder holds internal working files for daily Narrative Geopolitics runs.

Each run is operator-triggered by `daily-geopolitics` and should live at:

```text
work/daily/YYYY-MM-DD/
```

Each run should contain:

- `sources.md`
- `synthesis.md`
- `public-brief.md`
- `forecast.md`

For the normal evening synthesis session after the day's `best-intake` work is
done, use the single `geopolitical-synthesis` command:

```text
C:\Users\rober\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe scripts/geopolitical_synthesis.py --date YYYY-MM-DD
```

This command:

- bootstraps the daily run folder from the manifest day batch
- carries forward due forecast reviews into `forecast.md`
- validates the daily run against archive and ledger state
- syncs any missing forecast hooks into the ledger

Implementation note: `scripts/geopolitical_synthesis.py` is the operator-facing
entrypoint and delegates to the underlying orchestration helper. The older
`scripts/geo_synthesis.py` name remains as a compatibility shim.

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

Before trusting a daily run for synthesis or review, validate it against the
archive and forecast ledger:

```text
C:\Users\rober\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe scripts/validate_daily_run.py --date YYYY-MM-DD
```

The validator checks:

- the daily folder and expected files exist
- the manifest has rows for the date
- the referenced archive source files exist
- `sources.md` links cover the manifest day batch
- `forecast.md` hook ids are present in the forecast ledger

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

Do not create a dated run folder until there is a real run to process.
