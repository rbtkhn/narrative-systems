from __future__ import annotations

import argparse
import json
from collections import Counter
from datetime import date, timedelta
from pathlib import Path
from typing import Any

import bootstrap_daily_run as bootstrap


REPO_ROOT = Path(__file__).resolve().parent.parent
NG_ROOT = REPO_ROOT / "narrative-geopolitics"
MANIFEST_PATH = NG_ROOT / "archive" / "source-manifest.json"
DAILY_ROOT = NG_ROOT / "work" / "daily"


VOICE_ROLES = {
    "pape": ("Mechanism", "Escalation mechanism and leverage logic."),
    "marandi": ("Regional red line", "Iran-facing settlement and legitimacy test."),
    "davis": ("Practical room", "Military feasibility and coercive limits."),
    "mercouris": ("Sequence", "Negotiation sequence and diplomatic room."),
    "mearsheimer": ("Structure", "Hard incentives and off-ramp scarcity."),
    "diesen": ("Order transition", "System-level legitimacy and order shift."),
    "johnson": ("Counter-coercion", "Retaliatory logic and bargaining pressure."),
    "crooke": ("Political texture", "Elite bargaining texture and systemic drift."),
    "parsi": ("Negotiation lane", "U.S.-Iran bargaining and sabotage risk."),
    "sachs": ("Grand bargain", "Systemic settlement logic and external restraint."),
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build first-pass retrospective daily runs from archive-backed days.")
    parser.add_argument("--month", required=True, help="Month selector in YYYY-MM format.")
    parser.add_argument("--status", default="retrospective-backfill", help="Status to write into authored daily files.")
    parser.add_argument("--force", action="store_true", help="Overwrite already-authored files.")
    return parser.parse_args()


def load_manifest() -> dict[str, Any]:
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8-sig"))


def iter_month(month: str) -> list[str]:
    start = date.fromisoformat(f"{month}-01")
    if start.month == 12:
        end = date(start.year + 1, 1, 1) - timedelta(days=1)
    else:
        end = date(start.year, start.month + 1, 1) - timedelta(days=1)
    current = start
    dates: list[str] = []
    while current <= end:
        dates.append(current.isoformat())
        current += timedelta(days=1)
    return dates


def rows_for_date(manifest: dict[str, Any], run_date: str) -> list[dict[str, Any]]:
    rows = [row for row in manifest.get("sources", []) if row.get("date") == run_date]
    rows.sort(key=lambda row: row.get("local_path", ""))
    return rows


def infer_theme(rows: list[dict[str, Any]]) -> tuple[str, str, str]:
    titles = " ".join(row.get("title", "") for row in rows).lower()
    iran_score = sum(titles.count(term) for term in ("iran", "hormuz", "israel", "ceasefire", "mou", "strait", "lebanon"))
    russia_score = sum(titles.count(term) for term in ("russia", "putin", "kiev", "ukraine", "odessa", "sumy", "starmer"))

    if iran_score >= russia_score:
        if "ceasefire" in titles or "deal" in titles or "mou" in titles or "talks" in titles:
            return (
                "Iran/Hormuz bargaining fragility",
                "Whether coercive calm can hold while Iran retains Hormuz-linked leverage and wider settlement demands.",
                "The archive packet suggests the day centered on bargaining fragility rather than stable settlement.",
            )
        if "attack" in titles or "strike" in titles or "war" in titles:
            return (
                "Iran/Hormuz escalation pressure",
                "Whether Iran, Israel, and the United States are moving toward a wider escalation cycle around transit, regional deterrence, and settlement terms.",
                "The strongest read from the packet is that military signaling and bargaining pressure were moving together.",
            )
        return (
            "Hormuz leverage and regional bargaining",
            "Who controls the risk environment around Gulf transit and what price is being attached to restoring calm.",
            "The day packet is best read through leverage over transit and the political terms attached to de-escalation.",
        )

    if "talks" in titles or "deal" in titles:
        return (
            "Russia/Ukraine negotiation failure",
            "Whether negotiations are real de-escalation or only a bridge to further battlefield pressure.",
            "The day archive leans toward diplomacy failing to outrun battlefield logic.",
        )
    return (
        "Russia/Ukraine battlefield and negotiation pressure",
        "Whether battlefield developments are closing the room for negotiation faster than outside actors can reopen it.",
        "The packet reads as a battlefield-sequencing day rather than a stable diplomatic turn.",
    )


def top_voices(rows: list[dict[str, Any]]) -> list[str]:
    counts: Counter[str] = Counter()
    for row in rows:
        for slug in row.get("voice_slugs", []):
            counts[slug] += 1
    return [slug for slug, _ in counts.most_common(3)]


def top_hosts(rows: list[dict[str, Any]]) -> list[str]:
    counts: Counter[str] = Counter()
    for row in rows:
        host = row.get("host_slug")
        if host:
            counts[host] += 1
    return [slug for slug, _ in counts.most_common(2)]


def build_synthesis(run_date: str, status: str, rows: list[dict[str, Any]]) -> str:
    crisis_object, short_object, lead_note = infer_theme(rows)
    voices = top_voices(rows)
    hosts = top_hosts(rows)
    primary = voices[:2] if voices else ["pending"]
    role_rows = []
    for voice in primary:
        role, note = VOICE_ROLES.get(voice, ("Pressure voice", "Useful context inside the day packet."))
        role_rows.append(f"| {voice.title()} | {role} | {note} | Host conditioning or incomplete source mix may overstate confidence. |")
    host_text = ", ".join(hosts) if hosts else "mixed archive routing"
    pressure_voice = voices[2] if len(voices) > 2 else primary[-1]

    return f"""# Synthesis

Date: `{run_date}`

Status: `{status}`

## Lead Judgment

{lead_note} Across `{len(rows)}` archive-backed sources, the day is best understood as a test of **{crisis_object}**. The safest bounded judgment is that the archive packet points to mounting pressure rather than a settled outcome, with `{host_text}` supplying the strongest channel-conditioned stress on the day’s claims.

## Crisis Object

{short_object}

## Primary Voices

| Voice | Role In This Run | What It Adds | Main Risk |
| --- | --- | --- | --- |
{chr(10).join(role_rows)}

## Orthogonal Pressure Test

| Axis | Voice | Pressure Question | Effect On Judgment |
| --- | --- | --- | --- |
| Mechanism | {primary[0].title()} | What mechanism appears to be doing the real work in this day batch? | Pushes the judgment toward observable leverage rather than declaratory politics. |
| Sequence | {pressure_voice.title()} | Does the sequence widen or narrow room for de-escalation? | Keeps the run focused on whether the day advances a pause or another round. |
| Host conditioning | {host_text} | Which host formats are amplifying urgency, sabotage risk, or overconfidence? | Prevents the run from inheriting channel rhetoric without adjustment. |

## Actor Map

| Actor | Interest | Constraint | Narrative / Legitimacy Claim |
| --- | --- | --- | --- |
| United States | Contain immediate escalation costs while preserving bargaining leverage. | Military pressure and political signaling do not automatically create a stable off-ramp. | The U.S. can still shape the settlement terms. |
| Regional adversary bloc | Preserve leverage, avoid concession under pressure, and redefine acceptable terms. | Too much escalation can trigger wider retaliation or economic blowback. | Coercion proves why a wider settlement is required. |
| Secondary regional actors | Protect infrastructure, shipping, and political room. | They absorb the cost of instability faster than they control the strategy. | Stability requires a different security arrangement. |

## Draft Judgment

The day packet does not support a “crisis resolved” reading. It supports a narrower claim: the underlying bargaining structure remained unstable, and the most important movement was in leverage, sequencing, and signaling rather than in any final political settlement.

The most useful way to read this day is through source mix. Repeated appearances by `{", ".join(primary)}` suggest the archive was leaning on a familiar pressure lattice: mechanism, regional legitimacy, practical room, and bargaining sequence. That gives enough structure for a retrospective run, but not enough to erase uncertainty about host framing or real-world implementation.

## Uncertainty

This is a retrospective archive run, not a same-day live verification pass. The main uncertainty is whether host-conditioned urgency overstated how close the system was to immediate resolution or immediate collapse. Any later public use should re-check traffic, strike, negotiation, and market facts before quoting the judgment.

## Forecast Candidates

| Hook ID | Claim | Probability Band | Review Date |
| --- | --- | --- | --- |
| `NG-{run_date.replace('-', '')}-F01` | Within 30 days of `{run_date}`, the contested leverage structure visible in this day packet will still be visible through renewed bargaining stress, implementation disputes, or another coercive signaling cycle. | `likely` | `{(date.fromisoformat(run_date) + timedelta(days=30)).isoformat()}` |
"""


def build_forecast(run_date: str, status: str, rows: list[dict[str, Any]]) -> str:
    _, short_object, _ = infer_theme(rows)
    review_date = (date.fromisoformat(run_date) + timedelta(days=30)).isoformat()
    text = bootstrap.build_from_template("forecast.md", run_date, status)
    start = text.index("## Hooks\n")
    end = text.index("## Ledger Entries\n")
    hooks_block = f"""## Hooks

| Hook ID | Claim | Probability Band | Review Date | Strengthening Evidence | Weakening Evidence |
| --- | --- | --- | --- | --- | --- |
| `NG-{run_date.replace('-', '')}-F01` | Within 30 days, the leverage structure around {short_object.lower()} will remain visible through renewed bargaining stress, implementation disputes, or another coercive test. | `likely` | `{review_date}` | Continued disputes over access, transit, strikes, sanctions, or sequencing. | Sustained normalization with reduced pressure and no fresh coercive test. |

"""
    return text[:start] + hooks_block + text[end:]


def build_daily_brief(run_date: str, status: str, rows: list[dict[str, Any]]) -> str:
    crisis_object, short_object, lead_note = infer_theme(rows)
    voices = top_voices(rows)
    voice_text = ", ".join(voice.title() for voice in voices[:3]) if voices else "the day archive"
    review_date = (date.fromisoformat(run_date) + timedelta(days=30)).isoformat()
    return f"""# Narrative Geopolitics Daily Brief: {run_date}

Status: `not-promoted`

## Lead Judgment

{lead_note} The archive-backed June run suggests the live issue was **{crisis_object}**, not a durable settlement.

## Source Grounding

This retrospective brief is grounded in `{len(rows)}` archive sources already landed for the date, with the strongest pressure coming through {voice_text}.

## Crisis Object

{short_object}

## Actor And Narrative Map

The archive packet points to a familiar tension: one side trying to preserve leverage through pressure and sequencing, the other trying to regain a stable baseline without conceding the wider political argument.

## Voice Pressure Test

The run was most shaped by {voice_text}. Their value is not that they agree, but that together they pressure-test mechanism, feasibility, legitimacy, and sequencing.

## What To Watch

Watch whether later days show normalization in practice, or only new attempts to stabilize the narrative while leverage remains politically active.

## Forecast / Review Hooks

`NG-{run_date.replace('-', '')}-F01`: review on `{review_date}` whether the leverage structure visible on `{run_date}` actually eased, or merely changed form.
"""


def write_if_allowed(path: Path, content: str, force: bool) -> None:
    if path.exists() and not force:
        existing = path.read_text(encoding="utf-8")
        if "State the day's bounded geopolitical judgment" not in existing and "Await archive intake" not in existing and "State the bounded internal judgment" not in existing:
            return
    path.write_text(content.rstrip() + "\n", encoding="utf-8", newline="\n")


def main() -> None:
    args = parse_args()
    manifest = load_manifest()
    for run_date in iter_month(args.month):
        rows = rows_for_date(manifest, run_date)
        if not rows:
            continue
        run_dir = DAILY_ROOT / run_date
        run_dir.mkdir(parents=True, exist_ok=True)
        if run_date == "2026-06-30" and not args.force:
            continue
        write_if_allowed(run_dir / "synthesis.md", build_synthesis(run_date, args.status, rows), args.force)
        write_if_allowed(run_dir / "forecast.md", build_forecast(run_date, args.status, rows), args.force)
        write_if_allowed(run_dir / "daily-brief.md", build_daily_brief(run_date, args.status, rows), args.force)
        print(f"authored {run_date}")


if __name__ == "__main__":
    main()
