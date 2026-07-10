from __future__ import annotations

import argparse
import importlib.util
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
LAND_SCRIPT = REPO_ROOT / "scripts" / "land_best_intake.py"


def load_land_best_intake():
    spec = importlib.util.spec_from_file_location("land_best_intake", LAND_SCRIPT)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules["land_best_intake"] = module
    spec.loader.exec_module(module)
    return module


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Backfill transcript sectioning over an explicit source list with visible progress."
    )
    parser.add_argument(
        "--list-file",
        required=True,
        help="Text file containing repo-relative source markdown paths, one per line.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview what would be processed without writing files.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=0,
        help="Optional limit for bounded batches; 0 means all listed files.",
    )
    return parser.parse_args()


def load_paths(list_file: Path, limit: int) -> list[Path]:
    if not list_file.is_file():
        raise FileNotFoundError(f"List file not found: {list_file}")
    paths: list[Path] = []
    for raw_line in list_file.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        source_path = (REPO_ROOT / line).resolve()
        if not source_path.is_file():
            raise FileNotFoundError(f"Source file not found: {source_path}")
        paths.append(source_path)
        if limit and len(paths) >= limit:
            break
    if not paths:
        raise ValueError(f"No source paths found in: {list_file}")
    return paths


def main() -> int:
    args = parse_args()
    module = load_land_best_intake()
    list_file = (REPO_ROOT / args.list_file).resolve()
    paths = load_paths(list_file, args.limit)

    counts = {"TRIMMED": 0, "NORMALIZED": 0, "UNCHANGED": 0}
    total = len(paths)
    for index, path in enumerate(paths, start=1):
        result = module.retrofit_source(
            path,
            "1900-01-01",
            dry_run=args.dry_run,
            force_sections=True,
            sectioning="auto",
        )
        if result:
            status = result.split(" ", 1)[0]
            if status in counts:
                counts[status] += 1
            print(f"[{index}/{total}] {result}", flush=True)
        else:
            print(f"[{index}/{total}] SKIPPED {path.relative_to(REPO_ROOT).as_posix()}", flush=True)

    print(
        "SUMMARY "
        f"total={total} "
        f"trimmed={counts['TRIMMED']} "
        f"normalized={counts['NORMALIZED']} "
        f"unchanged={counts['UNCHANGED']}"
        ,
        flush=True,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
