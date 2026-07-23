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
REPO_ROOT = ENGINE.parent.parent

# Common operator-facing aliases. The archive remains the authority; this
# table only prevents a known display name from becoming a second shelf.
VOICE_ALIASES = {
    "jeffrey-sachs": "sachs",
    "john-mearsheimer": "mearsheimer",
    "mohammad-marandi": "marandi",
    "seyed-marandi": "marandi",
}


def canonical_voice_slug(slug: str) -> str:
    value = slug.strip().lower()
    return VOICE_ALIASES.get(value, value)


def normalize_voice_args(forwarded: list[str]) -> tuple[list[str], list[tuple[str, str]]]:
    """Rewrite explicit voice slugs and return an auditable alias receipt."""
    normalized = list(forwarded)
    aliases: list[tuple[str, str]] = []
    for index, item in enumerate(normalized[:-1]):
        if item != "--voice-slug":
            continue
        original = normalized[index + 1]
        canonical = canonical_voice_slug(original)
        if canonical != original:
            normalized[index + 1] = canonical
            aliases.append((original, canonical))
    return normalized, aliases


def print_receipt(aliases: list[tuple[str, str]]) -> None:
    """Emit a compact machine-readable post-land receipt when possible."""
    if aliases:
        for original, canonical in aliases:
            print(f"CANONICAL_VOICE={original}->{canonical}")
    print("INTAKE_RECEIPT=archive-and-manifest-owned")


def main() -> int:
    forwarded = list(sys.argv[1:])
    forwarded, aliases = normalize_voice_args(forwarded)
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
    if result.get("_smart_intake_exit", 0) == 0:
        print_receipt(aliases)
    return int(result.get("_smart_intake_exit", 0))


if __name__ == "__main__":
    raise SystemExit(main())
