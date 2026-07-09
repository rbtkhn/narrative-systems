# Forecast / Review Hooks

Date: `2026-07-27`

Status: `live-intake-first`

## Probability Bands

Use coarse bands, not false precision:

- `low`: roughly 10-30%
- `plausible`: roughly 30-45%
- `likely`: roughly 55-70%
- `high`: roughly 70-85%

## Due Review Hooks

Open forecast hooks whose review date is due on or before this run date:

| Hook ID | Original Date | Crisis Object | Claim | Probability Band | Review Date | Source Run |
| --- | --- | --- | --- | --- | --- | --- |
| `NG-20260708-F01` | `2026-07-08` | Hormuz transit governance breakdown | Within 14 days, major public handling of the Iran file will still treat Hormuz as a governed bargaining lane rather than a fully restored free-passage baseline. | `likely` | `2026-07-22` | [2026-07-08](../daily/2026-07-08/forecast.md) |

## Hooks

No new day-specific forecast hooks are authorized because this day is awaiting intake.

| Hook ID | Claim | Probability Band | Review Date | Strengthening Evidence | Weakening Evidence |
| --- | --- | --- | --- | --- | --- |
| `pending` | Await archive intake before making a new probability-bearing claim. |  |  |  |  |


| Hook ID | Claim | Probability Band | Review Date | Strengthening Evidence | Weakening Evidence |
| --- | --- | --- | --- | --- | --- |
| `NG-YYYYMMDD-F01` |  |  |  |  |  |

## Ledger Entries

Copy final hooks to `work/forecasts/forecast-ledger.md`.
