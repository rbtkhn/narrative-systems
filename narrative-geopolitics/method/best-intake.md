# Best Intake

`best-intake` is the default source-intake contract for Narrative Geopolitics.

It exists to solve one problem: intake should be fast enough to keep same-day source batches moving, but reliable enough that the archive does not fill with misleading half-truths.

## Purpose

`best-intake` is not the fastest possible intake mode and not the most exhaustive possible intake mode.

It is the best tradeoff between:

- speed
- source preservation
- honest uncertainty
- later retrievability
- downstream voice and channel work

Short rule:

```text
land quickly, preserve truthfully, defer safely
```

## Core Principle

The first obligation of intake is not interpretation.

The first obligation of intake is to make sure a source is:

- landed
- attributable
- recoverable
- linkable
- reviewable

If that happens, later enrichment can improve the record.

If that does not happen, later enrichment has nothing durable to work on.

## Best-Intake Standard

A `best-intake` source is adequate when it has:

- a real archive file under `archive/sources/YYYY-MM-DD/`
- a working source title
- a source URL when available
- the pasted body preserved
- a publication date or best-known provisional date
- at least one provisional `voice_slug`
- a `host_slug` when obvious
- an explicit review state when certainty is incomplete
- a manifest row

It does **not** need full routing, perfect family calibration, or public-synthesis readiness at landing time.

## Required Inputs

Minimum operator inputs:

- `date`
- `title`
- `url` when available
- `body`
- `voice_slug` when reasonably clear

Optional but preferred:

- `host_slug`
- `modality`
- `source_form`

For operator paste sessions, prefer filling
[../templates/intake-metadata.md](../templates/intake-metadata.md) first so the
source can be landed without reconstructing metadata from memory during intake.

If optional fields are unclear, preserve uncertainty instead of inventing precision.

## What Best-Intake Does

`best-intake` should:

1. Create the source file in `archive/sources/YYYY-MM-DD/`.
2. Preserve the pasted source body with minimal rewriting.
3. Add only enough frontmatter to keep provenance and retrieval usable.
4. Append a manifest row.
5. Mark uncertainty explicitly when classification is provisional.

## What Best-Intake Defers

`best-intake` should usually defer:

- deep title cleanup
- host-conditioning interpretation
- source-index updates beyond what is necessary
- voice-lens synthesis
- sectioning for readability
- public-brief extraction
- quote curation
- claim extraction
- forecast generation

Short rule:

```text
archive now, interpret later
```

Small deterministic wrapper removal is allowed when it saves obvious intake
waste without changing source meaning. Current approved case:

- `mario-nawfal` opening camera / rapport chatter before the real setup begins
- `mario-nawfal` closing scheduling / signoff chatter after the substantive interview ends
- `daniel-davis` closing next-show / subscribe / channel-promotion chatter after the substantive interview ends
- `alexander-mercouris` routine solo subscribe / platform signoff wrapper and standard subscribe reminder sentence in the opening
- `dialogue-works` transcript wrapper removal when a pasted body begins with a `... - YouTube` title line followed by `Transcripts:`

## Deterministic Trim Policy

Deterministic trimming is allowed only when the trim target is format noise,
not source substance.

Approval standard:

- the wrapper is recurring, not one-off
- the wrapper is host-format chatter, not guest analysis
- the cut point is detectable by stable phrase markers
- false-positive risk is low
- if the pattern is ambiguous, do not automate it

Safe deterministic trim:

- repeated host intros that occur before the real setup begins
- repeated host signoff or schedule chatter after the real interview ends
- repeated subscription or sponsor-style language that is clearly outside the source object

Unsafe semantic trim:

- removing setup because it "feels low value"
- deleting material that blends host framing with guest substance
- collapsing multi-speaker openings when the first substantive claim is not clearly separable

Short rule:

```text
if the cut depends on judgment, it is not deterministic trim
```

## Survey And Approval Workflow

When evaluating a new host or channel for trim automation:

