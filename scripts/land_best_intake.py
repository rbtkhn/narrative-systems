from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from types import SimpleNamespace


REPO_ROOT = Path(__file__).resolve().parent.parent
NG_ROOT = REPO_ROOT / "narrative-geopolitics"
ARCHIVE_ROOT = NG_ROOT / "archive"
MANIFEST_PATH = ARCHIVE_ROOT / "source-manifest.json"
ARCHIVE_SOURCES_ROOT = ARCHIVE_ROOT / "sources"
METADATA_SUFFIXES = (".txt", ".md")
REPEATABLE_FIELDS = {"voice_slug", "host_people", "guest_people"}
TRIM_FIELD_ORDER = (
    "opening_trim_applied",
    "opening_trim_rule",
    "opening_trim_chars_saved",
    "opening_trim_words_saved",
    "closing_trim_applied",
    "closing_trim_rule",
    "closing_trim_chars_saved",
    "closing_trim_words_saved",
)


@dataclass(frozen=True)
class HostTrimRule:
    slug: str
    label: str
    opening_markers: tuple[str, ...] = ()
    opening_snippets: tuple[str, ...] = ()
    opening_regexes: tuple[str, ...] = ()
    closing_markers: tuple[str, ...] = ()


HOST_TRIM_RULES: dict[str, HostTrimRule] = {
    "mario-nawfal": HostTrimRule(
        slug="mario-nawfal",
        label="mario-nawfal-v1",
        opening_markers=(
            "So just to kind of recap for the audience",
            "Well, the reality that we're dealing with now is",
            "The issue as I told you before",
            "What we know right now is",
            "The big issue right now is",
            "To kind of recap for the audience",
        ),
        closing_markers=(
            ">> Bye-bye. All right, guys.",
            ">> Bye-bye. >> Bye-bye. All right, guys.",
            "All right, guys. I'll be going live again",
            "Thanks everyone.",
        ),
    ),
    "daniel-davis": HostTrimRule(
        slug="daniel-davis",
        label="daniel-davis-closing-v1",
        closing_markers=(
            "And uh we will be back in about 1 hour.",
            "You know we don't have sponsors cuz we hate to hit you over the head with ads.",
            "And we'll see you this afternoon at I believe 2 o'clock.",
            "We'll see you then at 2 o'clock on the Daniel Davis deep dive.",
            "We'll see you on the next episode of the Daniel Davis deep dive.",
            "You know, I don't try to talk you into buying gold or tell you how to run your stock portfolio, but there is a way you can help us.",
            "That's all I got for you folks right now.",
        ),
    ),
    "alexander-mercouris": HostTrimRule(
        slug="alexander-mercouris",
        label="alexander-mercouris-v1",
        opening_snippets=(
            "And before I proceed with this program, let me remind you again to tick the like button and to check your subscription to this channel.",
            "And before I proceed with this program, let me remind you again to tick the like button and check your subscription to this channel.",
            "And before I proceed with this program, let me remind you to tick the like button and to check your subscription to this channel.",
            "And before I proceed with this program, let me remind you to tick the like button and check your subscription to this channel.",
        ),
        closing_markers=(
            "\n### Close",
            "Anyway, this is where I'm going to finish today's program.",
            "Anyway, this is where I am going to finish today's program.",
            "But in the meantime, this is where I'm going to finish today's program.",
            "Let me remind you again, you can find all our programs on our various platforms",
            "Let me remind you that you can find all our programs on our various platforms",
        ),
    ),
    "dialogue-works": HostTrimRule(
        slug="dialogue-works",
        label="dialogue-works-wrapper-v1",
        opening_regexes=(
            r"^[^\n]+ - YouTube\s*\n\s*Transcripts:\s*\n+",
        ),
    ),
}


def slugify(value: str) -> str:
    value = value.lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-")


