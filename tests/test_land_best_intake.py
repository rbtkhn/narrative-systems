from __future__ import annotations

import importlib.util
import shutil
import sys
import uuid
from pathlib import Path
from types import SimpleNamespace


REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPT_PATH = REPO_ROOT / "scripts" / "land_best_intake.py"
REPORT_PATH = REPO_ROOT / "scripts" / "report_trim_stats.py"


def load_module(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


land_best_intake = load_module("land_best_intake", SCRIPT_PATH)
report_trim_stats = load_module("report_trim_stats", REPORT_PATH)


def trim_args(host_slug: str | None, mode: str = "auto") -> SimpleNamespace:
    return SimpleNamespace(host_slug=host_slug, trim_opening=mode)


def make_local_temp_dir() -> Path:
    root = REPO_ROOT / ".codex-test-temp"
    root.mkdir(exist_ok=True)
    path = root / f"trim-{uuid.uuid4().hex}"
    path.mkdir()
    return path


def test_mario_opening_trim_applies_before_substance() -> None:
    body = "Hey guys thanks for waiting.\nSo just to kind of recap for the audience Iran struck ships.\n"

    trimmed, applied, rule, chars_saved, words_saved = land_best_intake.maybe_trim_opening(
        trim_args("mario-nawfal"),
        body,
    )

    assert applied is True
    assert rule == "mario-nawfal-v1"
    assert trimmed.startswith("So just to kind of recap for the audience")
    assert chars_saved == len("Hey guys thanks for waiting.\n")
    assert words_saved == land_best_intake.count_words("Hey guys thanks for waiting.\n")


def test_mario_opening_marker_at_position_zero_does_not_trim() -> None:
    body = "So just to kind of recap for the audience Iran struck ships.\n"

    trimmed, applied, rule, chars_saved, words_saved = land_best_intake.maybe_trim_opening(
        trim_args("mario-nawfal"),
        body,
    )

    assert trimmed == body
    assert applied is False
    assert rule == ""
    assert chars_saved == 0
    assert words_saved == 0


def test_daniel_davis_closing_trim_uses_earliest_marker() -> None:
    body = (
        "Substantive ending.\n"
        "And uh we will be back in about 1 hour.\n"
        "You know we don't have sponsors cuz we hate to hit you over the head with ads.\n"
    )

    trimmed, applied, rule, chars_saved, words_saved = land_best_intake.maybe_trim_closing(
        trim_args("daniel-davis"),
        body,
    )

    removed = (
        "And uh we will be back in about 1 hour.\n"
        "You know we don't have sponsors cuz we hate to hit you over the head with ads.\n"
    )
    assert applied is True
    assert rule == "daniel-davis-closing-v1"
    assert trimmed == "Substantive ending.\n"
    assert chars_saved == len(removed)
    assert words_saved == land_best_intake.count_words(removed)


def test_daniel_davis_closing_trim_cuts_at_next_episode_marker() -> None:
    body = (
        "Substantive ending.\n"
        "We'll see you on the next episode of the Daniel Davis deep dive.\n"
        "You know, I don't try to talk you into buying gold or tell you how to run your stock portfolio, but there is a way you can help us.\n"
    )

    trimmed, applied, rule, chars_saved, words_saved = land_best_intake.maybe_trim_closing(
        trim_args("daniel-davis"),
        body,
    )

    removed = (
        "We'll see you on the next episode of the Daniel Davis deep dive.\n"
        "You know, I don't try to talk you into buying gold or tell you how to run your stock portfolio, but there is a way you can help us.\n"
    )
    assert applied is True
    assert rule == "daniel-davis-closing-v1"
    assert trimmed == "Substantive ending.\n"
    assert chars_saved == len(removed)
    assert words_saved == land_best_intake.count_words(removed)


def test_mercouris_opening_snippet_trim_removes_subscribe_sentence_only() -> None:
    body = (
        "Good day. Today is Monday, 1st June 2026. "
        "And before I proceed with this program, let me remind you again to tick the like button "
        "and to check your subscription to this channel. "
        "Well, today we continue to have the two ongoing conflicts.\n"
    )

    trimmed, applied, rule, chars_saved, words_saved = land_best_intake.maybe_trim_opening(
        trim_args("alexander-mercouris"),
        body,
    )

    removed = (
        " And before I proceed with this program, let me remind you again to tick the like button "
        "and to check your subscription to this channel. "
    )
    assert applied is True
    assert rule == "alexander-mercouris-v1"
    assert trimmed == "Good day. Today is Monday, 1st June 2026. Well, today we continue to have the two ongoing conflicts.\n"
    assert chars_saved == len(removed)
    assert words_saved == land_best_intake.count_words(removed)


def test_mercouris_closing_trim_cuts_at_close_heading() -> None:
    body = (
        "Substantive ending.\n"
        "\n"
        "### Close - Platforms And Subscribe\n"
        "\n"
        "Anyway, this is where I'm going to finish today's program.\n"
    )

    trimmed, applied, rule, chars_saved, words_saved = land_best_intake.maybe_trim_closing(
        trim_args("alexander-mercouris"),
        body,
    )

    removed = (
        "\n### Close - Platforms And Subscribe\n"
        "\n"
        "Anyway, this is where I'm going to finish today's program.\n"
    )
    assert applied is True
    assert rule == "alexander-mercouris-v1"
    assert trimmed == "Substantive ending.\n"
    assert chars_saved == len(removed)
    assert words_saved == land_best_intake.count_words(removed)


def test_mercouris_closing_trim_cuts_at_i_am_finish_variant() -> None:
    body = (
        "Substantive ending.\n"
        "Anyway, this is where I am going to finish today's program.\n"
        "Let me remind you again that you can find all our programs on our various platforms.\n"
    )

    trimmed, applied, rule, chars_saved, words_saved = land_best_intake.maybe_trim_closing(
        trim_args("alexander-mercouris"),
        body,
    )

    removed = (
        "Anyway, this is where I am going to finish today's program.\n"
        "Let me remind you again that you can find all our programs on our various platforms.\n"
    )
    assert applied is True
    assert rule == "alexander-mercouris-v1"
    assert trimmed == "Substantive ending.\n"
    assert chars_saved == len(removed)
    assert words_saved == land_best_intake.count_words(removed)


def test_dialogue_works_opening_trim_removes_youtube_transcript_wrapper() -> None:
    body = (
        "Larry Johnson: Iran Strikes US Bases in Bahrain & Kuwait After US Strikes South Iran - Hormuz CLOSED - YouTube\n"
        "\n"
        "Transcripts:\n"
        "Hi everybody. Today's Wednesday, July 8th, 2026.\n"
    )

    trimmed, applied, rule, chars_saved, words_saved = land_best_intake.maybe_trim_opening(
        trim_args("dialogue-works"),
        body,
    )

    removed = (
        "Larry Johnson: Iran Strikes US Bases in Bahrain & Kuwait After US Strikes South Iran - Hormuz CLOSED - YouTube\n"
        "\n"
        "Transcripts:\n"
    )
    assert applied is True
    assert rule == "dialogue-works-wrapper-v1"
    assert trimmed == "Hi everybody. Today's Wednesday, July 8th, 2026.\n"
    assert chars_saved == len(removed)
    assert words_saved == land_best_intake.count_words(removed)


def test_dialogue_works_opening_trim_leaves_plain_transcript_alone() -> None:
    body = "Hi everybody. Today's Wednesday, July 8th, 2026.\n"

    trimmed, applied, rule, chars_saved, words_saved = land_best_intake.maybe_trim_opening(
        trim_args("dialogue-works"),
        body,
    )

    assert trimmed == body
    assert applied is False
    assert rule == ""
    assert chars_saved == 0
    assert words_saved == 0


def test_none_mode_disables_all_trimming() -> None:
    body = (
        "noise\nSo just to kind of recap for the audience test.\n"
        "And uh we will be back in about 1 hour.\n"
    )
    args = trim_args("mario-nawfal", mode="none")

    opening = land_best_intake.maybe_trim_opening(args, body)
    closing = land_best_intake.maybe_trim_closing(args, body)

    assert opening == (body, False, "", 0, 0)
    assert closing == (body, False, "", 0, 0)


def test_unapproved_host_is_left_unchanged_in_auto_mode() -> None:
    body = "Oh, I can't hear you, by the way.\nHi everybody.\n"

    opening = land_best_intake.maybe_trim_opening(trim_args("glenn-diesen"), body)
    closing = land_best_intake.maybe_trim_closing(trim_args("glenn-diesen"), body)

    assert opening == (body, False, "", 0, 0)
    assert closing == (body, False, "", 0, 0)


def test_frontmatter_includes_rule_and_metric_fields() -> None:
    args = SimpleNamespace(
        ingest_date="2026-07-08",
        pub_date="2026-07-07",
        kind="cleaned-transcript",
        source_form="interview",
        host_people=["Mario Nawfal"],
        guest_people=["Brandon Weichert"],
        show_title="Mario Nawfal",
        channel_name="Mario Nawfal",
        show="Mario Nawfal",
        host="Mario Nawfal",
        guest="Brandon Weichert",
        thread="weichert",
        voice_slugs=["weichert"],
        url="https://example.com",
        source_note="note",
        editorial_note="note",
        review_state="unreviewed",
        routing_state="provisional",
        opening_trim_applied=True,
        opening_trim_rule="mario-nawfal-v1",
        opening_trim_chars_saved=25,
        opening_trim_words_saved=5,
        closing_trim_applied=True,
        closing_trim_rule="mario-nawfal-v1",
        closing_trim_chars_saved=50,
        closing_trim_words_saved=10,
        title="Example Title",
    )

    doc = land_best_intake.build_frontmatter(args, "transcript-example", "Body\n")

    assert 'opening_trim_rule: "mario-nawfal-v1"' in doc
    assert "opening_trim_chars_saved: 25" in doc
    assert 'closing_trim_rule: "mario-nawfal-v1"' in doc
    assert "closing_trim_words_saved: 10" in doc


def test_report_frontmatter_parser_extracts_generated_fields() -> None:
    text = (
        "---\n"
        'host_slug: "daniel-davis"\n'
        "opening_trim_applied: false\n"
        "opening_trim_chars_saved: 0\n"
        "closing_trim_applied: true\n"
        "closing_trim_chars_saved: 120\n"
        "---\n"
        "# Example\n"
        "\n"
        "## Transcript\n"
        "\n"
        "Body\n"
    )

    parsed = report_trim_stats.parse_frontmatter(text)

    assert parsed["host_slug"] == "daniel-davis"
    assert parsed["closing_trim_applied"] == "true"
    assert parsed["closing_trim_chars_saved"] == "120"


def test_retrofit_source_trims_body_and_normalizes_metadata() -> None:
    tmp_dir = make_local_temp_dir()
    try:
        source = tmp_dir / "source-test.md"
        source.write_text(
            "---\n"
            "pub_date: 2026-07-07\n"
            "host_slug: daniel-davis\n"
            "routing_state: provisional\n"
            "---\n"
            "# Example\n"
            "\n"
            "## Transcript\n"
            "\n"
            "Substantive ending.\n"
            "And uh we will be back in about 1 hour.\n"
            "You know we don't have sponsors cuz we hate to hit you over the head with ads.\n",
            encoding="utf-8",
        )

        result = land_best_intake.retrofit_source(source, "2026-06-01")
        text = source.read_text(encoding="utf-8")

        assert result is not None
        assert result.startswith("TRIMMED")
        assert "closing_trim_applied: true" in text
        assert 'closing_trim_rule: "daniel-davis-closing-v1"' in text
        assert "And uh we will be back in about 1 hour." not in text
    finally:
        shutil.rmtree(tmp_dir)


def test_retrofit_source_normalizes_without_trimming() -> None:
    tmp_dir = make_local_temp_dir()
    try:
        source = tmp_dir / "source-test.md"
        source.write_text(
            "---\n"
            "pub_date: 2026-07-07\n"
            "host_slug: daniel-davis\n"
            "routing_state: provisional\n"
            "---\n"
            "# Example\n"
            "\n"
            "## Transcript\n"
            "\n"
            "Fully substantive ending only.\n",
            encoding="utf-8",
        )

        result = land_best_intake.retrofit_source(source, "2026-06-01")
        text = source.read_text(encoding="utf-8")

        expected_rel = source.relative_to(REPO_ROOT).as_posix()
        assert result == f"NORMALIZED {expected_rel}"
        assert "opening_trim_applied: false" in text
        assert 'opening_trim_rule: ""' in text
        assert "closing_trim_applied: false" in text
    finally:
        shutil.rmtree(tmp_dir)


def test_retrofit_source_normalizes_dialogue_works_without_wrapper_trim() -> None:
    tmp_dir = make_local_temp_dir()
    try:
        source = tmp_dir / "source-test.md"
        original = (
            "---\n"
            "pub_date: 2026-07-07\n"
            "host_slug: dialogue-works\n"
            "routing_state: provisional\n"
            "---\n"
            "# Example\n"
            "\n"
            "## Transcript\n"
            "\n"
            "Oh, I can't hear you, by the way.\n"
        )
        source.write_text(original, encoding="utf-8")

        result = land_best_intake.retrofit_source(source, "2026-06-01")
        text = source.read_text(encoding="utf-8")

        expected_rel = source.relative_to(REPO_ROOT).as_posix()
        assert result == f"NORMALIZED {expected_rel}"
        assert "Oh, I can't hear you, by the way.\n" in text
        assert "opening_trim_applied: false" in text
        assert "closing_trim_applied: false" in text
    finally:
        shutil.rmtree(tmp_dir)


def test_retrofit_source_uses_channel_slug_for_mercouris() -> None:
    tmp_dir = make_local_temp_dir()
    try:
        source = tmp_dir / "source-test.md"
        source.write_text(
            "---\n"
            "pub_date: 2026-06-10\n"
            "channel_slug: alexander-mercouris\n"
            "routing_state: provisional\n"
            "---\n"
            "# Example\n"
            "\n"
            "## Transcript\n"
            "\n"
            "Good day. Today is Wednesday 10th June 2026. "
            "And before I proceed with this program, let me remind you again to tick the like button "
            "and to check your subscription to this channel. "
            "Main body.\n"
            "\n"
            "### Close - Platforms And Subscribe\n"
            "\n"
            "Anyway, this is where I'm going to finish today's program.\n",
            encoding="utf-8",
        )

        result = land_best_intake.retrofit_source(source, "2026-06-01")
        text = source.read_text(encoding="utf-8")

        assert result is not None
        assert result.startswith("TRIMMED")
        assert 'opening_trim_rule: "alexander-mercouris-v1"' in text
        assert 'closing_trim_rule: "alexander-mercouris-v1"' in text
        assert "tick the like button" not in text
        assert "### Close - Platforms And Subscribe" not in text
    finally:
        shutil.rmtree(tmp_dir)


def test_retrofit_source_uses_filename_fallback_for_mercouris() -> None:
    tmp_dir = make_local_temp_dir()
    try:
        source = tmp_dir / "source-alexander-mercouris-example-2026-06-11.md"
        source.write_text(
            "---\n"
            "pub_date: 2026-06-11\n"
            "routing_state: provisional\n"
            "---\n"
            "# Example\n"
            "\n"
            "## Transcript\n"
            "\n"
            "Good day. Today is Wednesday 11th June 2026. "
            "And before I proceed with this program, let me remind you again to tick the like button "
            "and to check your subscription to this channel. "
            "Main body.\n"
            "\n"
            "Let me remind you again, you can find all our programs on our various platforms, Locals, Rumble, X, and Substack.\n",
            encoding="utf-8",
        )

        result = land_best_intake.retrofit_source(source, "2026-06-01")
        text = source.read_text(encoding="utf-8")

        assert result is not None
        assert result.startswith("TRIMMED")
        assert 'opening_trim_rule: "alexander-mercouris-v1"' in text
        assert 'closing_trim_rule: "alexander-mercouris-v1"' in text
    finally:
        shutil.rmtree(tmp_dir)
