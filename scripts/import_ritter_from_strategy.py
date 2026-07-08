from __future__ import annotations

import json
import re
import shutil
from collections import Counter
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
NG_ROOT = REPO_ROOT / "narrative-geopolitics"
ARCHIVE_ROOT = NG_ROOT / "archive"
ARCHIVE_SOURCES_ROOT = ARCHIVE_ROOT / "sources"
MANIFEST_PATH = ARCHIVE_ROOT / "source-manifest.json"
VOICE_ROOT = NG_ROOT / "voices" / "ritter"
STRATEGY_ROOT = Path(r"C:\dev\strategy-codex")
INDEX_PATH = STRATEGY_ROOT / "statecraft" / "voices" / "ritter" / "ritter-index.md"
SOURCE_ARCHIVE_ROOT = STRATEGY_ROOT / "source-archive" / "statecraft"


HOST_SLUG_MAP = {
    "glenn-diesen": "glenn-diesen",
    "diesen": "glenn-diesen",
    "dialogue-works": "dialogue-works",
    "daniel-davis": "daniel-davis",
    "judging-freedom": "judging-freedom",
    "napolitano": "judging-freedom",
    "india-global-left": "india-global-left",
    "consortium-news": "consortium-news",
    "garland-nixon": "garland-nixon",
    "ritter": "ritter",
}


def parse_index_paths() -> list[Path]:
    text = INDEX_PATH.read_text(encoding="utf-8", errors="ignore")
    raw_paths = re.findall(r"(source-archive/statecraft/\d{4}-\d{2}(?:-\d{2})?/source-[^)\]\s]+\.md)", text)
    unique_paths: list[Path] = []
    seen: set[str] = set()
    for raw in raw_paths:
        if raw in seen:
            continue
        seen.add(raw)
        unique_paths.append(STRATEGY_ROOT / raw)
    return unique_paths


def parse_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        return {}
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}
    data: dict[str, str] = {}
    for line in parts[1].splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip().strip("'\"")
    return data


def extract_title(text: str, frontmatter: dict[str, str], path: Path) -> str:
    for key in ("title",):
        value = frontmatter.get(key, "").strip()
        if value:
            return value
    for line in text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return path.stem


def infer_host_slug(path: Path, frontmatter: dict[str, str]) -> str:
    for key in ("host_slug", "channel_slug"):
        value = frontmatter.get(key, "").strip()
        if value:
            return HOST_SLUG_MAP.get(value, value)

    name = path.name.removeprefix("source-")
    for prefix, mapped in HOST_SLUG_MAP.items():
        if name.startswith(prefix + "-"):
            return mapped
    return "ritter"


def infer_source_class(frontmatter: dict[str, str], host_slug: str) -> str:
    source_form = frontmatter.get("source_form", "").strip().lower()
    if source_form == "newsletter":
        return "authored newsletter"
    if source_form == "interview":
        return "host-pressure test" if host_slug != "ritter" else "authored interview"
    if source_form == "debate":
        return "cross-voice debate"
    if source_form:
        return source_form
    return "imported voice source"


def load_manifest() -> dict:
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


def write_manifest(manifest: dict) -> None:
    MANIFEST_PATH.write_text(json.dumps(manifest, indent=2, ensure_ascii=True) + "\n", encoding="utf-8", newline="\n")


def copy_sources(source_paths: list[Path]) -> tuple[list[dict], list[Path]]:
    manifest = load_manifest()
    existing = {row["local_path"] for row in manifest.get("sources", [])}
    new_rows: list[dict] = []
    imported_paths: list[Path] = []

    for source_path in source_paths:
        text = source_path.read_text(encoding="utf-8", errors="ignore")
        frontmatter = parse_frontmatter(text)
        pub_date = frontmatter.get("pub_date") or source_path.parent.name
        title = extract_title(text, frontmatter, source_path)
        host_slug = infer_host_slug(source_path, frontmatter)
        modality = frontmatter.get("kind", "transcript")
        source_class = infer_source_class(frontmatter, host_slug)

        dest_dir = ARCHIVE_SOURCES_ROOT / pub_date
        dest_dir.mkdir(parents=True, exist_ok=True)
        dest_path = dest_dir / source_path.name
        rel_local = dest_path.relative_to(REPO_ROOT).as_posix()
        if rel_local in existing:
            continue

        shutil.copyfile(source_path, dest_path)
        imported_paths.append(dest_path)
        row = {
            "date": pub_date,
            "title": title,
            "local_path": rel_local,
            "voice_index_path": f"../../archive/sources/{pub_date}/{dest_path.name}",
            "upstream_path": source_path.as_posix(),
            "source_class": source_class,
            "modality": modality,
            "voice_slugs": ["ritter"],
            "host_slug": host_slug,
            "import_status": "imported",
        }
        manifest["sources"].append(row)
        new_rows.append(row)
        existing.add(rel_local)

    manifest["source_count"] = len(manifest.get("sources", []))
    write_manifest(manifest)
    return new_rows, imported_paths


