# Narrative Geopolitics Work Surface

`work/` holds internal dialogue, judgment, experiments, and forecast
accountability. It does not own source truth.

## Council Dialogues

`dialogues/` contains manual, corpus-bounded experiments in realistic dialogue
with curated intellectual voices. Start with
[dialogues/_template.md](dialogues/_template.md) and obey the
[dialogue contract](../method/dialogue-contract.md).

Each voice response is drafted separately from the same bounded question. A
moderator may compare or synthesize only after the responses exist; the
moderator must not silently make the voices agree. Dialogues are interpretive
work products, not archive evidence, actual interviews, or claims about a
person's present opinion.

The first manual experiment is the
[Council Value Test](dialogues/2026-07-council-value-test/README.md). It must
earn automation by demonstrating fidelity, differentiation, and reader value.

## On-Demand Daily Runs

A daily run exists only when the date has manifest-backed sources or an
intentional retrospective run. Empty dates create no directory.

```text
work/daily/YYYY-MM-DD/
├── sources.md
├── synthesis.md
├── forecast.md
└── daily-brief.md
```

Open a guided run:

```powershell
.\scripts\python.ps1 scripts\geopolitical_synthesis.py --date YYYY-MM-DD
```

Execute the full stack:

```powershell
.\scripts\python.ps1 scripts\geopolitical_synthesis.py --date YYYY-MM-DD --execute
```

Date-range and month modes skip dates without manifest rows. The legacy
`--scaffold-empty` flag is accepted for compatibility but writes nothing.

The guided menu is:

- `A` bootstrap or refresh a manifest-backed run;
- `B` reconcile intake coverage and routing;
- `C` deepen the owning crisis object;
- `D` sharpen forecast hooks and review logic;
- `E` execute the full stack.

The older `scripts/geo_synthesis.py` filename remains a compatibility shim.

## Validation

Before synthesis, normalize provisional person identifiers and reconcile
manifest-backed routes into voice shelves that already exist:

```powershell
.\scripts\python.ps1 scripts\canonicalize_voice_metadata.py --date YYYY-MM-DD --check
.\scripts\python.ps1 scripts\sync_voice_indexes.py --date YYYY-MM-DD --check
```

Guided choice `B` performs both repairs. This downstream step does not change
private intake, source bodies, filenames, archive paths, or host/channel slugs.
Manifest voices without an established shelf are reported but do not block
synthesis.

Validate a day at the relevant stage:

```powershell
.\scripts\python.ps1 scripts\validate_daily_run.py --date YYYY-MM-DD --stage synthesis
```

- `intake` reports stale coverage and a refresh instruction without blocking
  source landing;
- `synthesis`, `forecast`, and `publication` require exact Intake Batch coverage;
- the Run Source Set may be a documented analytical subset.

Validate the repository boundary:

```powershell
.\scripts\python.ps1 scripts\validate_repository.py
```

This checks archive/manifest parity, daily-run grounding, forecast/triage
parity, internal links, and the skill deployment allowlist.

## Forecast Accountability

The Markdown ledger preserves every historical row. Only timing-reviewed
`ex_ante` entries marked `Accountable: yes` belong in calibration.

```powershell
.\scripts\python.ps1 scripts\triage_forecast_ledger.py --as-of YYYY-MM-DD
.\scripts\python.ps1 scripts\sync_forecast_ledger.py --date YYYY-MM-DD --crisis-object "Bounded object"
```

Use `--dry-run` before ledger synchronization. When authorized evidence cannot
resolve an observable, record `unresolvable_with_authorized_evidence` rather
than forcing a result.

## Skill Deployment

Only the portable, repo-owned `best-intake` and `geopolitical-synthesis` drafts
are eligible for user-level synchronization:

```powershell
.\scripts\python.ps1 scripts\check_codex_skills_sync.py
.\scripts\python.ps1 scripts\sync_codex_skills.py --dry-run
```

Coffee and dream are local operator contracts. They are not globally deployed.
They close one advisory learning loop through an ignored local handoff:

```powershell
.\scripts\python.ps1 scripts\cadence.py coffee --json
.\scripts\python.ps1 scripts\cadence.py dream --experiment "TEXT" --outcome improved --lesson "TEXT" --improvement "TEXT" --evidence-summary "TEXT" --artifact-ref "PATH" --tomorrow-inherits "TEXT" --json
```

Dream verifies the repository before recording one experiment, its bounded
evidence, supporting repository artifacts, and a candidate method change.
Coffee inherits it only when verification passed and the Git worktree still
matches. The handoff is never archive evidence or a research ledger.

## Daily Operating Rule

The order remains:

```text
archive -> voices/channels -> work/daily or work/dialogues -> forecast review -> optional public
```

Use newly landed day sources first. Retrieve older material only when it changes
the crisis object, confidence, contradiction handling, or falsifiability. Do
not publish a daily brief unless it is intentionally promoted.

Private intake, transcript preservation, trimming, ASR repair, and manifest-row
creation remain governed by `method/best-intake.md`.
