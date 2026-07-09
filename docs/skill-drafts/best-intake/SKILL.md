---
name: best-intake
description: "Narrative Geopolitics source landing skill. Use when the operator has a transcript, newsletter, essay, report, or post ready to land into archive-first intake with honest provisional routing and deterministic wrapper trim where approved."
preferred_activation: best-intake
activation: best-intake
portable: false
version: 0.1.0
category: narrative-geopolitics
status: active
---
# Best Intake

**Preferred activation (operator):** say **`best-intake`**.

Use this skill for `narrative-geopolitics/` when the job is to land source truth
fast enough to keep the day moving, without pretending that intake is already
full synthesis.

## Core law

Read this stack in order:

`archive -> voices / channels -> work/daily`

Intake begins in `archive/`. It does not begin in `synthesis.md`,
`daily-brief.md`, or `public/`.

## Use this skill when

- the operator pasted a transcript or source body
- a same-day source needs to land under `archive/sources/YYYY-MM-DD/`
- throughput matters more than perfect enrichment
- voice and host routing are partly clear but not fully finished

## Do not use this skill when

- the source still needs to be fetched
- the task is to write the evening daily judgment
- the task is to publish or promote a public brief

## Adequacy standard

A `best-intake` land is adequate when it has:

- a real archive file
- preserved source body
- a truthful title and date
- a source URL when available
- at least one provisional `voice_slug`
- a `host_slug` when clear
- a manifest row

It does not need complete voice continuity, channel interpretation, quote
curation, claim extraction, or final `daily-brief.md` authoring.

## Deterministic trim law

Deterministic trim is allowed only for approved host-owned wrapper chatter that
is clearly separable from substantive content.

Current approved hosts:

- `mario-nawfal`
- `daniel-davis`
- `alexander-mercouris`
- `dialogue-works`

If the cut depends on judgment, do not automate it during intake.

## Workflow

1. Confirm the source body is materially real.
2. Land the source under `archive/sources/YYYY-MM-DD/source-*.md`.
3. Preserve the pasted body with minimal rewriting.
4. Apply only approved deterministic trim when the host rule matches.
5. Append or normalize the manifest row.
6. Mark uncertainty honestly instead of stalling on enrichment.
7. Stop once the day batch is archive-grounded.

## Handoff

`best-intake` ends when the archive truth is good enough for the day to become
reviewable.

Next move:

`geopolitical-synthesis`

Short rule:

`best-intake lands the day; geopolitical-synthesis judges the day`

## Repo surfaces

- `narrative-geopolitics/method/best-intake.md`
- `narrative-geopolitics/method/intake-speedup.md`
- `narrative-geopolitics/templates/intake-metadata.md`
- `scripts/land_best_intake.py`
- `scripts/report_trim_stats.py`

