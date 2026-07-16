from __future__ import annotations

import argparse
import shutil

from codex_skill_registry import build_registry, skill_files


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Sync repo skill drafts into the user-level Codex skills directory.")
    parser.add_argument(
        "--skill",
        action="append",
        dest="skills",
        help="Specific skill name to sync. Repeatable. Defaults to all registered skills.",
    )
    parser.add_argument("--dry-run", action="store_true", help="Show planned copy actions without writing files.")
    return parser.parse_args()


def resolve_skills(requested: list[str] | None) -> list[str]:
    registry = build_registry()
    if not requested:
        return sorted(registry)
    unknown = [name for name in requested if name not in registry]
    if unknown:
        raise SystemExit(f"Unknown skill(s): {', '.join(unknown)}")
    seen: list[str] = []
    for name in requested:
        if name not in seen:
            seen.append(name)
    return seen


def sync_skill(name: str, dry_run: bool) -> str:
    entry = build_registry()[name]
    if not entry.source.exists():
        raise SystemExit(f"Missing repo skill draft for {name}: {entry.source_dir}")

    source_files = skill_files(entry.source_dir)
    dest_files = skill_files(entry.dest_dir)
    if set(source_files) == set(dest_files) and all(
        source_files[path].read_bytes() == dest_files[path].read_bytes()
        for path in source_files
    ):
        return f"UNCHANGED {name} -> {entry.dest_dir}"

    if dry_run:
        return f"WOULD-SYNC {name} -> {entry.dest_dir}"

    entry.dest_dir.mkdir(parents=True, exist_ok=True)
    for relative_path in sorted(set(dest_files) - set(source_files)):
        dest_files[relative_path].unlink()
    for directory in sorted(
        (path for path in entry.dest_dir.rglob("*") if path.is_dir()),
        key=lambda path: len(path.parts),
        reverse=True,
    ):
        if not any(directory.iterdir()):
            directory.rmdir()
    for relative_path, source_path in source_files.items():
        destination = entry.dest_dir / relative_path
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source_path, destination)
    return f"SYNCED {name} -> {entry.dest_dir}"


def main() -> None:
    args = parse_args()
    for skill_name in resolve_skills(args.skills):
        print(sync_skill(skill_name, args.dry_run))


if __name__ == "__main__":
    main()
