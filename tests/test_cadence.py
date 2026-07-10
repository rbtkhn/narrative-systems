from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPT_PATH = REPO_ROOT / "scripts" / "cadence.py"


def load_module():
    spec = importlib.util.spec_from_file_location("cadence_tests", SCRIPT_PATH)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


cadence = load_module()


def verified(value: bool = True) -> dict:
    return {
        "integrity": {"passed": value, "returncode": 0 if value else 1},
        "tests": {"passed": value, "returncode": 0 if value else 1},
    }


def patch_repo_state(monkeypatch, *, head: str = "abc", dirty: list[str] | None = None):
    monkeypatch.setattr(cadence, "git_head", lambda: head)
    monkeypatch.setattr(cadence, "dirty_paths", lambda: dirty or [])
    monkeypatch.setattr(cadence, "worktree_fingerprint", lambda: "fingerprint")
    monkeypatch.setattr(cadence, "latest_daily_run", lambda: "2026-07-09")


def write_handoff(tmp_path: Path, *, outcome: str, verification: dict) -> Path:
    path = tmp_path / "last-dream.json"
    payload = {
        "schema_version": 2,
        "timestamp": "2026-07-10T00:00:00+00:00",
        "git_head": "abc",
        "dirty_paths": [],
        "worktree_fingerprint": "fingerprint",
        "verification": verification,
        "learning": {
            "experiment": "compare two retrieval methods",
            "outcome": outcome,
            "lesson": "bounded retrieval reduced citation repair",
            "method_change_candidate": "start with bounded retrieval",
            "evidence_summary": "citation repairs fell from 8 to 3",
            "artifact_refs": ["tests/test_cadence.py"],
            "tomorrow_inherits": "confirm the gain on a thinner crisis",
        },
    }
    path.write_text(json.dumps(payload), encoding="utf-8")
    return path


def test_cold_start_bootstraps_a_bounded_experiment(monkeypatch, tmp_path: Path) -> None:
    patch_repo_state(monkeypatch)
    state = cadence.coffee_state(tmp_path / "missing.json")
    assert state["handoff_status"] == "missing"
    assert state["next_mode"] == "bootstrap_bounded_experiment"


def test_measured_improvement_is_confirmed_before_consolidation(
    monkeypatch, tmp_path: Path
) -> None:
    patch_repo_state(monkeypatch)
    path = write_handoff(tmp_path, outcome="improved", verification=verified())
    state = cadence.coffee_state(path)
    assert state["handoff_status"] == "current"
    assert state["next_mode"] == "confirm_then_consolidate"
    assert state["handoff"]["learning"]["lesson"].startswith("bounded retrieval")
    assert state["handoff"]["learning"]["evidence_summary"] == (
        "citation repairs fell from 8 to 3"
    )


def test_inconclusive_result_generates_a_discriminating_test(
    monkeypatch, tmp_path: Path
) -> None:
    patch_repo_state(monkeypatch)
    path = write_handoff(tmp_path, outcome="inconclusive", verification=verified())
    state = cadence.coffee_state(path)
    assert state["next_mode"] == "run_discriminating_test"


def test_regression_generates_revert_and_diagnose(monkeypatch, tmp_path: Path) -> None:
    patch_repo_state(monkeypatch)
    path = write_handoff(tmp_path, outcome="regressed", verification=verified())
    state = cadence.coffee_state(path)
    assert state["next_mode"] == "revert_and_diagnose"


def test_failed_verification_blocks_learning(monkeypatch, tmp_path: Path) -> None:
    patch_repo_state(monkeypatch)
    path = write_handoff(tmp_path, outcome="improved", verification=verified(False))
    state = cadence.coffee_state(path)
    assert state["handoff_status"] == "verification_failed"
    assert state["next_mode"] == "repair_before_inheriting"


