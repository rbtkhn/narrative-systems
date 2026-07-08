# Davis Source Index

This index routes Daniel Davis voice work to the upstream Statecraft source basis.

Source basis: `strategy-codex/statecraft/voices/davis/`.

Status: `source-basis-pointer`

This pass does not import the full Davis corpus into `narrative-geopolitics/archive/sources/`. Davis's upstream surface is stream-native and double-role: he is both a recurring analyst voice and an important host/channel conditioner.

## Reading Rule

1. Davis is stream-native before he is a generic interview guest.
2. Route Davis-as-voice separately from Davis-as-channel-conditioning.
3. Use this file for routing, not source truth.
4. Do not treat guests on Daniel Davis Deep Dive as becoming Davis.
5. Open the channel shelf when Davis is shaping another voice as host.

## Upstream Open-First Surfaces

| Upstream surface | Job in Narrative Geopolitics |
| --- | --- |
| `statecraft/voices/davis/README.md` | Statecraft front door and boundary between Davis voice and Davis host work. |
| `statecraft/voices/davis/davis-profile.md` | Identity, style, recurring claims, and source pointers. |
| `statecraft/voices/davis/davis-speaker-object.md` | Defines Davis as a stream-native practical-room speaker object. |
| `statecraft/voices/davis/davis-host-law.md` | Explains when to open Davis as host for feasibility and war-termination testing. |
| `statecraft/voices/davis/davis-host-wiring-2026.md` | Explains how Davis transforms guest voices through military feasibility pressure. |
| `statecraft/voices/davis/davis-index.md` | Cross-host guest captures where Davis appears elsewhere. |
| `statecraft/voices/davis/davis-lane-map-2026-05.md` | Lane notes for Davis's restraint, feasibility, and negotiation-clock function. |
| `statecraft/channels/daniel-davis/daniel-davis-channel-index.md` | Host-channel captures where Davis is host or solo channel owner. |

## Corpus Shape From Statecraft

| Surface | Approximate role | Local Narrative status |
| --- | --- | --- |
| Daniel Davis Deep Dive captures | Native stream and host-conditioning body. | `partly-linked` |
| Cross-host guest captures | Glenn Diesen and Dialogue Works appearances. | `not-imported` |
| Davis profile / speaker object | Voice fingerprint and practical-room definition. | `source-basis` |
| Host law / host wiring | How Davis elicits feasibility and settlement-room tests from guests. | `source-basis` |
| Defense Priorities and written work | Written Davis source modality. | `not-imported` |

## Candidate Import Slices

| Slice | Why it is useful | Suggested first files |
| --- | --- | --- |
| Davis as practical-room baseline | Establishes the voice's own feasibility discipline before guest transformations. | Selected solo or Davis-authored 2026 captures. |
| Pape x Davis escalation lane | Tests Pape's mechanism/falsifier model against Davis's force-feasibility and off-ramp questions. | [../../archive/sources/2026-03-10/source-daniel-davis-pape-escalation-trap-2026-03-10.md](../../archive/sources/2026-03-10/source-daniel-davis-pape-escalation-trap-2026-03-10.md) |
| Mearsheimer x Davis bargaining lane | Tests structural realism against practical war-termination and bargaining-room constraints. | Selected Davis-hosted Mearsheimer captures. |
| Marandi x Davis coercion-resistance lane | Tests Iran-facing red-line and legitimacy claims against force feasibility and operational limits. | Selected Davis-hosted Marandi captures. |
| Technical feasibility lane | Separates Davis practical-room testing from technical specialists. | Selected Jermy, Postol, Ritter, or Martyanov captures on Davis. |
| Cross-host Davis guest rows | Tests how Davis sounds when he is not controlling the channel frame. | Glenn Diesen and Dialogue Works guest captures from `davis-index.md`. |

## Import Boundary

Before local synthesis uses a Davis source as source truth, import the selected capture into:

`narrative-geopolitics/archive/sources/YYYY-MM-DD/source-*.md`

Then add a manifest row with:

- `voice_slugs: ["davis"]` when Davis is the source-person whose own claims are being tracked
- `host_slug: "daniel-davis"` only when Davis is shaping another voice through the channel layer
- `source_class` such as `stream-native feasibility synthesis`, `host-convener transformation`, `guest interview pressure test`, or `restraint-realism article`
- `modality` such as `transcript`, `cleaned-transcript`, `stream`, `interview`, `article`, `social-post`, or `mixed`

## Local Route Status

| Route | Status | Notes |
| --- | --- | --- |
| [README.md](README.md) | `active-seed` | Local voice record exists. |
| [claim-map.md](claim-map.md) | `active-seed` | Claim families are seeded from Statecraft surfaces. |
| [../../channels/daniel-davis/README.md](../../channels/daniel-davis/README.md) | `active-lightweight` | Local Daniel Davis channel shelf exists from the Pape pilot. |
| Local archive imports | `partial` | One Pape-on-Davis source is already imported for Pape routing; Davis's own voice corpus is not imported yet. |
