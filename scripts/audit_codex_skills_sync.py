from __future__ import annotations

import argparse

from codex_skill_registry import build_registry, discover_codex_skill_names, discover_repo_skill_names, read_text


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Audit repo-owned skill drafts against installed Codex skills and report coverage gaps."
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit non-zero if any repo-owned skill is missing or drifting, or if any Codex-installed skill lacks a repo draft.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    repo_names = discover_repo_skill_names()
    codex_names = discover_codex_skill_names()
    registry = build_registry(repo_names)

    repo_only = [name for name in repo_names if name not in codex_names]
    codex_only = [name for name in codex_names if name not in repo_names]
    in_sync: list[str] = []
    drift: list[str] = []
    missing_dest: list[str] = []

    for name, entry in registry.items():
        if not entry.dest.exists():
            missing_dest.append(name)
            continue
        if read_text(entry.source) == read_text(entry.dest):
            in_sync.append(name)
        else:
            drift.append(name)

    print(f"repo_skill_drafts={len(repo_names)}")
    print(f"codex_installed_skills={len(codex_names)}")
    print(f"in_sync={len(in_sync)}")
    print(f"drift={len(drift)}")
    print(f"repo_only={len(repo_only)}")
    print(f"codex_only={len(codex_only)}")
    print(f"missing_dest={len(missing_dest)}")
    print("")

    if in_sync:
        print("IN-SYNC")
        for name in in_sync:
            print(f"- {name}")
        print("")
    if drift:
        print("DRIFT")
        for name in drift:
            print(f"- {name}")
        print("")
    if missing_dest:
        print("MISSING DEST")
        for name in missing_dest:
            print(f"- {name}")
        print("")
    if repo_only:
        print("REPO ONLY")
        for name in repo_only:
            print(f"- {name}")
        print("")
    if codex_only:
        print("CODEX ONLY")
        for name in codex_only:
            print(f"- {name}")
        print("")

    if args.strict and (drift or missing_dest or repo_only or codex_only):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