def test_missing_verification_blocks_learning(monkeypatch, tmp_path: Path) -> None:
    patch_repo_state(monkeypatch)
    path = write_handoff(tmp_path, outcome="improved", verification={})
    state = cadence.coffee_state(path)
    assert state["handoff_status"] == "verification_failed"


def test_changed_repository_state_requires_reconciliation(
    monkeypatch, tmp_path: Path
) -> None:
    patch_repo_state(monkeypatch, head="new-head")
    path = write_handoff(tmp_path, outcome="improved", verification=verified())
    state = cadence.coffee_state(path)
    assert state["handoff_status"] == "stale"
    assert state["next_mode"] == "reconcile_state_before_inheriting"


def test_changed_content_on_same_paths_requires_reconciliation(
    monkeypatch, tmp_path: Path
) -> None:
    patch_repo_state(monkeypatch)
    path = write_handoff(tmp_path, outcome="improved", verification=verified())
    monkeypatch.setattr(cadence, "worktree_fingerprint", lambda: "changed-content")
    state = cadence.coffee_state(path)
    assert state["handoff_status"] == "stale"


def test_dream_persists_the_learning_contract(monkeypatch, tmp_path: Path) -> None:
    patch_repo_state(monkeypatch)
    path = tmp_path / "cadence" / "last-dream.json"
    payload = cadence.write_dream(
        experiment="voice continuity comparison",
        outcome="no_change",
        lesson="voice work changed attribution but not judgment",
        improvement="reserve voice work for disputed attribution",
        evidence_summary="both notes reached the same central judgment",
        artifact_refs=["tests/test_cadence.py"],
        tomorrow_inherits="test the narrower rule on one crisis",
        path=path,
        verify=lambda: verified(),
    )
    assert path.exists()
    assert payload["schema_version"] == 2
    assert payload["learning"]["outcome"] == "no_change"
    assert payload["learning"]["artifact_refs"] == ["tests/test_cadence.py"]
    assert json.loads(path.read_text(encoding="utf-8")) == payload


def test_reconstruction_keeps_decisive_scope_and_artifacts(
    monkeypatch, tmp_path: Path
) -> None:
    patch_repo_state(monkeypatch)
    path = tmp_path / "last-dream.json"
    payload = cadence.write_dream(
        experiment="audit Ukraine primary-record coverage",
        outcome="no_change",
        lesson="commentary density cannot substitute for party-owned terms",
        improvement="activate only after primary-record intake",
        evidence_summary=(
            "1,007 archive sources scanned; 113 Ukraine candidates; "
            "0 official-domain records; qualifying coverage remains 0/3 actors"
        ),
        artifact_refs=[
            "narrative-geopolitics/work/experiments/2026-07-value-test/ukraine-official-terms-baseline.md",
            "narrative-geopolitics/archive/sources/2026-06-05/source-daniel-davis-zelensky-s-letter-to-putin-lt-col-daniel-davis-2026-06-05.md",
        ],
        tomorrow_inherits="wait for a party-owned terms record",
        path=path,
        verify=lambda: verified(),
    )
    view = cadence.coffee_view(cadence.coffee_state(path))
    assert view["learning"]["evidence_summary"] == payload["learning"][
        "evidence_summary"
    ]
    assert len(view["learning"]["artifact_refs"]) == 2


def test_dream_rejects_missing_or_escaping_artifact_references(
    monkeypatch, tmp_path: Path
) -> None:
    patch_repo_state(monkeypatch)
    common = {
        "experiment": "unsafe reference",
        "outcome": "inconclusive",
        "lesson": "none",
        "improvement": "none",
        "evidence_summary": "no evidence",
        "tomorrow_inherits": "repair",
        "path": tmp_path / "last-dream.json",
        "verify": lambda: verified(),
    }
    for artifact_ref in ("missing.md", "../outside.md"):
        try:
            cadence.write_dream(artifact_refs=[artifact_ref], **common)
        except ValueError as error:
            assert "artifact reference" in str(error)
        else:
            raise AssertionError("unsafe artifact reference was accepted")
