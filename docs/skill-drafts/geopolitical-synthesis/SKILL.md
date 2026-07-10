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

- `sources.md`
- `synthesis.md`
- `forecast.md`
- `daily-brief.md`

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
- `C` deepen the owning crisis object;
- `D` sharpen forecast hooks and review logic;
- `E` execute the full stack.

## Guardrails

- Require exact manifest coverage in the Intake Batch before synthesis.
- Permit a documented Run Source Set subset.
- Treat retrospective forecasts as retrospective unless timing proves otherwise.
- Keep `daily-brief.md` internal until intentionally promoted.
- Do not revive the old `public-brief.md` contract.
- Do not alter private intake behavior.