1. Collect 3 to 5 archived examples for one `host_slug`.
2. Inspect the first and last transcript segments.
3. Record repeated low-value wrapper phrases.
4. Reject the host if the cut point overlaps with substantive setup too often.
5. Add a rule only after the markers are documented and look stable.
6. Validate on one fresh landing and inspect the saved chars and words.
7. Keep the rule list curated. Do not auto-generate trim rules from transcripts.

Candidate and approved are different states:

- candidate = worth surveying
- approved = safe enough for deterministic auto-trim

Current candidate-only hosts:

- none currently documented here

Current approved hosts:

- `mario-nawfal`
- `daniel-davis`
- `alexander-mercouris`
- `dialogue-works`

## Status Model

Every `best-intake` source should be legible about its state.

Suggested state fields:

- `review_state: unreviewed`
- `routing_state: provisional`
- `source_form: unknown`
- `host_slug: null`

Use these only when needed. The point is not to create bureaucracy; the point is to avoid false completeness.

## Decision Rules

### Use Best-Intake By Default

Use `best-intake` for:

- operator-pasted same-day transcripts
- recurring voice sources with known ownership
- solo analyst uploads
- clearly attributable interviews
- same-day batch work where throughput matters

### Use Best-Intake With Caution

Use `best-intake` but mark provisional state for:

- uncertain host ownership
- likely clipped excerpts
- unclear modality
- mixed-format captures
- multi-speaker objects where one voice is primary but not exclusive

### Block Auto-Confidence

Do not let `best-intake` silently claim certainty for:

- panel ownership
- channel conditioning
- excerpt vs full-source distinction
- voice dominance in ambiguous multi-speaker material

When uncertain:

```text
land provisionally and flag for enrichment
```

## Failure Modes

`best-intake` fails when:

- speed is purchased by losing source truth
- provisional metadata is mistaken for final metadata
- ambiguous ownership is flattened into fake certainty
- the archive accumulates permanently unreviewed records with no later pass

This means `best-intake` must be paired with a later enrichment path.

## Enrichment Relationship

`best-intake` is a landing contract, not a finishing contract.

## Measuring Gain

Trim savings should be measurable by host, not anecdotal.

Newly landed sources can record:

- `opening_trim_applied`
- `opening_trim_rule`
- `opening_trim_chars_saved`
- `opening_trim_words_saved`
- `closing_trim_applied`
- `closing_trim_rule`
- `closing_trim_chars_saved`
- `closing_trim_words_saved`

For host-level reporting, use:

```powershell
python scripts\report_trim_stats.py
python scripts\report_trim_stats.py --host-slug mario-nawfal
python scripts\report_trim_stats.py --host-slug daniel-davis
```

Its companion step is a later enrichment pass that can:

- refine source form
- refine modality
- update routing surfaces
- improve title accuracy
- add sectioning
- support daily synthesis

The system should treat these as separate jobs.

## Why Best-Intake Is Better Than Fast-Intake Alone

Pure `fast-intake` is optimized almost entirely for throughput.

That is useful, but alone it can overproduce low-confidence records.

`best-intake` keeps most of the speed gains while adding two protections:

- explicit provisionality
- minimum retrieval integrity

So the contract is:

- faster than full bespoke intake
- safer than raw fast landing
- more scalable than manual perfection

## Voice Adequacy Claim

`best-intake` is adequate for all voice intakes because every voice shares the same first archival need:

- preserve source truth quickly
- preserve provenance honestly
- preserve enough metadata for later recovery

Voices differ mainly in interpretation and conditioning, not in the minimum conditions for safe landing.

That is why `best-intake` can serve:

- Pape
- Mercouris
- Marandi
- Mearsheimer
- Davis
- Diesen

and future voices as well.

## Repository Rule

When there is tension between:

- finishing intake perfectly
- and keeping source throughput alive

prefer `best-intake`, provided the source remains honest, archived, and reviewable.
