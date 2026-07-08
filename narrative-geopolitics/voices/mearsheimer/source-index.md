# Mearsheimer Source Index

This index routes John Mearsheimer voice work to the upstream Statecraft source basis.

Source basis: `strategy-codex/statecraft/voices/mearsheimer/`.

Status: `source-basis-pointer`

This pass does not import the full Mearsheimer corpus into `narrative-geopolitics/archive/sources/`. Statecraft currently identifies 96 eligible archive captures across host lanes, authored/shorthand material, and non-core appearances.

## Reading Rule

1. Mearsheimer is host-led: host lanes own the cleanest chronology and transformation.
2. Transcript-first evidence, arc-first interpretation.
3. Use the local claim map for structural-realism routing, not as source truth.
4. Do not collapse host lanes into one generic Mearsheimer verdict.

## Upstream Open-First Surfaces

| Upstream surface | Job in Narrative Geopolitics |
| --- | --- |
| `statecraft/voices/mearsheimer/README.md` | Statecraft front door and shelf-class explanation. |
| `statecraft/voices/mearsheimer/mearsheimer-profile.md` | Identity, voice fingerprint, failure modes, June 2026 receipts. |
| `statecraft/voices/mearsheimer/mearsheimer-routing.md` | Explains transcript-first evidence and arc-first interpretation. |
| `statecraft/voices/mearsheimer/mearsheimer-source-index.md` | Exhaustive route map for materialized appearances. |
| `statecraft/voices/mearsheimer/mearsheimer-surface-orthogonality-2026-05.md` | Host-lane orthogonality review. |
| `statecraft/voices/mearsheimer/mearsheimer-helix.md` | Support surface for durable host-led structure. |

## Corpus Shape From Statecraft

| Surface | Approximate role | Local Narrative status |
| --- | --- | --- |
| Glenn Diesen x Mearsheimer | Highest-altitude structural realism, security dilemma, order transition. | `not-imported` |
| Daniel Davis x Mearsheimer | Force-versus-bargaining, coercive failure, settlement impossibility. | `not-imported` |
| Judging Freedom x Mearsheimer | Defeat accounting, self-entrapment, Washington-has-already-lost reinforcement. | `not-imported` |
| Tucker / Hedges / Redacted / misc | Non-core appearance bench and auxiliary pressure tests. | `not-imported` |
| Authored/shorthand captures | Parity rows, not chronology substitutes. | `not-imported` |

## Candidate Import Slices

| Slice | Why it is useful | Suggested first files |
| --- | --- | --- |
| June 2026 Iran receipts | Direct comparison with Pape and Mercouris during the Iran/MOU period. | `2026-06-02` Napolitano, `2026-06-09` Tucker, `2026-06-11` Davis. |
| Diesen structural lane | Best source for security dilemma and order-transition altitude. | Selected Diesen x Mearsheimer 2026 rows. |
| Davis bargaining lane | Best source for force-versus-bargaining and punishment-failure analysis. | Selected Davis x Mearsheimer 2026 rows. |
| Iran authored / shorthand bench | Useful for comparing structural claims to Pape's authored forecast spine. | `The Tag Team Fails in Iran`, `Will Trump Go Kamikaze?`. |

## Import Boundary

Before local synthesis uses a Mearsheimer source as source truth, import the selected capture into:

`narrative-geopolitics/archive/sources/YYYY-MM-DD/source-*.md`

Then add a manifest row with:

- `voice_slugs: ["mearsheimer"]`
- `host_slug` only when a host/channel conditioning layer is present
- `source_class` such as `structural realism interview`, `guest interview pressure test`, or `authored structural claim`
- `modality` such as `transcript`, `cleaned-transcript`, `interview`, or `essay`

## Local Route Status

| Route | Status | Notes |
| --- | --- | --- |
| [README.md](README.md) | `active-seed` | Local voice record exists. |
| [claim-map.md](claim-map.md) | `active-seed` | Claim families are seeded from Statecraft surfaces. |
| Local archive imports | `not-started` | No Mearsheimer source captures are copied into Narrative archive yet. |
| Local channel shelves | `candidate` | Glenn Diesen, Daniel Davis, Judging Freedom, Tucker, and other host shelves should be promoted as import slices require. |
