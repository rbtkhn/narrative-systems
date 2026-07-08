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
VOICE_ROOT = NG_ROOT / "voices" / "parsi"
STRATEGY_ROOT = Path(r"C:\dev\strategy-codex")
INDEX_PATH = STRATEGY_ROOT / "statecraft" / "voices" / "parsi" / "parsi-index.md"


HOST_SLUG_MAP = {
    "breaking-points": "breaking-points",
    "daniel-davis": "daniel-davis",
    "davis": "daniel-davis",
    "dialogue-works": "dialogue-works",
    "diesen": "glenn-diesen",
    "duran": "the-duran",
    "glenn-diesen": "glenn-diesen",
    "india-global-left": "india-global-left",
    "judging-freedom": "judging-freedom",
    "mario-nawfal": "mario-nawfal",
    "moral-resistance": "moral-resistance",
    "napolitano": "judging-freedom",
    "nawfal": "mario-nawfal",
    "parsi": "parsi",
    "switzerland-with-tom-switzer": "tom-switzer",
    "switzer": "tom-switzer",
    "the-duran": "the-duran",
    "tom-switzer": "tom-switzer",
    "tucker": "tucker",
    "tucker-carlson": "tucker",
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
    value = frontmatter.get("title", "").strip()
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

    channel_name = frontmatter.get("channel_name", "").strip().lower()
    if channel_name:
        for prefix, mapped in HOST_SLUG_MAP.items():
            if channel_name == prefix or channel_name.startswith(prefix + "."):
                return mapped

    stem = path.name.removeprefix("source-")
    for prefix, mapped in HOST_SLUG_MAP.items():
        if stem.startswith(prefix + "-"):
            return mapped
    return "parsi"


def infer_source_class(path: Path, frontmatter: dict[str, str], host_slug: str) -> str:
    source_form = frontmatter.get("source_form", "").strip().lower()
    source_type = frontmatter.get("source_type", "").strip().lower()
    modality = frontmatter.get("kind", "").strip().lower()

    if path.name.startswith("source-x-bundle-") or source_form == "post":
        return "signal capture"
    if source_form == "newsletter":
        return "authored newsletter"
    if source_form == "article":
        return "authored analysis"
    if source_form == "interview":
        return "host-pressure test" if host_slug != "parsi" else "authored interview"
    if source_form == "panel":
        return "cross-voice panel"
    if source_form == "debate":
        return "cross-voice debate"
    if source_type in {"substack", "responsible-statecraft"}:
        return "authored analysis"
    if modality == "paste-bundle":
        return "paste-bundle"
    if source_form:
        return source_form
    return "imported voice source"


def load_manifest() -> dict:
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


def write_manifest(manifest: dict) -> None:
    MANIFEST_PATH.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def collect_target_local_paths(source_paths: list[Path]) -> set[str]:
    rel_paths: set[str] = set()
    for source_path in source_paths:
        text = source_path.read_text(encoding="utf-8", errors="ignore")
        frontmatter = parse_frontmatter(text)
        pub_date = frontmatter.get("pub_date") or source_path.parent.name
        rel_paths.add(f"narrative-geopolitics/archive/sources/{pub_date}/{source_path.name}")
    return rel_paths


def build_row_from_source_path(source_path: Path) -> dict[str, str | list[str]]:
    text = source_path.read_text(encoding="utf-8", errors="ignore")
    frontmatter = parse_frontmatter(text)
    pub_date = frontmatter.get("pub_date") or source_path.parent.name
    title = extract_title(text, frontmatter, source_path)
    host_slug = infer_host_slug(source_path, frontmatter)
    modality = frontmatter.get("kind", "transcript")
    source_class = infer_source_class(source_path, frontmatter, host_slug)
    return {
        "date": pub_date,
        "title": title,
        "local_path": f"narrative-geopolitics/archive/sources/{pub_date}/{source_path.name}",
        "voice_index_path": f"../../archive/sources/{pub_date}/{source_path.name}",
        "upstream_path": source_path.as_posix(),
        "source_class": source_class,
        "modality": modality,
        "voice_slugs": ["parsi"],
        "host_slug": host_slug,
        "import_status": "imported",
    }


def ensure_existing_rows_tagged(manifest: dict, target_local_paths: set[str]) -> int:
    updated = 0
    for row in manifest.get("sources", []):
        if row.get("local_path") not in target_local_paths:
            continue
        voice_slugs = row.setdefault("voice_slugs", [])
        if "parsi" not in voice_slugs:
            voice_slugs.append("parsi")
            updated += 1
    return updated


def normalize_existing_rows(manifest: dict, source_paths: list[Path]) -> int:
    desired_rows = {
        row["local_path"]: row
        for row in (build_row_from_source_path(source_path) for source_path in source_paths)
    }
    updated = 0
    for row in manifest.get("sources", []):
        local_path = row.get("local_path")
        if local_path not in desired_rows:
            continue
        desired = desired_rows[local_path]
        for key in ("date", "title", "voice_index_path", "upstream_path", "source_class", "modality", "host_slug", "import_status"):
            if row.get(key) != desired[key]:
                row[key] = desired[key]
                updated += 1
        voice_slugs = row.setdefault("voice_slugs", [])
        if "parsi" not in voice_slugs:
            voice_slugs.append("parsi")
            updated += 1
    return updated


def import_missing_sources(manifest: dict, source_paths: list[Path]) -> tuple[list[dict], int]:
    existing = {row["local_path"] for row in manifest.get("sources", [])}
    new_rows: list[dict] = []
    skipped_existing = 0

    for source_path in source_paths:
        row = build_row_from_source_path(source_path)
        pub_date = row["date"]

        dest_dir = ARCHIVE_SOURCES_ROOT / pub_date
        dest_dir.mkdir(parents=True, exist_ok=True)
        dest_path = dest_dir / source_path.name
        rel_local = dest_path.relative_to(REPO_ROOT).as_posix()
        if rel_local in existing:
            skipped_existing += 1
            continue

        shutil.copyfile(source_path, dest_path)
        manifest["sources"].append(row)
        new_rows.append(row)
        existing.add(rel_local)

    return new_rows, skipped_existing


def md_cell(value: str) -> str:
    return value.replace("|", r"\|")


def build_voice_files(source_basis_suffix: str) -> None:
    all_rows = [row for row in load_manifest().get("sources", []) if "parsi" in row.get("voice_slugs", [])]
    all_rows.sort(key=lambda row: (row["date"], row["title"]))
    counts = Counter(row["modality"] for row in all_rows)
    host_counts = Counter(row["host_slug"] for row in all_rows)

    modalities = ", ".join(f"`{name}`" for name in sorted(counts))
    hosts = ", ".join(f"`{name}`" for name in sorted(host_counts))
    route_lines = []
    for row in all_rows:
        route_lines.append(
            f"| `{row['date']}` | {md_cell(row['title'])} | `{md_cell(row['source_class'])}` | `{md_cell(row['host_slug'])}` | [source]({row['voice_index_path']}) |"
        )

    readme = f"""# Voice Record: Trita Parsi

Status: `internal`

## Profile

| Field | Value |
| --- | --- |
| Name | Trita Parsi |
| Slug | `parsi` |
| Role | Hybrid authored-plus-interview diplomacy, escalation, and regional-order voice |
| Source basis | `strategy-codex/statecraft/voices/parsi/parsi-index.md`{source_basis_suffix} |
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

Active host/channel shelves in this slice: {hosts}.

## Core Frame

Parsi supplies a hybrid authored-plus-guest reading of Iran diplomacy, escalation management, sanctions architecture, Israel-US bargaining, and regional security-order transitions.

## Use Guidance

Use this voice when:

- Use when a daily item needs negotiation logic, sanctions/diplomacy sequencing, or regional-order interpretation grounded across both authored and host-conditioned surfaces.

Be careful when:

- Be careful when fast-turn interview framing compresses distinctions between Parsi's authored positions, host pressure, and broader co-guest framing.

Evidence needed before relying on this voice:

- At least one imported source from [source-index.md](source-index.md).
- A host/channel check whenever `host_slug` is not `parsi`.
- Independent corroboration when high-speed interview claims outrun the authored spine.

## Parity Note

This voice is a unified local Parsi shelf built from the strategy-codex Parsi index and any already-routed local archive rows that match the imported corpus.
"""

    source_index = f"""# Trita Parsi Source Index

This index routes the unified local Parsi corpus for `parsi` to the central Narrative Geopolitics source archive.

Source basis: `strategy-codex/statecraft/voices/parsi/parsi-index.md`{source_basis_suffix}.

Corpus: {len(all_rows)} local route rows across {len(all_rows)} central archive source files.

Status: `imported-corpus`

## Reading Rule

1. Source truth lives in `../../archive/sources/`.
2. This file owns `parsi` routing and continuity only.
3. Open the relevant channel shelf before synthesis when `host_slug` is present.
4. Distinguish authored Parsi sources from host-conditioned Parsi appearances before promoting claims.

## Imported Route Map

| Date | Source | Role | Host slug | Archive link |
| --- | --- | --- | --- | --- |
{chr(10).join(route_lines)}

## Import Boundary

This import followed the strategy-codex Parsi index and copied source captures into `archive/sources/YYYY-MM-DD/` while preserving already-local matching archive rows.
"""

    profile = """# Trita Parsi Profile

Primary voice profile: [README.md](README.md)

This alias exists for navigability. The canonical voice profile surface remains [README.md](README.md).
"""

    index = """# Trita Parsi Index

Primary voice index: [source-index.md](source-index.md)

This alias exists for navigability. The canonical voice index surface remains [source-index.md](source-index.md).
"""

    VOICE_ROOT.mkdir(parents=True, exist_ok=True)
    (VOICE_ROOT / "README.md").write_text(readme + "\n", encoding="utf-8", newline="\n")
    (VOICE_ROOT / "source-index.md").write_text(source_index + "\n", encoding="utf-8", newline="\n")
    (VOICE_ROOT / "profile.md").write_text(profile + "\n", encoding="utf-8", newline="\n")
    (VOICE_ROOT / "index.md").write_text(index + "\n", encoding="utf-8", newline="\n")


def main() -> None:
    source_paths = parse_index_paths()
    manifest = load_manifest()
    target_local_paths = collect_target_local_paths(source_paths)
    tagged_existing = ensure_existing_rows_tagged(manifest, target_local_paths)
    normalized_existing = normalize_existing_rows(manifest, source_paths)
    new_rows, skipped_existing = import_missing_sources(manifest, source_paths)
    manifest["source_count"] = len(manifest.get("sources", []))
    write_manifest(manifest)

    source_basis_suffix = " plus already-local matching archive rows" if tagged_existing or skipped_existing else ""
    build_voice_files(source_basis_suffix)

    print(f"Index source paths: {len(source_paths)}")
    print(f"Imported new rows: {len(new_rows)}")
    print(f"Tagged existing rows: {tagged_existing}")
    print(f"Normalized existing rows: {normalized_existing}")
    print(f"Skipped existing rows: {skipped_existing}")
    print(f"Manifest source_count: {load_manifest()['source_count']}")


if __name__ == "__main__":
    main()
