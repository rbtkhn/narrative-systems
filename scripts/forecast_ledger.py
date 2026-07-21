from __future__ import annotations

import re
from collections import Counter
from dataclasses import dataclass


TRIAGE_HEADING = "## Accountability Triage"
FORECAST_TYPES = {
    "ex_ante",
    "retrospective_hypothesis",
    "indicator",
    "falsifier",
    "unscorable",
}
RESOLUTION_STATUSES = {
    "open",
    "hit",
    "miss",
    "mixed",
    "unresolved",
    "unresolvable_with_authorized_evidence",
    "excluded_retrospective",
    "excluded_unscorable",
}
VERIFICATION_REQUIRED_STATUSES = {
    "hit",
    "miss",
    "mixed",
    "unresolvable_with_authorized_evidence",
}
VERIFICATION_RE = re.compile(r"VER-\d{8}-\d{2}")
ENTRY_RE = re.compile(
    r"^\|\s*`(NG-\d{8}-F\d{2})`\s*\|\s*`([^`]+)`\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|"
    r"\s*`(low|plausible|likely|high)`\s*\|\s*`([^`]+)`\s*\|\s*(.*?)\s*\|\s*`([^`]+)`\s*\|$"
)
TRIAGE_RE = re.compile(
    r"^\|\s*`(NG-\d{8}-F\d{2})`\s*\|\s*`([^`]+)`\s*\|\s*`([^`]+)`\s*\|"
    r"\s*`([^`]+)`\s*\|\s*`([^`]+)`\s*\|\s*`(yes|no)`\s*\|\s*(.*?)\s*\|$"
)


@dataclass(frozen=True)
class ForecastEntry:
    hook_id: str
    run_date: str
    crisis_object: str
    claim: str
    probability_band: str
    review_date: str
    source_run: str
    status: str


@dataclass(frozen=True)
class ForecastTriage:
    hook_id: str
    authorship_bound: str
    timing_provenance: str
    forecast_type: str
    resolution_status: str
    accountable: bool
    review_note: str


@dataclass(frozen=True)
class RegistrationMetadata:
    authorship_bound: str
    timing_provenance: str
    forecast_type: str
    resolution_status: str
    accountable: bool
    review_note: str


def parse_entries(text: str) -> list[ForecastEntry]:
    rows: list[ForecastEntry] = []
    entry_text = text.partition(TRIAGE_HEADING)[0]
    for line in entry_text.splitlines():
        match = ENTRY_RE.match(line.strip())
        if match:
            rows.append(ForecastEntry(*match.groups()))
    return rows


def parse_triage(text: str) -> list[ForecastTriage]:
    rows: list[ForecastTriage] = []
    _, separator, triage_text = text.partition(TRIAGE_HEADING)
    if not separator:
        triage_text = text
    for line in triage_text.splitlines():
        match = TRIAGE_RE.match(line.strip())
        if not match:
            continue
        hook_id, bound, provenance, forecast_type, resolution, accountable, note = match.groups()
        rows.append(
            ForecastTriage(
                hook_id=hook_id,
                authorship_bound=bound,
                timing_provenance=provenance,
                forecast_type=forecast_type,
                resolution_status=resolution,
                accountable=accountable == "yes",
                review_note=note,
            )
        )
    return rows


def structural_failures(
    entries: list[ForecastEntry], triage_rows: list[ForecastTriage]
) -> list[str]:
    failures: list[str] = []
    entry_ids = [entry.hook_id for entry in entries]
    triage_ids = [row.hook_id for row in triage_rows]
    for hook_id, count in Counter(entry_ids).items():
        if count > 1:
            failures.append(f"duplicate forecast entry: {hook_id}")
    for hook_id, count in Counter(triage_ids).items():
        if count > 1:
            failures.append(f"duplicate triage row: {hook_id}")
    failures.extend(
        f"missing triage row: {hook_id}"
        for hook_id in sorted(set(entry_ids) - set(triage_ids))
    )
    failures.extend(
        f"triage row has no ledger entry: {hook_id}"
        for hook_id in sorted(set(triage_ids) - set(entry_ids))
    )

    entries_by_id = {entry.hook_id: entry for entry in entries}
    for row in triage_rows:
        if row.forecast_type not in FORECAST_TYPES:
            failures.append(f"invalid forecast type for {row.hook_id}: {row.forecast_type}")
        if row.resolution_status not in RESOLUTION_STATUSES:
            failures.append(
                f"invalid resolution status for {row.hook_id}: {row.resolution_status}"
            )
        if row.accountable and row.forecast_type != "ex_ante":
            failures.append(f"only ex_ante forecasts may be accountable: {row.hook_id}")
        if row.accountable and row.resolution_status.startswith("excluded_"):
            failures.append(f"accountable forecast cannot be excluded: {row.hook_id}")
        if (
            row.accountable
            and row.resolution_status in VERIFICATION_REQUIRED_STATUSES
            and not VERIFICATION_RE.search(row.review_note)
        ):
            failures.append(
                f"resolved accountable forecast missing verification packet: {row.hook_id}"
            )
        entry = entries_by_id.get(row.hook_id)
        if entry and entry.status != row.resolution_status:
            failures.append(
                f"forecast status mismatch for {row.hook_id}: "
                f"entry={entry.status} triage={row.resolution_status}"
            )
    return failures