def build_voice_files(rows: list[dict], imported_paths: list[Path]) -> None:
    all_rows = [row for row in load_manifest().get("sources", []) if "ritter" in row.get("voice_slugs", [])]
    all_rows.sort(key=lambda row: (row["date"], row["title"]))
    counts = Counter(row["modality"] for row in all_rows)
    host_counts = Counter(row["host_slug"] for row in all_rows)

    modalities = ", ".join(f"`{name}`" for name in sorted(counts))
    host_links = ", ".join(f"`{name}`" for name in sorted(host_counts))
    route_lines = []
    def md_cell(value: str) -> str:
        return value.replace("|", r"\|")

    for row in all_rows:
        link = row["voice_index_path"]
        route_lines.append(
            f"| `{row['date']}` | {md_cell(row['title'])} | `{md_cell(row['source_class'])}` | `{md_cell(row['host_slug'])}` | [source]({link}) |"
        )

    readme = f"""# Voice Record: Scott Ritter

Status: `internal`

## Profile

| Field | Value |
| --- | --- |
| Name | Scott Ritter |
| Slug | `ritter` |
| Role | Hybrid authored-plus-interview war interpretation voice |
| Source basis | `strategy-codex/statecraft/voices/ritter/ritter-index.md` |
| Public summary status | `none` |
| Parity status | `imported-corpus` |
| Imported source rows | {len(all_rows)} |
| Central archive files | {len(all_rows)} |
| Last reviewed | `2026-07-08` |

## Routing

| Route | Use when | Notes |
| --- | --- | --- |
| [source-index.md](source-index.md) | You need the imported local route map. | Links only to central archive source files. |

## Source Modalities

Imported modalities in this slice: {modalities}.

Active host/channel shelves in this slice: {host_links}.

## Core Frame

Ritter is a mixed authored-plus-guest voice. The imported slice includes his own newsletter/operator captures, host-conditioned interviews, mixed-guest files, and debate-style appearances across the Russia-Ukraine and Iran-war objects.

## Use Guidance

Use this voice when:

- Use when a daily item needs a force-structure, escalation, or coercion reading carried through both authored and host-conditioned surfaces.

Be careful when:

- Be careful when rhetorical intensity outruns verification or when mixed-guest files blur Ritter's claims with co-guest framing.

Evidence needed before relying on this voice:

- At least one imported source from [source-index.md](source-index.md).
- A host/channel check whenever `host_slug` is not `ritter`.
- Independent corroboration for battlefield specifics or institutional allegations.

## Parity Note

This voice now has an imported central archive corpus derived from the strategy-codex Ritter index. It is broad rather than curated-thin, so later cleanup may separate authored, guest, and discovery-adjacent slices more sharply.
"""

    source_index = f"""# Scott Ritter Source Index

This index routes the imported Ritter corpus for `ritter` to the central Narrative Geopolitics source archive.

Source basis: `strategy-codex/statecraft/voices/ritter/ritter-index.md`.

Corpus: {len(all_rows)} local route rows across {len(all_rows)} central archive source files.

Status: `imported-corpus`

## Reading Rule

1. Source truth lives in `../../archive/sources/`.
2. This file owns `ritter` routing and continuity only.
3. Open the relevant channel shelf before synthesis when `host_slug` is present.
4. Distinguish authored Ritter sources from host-conditioned Ritter appearances before promoting claims.

## Imported Route Map

| Date | Source | Role | Host slug | Archive link |
| --- | --- | --- | --- | --- |
{chr(10).join(route_lines)}

## Import Boundary

This import followed the strategy-codex Ritter index and copied source captures into `archive/sources/YYYY-MM-DD/` with manifest rows preserved locally.
"""

    VOICE_ROOT.mkdir(parents=True, exist_ok=True)
    (VOICE_ROOT / "README.md").write_text(readme + "\n", encoding="utf-8", newline="\n")
    (VOICE_ROOT / "source-index.md").write_text(source_index + "\n", encoding="utf-8", newline="\n")


def main() -> None:
    source_paths = parse_index_paths()
    new_rows, imported_paths = copy_sources(source_paths)
    build_voice_files(new_rows, imported_paths)
    print(f"Index source paths: {len(source_paths)}")
    print(f"Imported new rows: {len(new_rows)}")
    if new_rows:
        print(f"Manifest source_count: {load_manifest()['source_count']}")


if __name__ == "__main__":
    main()
