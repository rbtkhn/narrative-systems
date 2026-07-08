# Marandi Source Index

This index routes Seyed Mohammad Marandi voice work to the upstream Statecraft source basis.

Source basis: `strategy-codex/statecraft/voices/marandi/`.

Status: `source-basis-pointer`

This pass does not import the full Marandi corpus into `narrative-geopolitics/archive/sources/`. Statecraft currently identifies 73 eligible archive captures and a mature three-host core.

## Reading Rule

1. Marandi is a speaker-first, helix-centered cross-host object.
2. Dialogue Works, Diesen, and Davis each own distinct host transformations.
3. Use this file for routing, not source truth.
4. Do not collapse Iranian signaling into independently verified event fact.

## Upstream Open-First Surfaces

| Upstream surface | Job in Narrative Geopolitics |
| --- | --- |
| `statecraft/voices/marandi/README.md` | Statecraft front door and shelf-shape explanation. |
| `statecraft/voices/marandi/marandi-profile.md` | Identity, regional-embedded role, source handles. |
| `statecraft/voices/marandi/marandi-routing.md` | Fast task-to-host-lane routing. |
| `statecraft/voices/marandi/marandi-source-index.md` | Exhaustive route map for materialized Marandi appearances. |
| `statecraft/voices/marandi/marandi-surface-orthogonality-2026-05.md` | Host-lane orthogonality review. |
| `statecraft/voices/marandi/marandi-helix.md` | Explains the three-host mature core. |
| `statecraft/voices/marandi/marandi-2025-present-arc-threads.md` | Recurring thread atlas for legitimacy, Hormuz, siege, complicity, diplomacy, and sovereignty. |

## Corpus Shape From Statecraft

| Surface | Approximate role | Local Narrative status |
| --- | --- | --- |
| Dialogue Works x Marandi | Live-pressure legitimacy, selective Hormuz, Gulf complicity, red-line signaling. | `not-imported` |
| Glenn Diesen x Marandi | Strategic-order altitude, escalation horizon, blockade consequence. | `not-imported` |
| Daniel Davis x Marandi | Operational limits, failed intimidation, shrinking U.S. coercive room. | `not-imported` |
| Napolitano x Marandi | Tehran live / U.S.-audience translation support tier. | `not-imported` |
| Shorthand / X / reposts | Support evidence and signal captures. | `not-imported` |

## Candidate Import Slices

| Slice | Why it is useful | Suggested first files |
| --- | --- | --- |
| May 2026 Hormuz anchor | Best single opening for the strongest Marandi lane. | `2026-05-05` Dialogue Works x Marandi. |
| June 2026 MOU / Geneva / Hormuz week | Direct comparison with Pape, Mercouris, and Mearsheimer during the Iran/MOU period. | June cadence rows from `marandi-source-index.md`. |
| Davis failed-intimidation lane | Best source for force-versus-resilience and operational-limit testing. | `2026-05-10` Davis x Marandi and related 2026 rows. |
| Diesen escalation-horizon lane | Best source for regional escalation and order-transition implications. | `2026-05-05`, `2026-06-05`, and `2026-06-25` Diesen rows. |

## Import Boundary

Before local synthesis uses a Marandi source as source truth, import the selected capture into:

`narrative-geopolitics/archive/sources/YYYY-MM-DD/source-*.md`

Then add a manifest row with:

- `voice_slugs: ["marandi"]`
- `host_slug` only when a host/channel conditioning layer is present
- `source_class` such as `regional-embedded red-line interview`, `guest interview pressure test`, or `signal capture`
- `modality` such as `transcript`, `cleaned-transcript`, `interview`, `social-post`, or `mixed`

## Local Route Status

| Route | Status | Notes |
| --- | --- | --- |
| [README.md](README.md) | `active-seed` | Local voice record exists. |
| [claim-map.md](claim-map.md) | `active-seed` | Claim families are seeded from Statecraft surfaces. |
| Local archive imports | `not-started` | No Marandi source captures are copied into Narrative archive yet. |
| Local channel shelves | `candidate` | Dialogue Works, Glenn Diesen, Daniel Davis, Judging Freedom, and related host shelves should be promoted as import slices require. |
