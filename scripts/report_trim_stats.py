from __future__ import annotations

import argparse
import re
from collections import defaultdict
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
ARCHIVE_SOURCES_ROOT = REPO_ROOT / "narrative-geopolitics" / "archive" / "sources"
HOST_SLUG_ALIASES = {}


def parse_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        return {}
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}

    data: dict[str, str] = {}
    for raw_line in parts[1].splitlines():
        if ":" not in raw_line:
            continue
        key, value = raw_line.split(":", 1)
        data[key.strip()] = value.strip().strip('"')
    return data


def safe_int(value: str | None) -> int:
    if not value:
        return 0
    try:
        return int(value)
    except ValueError:
        return 0


def transcript_body(text: str) -> str:
    if "## Transcript" not in text:
        return ""
    return text.split("## Transcript", 1)[1].lstrip()


def canonical_host_slug(path: Path, frontmatter: dict[str, str]) -> str:
    host_slug = frontmatter.get("host_slug") or frontmatter.get("channel_slug") or "unknown"
    host_slug = HOST_SLUG_ALIASES.get(host_slug, host_slug)
    if host_slug == "unknown" and path.name.startswith("source-alexander-mercouris-"):
        return "alexander-mercouris"
    return host_slug


def main() -> int:
    parser = argparse.ArgumentParser(description="Summarize best-intake trim savings by host.")
    parser.add_argument("--host-slug", help="Optional host slug filter.")
    parser.add_argument("--since", help="Optional lower bound on pub_date in YYYY-MM-DD format.")
    args = parser.parse_args()

    host_rows: dict[str, dict[str, float]] = defaultdict(
        lambda: {
            "sources": 0,
            "opening_trimmed": 0,
            "closing_trimmed": 0,
            "opening_chars": 0,
            "opening_words": 0,
            "closing_chars": 0,
            "closing_words": 0,
            "body_chars": 0,
        }
    )

    for path in sorted(ARCHIVE_SOURCES_ROOT.rglob("source-*.md")):
        text = path.read_text(encoding="utf-8")
        frontmatter = parse_frontmatter(text)
        host_slug = canonical_host_slug(path, frontmatter)
        if args.host_slug and host_slug != args.host_slug:
            continue
        pub_date = frontmatter.get("pub_date", "").strip("'\"")
        if args.since and pub_date and pub_date < args.since:
            continue

        body = transcript_body(text)
        row = host_rows[host_slug]
        row["sources"] += 1
        row["body_chars"] += len(body)
        row["opening_trimmed"] += 1 if frontmatter.get("opening_trim_applied") == "true" else 0
        row["closing_trimmed"] += 1 if frontmatter.get("closing_trim_applied") == "true" else 0
        row["opening_chars"] += safe_int(frontmatter.get("opening_trim_chars_saved"))
        row["opening_words"] += safe_int(frontmatter.get("opening_trim_words_saved"))
        row["closing_chars"] += safe_int(frontmatter.get("closing_trim_chars_saved"))
        row["closing_words"] += safe_int(frontmatter.get("closing_trim_words_saved"))

    print(
        "host_slug\tsources\topening_trimmed\tclosing_trimmed\topening_chars\topening_words\tclosing_chars\tclosing_words\ttotal_chars_saved\tavg_pct_body_saved"
    )
    for host_slug in sorted(host_rows):
        row = host_rows[host_slug]
        total_chars_saved = int(row["opening_chars"] + row["closing_chars"])
        avg_pct = 0.0
        if row["body_chars"]:
            avg_pct = total_chars_saved / row["body_chars"] * 100
        print(
            f"{host_slug}\t{int(row['sources'])}\t{int(row['opening_trimmed'])}\t{int(row['closing_trimmed'])}\t"
            f"{int(row['opening_chars'])}\t{int(row['opening_words'])}\t{int(row['closing_chars'])}\t"
            f"{int(row['closing_words'])}\t{total_chars_saved}\t{avg_pct:.2f}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
