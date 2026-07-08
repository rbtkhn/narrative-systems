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
VOICE_ROOT = NG_ROOT / "voices" / "freeman"
STRATEGY_ROOT = Path(r"C:\dev\strategy-codex")
INDEX_PATH = STRATEGY_ROOT / "statecraft" / "voices" / "freeman" / "freeman-index.md"


HOST_SLUG_MAP = {
    "daniel-davis": "daniel-davis",
    "davis": "daniel-davis",
    "dialogue-works": "dialogue-works",
    "glenn-diesen": "glenn-diesen",
    "india-global-left": "india-global-left",
    "judging-freedom": "judging-freedom",
    "napolitano": "judging-freedom",
    "diesen": "glenn-diesen",
    "nima": "dialogue-works",
    "neutrality-studies": "neutrality-studies",
    "freeman": "freeman",
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
        if is_freeman_source(source_path):
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


def is_freeman_source(source_path: Path) -> bool:
    text = source_path.read_text(encoding="utf-8", errors="ignore")
    frontmatter = parse_frontmatter(text)
    markers = [
        frontmatter.get("thread", ""),
        frontmatter.get("thread_expert", ""),
        frontmatter.get("guest", ""),
        frontmatter.get("host", ""),
        frontmatter.get("title", ""),
        frontmatter.get("show_title", ""),
        frontmatter.get("channel_name", ""),
        source_path.name,
    ]
    joined = "\n".join(markers).lower()
    if "freeman" in joined:
        return True

    if "threads:" in text.lower():
        frontmatter_block = text.split("---", 2)[1].lower() if text.startswith("---\n") and text.count("---") >= 2 else ""
        if re.search(r"^\s*-\s*freeman\s*$", frontmatter_block, flags=re.MULTILINE):
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
    return "freeman"


def infer_source_class(frontmatter: dict[str, str], host_slug: str) -> str:
    source_form = frontmatter.get("source_form", "").strip().lower()
    source_type = frontmatter.get("source_type", "").strip().lower()
    modality = frontmatter.get("kind", "").strip().lower()

    if source_form == "newsletter":
        return "authored newsletter"
    if source_form == "article":
        return "authored analysis"
    if source_form == "interview":
        return "host-pressure test" if host_slug != "freeman" else "authored interview"
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
        "voice_slugs": ["freeman"],
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
        if "freeman" not in voice_slugs:
            voice_slugs.append("freeman")
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
        if "freeman" not in voice_slugs:
            voice_slugs.append("freeman")
            updated += 1
    return updated


def cleanup_out_of_scope_rows(manifest: dict, target_local_paths: set[str]) -> tuple[int, int]:
    retained_rows = []
    rows_removed = 0
    freeman_tags_removed = 0

    for row in manifest.get("sources", []):
        local_path = row.get("local_path")
        voice_slugs = row.get("voice_slugs", [])
        if "freeman" not in voice_slugs or local_path in target_local_paths:
            retained_rows.append(row)
            continue

        if len(voice_slugs) == 1:
            rows_removed += 1
            local_file = REPO_ROOT / local_path
            if local_file.exists():
                local_file.unlink()
            continue

        row["voice_slugs"] = [slug for slug in voice_slugs if slug != "freeman"]
        freeman_tags_removed += 1
        retained_rows.append(row)

    manifest["sources"] = retained_rows
    return rows_removed, freeman_tags_removed


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
    all_rows = [row for row in load_manifest().get("sources", []) if "freeman" in row.get("voice_slugs", [])]
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

    readme = f"""# Voice Record: Chas Freeman

Status: `internal`

## Profile

| Field | Value |
| --- | --- |
| Name | Chas Freeman |
| Slug | `freeman` |
| Role | Hybrid interview-centered strategic backfire, alliance-law, and order-transition voice |
| Source basis | `strategy-codex/statecraft/voices/freeman/freeman-index.md`{source_basis_suffix} |
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

Freeman supplies a host-conditioned diplomacy-and-order reading centered on strategic backfire, alliance credibility, escalation risk, and the institutional consequences of US and Israeli policy.

## Use Guidance

Use this voice when:

- Use when a daily item needs alliance-law, diplomacy-collapse, strategic-backfire, or order-transition framing across repeated host contexts.

Be careful when:

- Be careful when recurring host cadence compresses Freeman's independent register into show-specific framing or multi-guest consensus language.

Evidence needed before relying on this voice:

- At least one imported source from [source-index.md](source-index.md).
- A host/channel check whenever `host_slug` is not `freeman`.
- Independent corroboration when panel dynamics blur Freeman's claims with co-guest framing.

## Parity Note

This voice is a unified local Freeman shelf built from the strategy-codex Freeman index and any already-routed local archive rows that match the imported corpus.
"""

    source_index = f"""# Chas Freeman Source Index

This index routes the unified local Freeman corpus for `freeman` to the central Narrative Geopolitics source archive.

Source basis: `strategy-codex/statecraft/voices/freeman/freeman-index.md`{source_basis_suffix}.

Corpus: {len(all_rows)} local route rows across {len(all_rows)} central archive source files.

Status: `imported-corpus`

## Reading Rule

1. Source truth lives in `../../archive/sources/`.
2. This file owns `freeman` routing and continuity only.
3. Open the relevant channel shelf before synthesis when `host_slug` is present.
4. Distinguish solo Freeman appearances from panel and host-conditioned files before promoting claims.

## Imported Route Map

| Date | Source | Role | Host slug | Archive link |
| --- | --- | --- | --- | --- |
{chr(10).join(route_lines)}

## Import Boundary

This import followed the strategy-codex Freeman index and copied source captures into `archive/sources/YYYY-MM-DD/` while preserving already-local matching archive rows.
"""

    profile = """# Chas Freeman Profile

Primary voice profile: [README.md](README.md)

This alias exists for navigability. The canonical voice profile surface remains [README.md](README.md).
"""

    index = """# Chas Freeman Index

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
    rows_removed, freeman_tags_removed = cleanup_out_of_scope_rows(manifest, target_local_paths)
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
    print(f"Removed out-of-scope freeman tags: {freeman_tags_removed}")
    print(f"Tagged existing rows: {tagged_existing}")
    print(f"Normalized existing rows: {normalized_existing}")
    print(f"Skipped existing rows: {skipped_existing}")
    print(f"Manifest source_count: {load_manifest()['source_count']}")


if __name__ == "__main__":
    main()