def yaml_quote(value: str) -> str:
    escaped = value.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def build_frontmatter(args: SimpleNamespace, title_slug: str, body: str) -> str:
    lines = [
        "---",
        f"ingest_date: {args.ingest_date}",
        f"pub_date: {args.pub_date}",
        f"kind: {args.kind}",
        f"source_form: {args.source_form}",
        "host_people:",
    ]

    if args.host_people:
        lines.extend([f"  - {item}" for item in args.host_people])
    else:
        lines.append("  -")

    lines.append("guest_people:")
    if args.guest_people:
        lines.extend([f"  - {item}" for item in args.guest_people])
    else:
        lines.append("  -")

    lines.extend(
        [
            f"show_title: {args.show_title}",
            f"channel_name: {args.channel_name}",
            f"show: {args.show}",
            f"host: {args.host}",
            f"guest: {yaml_quote(args.guest)}",
            f"thread: {args.thread or args.voice_slugs[0]}",
            f"source_url: {yaml_quote(args.url)}",
            f"source_note: {yaml_quote(args.source_note)}",
            f"title_slug: {title_slug}",
            f"editorial_note: {yaml_quote(args.editorial_note)}",
            f"review_state: {args.review_state}",
            f"routing_state: {args.routing_state}",
            f"opening_trim_applied: {'true' if args.opening_trim_applied else 'false'}",
            f"opening_trim_rule: {yaml_quote(args.opening_trim_rule)}",
            f"opening_trim_chars_saved: {args.opening_trim_chars_saved}",
            f"opening_trim_words_saved: {args.opening_trim_words_saved}",
            f"closing_trim_applied: {'true' if args.closing_trim_applied else 'false'}",
            f"closing_trim_rule: {yaml_quote(args.closing_trim_rule)}",
            f"closing_trim_chars_saved: {args.closing_trim_chars_saved}",
            f"closing_trim_words_saved: {args.closing_trim_words_saved}",
            "---",
            f"# {args.title}",
            "",
            "## Transcript",
            "",
            body.rstrip(),
            "",
        ]
    )
    return "\n".join(lines)


def load_manifest() -> dict:
    with MANIFEST_PATH.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def write_manifest(manifest: dict) -> None:
    with MANIFEST_PATH.open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(manifest, handle, indent=2, ensure_ascii=False)
        handle.write("\n")


def build_manifest_row(
    args: SimpleNamespace,
    source_path: Path,
    upstream_path: str,
) -> dict:
    rel_local = source_path.relative_to(REPO_ROOT).as_posix()
    return {
        "date": args.pub_date,
        "title": args.title,
        "local_path": rel_local,
        "voice_index_path": f"../../archive/sources/{args.pub_date}/{source_path.name}",
        "upstream_path": upstream_path,
        "source_class": args.source_class,
        "modality": args.modality,
        "voice_slugs": args.voice_slugs,
        "host_slug": args.host_slug,
        "import_status": "imported",
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Land Narrative Geopolitics best-intake sources and append manifest rows."
    )
    parser.add_argument("--pub-date")
    parser.add_argument("--ingest-date")
    parser.add_argument("--title")
    parser.add_argument("--url")
    parser.add_argument("--body-file")
    parser.add_argument("--voice-slug", dest="voice_slugs", action="append")
    parser.add_argument("--host-slug")
    parser.add_argument("--host", default="")
    parser.add_argument("--guest", default="")
    parser.add_argument("--host-people", action="append")
    parser.add_argument("--guest-people", action="append")
    parser.add_argument("--show-title", default="")
    parser.add_argument("--channel-name", default="")
    parser.add_argument("--show", default="")
    parser.add_argument("--thread")
    parser.add_argument("--kind", default="cleaned-transcript")
    parser.add_argument("--source-form", default="interview")
    parser.add_argument("--source-class", default="guest interview pressure test")
    parser.add_argument("--modality", default="cleaned-transcript")
    parser.add_argument("--review-state", default="unreviewed")
    parser.add_argument("--routing-state", default="provisional")
    parser.add_argument(
        "--source-note",
        default="Operator-pasted source body. Best-intake landing with preserved transcript body and provisional routing where needed.",
    )
    parser.add_argument(
        "--editorial-note",
        default="Preserve as raw cleaned transcript. Not human-verified verbatim.",
    )
    parser.add_argument(
        "--upstream-path",
        help="Optional upstream path. Defaults to an operator-paste URI based on ingest date and title.",
    )
    parser.add_argument(
        "--metadata-file",
        help="Read single-source metadata from an intake sidecar file.",
    )
    parser.add_argument(
        "--batch-dir",
        help="Read every metadata sidecar in a directory and land them as a batch.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print planned output paths and manifest rows without writing files.",
    )
    parser.add_argument(
        "--trim-opening",
        choices=("auto", "none", *sorted(HOST_TRIM_RULES)),
        default="auto",
        help="Optionally trim known host preamble chatter before landing the source body.",
    )
    parser.add_argument(
        "--backfill-since",
        help="Retrofit approved trim rules onto already-landed archive sources with pub_date on or after this YYYY-MM-DD date.",
    )
    return parser.parse_args()


