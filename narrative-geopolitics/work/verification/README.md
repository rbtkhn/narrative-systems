# From Claims to Consequences: Operational Verification

Status: `active work contract`

Operational verification tests a selected claim against bounded external evidence. It does not turn repeated commentary into fact, replace archive provenance, or authorize generalized collection.

## Boundary

- Requests are created explicitly for load-bearing claims.
- Research is limited to the packet's named observables.
- Evidence remains under `work/verification/`; it is not archive source truth.
- Store citations, short compliant excerpts or paraphrases, provenance, and assessment notes—not copied webpages.
- Several URLs derived from one originating report remain one evidence chain.
- The source registry records capability and situated perspective, never a universal trust score.
- Perspective diversity improves access and contradiction detection; observable evidence still governs the assessment.
- Automation validates packet completeness; a human owns the assessment.

## Workflow

```text
source_assertion
-> explicit VER request
-> bounded evidence records
-> independence analysis
-> human assessment
-> optional judgment, promotion, publication, or forecast review
```

Commands:

```powershell
.\scripts\python.ps1 scripts\verification.py new --date YYYY-MM-DD --slug TEXT
.\scripts\python.ps1 scripts\verification.py list --json
.\scripts\python.ps1 scripts\verification.py check [VER-ID] --json
.\scripts\python.ps1 scripts\verification.py close VER-ID
.\scripts\python.ps1 scripts\verification.py sources --domain maritime_incident --json
```

## Source Registry and Coverage

[`source-registry.md`](source-registry.md) contains 36 manually reviewed sources with stable `VSRC-*` IDs. Each evidence row cites one ID and retains its own URL, event time, originating chain, and translation provenance. Paid sources have open fallbacks. State-affiliated and interested official sources are retained for official positions, warning language, local leads, and contradiction checks; they cannot independently establish an operational fact.

An assessed packet audits six coverage floors. Missing categories are honest waivers, not silent omissions. Two outlets inheriting one report still count as one chain, regardless of political or cultural difference.

## States and Outcomes

Workflow states: `requested`, `researching`, `assessed`, `closed`.

Assessment outcomes: `operationally_supported`, `operationally_contested`, `disconfirmed`, `unresolvable_with_authorized_evidence`, `not_investigated`.

`operationally_supported` means the packet contains affirmative operational evidence adequate for the bounded claim. It never means omniscient or final truth.

## Judgment Gate

Attributed narrative claims may remain `source_assertion` without a packet. A document adopting an operational claim uses:

```markdown
Operational status: `operationally_supported`
Verification packet: VER-YYYYMMDD-NN plus its resolving relative Markdown link
```

Watch promotion and publication templates must use the same gate when a concrete event carries the decision. Accountable forecast resolutions cite a completed `VER-*` packet in the ledger review note.
