from __future__ import annotations

import argparse
from codex_skill_registry import build_registry, read_text


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
    source = entry.source
    dest = entry.dest
    if not source.exists():
        raise SystemExit(f"Missing repo skill draft for {name}: {source}")

    source_text = read_text(source)
    if dest.exists():
        dest_text = read_text(dest)
        if dest_text == source_text:
            return f"UNCHANGED {name} -> {dest}"

    if dry_run:
        return f"WOULD-SYNC {name} -> {dest}"

    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(source_text, encoding="utf-8", newline="\n")
    return f"SYNCED {name} -> {dest}"


def main() -> None:
    args = parse_args()
    for skill_name in resolve_skills(args.skills):
        print(sync_skill(skill_name, args.dry_run))


if __name__ == "__main__":
    main()