def ensure_required_fields(args: SimpleNamespace) -> None:
    required = ("pub_date", "ingest_date", "title", "url", "body_file", "voice_slugs")
    missing = []
    for field in required:
        value = getattr(args, field, None)
        if field == "voice_slugs":
            if not value:
                missing.append("voice_slug")
        elif value in (None, ""):
            missing.append(field)
    if missing:
        raise ValueError(f"Missing required fields: {', '.join(missing)}")


def normalize_args(args: SimpleNamespace) -> SimpleNamespace:
    args.host_people = [item for item in (args.host_people or []) if item]
    args.guest_people = [item for item in (args.guest_people or []) if item]
    args.voice_slugs = [item for item in (args.voice_slugs or []) if item]
    ensure_required_fields(args)
    return args


def parse_metadata_file(path: Path) -> dict[str, object]:
    data: dict[str, object] = {}
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or line.startswith("```"):
            continue
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()
        if not key:
            continue
        if key in REPEATABLE_FIELDS:
            items = data.setdefault(key, [])
            if value:
                assert isinstance(items, list)
                items.append(value)
        else:
            data[key] = value
    return data


def args_from_metadata(metadata: dict[str, object], metadata_path: Path, cli_args: argparse.Namespace) -> SimpleNamespace:
    defaults = {
        "host_slug": None,
        "host": "",
        "guest": "",
        "host_people": [],
        "guest_people": [],
        "show_title": "",
        "channel_name": "",
        "show": "",
        "thread": None,
        "kind": "cleaned-transcript",
        "source_form": "interview",
        "source_class": "guest interview pressure test",
        "modality": "cleaned-transcript",
        "review_state": "unreviewed",
        "routing_state": "provisional",
        "source_note": "Operator-pasted source body. Best-intake landing with preserved transcript body and provisional routing where needed.",
        "editorial_note": "Preserve as raw cleaned transcript. Not human-verified verbatim.",
        "upstream_path": None,
        "trim_opening": "auto",
    }
    mapped = defaults.copy()
    mapped.update(
        {
            "pub_date": metadata.get("pub_date", ""),
            "ingest_date": metadata.get("ingest_date", ""),
            "title": metadata.get("title", ""),
            "url": metadata.get("url", ""),
            "body_file": metadata.get("body_file", ""),
            "voice_slugs": metadata.get("voice_slug", []),
            "host_slug": metadata.get("host_slug") or None,
            "host": metadata.get("host", ""),
            "guest": metadata.get("guest", ""),
            "host_people": metadata.get("host_people", []),
            "guest_people": metadata.get("guest_people", []),
            "show_title": metadata.get("show_title", ""),
            "channel_name": metadata.get("channel_name", ""),
            "show": metadata.get("show", ""),
            "thread": metadata.get("thread") or None,
            "kind": metadata.get("kind", defaults["kind"]),
            "source_form": metadata.get("source_form", defaults["source_form"]),
            "source_class": metadata.get("source_class", defaults["source_class"]),
            "modality": metadata.get("modality", defaults["modality"]),
            "review_state": metadata.get("review_state", defaults["review_state"]),
            "routing_state": metadata.get("routing_state", defaults["routing_state"]),
            "source_note": metadata.get("source_note", defaults["source_note"]),
            "editorial_note": metadata.get("editorial_note", defaults["editorial_note"]),
            "upstream_path": metadata.get("upstream_path") or None,
            "trim_opening": metadata.get("trim_opening", defaults["trim_opening"]),
        }
    )
    if mapped["body_file"]:
        body_file = Path(str(mapped["body_file"]))
        if not body_file.is_absolute():
            mapped["body_file"] = str((metadata_path.parent / body_file).resolve())
    mapped["dry_run"] = cli_args.dry_run
    mapped["opening_trim_applied"] = False
    mapped["opening_trim_rule"] = ""
    mapped["opening_trim_chars_saved"] = 0
    mapped["opening_trim_words_saved"] = 0
    mapped["closing_trim_applied"] = False
    mapped["closing_trim_rule"] = ""
    mapped["closing_trim_chars_saved"] = 0
    mapped["closing_trim_words_saved"] = 0
    return normalize_args(SimpleNamespace(**mapped))


