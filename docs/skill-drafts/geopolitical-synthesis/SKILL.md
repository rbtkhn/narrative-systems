---
name: geopolitical-synthesis
description: "Narrative Geopolitics guided daily synthesis skill. Use after intake lands to open, scaffold, reconcile, deepen, or execute a daily run with one contract across live, retrospective, and placeholder days."
preferred_activation: geopolitical-synthesis
activation: geopolitical-synthesis
portable: false
version: 0.1.0
category: narrative-geopolitics
status: active
---
# Geopolitical Synthesis

**Preferred activation (operator):** say **`geopolitical-synthesis`**.

Use this skill after the day has been landed into the central archive, or when
you need to inspect whether a day is a real run, a placeholder scaffold, or a
retrospective authored run.

## Core law

Read this stack in order:

`archive -> voices / channels -> work/daily`

This skill owns the `work/daily/YYYY-MM-DD/` layer. It does not replace
`best-intake`.

## Daily contract

Canonical daily files:

- `sources.md`
- `synthesis.md`
- `forecast.md`
- `daily-brief.md`

Session receipt:

- `work/daily/YYYY-MM-DD/geopolitical-synthesis-session.json`

## Supported day states

This skill must distinguish:

- real sourced daily run
- placeholder scaffold awaiting intake
- retrospective authored run

`daily_run_exists` means a real sourced run exists.

`daily_scaffold_exists` means the canonical daily folder exists, even if the day
is still awaiting intake.

## Operator entrypoint

Default command:

```text
python scripts/geopolitical_synthesis.py --date YYYY-MM-DD
```

Direct execution:

```text
python scripts/geopolitical_synthesis.py --date YYYY-MM-DD --execute
```

Month or range scaffold:

```text
python scripts/geopolitical_synthesis.py --month YYYY-MM --scaffold-empty
python scripts/geopolitical_synthesis.py --start-date YYYY-MM-DD --end-date YYYY-MM-DD --scaffold-empty
```

## Guided menu

- `A` bootstrap or refresh the day run
- `B` reconcile intake coverage and routing
- `C` deepen synthesis around the owning object
- `D` sharpen forecast hooks and review logic
- `E` execute the full daily stack immediately

## Workflow

1. Inspect manifest coverage for the requested date.
2. Classify the day as real, placeholder, or retrospective.
3. Write or refresh the session receipt.
4. Use the guided menu first unless the operator explicitly wants `--execute`.
5. Keep placeholder days explicit when intake is missing.
6. Treat `daily-brief.md` as internal-first unless intentionally promoted.

## Guardrails

- Do not treat placeholder scaffolds as real runs.
- Do not execute a real daily stack for a day with no manifest rows.
- Do not jump straight to `public/` before internal source grounding exists.
- Do not revive the old `public-brief.md` contract.

## Repo surfaces

- `narrative-geopolitics/work/README.md`
- `narrative-geopolitics/templates/daily-brief.md`
- `scripts/geopolitical_synthesis.py`
- `scripts/bootstrap_daily_run.py`
- `scripts/validate_daily_run.py`
- `scripts/demo_daily_runs.py`

