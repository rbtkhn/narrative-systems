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
CORE_VOICES = ["pape", "mercouris", "mearsheimer", "marandi", "diesen", "davis"]
AXES = {
    "pape": ("mechanism / falsifier", "What coercive mechanism is unfolding, and what would falsify it?"),
    "mercouris": ("room / sequence / legitimacy", "What room do actors have, and how is the institutional story moving?"),
    "mearsheimer": ("structure / security dilemma", "What structural incentives make this crisis likely?"),
    "marandi": ("regional red line / legitimacy", "How do regional actors define acceptable settlement?"),
    "diesen": ("multipolar order / host-convener", "How does the crisis reveal order transition?"),
    "davis": ("practical room / military feasibility", "What can force still do, and what can coercion no longer recover?"),
}
DIMENSIONS = ("native_axis_clarity", "claim_family_distinctness", "mechanism_diversity", "time_horizon_coverage", "actor_perspective_coverage", "evidence_modality_diversity", "falsifiability", "revision_transparency", "blind_spot_complementarity", "crisis_portability", "decision_usefulness", "source_sufficiency")
PAIR_DIMENSIONS = ("axis_separation", "mechanism_separation", "evidence_independence", "host_independence", "actor_perspective_separation", "time_horizon_separation", "conclusion_overlap", "proposition_redundancy", "marginal_correction_value", "synthesis_marginal_value", "blind_spot_complementarity", "collapse_risk")


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
    p.add_argument("command", choices=("states", "revisions", "forecasts", "hosts", "convergence", "select-voices", "orthogonality", "validate"))
    p.add_argument("--voice")
    p.add_argument("--since")
    p.add_argument("--date")
    p.add_argument("--start-date")
    p.add_argument("--end-date")
    p.add_argument("--crisis-object", default="")
    p.add_argument("--format", choices=("md", "json"), default="md")
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--pair")
    p.add_argument("--output")
    return p.parse_args()


def emit(payload, title):
    if isinstance(payload, dict) and payload.get("failures") is not None:
        pass
    rendered = json.dumps(payload, indent=2, ensure_ascii=False) if ARGS.format == "json" else markdown_payload(payload, title)
    if ARGS.output and not ARGS.dry_run:
        target = Path(ARGS.output)
        if not target.is_absolute(): target = ROOT / target
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(rendered, encoding="utf-8")
    else:
        print(rendered)


def markdown_payload(payload, title):
    result = [f"# {title}", ""]
    if isinstance(payload, list):
        for item in payload:
            result.append("- " + " | ".join(f"{k}={v}" for k, v in item.items()))
    else:
        for key, value in payload.items():
            if isinstance(value, list):
                result.append(f"## {key.replace('_', ' ').title()}")
                result.extend(["", *["- " + " | ".join(f"{k}={v}" for k, v in item.items()) if isinstance(item, dict) else f"- {item}" for item in value]])
            else:
                result.append(f"- **{key}:** {value}")
    return "\n".join(result) + "\n"


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


def score_voice(voice, own_states, all_state_rows):
    profile = VOICES / voice / "README.md"
    has_profile = profile.exists()
    has_ledger = bool(own_states)
    role, question = AXES.get(voice, ("unmapped", "No canonical axis assigned."))
    coverage = min(3, len(own_states)) if has_ledger else 0
    basis = [{"state_ids": [s["state_id"] for s in own_states], "profile_reference": role, "note": question}]
    scores = {
        "native_axis_clarity": 3 if role != "unmapped" and has_profile else 0,
        "claim_family_distinctness": 2 if has_ledger else 0,
        "mechanism_diversity": 2 if has_ledger else 0,
        "time_horizon_coverage": 2 if has_ledger else 0,
        "actor_perspective_coverage": 2 if has_ledger else 0,
        "evidence_modality_diversity": 2 if has_ledger else 0,
        "falsifiability": 2 if any(s["forecast_hook"] not in {"", "none", "—"} for s in own_states) else (1 if has_ledger else 0),
        "revision_transparency": 2 if has_ledger else 0,
        "blind_spot_complementarity": 2 if role != "unmapped" else 0,
        "crisis_portability": 1 if has_ledger else 0,
        "decision_usefulness": 2 if role != "unmapped" else 0,
        "source_sufficiency": coverage,
    }
    confidence = "supported" if has_ledger else "insufficient-evidence"
    return {"voice": voice, "axis": role, "scores": scores, "basis": basis, "confidence": confidence, "state_count": len(own_states)}


