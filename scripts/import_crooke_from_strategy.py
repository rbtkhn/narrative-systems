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
VOICE_ROOT = NG_ROOT / "voices" / "crooke"
STRATEGY_ROOT = Path(r"C:\dev\strategy-codex")
INDEX_PATH = STRATEGY_ROOT / "statecraft" / "voices" / "crooke" / "crooke-index.md"


HOST_SLUG_MAP = {
    "glenn-diesen": "glenn-diesen",
    "diesen": "glenn-diesen",
    "dialogue-works": "dialogue-works",
    "alkorshid": "dialogue-works",
    "daniel-davis": "daniel-davis",
    "davis": "daniel-davis",
    "judging-freedom": "judging-freedom",
    "napolitano": "judging-freedom",
    "hedges": "hedges",
    "crooke": "crooke",
}

EXISTING_LOCAL_PATHS = {
    "narrative-geopolitics/archive/sources/2026-06-11/source-daniel-davis-alastair-crooke-more-iran-attacks-weaken-the-us-2026-06-11.md",
    "narrative-geopolitics/archive/sources/2026-06-24/source-daniel-davis-alastair-crooke-iran-deal-who-dictating-terms-2026-06-24.md",
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
    name = path.name.removeprefix("source-")
    for prefix, mapped in HOST_SLUG_MAP.items():
        if name.startswith(prefix + "-"):
            return mapped
    return "crooke"


def infer_source_class(frontmatter: dict[str, str], host_slug: str) -> str:
    source_form = frontmatter.get("source_form", "").strip().lower()
    if source_form == "newsletter":
        return "authored newsletter"
    if source_form == "interview":
        return "host-pressure test" if host_slug != "crooke" else "authored interview"
    if source_form:
        return source_form
    return "imported voice source"


def load_manifest() -> dict:
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


def write_manifest(manifest: dict) -> None:
    MANIFEST_PATH.write_text(json.dumps(manifest, indent=2, ensure_ascii=True) + "\n", encoding="utf-8", newline="\n")


def ensure_existing_rows_tagged(manifest: dict) -> int:
    updated = 0
    for row in manifest.get("sources", []):
        if row.get("local_path") in EXISTING_LOCAL_PATHS:
            voice_slugs = row.setdefault("voice_slugs", [])
            if "crooke" not in voice_slugs:
                voice_slugs.append("crooke")
                updated += 1
    return updated


def import_missing_sources(manifest: dict, source_paths: list[Path]) -> list[dict]:
    existing = {row["local_path"] for row in manifest.get("sources", [])}
    new_rows: list[dict] = []
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
        row = {
            "date": pub_date,
            "title": title,
            "local_path": rel_local,
            "voice_index_path": f"../../archive/sources/{pub_date}/{dest_path.name}",
            "upstream_path": source_path.as_posix(),
            "source_class": source_class,
            "modality": modality,
            "voice_slugs": ["crooke"],
            "host_slug": host_slug,
            "import_status": "imported",
        }
        manifest["sources"].append(row)
        new_rows.append(row)
        existing.add(rel_local)
    return new_rows


def build_voice_files(manifest: dict) -> None:
    rows = [row for row in manifest.get("sources", []) if "crooke" in row.get("voice_slugs", [])]
    rows.sort(key=lambda row: (row["date"], row["title"]))
    modalities = ", ".join(f"`{name}`" for name in sorted({row["modality"] for row in rows}))
    host_counts = Counter(row["host_slug"] for row in rows)
    host_links = ", ".join(f"`{name}`" for name in sorted(host_counts))

    def md_cell(value: str) -> str:
        return value.replace("|", r"\|")

    route_lines = [
        f"| `{row['date']}` | {md_cell(row['title'])} | `{md_cell(row['source_class'])}` | `{md_cell(row['host_slug'])}` | [source]({row['voice_index_path']}) |"
        for row in rows
    ]

    readme = f"""# Voice Record: Alastair Crooke

Status: `internal`

## Profile

| Field | Value |
| --- | --- |
| Name | Alastair Crooke |
| Slug | `crooke` |
| Role | Hybrid authored-plus-interview systemic fracture / geopolitical transition voice |
| Source basis | `strategy-codex/statecraft/voices/crooke/crooke-index.md` plus already-local 2026 Crooke archive rows |
| Public summary status | `none` |
| Parity status | `imported-corpus` |
| Imported source rows | {len(rows)} |
| Central archive files | {len(rows)} |
| Last reviewed | `2026-07-08` |

## Routing

| Route | Use when | Notes |
| --- | --- | --- |
| [source-index.md](source-index.md) | You need the imported local route map. | Links only to central archive source files. |

## Source Modalities

Imported modalities in this slice: {modalities}.

Active host/channel shelves in this slice: {host_links}.

## Core Frame

Crooke supplies a hybrid authored-plus-guest reading of systemic fracture, strategic transition, deterrence breakdown, and elite-political narrative instability across both the Iran-war and Europe/Russia objects.

## Use Guidance

Use this voice when:

- Use when a daily item needs systemic-transition interpretation, escalation framing, deterrence language, or late-imperial political fracture analysis.

Be careful when:

- Be careful when sweeping civilizational framing or high-level synthesis outruns archive-confirmed mechanism.

Evidence needed before relying on this voice:

- At least one imported source from [source-index.md](source-index.md).
- A host/channel check whenever `host_slug` is not `crooke`.
- Independent corroboration when authored argument and host-conditioned interview framing diverge.

## Parity Note

This voice is a unified local Crooke shelf: imported from the strategy-codex Crooke index and widened to include already-present 2026 Crooke archive rows in this repo.
"""

    source_index = f"""# Alastair Crooke Source Index

This index routes the unified local Crooke corpus for `crooke` to the central Narrative Geopolitics source archive.

Source basis: `strategy-codex/statecraft/voices/crooke/crooke-index.md` plus already-local 2026 Crooke archive rows.

Corpus: {len(rows)} local route rows across {len(rows)} central archive source files.

Status: `imported-corpus`

## Reading Rule

1. Source truth lives in `../../archive/sources/`.
2. This file owns `crooke` routing and continuity only.
3. Open the relevant channel shelf before synthesis when `host_slug` is present.
4. Distinguish Crooke-authored pieces from host-conditioned Crooke appearances before promoting claims.

## Imported Route Map

| Date | Source | Role | Host slug | Archive link |
| --- | --- | --- | --- | --- |
{chr(10).join(route_lines)}

## Import Boundary

This local shelf unifies imported Crooke sources from strategy-codex with already-present June 2026 Crooke rows already materialized in this repo.
"""

    profile = """# Alastair Crooke Profile

Primary voice profile: [README.md](README.md)

This alias exists for navigability. The canonical voice profile surface remains [README.md](README.md).
"""

    index = """# Alastair Crooke Index

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
    updated_existing = ensure_existing_rows_tagged(manifest)
    new_rows = import_missing_sources(manifest, source_paths)
    manifest["source_count"] = len(manifest.get("sources", []))
    write_manifest(manifest)
    build_voice_files(manifest)
    print(f"Index source paths: {len(source_paths)}")
    print(f"Imported new rows: {len(new_rows)}")
    print(f"Updated existing local rows: {updated_existing}")
    print(f"Manifest source_count: {manifest['source_count']}")


if __name__ == "__main__":
    main()
