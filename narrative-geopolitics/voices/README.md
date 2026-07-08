# Voices

`voices/` is the voice continuity layer for Narrative Geopolitics.

A voice is a recurring source-person whose claims, frames, forecasts, contradictions, and source modalities matter across time. A voice may be a speaker, writer, essayist, interview guest, social poster, streamer, report author, or mixed-format analyst.

## Purpose

Voice records help daily geopolitics work remember whether a claim is new, recurring, contradicted, forecast-bearing, or shaped by source modality.

They keep the system from treating every quote or article as isolated.

## Voice Records

A `voice record` is the durable continuity object for one person/source.

Use [_template.md](_template.md) for every new voice record. The template is intentionally lighter than the inherited `strategy-codex/statecraft` voice machinery, but it preserves one important law: every recurring voice should have the same basic shape.

For navigability, each voice directory should now expose:

- `README.md` as the canonical profile surface
- `source-index.md` as the canonical routing/index surface
- `profile.md` as a stable alias to the profile surface
- `index.md` as a stable alias to the routing/index surface

## Pape-Parity Standard

`Pape parity` means a voice has the same operational shape as Pape, even if it does not yet have Pape's full 75-source depth.

A parity-ready voice has:

- a voice record, source index, and claim map
- at least two voice-native retrieval lenses
- imported central archive sources
- manifest rows for those sources
- channel-aware routing when a source is host-conditioned

Pape is currently `full-source-parity`. The other core voices are `first-slice-parity`: source-backed enough for synthesis, but not yet exhaustive.

## Current Voice Records

| Voice | Profile | Index | Status |
| --- | --- | --- | --- |
| Alexander Mercouris | [mercouris/profile.md](mercouris/profile.md) | [mercouris/index.md](mercouris/index.md) | internal / first-slice-parity |
| Daniel Davis | [davis/profile.md](davis/profile.md) | [davis/index.md](davis/index.md) | internal / first-slice-parity |
| Douglas Macgregor | [macgregor/profile.md](macgregor/profile.md) | [macgregor/index.md](macgregor/index.md) | internal / first-slice-parity |
| Glenn Diesen | [diesen/profile.md](diesen/profile.md) | [diesen/index.md](diesen/index.md) | internal / first-slice-parity |
| Larry Johnson | [johnson/profile.md](johnson/profile.md) | [johnson/index.md](johnson/index.md) | internal / first-slice-parity |
| John Mearsheimer | [mearsheimer/profile.md](mearsheimer/profile.md) | [mearsheimer/index.md](mearsheimer/index.md) | internal / first-slice-parity |
| Seyed Mohammad Marandi | [marandi/profile.md](marandi/profile.md) | [marandi/index.md](marandi/index.md) | internal / first-slice-parity |
| Robert Pape | [pape/profile.md](pape/profile.md) | [pape/index.md](pape/index.md) | internal / full-source-parity |

## Comparison Notes

| Comparison | Purpose | Status |
| --- | --- | --- |
| [Voice orthogonality map](comparisons/orthogonality-map.md) | Preserves the current six-axis ensemble and its do-not-collapse rules. | seed-map |
| [Pape / Mearsheimer comparison](comparisons/pape-mearsheimer.md) | Distinguishes mechanism-and-falsifier retrieval from structure-and-bargaining-geometry retrieval. | working-comparison |
| [Pape / Mercouris orthogonality](comparisons/pape-mercouris.md) | Compatibility pointer to the ensemble orthogonality map. | compat-pointer |

## Status

Voice records are internal first. Public summaries can come later when a record is stable enough to share.

People come first. Entity, institution, publication, or channel records can be added later if daily runs prove they need their own continuity objects.

Host, show, and channel conditioning belongs in [../channels/](../channels/README.md), not in a voice record, unless the host also becomes a recurring source-person whose own claims need continuity.

## Minimum Rule

Do not add a voice record just because a source appears once.

Add a record when at least one of these is true:

- the voice recurs across daily runs
- the voice makes forecast-bearing claims
- the voice's prior pattern materially changes interpretation
- the source modality changes how the claim should be read
- contradictions or tensions need continuity tracking
