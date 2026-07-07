# Predictive History Research Target

Source repository: [`rbtkhn/predictive-history`](https://github.com/rbtkhn/predictive-history)

Local source inspected: `C:\dev\predictive-history`

## Working Read

Predictive History is a public narrative system organized as a namespace catalog hub. Its reader-facing shape is not a single argument or linear book; it is a routed corpus of chapters, commentaries, indexes, cards, and LLM-oriented entry contracts.

The system's most important design move is traversal discipline. It tells a reader or model what to open first, what counts as evidence, when interpretation is allowed to widen, and which older frames are deprecated but still present for compatibility.

## Observed Narrative Units

- `START-HERE.md`: the bootloader and first-response contract for LLM chats.
- `docs/predictive-history-index.json`: the machine-readable namespace catalog hub.
- `data/cards.jsonl`: the stated single source of truth for public cards.
- `data/routes/seed.json`: the 10-route spine seed.
- `docs/onboarding/first-tour.md`: the default guided reader experience.
- `docs/methodology/source-lattice.md`: the retrieval and interpretation discipline.
- `lectures/`, `essays/`, `interviews/`: the three root chapter corpora.

## Observed Relations

- `START-HERE.md` opens the namespace catalog hub and defines the default `first_tour` mode.
- `data/routes/seed.json` selects the first 10-route spine seed.
- `docs/onboarding/first-tour.md` narrates that seed as a guided sequence.
- `docs/methodology/source-lattice.md` constrains how readers move from doorway to primary source floor, then to support and widened interpretation.
- `data/cards.jsonl` supports the generated catalog indexes and route resolution.
- The deprecated `ph-civ` / `ph-apo` frame remains as compatibility context rather than active onboarding.

## Initial Analysis Questions

- How does a repository become a narrative interface rather than only a storage container?
- Which files act as doorways, evidence floors, route maps, and interpretation surfaces?
- How do deprecation notes preserve continuity without letting an old frame control the current reader path?
- Can the source-lattice be modeled as a general pattern for LLM-readable narrative systems?

## Next Research Move

Use the current `NarrativeSystem` primitives to model Predictive History at the layer level first. Do not attempt chapter-level extraction until the layer model can distinguish doorway, catalog, route, source floor, and widened interpretation.
