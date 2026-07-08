# Voices

`voices/` is the voice continuity layer for Narrative Geopolitics.

A voice is a recurring source-person whose claims, frames, forecasts, contradictions, and source modalities matter across time. A voice may be a speaker, writer, essayist, interview guest, social poster, streamer, report author, or mixed-format analyst.

## Purpose

Voice records help daily geopolitics work remember whether a claim is new, recurring, contradicted, forecast-bearing, or shaped by source modality.

They keep the system from treating every quote or article as isolated.

## Voice Records

A `voice record` is the durable continuity object for one person/source.

Use [_template.md](_template.md) for every new voice record. The template is intentionally lighter than the inherited `strategy-codex/statecraft` voice machinery, but it preserves one important law: every recurring voice should have the same basic shape.

## Current Voice Records

| Voice | Record | Source index | Status |
| --- | --- | --- | --- |
| Alexander Mercouris | [mercouris/README.md](mercouris/README.md) | [mercouris/source-index.md](mercouris/source-index.md) | internal-seed |
| John Mearsheimer | [mearsheimer/README.md](mearsheimer/README.md) | [mearsheimer/source-index.md](mearsheimer/source-index.md) | internal-seed |
| Seyed Mohammad Marandi | [marandi/README.md](marandi/README.md) | [marandi/source-index.md](marandi/source-index.md) | internal-seed |
| Robert Pape | [pape/README.md](pape/README.md) | [pape/source-index.md](pape/source-index.md) | internal |

## Comparison Notes

| Comparison | Purpose | Status |
| --- | --- | --- |
| [Pape / Mercouris orthogonality](comparisons/pape-mercouris.md) | Preserves the mechanism/falsifier axis vs room/sequence/legitimacy axis. | seed-comparison |

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
