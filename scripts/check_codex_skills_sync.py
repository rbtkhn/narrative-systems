from __future__ import annotations

import argparse
from codex_skill_registry import build_registry, read_text


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
    source = entry.source
    dest = entry.dest
    if not source.exists():
        return (f"MISSING-SOURCE {name} -> {source}", False)
    if not dest.exists():
        return (f"MISSING-DEST {name} -> {dest}", False)
    if read_text(source) != read_text(dest):
        return (f"DRIFT {name} -> {dest}", False)
    return (f"IN-SYNC {name} -> {dest}", True)



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
