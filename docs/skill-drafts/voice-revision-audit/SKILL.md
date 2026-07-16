---
name: voice-revision-audit
description: Audit Narrative Geopolitics archive transcripts for substantive instances where a featured voice admits error or transparently revises a position, forecast, or analytical model. Use for date-bounded or voice-bounded accountability audits, prediction-revision searches, intellectual-honesty comparisons, and requests to find when a voice said they were wrong. Do not use for general fact-checking or to decide whether the revised claim is true.
---

# Voice Revision Audit

Use only with the Narrative Geopolitics archive. Keep the audit read-only.

## Retrieve candidates

1. Resolve the requested inclusive date range. If none is supplied, ask for one.
2. Execute the bundled `scripts/find_revision_candidates.py` retrieval aid
   with a Python 3.11+ interpreter, the inclusive `--from` and `--to` dates,
   and `--repo-root` pointing at the repository root. This draft does not add a
   public repository command surface.
3. Use `--voice TEXT` when the operator limits the audit to a named voice.
4. Treat the JSON as candidate retrieval, never as findings. Read each cited
   transcript passage and enough preceding dialogue to establish the speaker,
   prior belief, new belief, and reason for the change.

## Adjudicate

Retain only substantive changes and assign exactly one class:

- `explicit-personal-admission`: the speaker directly says they were wrong,
  mistaken, ignorant, or had misjudged the matter.
- `personal-position-revision`: the speaker abandons or materially changes a
  prior interpretation or policy position.
- `personal-prediction-revision`: events cause the speaker to withdraw,
  narrow, delay, or otherwise modify a forecast.
- `qualified-collective-revision`: the speaker uses `we` or otherwise makes
  personal accountability plausible but not certain. Report these separately.

Require evidence of both the prior position and the revision. Do not infer an
admission merely because a current statement conflicts with older material.

Reject:

- claims that another person, institution, or government was wrong;
- conditional promises such as “if I am wrong”;
- predictions described as confirmed rather than revised;
- rhetorical hypotheticals and quoted speech;
- trivial slips unless the operator explicitly requests them;
- duplicate mentions of the same revision in one appearance;
- passages whose speaker cannot be resolved from metadata and turn context.

Do not convert a host's statement into a guest finding. Flag damaged ASR,
ambiguous pronouns, and collective language rather than silently resolving
them. The audit measures transparent updating, not whether either the original
or revised claim is factually correct.

## Return

State the date range and number of source files examined. Report:

1. strong personal findings and unique-voice count;
2. a compact table with date, voice, prior view, revision, and class;
3. short excerpts linked to absolute source paths and line numbers;
4. qualified collective findings in a separate section;
5. representative exclusions and the reason for exclusion;
6. transcript review or ASR limitations;
7. confirmation that no archive files were changed.

Prefer precise counts over claims that the search was exhaustive beyond the
files actually present. Keep excerpts short and distinguish transcript evidence
from audio-verified quotation.
