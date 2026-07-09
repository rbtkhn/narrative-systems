# Narrative Geopolitics

Narrative Geopolitics is a workflow-first project for building a public geopolitical judgment model.

It uses `strategy-codex/statecraft` as its source basis and predecessor system, but its goal is not to copy that inherited operator machinery. Its goal is to distill the best parts of statecraft into a cleaner public model that can stand beside Predictive History.

```text
statecraft = source basis and operator ancestor
narrative-geopolitics = public geopolitical judgment model
predictive-history = public historical/civilizational reading model
```

## Purpose

Narrative Geopolitics turns transcripts, expert claims, current crises, actor incentives, legitimacy claims, historical memory, and competing narratives into public geopolitical judgment.

It is not an oracle and not a generic news summary. It is a bounded analyst system: source-heavy, calm, quote-aware, uncertainty-conscious, and reviewable.

## V1 Workflow

The initial operating loop is:

```text
best-intake through the day
-> archive/sources/YYYY-MM-DD/source-*.md
-> archive/source-manifest.json
-> geopolitical-synthesis
-> work/daily/YYYY-MM-DD/sources.md
-> work/daily/YYYY-MM-DD/synthesis.md
-> work/daily/YYYY-MM-DD/daily-brief.md
-> work/daily/YYYY-MM-DD/forecast.md
-> work/forecasts/forecast-ledger.md
-> public/briefs/daily/YYYY-MM-DD.md (only when intentionally promoted)
```

## Directory Map

```text
narrative-geopolitics/
├── README.md
├── archive/
│   ├── README.md
│   ├── source-manifest.json
│   └── sources/
├── channels/
│   ├── README.md
│   ├── channel-index.md
│   └── _template.md
├── method/
│   ├── narrative-statecraft.md
│   └── voice-continuity.md
├── public/
│   ├── README.md
│   └── briefs/
│       └── daily/
├── templates/
│   ├── sources.md
│   ├── synthesis.md
│   ├── daily-brief.md
│   └── forecast.md
├── voices/
│   ├── README.md
│   └── _template.md
└── work/
    ├── README.md
    ├── daily/
    └── forecasts/
        └── forecast-ledger.md
```

## Source Basis

The first source basis is `strategy-codex/statecraft`, especially its daily transcript intake and synthesis responsibilities.

V1 should use a manual manifest for each run. Automated extraction can come later.

Imported source truth lives in [archive/](archive/README.md). Voice records link into that central archive instead of duplicating transcripts or essays per voice.

## Intake Contract

Default source landing should follow [method/best-intake.md](method/best-intake.md).

Use `best-intake` when the priority is to land same-day source truth quickly without pretending that provisional routing is final interpretation.

See [method/intake-speedup.md](method/intake-speedup.md) for the current speedup plan and [../scripts/land_best_intake.py](../scripts/land_best_intake.py) for the first helper that automates archive-file creation plus manifest append.

Once the day batch is materially real, use `geopolitical-synthesis` as the
single evening synthesis command. It supports three day states under one
contract:

- real sourced daily runs
- placeholder scaffolds awaiting intake
- retrospective authored runs

## Voice Continuity

Narrative Geopolitics uses [voices/](voices/README.md) for durable voice records. A voice can be a speaker, writer, essayist, interview guest, social poster, or mixed-format analyst.

Voice continuity means remembered interpretive pattern across sources and time. Voice records are internal first; public summaries can come later after a record is stable enough to share.

## Channel Conditioning

Narrative Geopolitics uses [channels/](channels/README.md) for host, show, and channel conditioning. Open this layer when the real question is how a host frames, pressures, selects, amplifies, compresses, or translates a guest's claims.

Pape remains the analyst voice. Pape-on-host sources route through channel shelves when host context changes interpretation.

## Public Voice

The public voice should be a calm public analyst:

- source-heavy and quote-aware
- willing to make bounded judgments
- careful with uncertainty in normal prose
- committed to at least one forecast or review hook per brief
- readable without becoming thin
