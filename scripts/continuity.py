from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NG = ROOT / "narrative-geopolitics"
VOICES = NG / "voices"
MANIFEST = NG / "archive" / "source-manifest.json"
DAILY = NG / "work" / "daily"
STATES = {"new", "persistent", "revised", "abandoned", "unclear"}
EXPRESSION = {"explicit", "close-paraphrase", "inference", "unknown"}


def ledgers():
    for path in VOICES.glob("*/state-ledger.md"):
        yield path.parent.name, path


def rows(path: Path):
    text = path.read_text(encoding="utf-8")
    active = text.split("## Active Trajectory", 1)[-1].split("## Unclear", 1)[0]
    for line in active.splitlines():
        if not line.startswith("|") or "State ID" in line or set(line.replace("|", "").strip()) <= {"-", ":", " "}:
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) >= 10 and cells[0].startswith("`"):
            yield {"state_id": cells[0].strip("`"), "proposition": cells[1], "state": cells[2].strip("`"), "first_seen": cells[3].strip("`"), "last_seen": cells[4].strip("`"), "expression_type": cells[5].strip("`"), "source_ids": cells[6], "daily_blocks": cells[7], "forecast_hook": cells[8], "revision_note": cells[9]}


def all_states():
    out = []
    for voice, path in ledgers():
        for item in rows(path):
            item["voice"] = voice
            item["ledger"] = str(path.relative_to(ROOT)).replace("\\", "/")
            out.append(item)
    return out


def parse_args():
    p = argparse.ArgumentParser(description="Audit Narrative Geopolitics voice-state continuity.")
    p.add_argument("command", choices=("states", "revisions", "forecasts", "hosts", "convergence", "select-voices", "validate"))
    p.add_argument("--voice")
    p.add_argument("--since")
    p.add_argument("--date")
    p.add_argument("--start-date")
    p.add_argument("--end-date")
    p.add_argument("--crisis-object", default="")
    p.add_argument("--format", choices=("md", "json"), default="md")
    p.add_argument("--dry-run", action="store_true")
    return p.parse_args()


def emit(payload, title):
    if isinstance(payload, dict) and payload.get("failures") is not None:
        pass
    if ARGS.format == "json":
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        return
    print(f"# {title}\n")
    if isinstance(payload, list):
        for item in payload:
            print("- " + " | ".join(f"{k}={v}" for k, v in item.items()))
    else:
        for key, value in payload.items():
            print(f"- **{key}:** {value}")


def manifest_rows():
    if not MANIFEST.exists():
        return []
    return json.loads(MANIFEST.read_text(encoding="utf-8")).get("sources", [])


def command_states(states):
    selected = [s for s in states if not ARGS.voice or s["voice"] == ARGS.voice]
    if ARGS.date:
        selected = [s for s in selected if ARGS.date in s["daily_blocks"]]
    emit(selected, "Voice State Ledger")


def command_revisions(states):
    selected = [s for s in states if s["state"] in {"revised", "abandoned", "unclear"} and (not ARGS.voice or s["voice"] == ARGS.voice)]
    if ARGS.since:
        selected = [s for s in selected if s["last_seen"] >= ARGS.since]
    emit(selected, "Voice Revision Audit")


def command_forecasts(states):
    selected = [s for s in states if s["forecast_hook"] not in {"", "none", "—"} and (not ARGS.voice or s["voice"] == ARGS.voice)]
    emit(selected, "Forecasts Linked to Voice States")


def command_hosts(states):
    wanted = {s["voice"] for s in states if not ARGS.voice or s["voice"] == ARGS.voice}
    counts = Counter()
    for row in manifest_rows():
        voices = row.get("voice_slugs", [])
        if wanted.intersection(voices):
            counts[(next(iter(wanted.intersection(voices))), row.get("host_slug") or "unhosted")] += 1
    emit([{"voice": v, "host": h, "source_count": n} for (v, h), n in sorted(counts.items())], "Host Conditioning Inventory")


def tokens(value):
    return {x for x in re.findall(r"[a-z][a-z-]{3,}", value.lower()) if x not in {"that", "this", "with", "from", "without", "their", "which"}}


def command_convergence(states):
    selected = [s for s in states if s["state"] != "abandoned"]
    pairs = []
    for i, left in enumerate(selected):
        for right in selected[i + 1:]:
            if left["voice"] == right["voice"]:
                continue
            overlap = tokens(left["proposition"]) & tokens(right["proposition"])
            if len(overlap) >= 3:
                pairs.append({"left": left["state_id"], "right": right["state_id"], "voices": f"{left['voice']},{right['voice']}", "shared_terms": ",".join(sorted(overlap)), "classification": "candidate-convergence"})
    emit(pairs, "Cross-Voice Convergence Candidates")


def command_select(states):
    query = tokens(ARGS.crisis_object)
    scores = []
    for voice in sorted({s["voice"] for s in states}):
        own = [s for s in states if s["voice"] == voice]
        score = sum(len(query & tokens(s["proposition"])) for s in own)
        scores.append({"voice": voice, "relevance_score": score, "state_count": len(own), "selection_basis": "proposition-term overlap; review for orthogonality"})
    emit(sorted(scores, key=lambda x: (-x["relevance_score"], x["voice"])), "Evidence-Weighted Voice Selection")


def command_validate(states):
    failures = []
    ids = set()
    source_ids = set()
    for source_file in DAILY.glob("*/sources.md"):
        source_ids.update(re.findall(r"`(SRC-[0-9]+)`", source_file.read_text(encoding="utf-8")))
    for state in states:
        sid = state["state_id"]
        if sid in ids: failures.append(f"duplicate state id: {sid}")
        ids.add(sid)
        if state["state"] not in STATES: failures.append(f"invalid state {state['state']}: {sid}")
        if state["expression_type"] not in EXPRESSION: failures.append(f"invalid expression type {state['expression_type']}: {sid}")
        for source in re.findall(r"SRC-[0-9]+", state["source_ids"]):
            if source not in source_ids: failures.append(f"missing source {source}: {sid}")
    daily_text = "\n".join(p.read_text(encoding="utf-8") for p in DAILY.glob("*/synthesis.md"))
    for sid in re.findall(r"STATE-[A-Z0-9-]+", daily_text):
        if sid not in ids: failures.append(f"daily state has no ledger: {sid}")
    emit({"state_count": len(states), "ledger_count": len(list(ledgers())), "failures": failures, "status": "pass" if not failures else "fail"}, "Continuity Validation")
    return 0 if not failures else 1


def main():
    global ARGS
    ARGS = parse_args()
    states = all_states()
    if ARGS.command == "states": command_states(states)
    elif ARGS.command == "revisions": command_revisions(states)
    elif ARGS.command == "forecasts": command_forecasts(states)
    elif ARGS.command == "hosts": command_hosts(states)
    elif ARGS.command == "convergence": command_convergence(states)
    elif ARGS.command == "select-voices": command_select(states)
    else: return command_validate(states)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
