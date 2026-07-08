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
VOICE_ROOT = NG_ROOT / "voices" / "postol"
STRATEGY_ROOT = Path(r"C:\dev\strategy-codex")
INDEX_PATH = STRATEGY_ROOT / "statecraft" / "voices" / "postol" / "postol-index.md"


HOST_SLUG_MAP = {
    "dialogue-works": "dialogue-works",
    "nima": "dialogue-works",
    "alkhorshid": "dialogue-works",
    "daniel-davis": "daniel-davis",
    "davis": "daniel-davis",
    "postol": "postol",
    "ted-postol": "postol",
    "theodore-postol": "postol",
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
        source_path = STRATEGY_ROOT / raw
        if is_postol_source(source_path):
            unique_paths.append(source_path)
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


def is_postol_source(source_path: Path) -> bool:
    text = source_path.read_text(encoding="utf-8", errors="ignore")
    frontmatter = parse_frontmatter(text)
    markers = [
        frontmatter.get("thread", ""),
        frontmatter.get("thread_expert", ""),
        frontmatter.get("guest", ""),
        frontmatter.get("host", ""),
        frontmatter.get("author", ""),
        frontmatter.get("title", ""),
        frontmatter.get("show_title", ""),
        frontmatter.get("channel_name", ""),
        source_path.name,
    ]
    joined = "\n".join(markers).lower()
    if "ted postol" in joined or "theodore postol" in joined or "postol" in joined:
        return True

    if "threads:" in text.lower():
        frontmatter_block = text.split("---", 2)[1].lower() if text.startswith("---\n") and text.count("---") >= 2 else ""
        if re.search(r"^\s*-\s*postol\s*$", frontmatter_block, flags=re.MULTILINE):
            return True
    return False


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
    return "postol"


def infer_source_class(frontmatter: dict[str, str], host_slug: str) -> str:
    source_form = frontmatter.get("source_form", "").strip().lower()
    source_type = frontmatter.get("source_type", "").strip().lower()
    modality = frontmatter.get("kind", "").strip().lower()

    if source_form == "newsletter":
        return "authored newsletter"
    if source_form == "article":
        return "authored analysis"
    if source_form == "interview":
        return "host-pressure test" if host_slug != "postol" else "authored interview"
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


def build_row_from_source_path(source_path: Path) -> dict[str, str | list[str]]:
    text = source_path.read_text(encoding="utf-8", errors="ignore")
    frontmatter = parse_frontmatter(text)
    pub_date = frontmatter.get("pub_date") or source_path.parent.name
    title = extract_title(text, frontmatter, source_path)
    host_slug = infer_host_slug(source_path, frontmatter)
    modality = frontmatter.get("kind", "transcript")
    source_class = infer_source_class(frontmatter, host_slug)
    return {
        "date": pub_date,
        "title": title,
        "local_path": f"narrative-geopolitics/archive/sources/{pub_date}/{source_path.name}",
        "voice_index_path": f"../../archive/sources/{pub_date}/{source_path.name}",
        "upstream_path": source_path.as_posix(),
        "source_class": source_class,
        "modality": modality,
        "voice_slugs": ["postol"],
        "host_slug": host_slug,
        "import_status": "imported",
    }


def collect_target_local_paths(source_paths: list[Path]) -> set[str]:
    return {build_row_from_source_path(source_path)["local_path"] for source_path in source_paths}


def ensure_existing_rows_tagged(manifest: dict, target_local_paths: set[str]) -> int:
    updated = 0
    for row in manifest.get("sources", []):
        if row.get("local_path") not in target_local_paths:
            continue
        voice_slugs = row.setdefault("voice_slugs", [])
        if "postol" not in voice_slugs:
            voice_slugs.append("postol")
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
        if "postol" not in voice_slugs:
            voice_slugs.append("postol")
            updated += 1
    return updated


def cleanup_out_of_scope_rows(manifest: dict, target_local_paths: set[str]) -> tuple[int, int]:
    return 0, 0


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
    all_rows = [row for row in load_manifest().get("sources", []) if "postol" in row.get("voice_slugs", [])]
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

    readme = f"""# Voice Record: Ted Postol

Status: `internal`

## Profile

| Field | Value |
| --- | --- |
| Name | Ted Postol |
| Slug | `postol` |
| Role | Host-conditioned missile-defense, deterrence, and technical-feasibility voice |
| Source basis | `strategy-codex/statecraft/voices/postol/postol-index.md`{source_basis_suffix} |
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

Postol supplies a host-conditioned register centered on missile-defense performance, deterrence consequence, targeting reality, and technical-feasibility limits across Iran-war and air-defense claims.

## Use Guidance

Use this voice when:

- Use when a daily item needs technical missile-defense analysis, strike-feasibility critique, or deterrence-performance pressure under repeated host framing.

Be careful when:

- Be careful when single-system technical judgments are stretched into broader political or strategic certainty without corroboration.

Evidence needed before relying on this voice:

- At least one imported source from [source-index.md](source-index.md).
- A host/channel check whenever `host_slug` is not `postol`.
- Independent corroboration when technical performance claims outrun archive-confirmed evidence.

## Parity Note

This voice is a unified local Postol shelf built from the strategy-codex Postol index and any already-routed local archive rows that match the imported corpus.
"""

    source_index = f"""# Ted Postol Source Index

This index routes the unified local Postol corpus for `postol` to the central Narrative Geopolitics source archive.

Source basis: `strategy-codex/statecraft/voices/postol/postol-index.md`{source_basis_suffix}.

Corpus: {len(all_rows)} local route rows across {len(all_rows)} central archive source files.

Status: `imported-corpus`

## Reading Rule

1. Source truth lives in `../../archive/sources/`.
2. This file owns `postol` routing and continuity only.
3. Open the relevant channel shelf before synthesis when `host_slug` is present.
4. Distinguish technical-performance analysis from broader commentary or macro-constraint voices before promoting claims.

## Imported Route Map

| Date | Source | Role | Host slug | Archive link |
| --- | --- | --- | --- | --- |
{chr(10).join(route_lines)}

## Import Boundary

This import followed the strategy-codex Postol index and copied source captures into `archive/sources/YYYY-MM-DD/` while preserving already-local matching archive rows.
"""

    profile = """# Ted Postol Profile

Primary voice profile: [README.md](README.md)

This alias exists for navigability. The canonical voice profile surface remains [README.md](README.md).
"""

    index = """# Ted Postol Index

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
    rows_removed, postol_tags_removed = cleanup_out_of_scope_rows(manifest, target_local_paths)
    tagged_existing = ensure_existing_rows_tagged(manifest, target_local_paths)
    normalized_existing = normalize_existing_rows(manifest, source_paths)
    new_rows, skipped_existing = import_missing_sources(manifest, source_paths)
    manifest["source_count"] = len(manifest.get("sources", []))
    write_manifest(manifest)

    source_basis_suffix = " plus already-local matching archive rows" if tagged_existing or skipped_existing else ""
    build_voice_files(source_basis_suffix)

    print(f"Index source paths: {len(source_paths)}")
    print(f"Imported new rows: {len(new_rows)}")
    print(f"Removed out-of-scope rows: {rows_removed}")
    print(f"Removed out-of-scope postol tags: {postol_tags_removed}")
    print(f"Tagged existing rows: {tagged_existing}")
    print(f"Normalized existing rows: {normalized_existing}")
    print(f"Skipped existing rows: {skipped_existing}")
    print(f"Manifest source_count: {load_manifest()['source_count']}")


if __name__ == "__main__":
    main()