def due_failures(
    entries: list[ForecastEntry], triage_rows: list[ForecastTriage], as_of: str
) -> list[str]:
    entries_by_id = {entry.hook_id: entry for entry in entries}
    failures: list[str] = []
    for row in triage_rows:
        entry = entries_by_id.get(row.hook_id)
        if (
            entry
            and row.accountable
            and entry.review_date <= as_of
            and row.resolution_status == "open"
        ):
            failures.append(f"overdue accountable forecast remains open: {row.hook_id}")
    return failures


def validate_registration(metadata: RegistrationMetadata) -> list[str]:
    probe = ForecastTriage(
        hook_id="NG-00000000-F00",
        authorship_bound=metadata.authorship_bound,
        timing_provenance=metadata.timing_provenance,
        forecast_type=metadata.forecast_type,
        resolution_status=metadata.resolution_status,
        accountable=metadata.accountable,
        review_note=metadata.review_note,
    )
    entry = ForecastEntry(
        probe.hook_id,
        "0000-00-00",
        "probe",
        "probe",
        "low",
        "0000-00-00",
        "probe",
        metadata.resolution_status,
    )
    failures = structural_failures([entry], [probe])
    if not metadata.authorship_bound.strip():
        failures.append("forecast authorship bound is required")
    if not metadata.timing_provenance.strip():
        failures.append("forecast timing provenance is required")
    if not metadata.review_note.strip():
        failures.append("forecast review note is required")
    return failures


def render_triage_row(hook_id: str, metadata: RegistrationMetadata) -> str:
    accountable = "yes" if metadata.accountable else "no"
    return (
        f"| `{hook_id}` | `{metadata.authorship_bound}` | `{metadata.timing_provenance}` | "
        f"`{metadata.forecast_type}` | `{metadata.resolution_status}` | "
        f"`{accountable}` | {metadata.review_note} |"
    )


def insert_rows(
    ledger_text: str, entry_rows: list[str], triage_rows: list[str]
) -> str:
    if not entry_rows and not triage_rows:
        return ledger_text
    entry_text, separator, triage_text = ledger_text.partition(TRIAGE_HEADING)
    if not separator:
        raise ValueError("forecast ledger missing Accountability Triage section")

    entry_lines = entry_text.rstrip().splitlines()
    if entry_rows:
        last_entry = max(
            (index for index, line in enumerate(entry_lines) if line.startswith("| `NG-")),
            default=-1,
        )
        if last_entry < 0:
            raise ValueError("forecast ledger Entries table has no data rows")
        entry_lines[last_entry + 1 : last_entry + 1] = entry_rows

    triage_lines = triage_text.rstrip().splitlines()
    if triage_rows:
        last_triage = max(
            (index for index, line in enumerate(triage_lines) if line.startswith("| `NG-")),
            default=-1,
        )
        if last_triage < 0:
            raise ValueError("forecast ledger triage table has no data rows")
        triage_lines[last_triage + 1 : last_triage + 1] = triage_rows

    return (
        "\n".join(entry_lines).rstrip()
        + "\n\n\n"
        + TRIAGE_HEADING
        + "\n"
        + "\n".join(triage_lines).lstrip("\n")
        + "\n"
    )


def align_entry_statuses(text: str) -> str:
    statuses = {row.hook_id: row.resolution_status for row in parse_triage(text)}
    lines: list[str] = []
    in_entries = True
    for line in text.splitlines():
        if line == TRIAGE_HEADING:
            in_entries = False
        match = ENTRY_RE.match(line.strip()) if in_entries else None
        if match and match.group(1) in statuses:
            cells = line.split("|")
            cells[-2] = f" `{statuses[match.group(1)]}` "
            line = "|".join(cells)
        lines.append(line)
    return "\n".join(lines) + ("\n" if text.endswith(("\n", "\r\n")) else "")
