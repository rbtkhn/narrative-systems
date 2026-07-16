---
name: geopolitical-synthesis
description: "Narrative Geopolitics guided synthesis for manifest-backed live or intentional retrospective days."
preferred_activation: geopolitical-synthesis
portable: false
version: 0.2.0
category: narrative-geopolitics
status: active
---

# Geopolitical Synthesis

Use after intake has landed or when deepening an existing retrospective run.

## Core Law

Read in this order:

```text
archive -> voices/channels -> work/daily
```

This skill does not replace `best-intake` and never creates a daily directory
for a date without manifest rows.

## Daily Contract

Canonical:

- `sources.md`
- `synthesis.md`
- `forecast.md`
- `daily-brief.md`

Generated after the canonical files are issue-ready:

- `issue.md`

There is no tracked session receipt or placeholder-day state.

## Entrypoint

```powershell
.\scripts\python.ps1 scripts\geopolitical_synthesis.py --date YYYY-MM-DD
.\scripts\python.ps1 scripts\geopolitical_synthesis.py --date YYYY-MM-DD --execute
```

Month and range modes process only dates with manifest rows. The deprecated
`--scaffold-empty` flag reports skipped dates and writes nothing.

## Guided Menu

- `A` bootstrap or refresh the run;
- `B` reconcile intake coverage and routing;
- `C` deepen the owning crisis object and report exception-only operational-claim triage;
- `D` sharpen forecast hooks and report their `OPC-*` dependencies;
- `E` execute the full stack.

## Guardrails

- Require exact manifest coverage in the Intake Batch before synthesis.
- Permit a documented Run Source Set subset.
- Treat retrospective forecasts as retrospective unless timing proves otherwise.
- Keep `daily-brief.md` internal until intentionally promoted.
- Keep `issue.md` internal reader-facing; generation is not publication.
- Declare issue membership in the synthesis `Issue Story Desk`; require matching `Issue Copy` in `daily-brief.md` and regenerate rather than hand-editing `issue.md`.
- Do not revive the old `public-brief.md` contract.
- Do not alter private intake behavior.
- Do not browse, create verification packets, or assign operational truth automatically.
- Print an explicit packet-request command for `request` rows; operator action remains required.
- Permit bounded internal synthesis with unresolved claims. Block high-consequence public factual use and accountable forecast resolution until packet requirements are met.
- Reject orphan `OPC-*` rows: every retained claim must control planned public factual use, watch promotion, or a forecast dependency.
