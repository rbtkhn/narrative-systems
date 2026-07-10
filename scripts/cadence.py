from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable


REPO_ROOT = Path(__file__).resolve().parent.parent
HANDOFF_PATH = (
    REPO_ROOT / "narrative-geopolitics" / "work" / "cadence" / "last-dream.json"
)
DAILY_ROOT = REPO_ROOT / "narrative-geopolitics" / "work" / "daily"
OUTCOMES = ("improved", "no_change", "regressed", "inconclusive")
NEXT_MODES = {
    "improved": "confirm_then_consolidate",
    "no_change": "retire_or_narrow",
    "regressed": "revert_and_diagnose",
    "inconclusive": "run_discriminating_test",
}


def run_git(*args: str) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=REPO_ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.rstrip()


def git_head() -> str:
    return run_git("rev-parse", "HEAD")


def dirty_paths() -> list[str]:
    paths: list[str] = []
    for line in run_git("status", "--short").splitlines():
        value = line[3:].strip()
        paths.append(value.split(" -> ", 1)[-1])
    return sorted(paths)


def worktree_fingerprint() -> str:
    digest = hashlib.sha256()
    for command in (
        ["git", "status", "--porcelain=v1", "-z"],
        ["git", "diff", "--binary", "--no-ext-diff"],
    ):
        result = subprocess.run(
            command,
            cwd=REPO_ROOT,
            check=True,
            capture_output=True,
        )
        digest.update(result.stdout)
    untracked = subprocess.run(
        ["git", "ls-files", "--others", "--exclude-standard", "-z"],
        cwd=REPO_ROOT,
        check=True,
        capture_output=True,
    ).stdout
    for raw_path in sorted(value for value in untracked.split(b"\0") if value):
        digest.update(raw_path)
        path = REPO_ROOT / raw_path.decode("utf-8", errors="surrogateescape")
        if path.is_file():
            digest.update(path.read_bytes())
    return digest.hexdigest()


def latest_daily_run() -> str | None:
    if not DAILY_ROOT.exists():
        return None
    dates = sorted(path.name for path in DAILY_ROOT.iterdir() if path.is_dir())
    return dates[-1] if dates else None


def load_handoff(path: Path = HANDOFF_PATH) -> dict | None:
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def verification_passed(verification: dict) -> bool:
    required = {"integrity", "tests"}
    return required <= set(verification) and all(
        verification[name].get("passed") is True for name in required
    )


def normalize_artifact_refs(values: list[str]) -> list[str]:
    normalized: list[str] = []
    root = REPO_ROOT.resolve()
    for value in values:
        ref = value.strip().replace("\\", "/")
        path_text = ref.split("#", 1)[0]
        candidate = Path(path_text)
        if not ref or candidate.is_absolute() or ".." in candidate.parts:
            raise ValueError(f"artifact reference must be repo-relative: {value}")
        resolved = (REPO_ROOT / candidate).resolve()
        try:
            resolved.relative_to(root)
        except ValueError as error:
            raise ValueError(f"artifact reference escapes repository: {value}") from error
        if not resolved.exists():
            raise ValueError(f"artifact reference does not exist: {value}")
        if ref not in normalized:
            normalized.append(ref)
    if not normalized:
        raise ValueError("at least one artifact reference is required")
    return normalized


def coffee_state(path: Path = HANDOFF_PATH) -> dict:
    current_head = git_head()
    current_dirty = dirty_paths()
    current_fingerprint = worktree_fingerprint()
    handoff = load_handoff(path)
    state = {
        "git_head": current_head,
        "dirty_paths": current_dirty,
        "worktree_fingerprint": current_fingerprint,
        "latest_daily_run": latest_daily_run(),
        "handoff": handoff,
        "handoff_status": "missing",
        "next_mode": "bootstrap_bounded_experiment",
    }
    if handoff is None:
        return state

    same_head = handoff.get("git_head") == current_head
    if "worktree_fingerprint" in handoff:
        same_dirty = handoff["worktree_fingerprint"] == current_fingerprint
    else:
        same_dirty = handoff.get("dirty_paths") == current_dirty
    verified = verification_passed(handoff.get("verification", {}))
    if not verified:
        status = "verification_failed"
        mode = "repair_before_inheriting"
    elif not (same_head and same_dirty):
        status = "stale"
        mode = "reconcile_state_before_inheriting"
    else:
        status = "current"
        outcome = handoff.get("learning", {}).get("outcome", "inconclusive")
        mode = NEXT_MODES.get(outcome, "run_discriminating_test")
    state["handoff_status"] = status
    state["next_mode"] = mode
    return state


