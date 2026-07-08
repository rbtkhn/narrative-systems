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
VOICE_ROOT = NG_ROOT / "voices" / "mate"
STRATEGY_ROOT = Path(r"C:\dev\strategy-codex")
INDEX_PATH = STRATEGY_ROOT / "statecraft" / "voices" / "mate" / "mate-index.md"


HOST_SLUG_MAP = {
    "judging-freedom": "judging-freedom",
    "napolitano": "judging-freedom",
    "judge-andrew-napolitano": "judging-freedom",
    "mate": "mate",
    "aaron-mate": "mate",
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
        if is_mate_source(source_path):
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


def is_mate_source(source_path: Path) -> bool:
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
    if "aaron mat" in joined or "mate" in joined:
        return True
    return False


def extract_title(text: str, fallback: str) -> str:
    frontmatter = parse_frontmatter(text)
    for key in ("title", "show_title"):
        value = frontmatter.get(key, "").strip()
        if value:
            return value
    body = text.split("---", 2)[-1] if text.startswith("---\n") else text
    for line in body.splitlines():
        stripped = line.strip()
        if stripped.startswith("# "):
            return stripped[2:].strip()
    return fallback


def infer_host_slug(source_path: Path, frontmatter: dict[str, str]) -> str:
    candidates = [
        frontmatter.get("host", ""),
        frontmatter.get("channel_name", ""),
        frontmatter.get("show_title", ""),
        frontmatter.get("title", ""),
        source_path.name,
    ]
    for candidate in candidates:
        normalized = (
            candidate.lower()
            .replace("&", "and")
            .replace("/", " ")
            .replace("'", "")
        )
        tokens = re.findall(r"[a-z0-9]+(?:-[a-z0-9]+)?", normalized)
        joined = "-".join(tokens)
        for key, value in HOST_SLUG_MAP.items():
            if key in normalized or key in joined:
                return value
    return "mate"


def infer_source_class(frontmatter: dict[str, str], host_slug: str) -> str:
    source_form = frontmatter.get("source_form", "").strip().lower()
    if source_form == "panel":
        return "cross-voice panel"
    if source_form == "debate":
        return "cross-voice debate"
    if source_form == "interview" and host_slug != "mate":
        return "host-pressure test"
    if source_form:
        return source_form
    if host_slug != "mate":
        return "host-pressure test"
    return "imported voice source"


def load_manifest() -> dict:
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


def write_manifest(manifest: dict) -> None:
    MANIFEST_PATH.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")


def build_row_from_source_path(source_path: Path) -> tuple[dict, str]:
    text = source_path.read_text(encoding="utf-8", errors="ignore")
    frontmatter = parse_frontmatter(text)
    pub_date = frontmatter.get("pub_date", "").strip() or source_path.parent.name
    local_rel = Path("narrative-geopolitics") / "archive" / "sources" / source_path.parent.name / source_path.name
    title = extract_title(text, source_path.stem)
    host_slug = infer_host_slug(source_path, frontmatter)
    voice_slugs = ["mate"]
    modality = frontmatter.get("modality", "").strip() or "transcript"
    source_class = infer_source_class(frontmatter, host_slug)
    row = {
        "date": pub_date,
        "title": title,
        "local_path": local_rel.as_posix(),
        "voice_index_path": f"../../archive/sources/{source_path.parent.name}/{source_path.name}",
        "upstream_path": source_path.as_posix(),
        "voice_slugs": voice_slugs,
        "host_slug": host_slug,
        "source_class": source_class,
        "modality": modality,
        "import_status": "imported",
    }
    return row, text


def collect_target_local_paths(source_paths: list[Path]) -> set[str]:
    targets: set[str] = set()
    for source_path in source_paths:
        local_rel = Path("narrative-geopolitics") / "archive" / "sources" / source_path.parent.name / source_path.name
        targets.add(local_rel.as_posix())
    return targets


def ensure_existing_rows_tagged(manifest: dict, target_local_paths: set[str]) -> int:
    updated = 0
    for row in manifest.get("sources", []):
        if row.get("local_path") not in target_local_paths:
            continue
        voice_slugs = row.setdefault("voice_slugs", [])
        if "mate" not in voice_slugs:
            voice_slugs.append("mate")
            updated += 1
    return updated


def normalize_existing_rows(manifest: dict, source_paths: list[Path]) -> int:
    source_map = {}
    for source_path in source_paths:
        row, _ = build_row_from_source_path(source_path)
        source_map[row["local_path"]] = row

    updated = 0
    for row in manifest.get("sources", []):
        local_path = row.get("local_path")
        if local_path not in source_map:
            continue
        canonical = source_map[local_path]
        changed = False
        for key in ("date", "voice_index_path", "upstream_path", "host_slug", "source_class", "modality", "import_status"):
            if row.get(key) != canonical[key]:
                row[key] = canonical[key]
                changed = True
        voice_slugs = row.setdefault("voice_slugs", [])
        if "mate" not in voice_slugs:
            voice_slugs.append("mate")
            changed = True
        if changed:
            updated += 1
    return updated


def cleanup_out_of_scope_rows(manifest: dict, target_local_paths: set[str]) -> tuple[int, int]:
    return 0, 0


def import_missing_sources(manifest: dict, source_paths: list[Path]) -> tuple[list[str], int]:
    existing_paths = {row.get("local_path") for row in manifest.get("sources", [])}
    new_rows: list[str] = []
    skipped_existing = 0
    for source_path in source_paths:
        row, text = build_row_from_source_path(source_path)
        local_path = REPO_ROOT / Path(row["local_path"])
        local_path.parent.mkdir(parents=True, exist_ok=True)
        if row["local_path"] in existing_paths:
            skipped_existing += 1
            continue
        shutil.copyfile(source_path, local_path)
        if local_path.read_text(encoding="utf-8", errors="ignore") != text:
            local_path.write_text(text, encoding="utf-8", newline="\n")
        manifest.setdefault("sources", []).append(row)
        existing_paths.add(row["local_path"])
        new_rows.append(row["local_path"])
    return new_rows, skipped_existing


def md_cell(value: str) -> str:
    return value.replace("|", "\\|")


def build_voice_files(source_basis_suffix: str) -> None:
    manifest = load_manifest()
    all_rows = [
        row for row in manifest.get("sources", [])
        if "mate" in row.get("voice_slugs", [])
    ]
    all_rows.sort(key=lambda row: (row.get("local_path", ""), row.get("title", "")))

    modalities = ", ".join(
        f"`{item}`" for item, _ in sorted(Counter(row.get("modality", "unknown") for row in all_rows).items())
    ) or "`unknown`"
    hosts = ", ".join(
        f"`{item}`" for item, _ in sorted(Counter(row.get("host_slug", "unknown") for row in all_rows).items())
    ) or "`unknown`"

    route_lines = []
    for row in all_rows:
        local_path = row["local_path"]
        date_slug = Path(local_path).parent.name
        title = md_cell(row.get("title", Path(local_path).stem))
        role = md_cell(row.get("source_class", "imported voice source"))
        host_slug = md_cell(row.get("host_slug", "unknown"))
        archive_link = row.get("voice_index_path", "")
        route_lines.append(
            f"| `{date_slug}` | {title} | `{role}` | `{host_slug}` | [source]({archive_link}) |"
        )

    readme = f"""# Voice Record: Aaron Mate

Status: `internal`

## Profile

| Field | Value |
| --- | --- |
| Name | Aaron Mate |
| Slug | `mate` |
| Role | Host-conditioned Israel-deception and domestic-politics accountability voice |
| Source basis | `strategy-codex/statecraft/voices/mate/mate-index.md`{source_basis_suffix} |
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

Mate supplies a host-conditioned register centered on Israel-first influence, negotiation-deception framing, Iran-war narrative challenge, and domestic-political accountability spillover.

## Use Guidance

Use this voice when:

- Use when a daily item needs a compact Israel-lobby, negotiation, or domestic-politics accountability read tied to Iran escalation claims.

Be careful when:

- Be careful when a polemical domestic frame outruns archive-confirmed mechanism or leans on implied motive more than sourced causal proof.

Evidence needed before relying on this voice:

- At least one imported source from [source-index.md](source-index.md).
- A host/channel check whenever `host_slug` is not `mate`.
- Independent corroboration before promoting high-confidence claims about covert intent, internal factional control, or deception operations.

## Parity Note

This voice is a unified local Mate shelf built from the strategy-codex Mate index and any already-routed local archive rows that match the imported corpus.
"""

    source_index = f"""# Aaron Mate Source Index

This index routes the unified local Mate corpus for `mate` to the central Narrative Geopolitics source archive.

Source basis: `strategy-codex/statecraft/voices/mate/mate-index.md`{source_basis_suffix}.

Corpus: {len(all_rows)} local route rows across {len(all_rows)} central archive source files.

Status: `imported-corpus`

## Reading Rule

1. Source truth lives in `../../archive/sources/`.
2. This file owns `mate` routing and continuity only.
3. Open the relevant channel shelf before synthesis when `host_slug` is present.
4. Distinguish domestic-political and Israel-lobby accountability framing from military-operational evidence before promoting claims.

## Imported Route Map

| Date | Source | Role | Host slug | Archive link |
| --- | --- | --- | --- | --- |
{chr(10).join(route_lines)}

## Import Boundary

This import followed the strategy-codex Mate index and copied source captures into `archive/sources/YYYY-MM-DD/` while preserving already-local matching archive rows.
"""

    profile = """# Aaron Mate Profile

Primary voice profile: [README.md](README.md)

This alias exists for navigability. The canonical voice profile surface remains [README.md](README.md).
"""

    index = """# Aaron Mate Index

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
    rows_removed, mate_tags_removed = cleanup_out_of_scope_rows(manifest, target_local_paths)
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
    print(f"Removed out-of-scope mate tags: {mate_tags_removed}")
    print(f"Tagged existing rows: {tagged_existing}")
    print(f"Normalized existing rows: {normalized_existing}")
    print(f"Skipped existing rows: {skipped_existing}")
    print(f"Manifest source_count: {load_manifest()['source_count']}")


if __name__ == "__main__":
    main()
