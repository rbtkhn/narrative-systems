from __future__ import annotations

import json
import contextlib
import io
import sys
from pathlib import Path

from scripts import continuity

ROOT = Path(__file__).resolve().parents[1]


def run_continuity(*args: str):
    buffer = io.StringIO()
    original = sys.argv
    sys.argv = ["continuity.py", *args]
    try:
        with contextlib.redirect_stdout(buffer):
            code = continuity.main()
    finally:
        sys.argv = original
    return code, buffer.getvalue()


def test_continuity_validation_passes():
    code, output = run_continuity("validate", "--format", "json")
    assert code == 0, output
    assert json.loads(output)["failures"] == []


def test_state_query_is_provenance_bearing():
    code, output = run_continuity("states", "--voice", "mearsheimer", "--format", "json")
    assert code == 0
    payload = json.loads(output)
    assert payload[0]["state_id"] == "STATE-MEARSHEIMER-0001"
    assert payload[0]["source_ids"]
    assert payload[0]["daily_blocks"]


def test_host_inventory_is_read_only_and_filtered():
    code, output = run_continuity("hosts", "--voice", "mearsheimer", "--format", "json")
    assert code == 0
    payload = json.loads(output)
    assert payload
    assert all(item["voice"] == "mearsheimer" for item in payload)


def test_orthogonality_defaults_to_six_voice_scope_and_json_shape():
    code, output = run_continuity("orthogonality", "--format", "json", "--dry-run")
    assert code == 0
    payload = json.loads(output)
    assert payload["coverage"]["core_voices"] == ["pape", "mercouris", "mearsheimer", "marandi", "diesen", "davis"]
    assert {item["voice"] for item in payload["voices"]} == set(payload["coverage"]["core_voices"])
    assert all(0 <= score <= 3 for item in payload["voices"] for score in item["scores"].values())


def test_orthogonality_dry_run_does_not_write(tmp_path):
    target = tmp_path / "orthogonality.md"
    code, _ = run_continuity("orthogonality", "--output", str(target), "--dry-run")
    assert code == 0
    assert not target.exists()