def coffee_view(state: dict) -> dict:
    handoff = state.get("handoff")
    return {
        "git_head": state["git_head"],
        "dirty_path_count": len(state["dirty_paths"]),
        "latest_daily_run": state["latest_daily_run"],
        "handoff_status": state["handoff_status"],
        "next_mode": state["next_mode"],
        "learning": handoff.get("learning") if handoff else None,
        "verification_passed": (
            verification_passed(handoff.get("verification", {})) if handoff else None
        ),
    }


def run_verification() -> dict:
    commands = {
        "integrity": [sys.executable, "scripts/validate_repository.py"],
        "tests": [
            sys.executable,
            "-m",
            "pytest",
            "-q",
            "--basetemp=.pytest_cache/cadence-dream",
        ],
    }
    results: dict[str, dict] = {}
    for name, command in commands.items():
        result = subprocess.run(
            command,
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
        )
        output = (result.stdout + result.stderr).strip()
        results[name] = {
            "passed": result.returncode == 0,
            "returncode": result.returncode,
            "output_tail": output[-2000:],
        }
    return results


def write_dream(
    *,
    experiment: str,
    outcome: str,
    lesson: str,
    improvement: str,
    evidence_summary: str,
    artifact_refs: list[str],
    tomorrow_inherits: str,
    path: Path = HANDOFF_PATH,
    verify: Callable[[], dict] = run_verification,
) -> dict:
    evidence_summary = evidence_summary.strip()
    if not evidence_summary:
        raise ValueError("evidence summary must not be empty")
    artifact_refs = normalize_artifact_refs(artifact_refs)
    verification = verify()
    payload = {
        "schema_version": 2,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "git_head": git_head(),
        "dirty_paths": dirty_paths(),
        "worktree_fingerprint": worktree_fingerprint(),
        "verification": verification,
        "learning": {
            "experiment": experiment,
            "outcome": outcome,
            "lesson": lesson,
            "method_change_candidate": improvement,
            "evidence_summary": evidence_summary,
            "artifact_refs": artifact_refs,
            "tomorrow_inherits": tomorrow_inherits,
        },
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(".tmp")
    temporary.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)
    return payload


def print_coffee(state: dict) -> None:
    print(f"handoff_status={state['handoff_status']}")
    print(f"next_mode={state['next_mode']}")
    print(f"latest_daily_run={state['latest_daily_run'] or 'none'}")
    handoff = state.get("handoff")
    if handoff:
        learning = handoff.get("learning", {})
        print(f"experiment={learning.get('experiment', '')}")
        print(f"outcome={learning.get('outcome', '')}")
        print(f"lesson={learning.get('lesson', '')}")
        print(f"method_change_candidate={learning.get('method_change_candidate', '')}")
        print(f"evidence_summary={learning.get('evidence_summary', '')}")
        print(f"artifact_refs={','.join(learning.get('artifact_refs', []))}")
        print(f"tomorrow_inherits={learning.get('tomorrow_inherits', '')}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Local coffee/dream learning cadence.")
    subparsers = parser.add_subparsers(dest="command", required=True)
    coffee = subparsers.add_parser("coffee", help="Read the last learning handoff.")
    coffee.add_argument("--json", action="store_true")
    dream = subparsers.add_parser("dream", help="Verify and persist one learning handoff.")
    dream.add_argument("--experiment", required=True)
    dream.add_argument("--outcome", choices=OUTCOMES, required=True)
    dream.add_argument("--lesson", required=True)
    dream.add_argument("--improvement", required=True)
    dream.add_argument("--evidence-summary", required=True)
    dream.add_argument("--artifact-ref", action="append", required=True)
    dream.add_argument("--tomorrow-inherits", required=True)
    dream.add_argument("--json", action="store_true")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    if args.command == "coffee":
        state = coffee_state()
        if args.json:
            print(json.dumps(coffee_view(state), indent=2))
        else:
            print_coffee(state)
        return

    payload = write_dream(
        experiment=args.experiment,
        outcome=args.outcome,
        lesson=args.lesson,
        improvement=args.improvement,
        evidence_summary=args.evidence_summary,
        artifact_refs=args.artifact_ref,
        tomorrow_inherits=args.tomorrow_inherits,
    )
    if args.json:
        print(json.dumps(payload, indent=2))
    else:
        passed = verification_passed(payload["verification"])
        print(f"dream_written={HANDOFF_PATH.relative_to(REPO_ROOT).as_posix()}")
        print(f"verification_passed={str(passed).lower()}")
        print(f"next_mode={NEXT_MODES[args.outcome] if passed else 'repair_before_inheriting'}")
    if not verification_passed(payload["verification"]):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
