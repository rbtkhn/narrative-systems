# Intake Speedup

This note turns the July 2026 intake slowdown diagnosis into an operating plan.

## What Actually Made Intake Slow

The bottleneck was not one giant problem. It was a stack of small manual costs
that repeated for every source:

1. read enough of each pasted transcript to infer title, date, host, guest, and routing
2. write a custom archive file by hand
3. hand-edit `archive/source-manifest.json`
4. re-check voice and channel continuity during landing
5. verify the new source manually

That meant `best-intake` was acting like a careful editorial micro-project for
each item instead of a fast landing contract.

## Root Cause

Narrative Geopolitics has a `best-intake` doctrine, but it did not yet have a
matching `best-intake` mechanism.

The repo had:

- method guidance
- archive conventions
- templates

But it did not yet have a dedicated helper that could:

- create the archive file
- build the frontmatter
- append the manifest row
- increment `source_count`

in one pass.

## Design Rule

Intake speed improves when we separate **landing** from **enrichment**.

Landing should do only this:

- preserve the source body
- create a valid archive file
- append a manifest row
- mark uncertainty honestly

Small host-specific wrapper removal is allowed when it is deterministic,
reversible in principle, and clearly lower-value than the substantive source
body. Mario Nawfal opening chatter is the first approved case.

Landing should **not** pause for:

- full voice-shelf creation
- deep channel interpretation
- synthesis-grade quote extraction
- daily-brief readiness

## Immediate Fix

Use the helper at [../../scripts/land_best_intake.py](../../scripts/land_best_intake.py).

For operator paste sessions, pair it with
[../templates/intake-metadata.md](../templates/intake-metadata.md).

It automates the slowest repeated operations:

- slugging the source title
- creating `archive/sources/YYYY-MM-DD/source-*.md`
- writing standard frontmatter
- appending a manifest row
- incrementing manifest `source_count`

## New Fast Path

For each pasted transcript:

1. Save the pasted body to a local text file.
2. Fill [../templates/intake-metadata.md](../templates/intake-metadata.md).
3. Run `land_best_intake.py` with `--metadata-file` for one source or `--batch-dir` for a whole folder.
4. Review the generated archive file header once.
5. Defer voice/channel enrichment unless the source is immediately synthesis-critical.

## Minimal Metadata Rule

Require only:

- `pub_date`
- `ingest_date`
- `title`
- `url`
- `body_file`
- one provisional `voice_slug`

Optional:

- `host_slug`
- `host`
- `guest`
- `show_title`
- `channel_name`
- `source_class`
- `editorial_note`

If the optional fields are unclear, land with provisional metadata instead of
stopping the batch.

## Operational Rules

- Missing voice shelf is not an intake blocker.
- Missing channel shelf is not an intake blocker.
- If host identity is only moderately clear, route provisionally and continue.
- If title cleanup is imperfect but truthful, continue.
- If transcript quality is noisy, preserve the noise and continue.

## Recommended Batch Workflow

Use two passes:

### Pass 1: landing

- land every source
- preserve body
- create manifest row
- do no synthesis work

### Pass 2: enrichment

- fix titles if needed
- expand voice continuity when warranted
- open channel shelves only for synthesis-relevant items
- create the daily run after the archive batch is complete
- hand off to `geopolitical-synthesis` for guided bootstrap, reconciliation, or execution

## Next Improvements

1. Add a manifest regeneration command so the central manifest stops being a
   high-friction hand-edited surface.
2. Add lightweight tests for archive-file generation and manifest append logic.

## Success Standard

`best-intake` is fast enough when a same-day five-source batch feels like:

- one metadata decision per source
- one helper invocation per source
- one quick verification pass for the batch

not five bespoke archival compositions.