def args_from_cli(cli_args: argparse.Namespace) -> SimpleNamespace:
    mapped = {
        "pub_date": cli_args.pub_date,
        "ingest_date": cli_args.ingest_date,
        "title": cli_args.title,
        "url": cli_args.url,
        "body_file": cli_args.body_file,
        "voice_slugs": cli_args.voice_slugs,
        "host_slug": cli_args.host_slug,
        "host": cli_args.host,
        "guest": cli_args.guest,
        "host_people": cli_args.host_people,
        "guest_people": cli_args.guest_people,
        "show_title": cli_args.show_title,
        "channel_name": cli_args.channel_name,
        "show": cli_args.show,
        "thread": cli_args.thread,
        "kind": cli_args.kind,
        "source_form": cli_args.source_form,
        "source_class": cli_args.source_class,
        "modality": cli_args.modality,
        "review_state": cli_args.review_state,
        "routing_state": cli_args.routing_state,
        "source_note": cli_args.source_note,
        "editorial_note": cli_args.editorial_note,
        "upstream_path": cli_args.upstream_path,
        "dry_run": cli_args.dry_run,
        "trim_opening": cli_args.trim_opening,
        "opening_trim_applied": False,
        "opening_trim_rule": "",
        "opening_trim_chars_saved": 0,
        "opening_trim_words_saved": 0,
        "closing_trim_applied": False,
        "closing_trim_rule": "",
        "closing_trim_chars_saved": 0,
        "closing_trim_words_saved": 0,
    }
    return normalize_args(SimpleNamespace(**mapped))


def count_words(text: str) -> int:
    return len(re.findall(r"\S+", text))


def get_trim_rule(args: SimpleNamespace) -> HostTrimRule | None:
    trim_mode = getattr(args, "trim_opening", "auto")
    if trim_mode == "none":
        return None
    if trim_mode == "auto":
        host_slug = getattr(args, "host_slug", None)
        if not host_slug:
            return None
        return HOST_TRIM_RULES.get(host_slug)
    return HOST_TRIM_RULES.get(trim_mode)


def trim_opening_by_rule(body: str, rule: HostTrimRule) -> tuple[str, bool, str, int, int]:
    normalized = body.lstrip()
    for pattern in rule.opening_regexes:
        match = re.match(pattern, normalized)
        if match:
            trimmed = normalized[match.end():].lstrip()
            if trimmed:
                removed = normalized[: match.end()]
                return trimmed, True, rule.label, len(removed), count_words(removed)
    for marker in rule.opening_markers:
        idx = normalized.find(marker)
        if idx > 0:
            trimmed = normalized[idx:].lstrip()
            if trimmed:
                removed = normalized[:idx]
                return trimmed, True, rule.label, len(removed), count_words(removed)
    for snippet in rule.opening_snippets:
        idx = normalized.find(snippet)
        if 0 <= idx <= 400:
            removed = ""
            replacements = (
                (f" {snippet} ", " "),
                (f"{snippet} ", ""),
                (snippet, ""),
            )
            trimmed = normalized
            for candidate, replacement in replacements:
                candidate_idx = trimmed.find(candidate)
                if 0 <= candidate_idx <= 400:
                    removed = candidate
                    trimmed = trimmed.replace(candidate, replacement, 1)
                    break
            trimmed = re.sub(r"(?<=\S) {2,}", " ", trimmed, count=1)
            if trimmed and removed:
                return trimmed, True, rule.label, len(removed), count_words(removed)
    return body, False, "", 0, 0


