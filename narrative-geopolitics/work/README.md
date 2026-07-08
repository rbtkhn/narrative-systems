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

## Operating Rule

Daily runs are internal-first judgment work. They should identify the crisis object, route primary and pressure voices, make a bounded judgment, and create at least one reviewable forecast hook.

Use coarse probability bands for v1:

- `low`: roughly 10-30%
- `plausible`: roughly 30-45%
- `likely`: roughly 55-70%
- `high`: roughly 70-85%

Do not publish a draft brief to `public/` until it is intentionally promoted.

Do not create a dated run folder until there is a real run to process.
