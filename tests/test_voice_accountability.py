from __future__ import annotations

import copy
import importlib.util
import json
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


voice_accountability = load_module(
    "voice_accountability_tests", REPO_ROOT / "scripts" / "voice_accountability.py"
)


def write_tracker(
    tmp_path: Path,
    ledger: dict,
    *,
    markdown_ids: list[str] | None = None,
    near_misses: str = "# Near-Misses\n\n| Near-Miss ID |\n| --- |\n| `NM-20260716-01` |\n",
) -> tuple[Path, Path, Path]:
    markdown_ids = markdown_ids if markdown_ids is not None else [
        entry["id"] for entry in ledger["entries"]
    ]
    md = tmp_path / "voice-revision-ledger.md"
    rows = "\n".join(
        f"| `{revision_id}` | `2026-07-16` | `mearsheimer` |" for revision_id in markdown_ids
    )
    md.write_text(
        "# Voice Revision Ledger\n\n## Entries\n\n"
        "| Revision ID | Date | Voice |\n| --- | --- | --- |\n"
        f"{rows}\n",
        encoding="utf-8",
    )
    js = tmp_path / "voice-revision-ledger.json"
    js.write_text(json.dumps(ledger, indent=2), encoding="utf-8")
    near = tmp_path / "voice-revision-near-misses.md"
    near.write_text(near_misses, encoding="utf-8")
    return md, js, near


def valid_seed_ledger() -> dict:
    return copy.deepcopy(voice_accountability.load_ledger())


def validate_tmp(tmp_path: Path, ledger: dict, **kwargs) -> list[str]:
    md, js, near = write_tracker(tmp_path, ledger, **kwargs)
    return voice_accountability.validate_ledger(
        repo_root=REPO_ROOT,
        markdown_path=md,
        json_path=js,
        near_misses_path=near,
    )


def test_seeded_mearsheimer_entry_validates_as_strict() -> None:
    assert voice_accountability.validate_ledger() == []
    entry = voice_accountability.load_ledger()["entries"][0]
    assert entry["id"] == "VR-20260716-01"
    assert entry["voice_slug"] == "mearsheimer"
    assert entry["class"] == "explicit-personal-admission"
    assert "did not fully appreciate" in entry["revised_view"].lower()


def test_markdown_json_id_mismatch_is_rejected(tmp_path: Path) -> None:
    ledger = valid_seed_ledger()
    failures = validate_tmp(tmp_path, ledger, markdown_ids=["VR-20260716-02"])
    assert any("Markdown/JSON ID mismatch" in failure for failure in failures)


def test_duplicate_voice_revision_ids_are_rejected(tmp_path: Path) -> None:
    ledger = valid_seed_ledger()
    ledger["entries"].append(copy.deepcopy(ledger["entries"][0]))
    failures = validate_tmp(tmp_path, ledger)
    assert any("duplicate voice-revision ID" in failure for failure in failures)


def test_invalid_class_and_status_are_rejected(tmp_path: Path) -> None:
    ledger = valid_seed_ledger()
    ledger["entries"][0]["class"] = "soft-vibes"
    ledger["entries"][0]["status"] = "maybe"
    failures = validate_tmp(tmp_path, ledger)
    assert any("invalid voice-revision class" in failure for failure in failures)
    assert any("invalid voice-revision status" in failure for failure in failures)


def test_missing_source_paths_and_bad_lines_are_rejected(tmp_path: Path) -> None:
    ledger = valid_seed_ledger()
    ledger["entries"][0]["source_path"] = "narrative-geopolitics/archive/sources/missing.md"
    failures = validate_tmp(tmp_path, ledger)
    assert any("source path missing" in failure for failure in failures)

    ledger = valid_seed_ledger()
    ledger["entries"][0]["line"] = 999999
    failures = validate_tmp(tmp_path, ledger)
    assert any("line reference out of range" in failure for failure in failures)


def test_near_miss_entries_are_rejected_from_main_ledger(tmp_path: Path) -> None:
    ledger = valid_seed_ledger()
    ledger["entries"][0]["adjudication_note"] += " NM-20260716-01"
    failures = validate_tmp(tmp_path, ledger)
    assert any("near-miss entry leaked" in failure for failure in failures)


def test_voice_accountability_command_surface_validates() -> None:
    result = subprocess.run(
        [
            sys.executable,
            str(REPO_ROOT / "tools" / "run_repo.py"),
            "voice-accountability",
            "validate",
        ],
        cwd=REPO_ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "voice_accountability_failures=0" in result.stdout