def trim_closing_by_rule(body: str, rule: HostTrimRule) -> tuple[str, bool, str, int, int]:
    cut_index = -1
    for marker in rule.closing_markers:
        idx = body.find(marker)
        if idx >= 0 and (cut_index == -1 or idx < cut_index):
            cut_index = idx
    if cut_index >= 0:
        trimmed = body[:cut_index].rstrip()
        if trimmed:
            removed = body[cut_index:]
            return trimmed + "\n", True, rule.label, len(removed), count_words(removed)
    return body, False, "", 0, 0


def maybe_trim_opening(args: SimpleNamespace, body: str) -> tuple[str, bool, str, int, int]:
    rule = get_trim_rule(args)
    if not rule or (not rule.opening_markers and not rule.opening_snippets and not rule.opening_regexes):
        return body, False, "", 0, 0
    return trim_opening_by_rule(body, rule)


def maybe_trim_closing(args: SimpleNamespace, body: str) -> tuple[str, bool, str, int, int]:
    rule = get_trim_rule(args)
    if not rule or not rule.closing_markers:
        return body, False, "", 0, 0
    return trim_closing_by_rule(body, rule)


def apply_trim_metadata(args: SimpleNamespace, body: str) -> str:
    body, opening_trim_applied, opening_trim_rule, opening_trim_chars_saved, opening_trim_words_saved = maybe_trim_opening(args, body)
    body, closing_trim_applied, closing_trim_rule, closing_trim_chars_saved, closing_trim_words_saved = maybe_trim_closing(args, body)
    args.opening_trim_applied = opening_trim_applied
    args.opening_trim_rule = opening_trim_rule
    args.opening_trim_chars_saved = opening_trim_chars_saved
    args.opening_trim_words_saved = opening_trim_words_saved
    args.closing_trim_applied = closing_trim_applied
    args.closing_trim_rule = closing_trim_rule
    args.closing_trim_chars_saved = closing_trim_chars_saved
    args.closing_trim_words_saved = closing_trim_words_saved
    return body


def split_source_document(text: str) -> tuple[list[str], str, str] | None:
    if not text.startswith("---\n"):
        return None
    parts = text.split("---", 2)
    if len(parts) < 3:
        return None
    frontmatter_lines = parts[1].splitlines()
    content = parts[2]
    if "## Transcript" in content:
        body_prefix, transcript_body = content.split("## Transcript", 1)
        return frontmatter_lines, body_prefix + "## Transcript\n\n", transcript_body.lstrip()

    heading_match = re.search(r"(?m)^# .+\n", content)
    if not heading_match:
        return None
    after_heading = content[heading_match.end():]
    metadata_block_match = re.match(r"(?:\n|[^\n]*\n)*(?:\n){2}", after_heading)
    if metadata_block_match:
        prefix = content[: heading_match.end() + metadata_block_match.end()]
        body = content[heading_match.end() + metadata_block_match.end():]
        return frontmatter_lines, prefix, body.lstrip()
    return frontmatter_lines, content[: heading_match.end() + len(after_heading)], ""


def parse_frontmatter_lines(lines: list[str]) -> dict[str, str]:
    data: dict[str, str] = {}
    for line in lines:
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip()
    return data


