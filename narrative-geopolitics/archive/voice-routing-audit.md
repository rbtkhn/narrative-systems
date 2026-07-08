# Voice Routing Audit

Status: `working`

This note records archive-level checks for whether imported sources should carry more than one `voice_slug`.

## Rule

Use `voice_slugs` for recurring source-people whose interpretive pattern may need continuity tracking.

Use `host_slug` for host, channel, show, or publication routing when the host context matters but a durable voice record is not yet justified.

Do not add entity, institution, publication, or channel slugs to `voice_slugs` until the system explicitly supports non-person continuity records.

## Pape Import Audit

Audit date: `2026-07-07`

Source basis: [source-manifest.json](source-manifest.json)

The Pape import contains 17 guest/interview pressure-test sources. Most should remain `voice_slugs: ["pape"]` because Pape is the load-bearing voice and the host is either a one-off person or a channel/entity.

One recurring host-pressure voice should already be represented in `voice_slugs`:

| Voice slug | Evidence | Decision |
| --- | --- | --- |
| `mario-nawfal` | Appears as person-host across 7 Pape interview captures. | Add alongside `pape` on those 7 source rows. |

These person-hosts remain candidates, but are not promoted in this pass:

| Candidate slug | Evidence | Reason held back |
| --- | --- | --- |
| `clayton-morris` | Appears in 2 Redacted captures. | Redacted may need a channel/show continuity model before person-host promotion. |
| `natali-morris` | Appears in 2 Redacted captures. | Same as above. |
| `daniel-davis` | Appears in 1 Pape capture. | One source is not enough for a voice record. |
| `cyrus-janssen` | Appears in 1 Pape capture. | One source is not enough for a voice record. |
| `ryan-grim` | Appears in 1 Pape capture. | One source is not enough for a voice record. |
| `tom-switzer` | Appears in 1 Pape capture. | One source is not enough for a voice record. |
| `sulaiman-ahmed` | Appears in 1 Pape capture. | One source is not enough for a voice record. |

## Follow-Up

If `mario-nawfal` becomes a full voice record, its source index should link back into the 7 shared archive files already tagged in the manifest.
