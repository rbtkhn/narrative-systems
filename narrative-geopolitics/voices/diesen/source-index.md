# Diesen Source Index

This index routes Glenn Diesen voice work to the upstream Statecraft source basis.

Source basis: `strategy-codex/statecraft/voices/diesen/`.

Status: `source-basis-pointer`

This pass does not import the full Diesen corpus into `narrative-geopolitics/archive/sources/`. Diesen's upstream surface is high-density and stream-native, with a large Glenn Diesen channel body plus a small cross-host guest index.

## Reading Rule

1. Diesen is stream-native and also a host/convener.
2. Route Diesen-as-voice separately from Diesen-as-channel-conditioning.
3. Use this file for routing, not source truth.
4. Do not treat guest transformations on the Glenn Diesen channel as erasing the guest voice.

## Upstream Open-First Surfaces

| Upstream surface | Job in Narrative Geopolitics |
| --- | --- |
| `statecraft/voices/diesen/README.md` | Statecraft front door and stream-native shelf explanation. |
| `statecraft/voices/diesen/diesen-profile.md` | Identity, role, public source pointers, and ledger notes. |
| `statecraft/voices/diesen/diesen-speaker-object.md` | Defines Diesen as a first-class stream-native speaker object. |
| `statecraft/voices/diesen/diesen-host-wiring-2026.md` | Explains how Diesen as host transforms guest voices. |
| `statecraft/voices/diesen/diesen-index.md` | Cross-host guest captures where Diesen appears elsewhere. |
| `statecraft/channels/glenn-diesen/glenn-diesen-channel-index.md` | Host-channel captures where Diesen is host or solo channel owner. |

## Corpus Shape From Statecraft

| Surface | Approximate role | Local Narrative status |
| --- | --- | --- |
| Glenn Diesen channel captures | Native stream and host-convener body. | `not-imported` |
| Cross-host guest captures | Daniel Davis, Mario Nawfal, Judging Freedom. | `not-imported` |
| Guest transformation matrix | How Diesen elicits order-transition readings from other voices. | `source-basis` |
| Guest ledgers | Mearsheimer, Sachs, Ritter, Macgregor, and other stream ledgers. | `source-basis` |

## Candidate Import Slices

| Slice | Why it is useful | Suggested first files |
| --- | --- | --- |
| Mearsheimer x Diesen structural lane | Tests Diesen as order-transition convener against Mearsheimer as structural realist. | Selected 2026 Diesen x Mearsheimer captures. |
| Marandi x Diesen escalation horizon | Tests regional red-line framing lifted into order-transition consequence. | Selected Marandi x Diesen 2026 captures. |
| Sachs x Diesen economic-order lane | Adds economic-system and development-order pressure. | Selected Sachs x Diesen captures. |
| Cross-host Diesen guest rows | Tests how Diesen sounds when not controlling the channel frame. | Davis, Mario Nawfal, and Judging Freedom guest rows. |

## Import Boundary

Before local synthesis uses a Diesen source as source truth, import the selected capture into:

`narrative-geopolitics/archive/sources/YYYY-MM-DD/source-*.md`

Then add a manifest row with:

- `voice_slugs: ["diesen"]`
- `host_slug` only when a host/channel conditioning layer is present
- `source_class` such as `stream-native order synthesis`, `host-convener transformation`, or `guest interview pressure test`
- `modality` such as `transcript`, `cleaned-transcript`, `stream`, `interview`, or `mixed`

## Local Route Status

| Route | Status | Notes |
| --- | --- | --- |
| [README.md](README.md) | `active-seed` | Local voice record exists. |
| [claim-map.md](claim-map.md) | `active-seed` | Claim families are seeded from Statecraft surfaces. |
| Local archive imports | `not-started` | No Diesen source captures are copied into Narrative archive yet. |
| Local channel shelves | `candidate` | `glenn-diesen` should be promoted when channel conditioning is needed. |