def unquote_scalar(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        return value[1:-1]
    return value


def truthy_scalar(value: str | None) -> bool:
    return unquote_scalar(value or "").lower() == "true"


def build_trim_field_lines(args: SimpleNamespace) -> list[str]:
    return [
        f"opening_trim_applied: {'true' if args.opening_trim_applied else 'false'}",
        f"opening_trim_rule: {yaml_quote(args.opening_trim_rule)}",
        f"opening_trim_chars_saved: {args.opening_trim_chars_saved}",
        f"opening_trim_words_saved: {args.opening_trim_words_saved}",
        f"closing_trim_applied: {'true' if args.closing_trim_applied else 'false'}",
        f"closing_trim_rule: {yaml_quote(args.closing_trim_rule)}",
        f"closing_trim_chars_saved: {args.closing_trim_chars_saved}",
        f"closing_trim_words_saved: {args.closing_trim_words_saved}",
    ]


def normalize_frontmatter_trim_fields(frontmatter_lines: list[str], args: SimpleNamespace) -> list[str]:
    new_lines: list[str] = []
    inserted = False
    for line in frontmatter_lines:
        stripped = line.strip()
        key = stripped.split(":", 1)[0] if ":" in stripped else ""
        if key in TRIM_FIELD_ORDER:
            continue
        new_lines.append(line)
        if key == "routing_state":
            new_lines.extend(build_trim_field_lines(args))
            inserted = True

    if not inserted:
        new_lines.extend(build_trim_field_lines(args))
    return new_lines


def retrofit_source(path: Path, since_date: str, dry_run: bool = False) -> str | None:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return None
    parts = text.split("---", 2)
    if len(parts) < 3:
        return None
    frontmatter_lines = parts[1].splitlines()
    frontmatter = parse_frontmatter_lines(frontmatter_lines)
    host_slug = unquote_scalar(frontmatter.get("host_slug", "")) or unquote_scalar(frontmatter.get("channel_slug", ""))
    if not host_slug and path.name.startswith("source-alexander-mercouris-"):
        host_slug = "alexander-mercouris"
    pub_date = unquote_scalar(frontmatter.get("pub_date", ""))
    if not host_slug or host_slug not in HOST_TRIM_RULES or pub_date < since_date:
        return None
    split = split_source_document(text)
    if split is None:
        return f"SKIP malformed {path.relative_to(REPO_ROOT).as_posix()}"

    _, body_prefix, body = split

    args = SimpleNamespace(
        host_slug=host_slug,
        trim_opening="auto",
        opening_trim_applied=False,
        opening_trim_rule="",
        opening_trim_chars_saved=0,
        opening_trim_words_saved=0,
        closing_trim_applied=False,
        closing_trim_rule="",
        closing_trim_chars_saved=0,
        closing_trim_words_saved=0,
    )
    trimmed_body = apply_trim_metadata(args, body)
    new_frontmatter_lines = normalize_frontmatter_trim_fields(frontmatter_lines, args)
    new_text = "---\n" + "\n".join(new_frontmatter_lines) + "\n---" + body_prefix + trimmed_body.rstrip() + "\n"

    body_changed = trimmed_body != body
    metadata_changed = new_frontmatter_lines != frontmatter_lines
    if not body_changed and not metadata_changed:
        return f"UNCHANGED {path.relative_to(REPO_ROOT).as_posix()}"

    if not dry_run:
        path.write_text(new_text, encoding="utf-8", newline="\n")

    if body_changed:
        return (
            f"TRIMMED {path.relative_to(REPO_ROOT).as_posix()} "
            f"opening={args.opening_trim_chars_saved} closing={args.closing_trim_chars_saved}"
        )
    return f"NORMALIZED {path.relative_to(REPO_ROOT).as_posix()}"


def backfill_sources(since_date: str, dry_run: bool = False) -> list[str]:
    messages: list[str] = []
    for path in sorted(ARCHIVE_SOURCES_ROOT.rglob("source-*.md")):
        result = retrofit_source(path, since_date, dry_run=dry_run)
        if result:
            messages.append(result)
    return messages


def source_plan(args: SimpleNamespace) -> tuple[Path, str, str]:
    title_core_slug = slugify(args.title)
    file_slug = f"source-{title_core_slug}-{args.pub_date}.md"
    title_slug = f"transcript-{title_core_slug}-{args.pub_date}"
    day_dir = ARCHIVE_ROOT / "sources" / args.pub_date
    source_path = day_dir / file_slug
    upstream_path = args.upstream_path or f"operator-paste://{args.ingest_date}/{title_core_slug}"
    return source_path, title_slug, upstream_path


def land_one(args: SimpleNamespace, manifest: dict) -> tuple[str, int]:
    body_path = Path(args.body_file)
    if not body_path.is_file():
        raise FileNotFoundError(f"Body file not found: {body_path}")

    source_path, title_slug, upstream_path = source_plan(args)
    body = body_path.read_text(encoding="utf-8")
    body = apply_trim_metadata(args, body)
    frontmatter_doc = build_frontmatter(args, title_slug, body)
    manifest_row = build_manifest_row(args, source_path, upstream_path)

    if args.dry_run:
        return (
            f"DRY RUN: {source_path.relative_to(REPO_ROOT).as_posix()}\n"
            f"{json.dumps(manifest_row, indent=2)}",
            len(manifest.get("sources", [])),
        )

    if source_path.exists():
        raise FileExistsError(f"Refusing to overwrite existing source file: {source_path}")

    day_dir = source_path.parent
    day_dir.mkdir(parents=True, exist_ok=True)
    source_path.write_text(frontmatter_doc, encoding="utf-8", newline="\n")

    manifest_sources = manifest.get("sources")
    if not isinstance(manifest_sources, list):
        raise ValueError("Manifest format error: 'sources' is not a list.")

    manifest_sources.append(manifest_row)
    manifest["source_count"] = len(manifest_sources)
    return (
        f"Landed source: {source_path.relative_to(REPO_ROOT).as_posix()}",
        manifest["source_count"],
    )


def metadata_files_from_batch_dir(batch_dir: Path) -> list[Path]:
    if not batch_dir.is_dir():
        raise NotADirectoryError(f"Batch directory not found: {batch_dir}")
    files = [
        path
        for path in sorted(batch_dir.iterdir())
        if path.is_file() and path.suffix.lower() in METADATA_SUFFIXES
    ]
    if not files:
        raise FileNotFoundError(f"No metadata sidecars found in: {batch_dir}")
    return files


def gather_sources(cli_args: argparse.Namespace) -> list[SimpleNamespace]:
    mode_count = sum(bool(item) for item in (cli_args.metadata_file, cli_args.batch_dir))
    if mode_count > 1:
        raise ValueError("Choose only one of --metadata-file or --batch-dir.")

    if cli_args.batch_dir:
        batch_dir = Path(cli_args.batch_dir)
        return [
            args_from_metadata(parse_metadata_file(path), path, cli_args)
            for path in metadata_files_from_batch_dir(batch_dir)
        ]

    if cli_args.metadata_file:
        metadata_path = Path(cli_args.metadata_file)
        if not metadata_path.is_file():
            raise FileNotFoundError(f"Metadata file not found: {metadata_path}")
        return [args_from_metadata(parse_metadata_file(metadata_path), metadata_path, cli_args)]

    return [args_from_cli(cli_args)]


def main() -> int:
    cli_args = parse_args()

    try:
        if cli_args.backfill_since:
            messages = backfill_sources(cli_args.backfill_since, dry_run=cli_args.dry_run)
            print("\n".join(messages))
            return 0
        source_args = gather_sources(cli_args)
        manifest = load_manifest()
        messages: list[str] = []
        for item in source_args:
            message, manifest_count = land_one(item, manifest)
            messages.append(message)
        if not cli_args.dry_run:
            write_manifest(manifest)
            messages.append(f"Manifest count: {manifest_count}")
        print("\n".join(messages))
        return 0
    except Exception as exc:  # noqa: BLE001
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
