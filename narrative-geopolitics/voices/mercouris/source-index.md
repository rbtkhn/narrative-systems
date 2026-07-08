# Mercouris Source Index

This index routes Alexander Mercouris voice work to the upstream Statecraft source basis.

Source basis: `strategy-codex/statecraft/voices/mercouris/`.

Status: `source-basis-pointer`

This pass does not import the full Mercouris corpus into `narrative-geopolitics/archive/sources/`. Mercouris has a much larger stream-native source surface than Pape, so the first Narrative Geopolitics move is to establish voice continuity and claim routing before selecting an import slice.

## Reading Rule

1. Mercouris is stream-native: solo `@AlexMercouris` continuity is the main shape.
2. Cross-host guest captures are reinforcement and pressure tests, not the whole voice.
3. The Duran rows need special care because Mercouris may appear as co-host, guest, or analyst voice inside a channel object.
4. Do not use this file as source truth; source truth remains upstream until selected captures are imported into `archive/sources/`.

## Upstream Open-First Surfaces

| Upstream surface | Job in Narrative Geopolitics |
| --- | --- |
| `statecraft/voices/mercouris/README.md` | Statecraft front door and canonical shelf explanation. |
| `statecraft/voices/mercouris/mercouris-profile.md` | Identity, voice fingerprint, failure modes, use guidance. |
| `statecraft/voices/mercouris/mercouris-routing.md` | Explains why Mercouris should be opened as a stream-native object. |
| `statecraft/voices/mercouris/mercouris-index.md` | Cross-host guest captures and guest route map. |
| `statecraft/voices/mercouris/mercouris-analytical-bench.md` | Hinge anchors, monthly synthesis routing, and cross-weaves. |
| `statecraft/channels/alexander-mercouris/alexander-mercouris-channel-index.md` | Solo `@AlexMercouris` host-channel capture index. |
| `statecraft/channels/the-duran/the-duran-channel-index.md` | The Duran host-channel captures involving Mercouris and other guests. |

## Corpus Shape From Statecraft

| Surface | Approximate role | Local Narrative status |
| --- | --- | --- |
| Solo `@AlexMercouris` captures | Native continuity, daily/weekly stream arc, month shelves. | `not-imported` |
| Cross-host guest captures | Daniel Davis, Glenn Diesen, The Duran, Neutrality Studies, and related panels. | `not-imported` |
| Analytical bench | Curated hinges for January 2025, February 2025, June 2026, and cross-weaves. | `source-basis` |
| Monthly shelves | Bounded synthesis shelves that summarize the Mercouris object without owning chronology. | `source-basis` |

## Candidate Import Slices

| Slice | Why it is useful | Suggested first files |
| --- | --- | --- |
| June 2026 hinge | Direct comparison with Pape's Iran/MOU/Oreshnik period. | `mercouris-shelf-2026-06.md`, June hinge sources from `mercouris-analytical-bench.md`. |
| Cross-host guest map | Tests voice vs channel separation across Daniel Davis, Glenn Diesen, The Duran, and Neutrality Studies. | `mercouris-index.md` selected 2026 rows. |
| Solo channel sample | Tests stream-native continuity against Pape's authored forecast spine. | Selected `@AlexMercouris` June 2026 sources. |
| Prehistory anchors | Provides order-transition and Ukraine negotiation context. | January-February 2025 anchors from `mercouris-analytical-bench.md`. |

## Import Boundary

Before local synthesis uses a Mercouris source as source truth, import the selected capture into:

`narrative-geopolitics/archive/sources/YYYY-MM-DD/source-*.md`

Then add a manifest row with:

- `voice_slugs: ["mercouris"]`
- `host_slug` only when a host/channel conditioning layer is present
- `source_class` such as `stream-native synthesis`, `guest interview pressure test`, or `panel reinforcement`
- `modality` such as `transcript`, `cleaned-transcript`, `stream`, or `mixed`

## Local Route Status

| Route | Status | Notes |
| --- | --- | --- |
| [README.md](README.md) | `active-seed` | Local voice record exists. |
| [claim-map.md](claim-map.md) | `active-seed` | Claim families are seeded from Statecraft surfaces. |
| Local archive imports | `not-started` | No Mercouris source captures are copied into Narrative archive yet. |
| Local channel shelves | `candidate` | `alexander-mercouris` and `the-duran` should be promoted when an import slice is selected. |
