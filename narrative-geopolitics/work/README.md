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
