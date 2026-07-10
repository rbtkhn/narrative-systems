# narrative-systems

An archive-first geopolitical research workbench.

The executable center is [Narrative Geopolitics](narrative-geopolitics/README.md):
a source-bounded system for transcript intake, voice and channel continuity,
daily synthesis, accountable forecasts, and selective public briefs.

[Predictive History](predictive-history/README.md) remains a sibling study of
public historical and civilizational corpus traversal.

## Layout

```text
.
├── narrative-geopolitics/  Archive, continuity, work, forecasts, and public output
├── predictive-history/     Sibling public-system study
├── docs/                   Method and local skill contracts
├── scripts/                Operator commands and validators
└── tests/                  Intake, synthesis, forecast, and integrity tests
```

## Development

Create the local environment once, then use the repository launcher. It resolves
`.venv` directly, so commands do not depend on global Python or shell activation.

```powershell
py -3 -m venv .venv
.\scripts\python.ps1 -m pip install -e ".[test]"
.\scripts\python.ps1 -m pytest
.\scripts\python.ps1 scripts\validate_repository.py
```

If `py` is unavailable during environment creation, install Python 3.10 or
newer. Private intake behavior is documented separately under
`narrative-geopolitics/method/` and is not part of repository maintenance.

## Operating Boundary

- `archive/` owns source truth.
- `voices/` and `channels/` own continuity and conditioning.
- `work/` owns internal judgment and forecast review.
- `public/` contains intentionally promoted reader-facing material.
- Empty dates create no daily directory.
