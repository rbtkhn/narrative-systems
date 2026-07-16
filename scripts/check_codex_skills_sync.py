from __future__ import annotations

import argparse
from codex_skill_registry import build_registry, skill_files


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Check whether repo skill drafts match installed Codex skills.")
    parser.add_argument(
        "--skill",
        action="append",
        dest="skills",
        help="Specific skill name to check. Repeatable. Defaults to all registered skills.",
    )
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


def check_skill(name: str) -> tuple[str, bool]:
    entry = build_registry()[name]
    if not entry.source.exists():
        return (f"MISSING-SOURCE {name} -> {entry.source_dir}", False)
    if not entry.dest.exists():
        return (f"MISSING-DEST {name} -> {entry.dest_dir}", False)
    source_files = skill_files(entry.source_dir)
    dest_files = skill_files(entry.dest_dir)
    if set(source_files) != set(dest_files):
        return (f"DRIFT {name} -> {entry.dest_dir}", False)
    if any(source_files[path].read_bytes() != dest_files[path].read_bytes() for path in source_files):
        return (f"DRIFT {name} -> {entry.dest_dir}", False)
    return (f"IN-SYNC {name} -> {entry.dest_dir}", True)



def main() -> None:
    args = parse_args()
    ok = True
    for skill_name in resolve_skills(args.skills):
        message, skill_ok = check_skill(skill_name)
        print(message)
        ok = ok and skill_ok
    if not ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
