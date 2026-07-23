"""Canonical smart-intake front door.

The best-intake engine remains the implementation authority. This wrapper
normalizes routine URL/body/date invocations into quick intake and delegates
all archive, provenance, trim, sectioning, manifest, and rollback behavior to
land_best_intake.py.
"""

from __future__ import annotations

import runpy
import sys
import argparse
from pathlib import Path


ENGINE = Path(__file__).with_name("land_best_intake.py")


def main() -> int:
    forwarded = list(sys.argv[1:])
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--confidence-gate", action="store_true")
    parser.add_argument("--no-confidence-gate", action="store_true")
    gate_args, _ = parser.parse_known_args(forwarded)
    gate_enabled = not gate_args.no_confidence_gate and "--help" not in forwarded and "-h" not in forwarded
    if gate_enabled:
        reasons: list[str] = []
        has_body = "--body-file" in forwarded or "--body-text" in forwarded
        has_url = "--url" in forwarded or any(item.startswith(("http://", "https://")) for item in forwarded)
        has_date = any(flag in forwarded for flag in ("--date", "--pub-date"))
        has_host = "--host-slug" in forwarded
        has_voice = "--voice-slug" in forwarded
        if not has_body:
            reasons.append("source body is missing")
        if not has_url:
            reasons.append("source URL is missing")
        if not has_date:
            reasons.append("publication/intake date is missing")
        if not has_host:
            reasons.append("host/channel routing is unresolved; provide --host-slug")
        if not has_voice:
            reasons.append("voice routing is unresolved; provide --voice-slug")
        if reasons:
            print("CONFIDENCE_GATE=PAUSE")
            print("Clarification required before landing:")
            for reason in reasons:
                print(f"- {reason}")
            print("Use --no-confidence-gate to override after reviewing the ambiguity.")
            return 2
    control_flags = {"--help", "-h", "--backfill-since", "--batch-dir", "--metadata-file"}
    if not any(flag in forwarded for flag in control_flags):
        if "--quick" not in forwarded:
            forwarded.insert(0, "--quick")
    sys.argv = [str(ENGINE), *forwarded]
    result = runpy.run_path(str(ENGINE), run_name="__main__")
    return int(result.get("_smart_intake_exit", 0))


if __name__ == "__main__":
    raise SystemExit(main())
