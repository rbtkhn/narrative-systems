from __future__ import annotations

import argparse
import json

import voice_indexes


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Reconcile existing voice indexes from canonical manifest routes.")
    scope = parser.add_mutually_exclusive_group(required=True)
    scope.add_argument("--date")
    scope.add_argument("--all", action="store_true")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--write", action="store_true")
    parser.add_argument("--json", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    report = voice_indexes.reconcile(
        voice_indexes.load_manifest(),
        run_date=None if args.all else args.date,
        write=args.write,
    )
    payload = {"mode": "write" if args.write else "check", "date": None if args.all else args.date, **report}
    if args.json:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        print(f"changed_shelves={len(report['changed_shelves'])}")
        print(f"added_routes={len(report['added_routes'])}")
        print(f"unindexed_voices={len(report['unindexed_voices'])}")
        print(f"failures={len(report['failures'])}")
        for item in report["failures"]:
            print(f"FAIL {item}")
    if report["failures"] or (args.check and report["changed_shelves"]):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
