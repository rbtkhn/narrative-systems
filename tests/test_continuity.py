from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def run_continuity(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "tools/run_repo.py", "continuity", *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )


def test_continuity_validation_passes():
    result = run_continuity("validate", "--format", "json")
    assert result.returncode == 0, result.stdout + result.stderr
    assert json.loads(result.stdout)["failures"] == []


def test_state_query_is_provenance_bearing():
    result = run_continuity("states", "--voice", "mearsheimer", "--format", "json")
    assert result.returncode == 0
    payload = json.loads(result.stdout)
    assert payload[0]["state_id"] == "STATE-MEARSHEIMER-0001"
    assert payload[0]["source_ids"]
    assert payload[0]["daily_blocks"]


def test_host_inventory_is_read_only_and_filtered():
    result = run_continuity("hosts", "--voice", "mearsheimer", "--format", "json")
    assert result.returncode == 0
    payload = json.loads(result.stdout)
    assert payload
    assert all(item["voice"] == "mearsheimer" for item in payload)