def pair_report(left, right, voice_reports, states):
    lrole, _ = AXES.get(left, ("unmapped", "")); rrole, _ = AXES.get(right, ("unmapped", ""))
    ls = [s for s in states if s["voice"] == left]; rs = [s for s in states if s["voice"] == right]
    lt = set().union(*(tokens(s["proposition"]) for s in ls)) if ls else set(); rt = set().union(*(tokens(s["proposition"]) for s in rs)) if rs else set()
    overlap = len(lt & rt)
    shared_hosts = set()
    for row in manifest_rows():
        voices = set(row.get("voice_slugs", []));
        if {left, right}.issubset(voices): shared_hosts.add(row.get("host_slug") or "unhosted")
    distinct_axis = 3 if lrole != rrole and lrole != "unmapped" and rrole != "unmapped" else 0
    scores = {d: 2 for d in PAIR_DIMENSIONS}
    scores["axis_separation"] = distinct_axis
    scores["mechanism_separation"] = 3 if distinct_axis else 0
    scores["evidence_independence"] = 1 if shared_hosts else 3
    scores["host_independence"] = 1 if shared_hosts else 3
    scores["conclusion_overlap"] = min(3, overlap)
    scores["proposition_redundancy"] = min(3, overlap)
    scores["marginal_correction_value"] = 3 if distinct_axis else 1
    scores["synthesis_marginal_value"] = 2 if ls and rs else 0
    scores["collapse_risk"] = 3 if overlap >= 3 else (1 if distinct_axis else 2)
    if overlap >= 3 and scores["marginal_correction_value"] >= 2: classification = "high overlap, high correction value"
    elif overlap >= 3: classification = "high overlap, low correction value"
    elif distinct_axis: classification = "low overlap, high correction value"
    else: classification = "low overlap, low relevance"
    return {"voices": [left, right], "scores": scores, "classification": classification, "shared_terms": sorted(lt & rt), "shared_hosts": sorted(shared_hosts), "basis": [{"profile_reference": f"{lrole} vs {rrole}", "state_ids": [s["state_id"] for s in ls + rs], "note": "Automated candidate; human review required."}]}


def command_orthogonality(states):
    voices = CORE_VOICES
    if ARGS.voice: voices = [v for v in voices if v == ARGS.voice]
    if ARGS.pair:
        voices = [v for v in ARGS.pair.split(",") if v in CORE_VOICES]
    reports = [score_voice(v, [s for s in states if s["voice"] == v], states) for v in voices]
    pairs = [pair_report(a, b, reports, states) for i, a in enumerate(voices) for b in voices[i + 1:]]
    recommendations = []
    if ARGS.crisis_object:
        query = tokens(ARGS.crisis_object)
        ranked = sorted(((len(query & tokens(s["proposition"])), s["voice"]) for s in states if s["voice"] in voices), reverse=True)
        if ranked: recommendations.append({"primary": ranked[0][1], "pressure_test": next((v for v in voices if v != ranked[0][1]), None), "basis": "crisis-object term overlap; review against axis and evidence coverage"})
    payload = {"as_of": ARGS.date or date.today().isoformat(), "voices": reports, "pairs": pairs, "coverage": {"core_voices": voices, "ledger_coverage": sum(bool([s for s in states if s["voice"] == v]) for v in voices)}, "blind_spots": [], "recommendations": recommendations, "limitations": ["Automated overlap is candidate evidence, not semantic adjudication.", "Missing ledgers reduce confidence rather than proving low orthogonality.", "Scores describe analytical roles, not private beliefs."]}
    emit(payload, "Voice Orthogonality Audit")


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
    elif ARGS.command == "orthogonality": command_orthogonality(states)
    else: return command_validate(states)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
