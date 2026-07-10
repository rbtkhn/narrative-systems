from __future__ import annotations

import importlib.util
import shutil
import sys
import uuid
from pathlib import Path
from types import SimpleNamespace

import pytest


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
    return SimpleNamespace(
        host_slug=host_slug,
        trim_opening=mode,
        asr_repair="auto",
        asr_repair_applied=False,
        asr_repair_pass="",
        sectioning="auto",
        title="Example Title",
        source_form="interview",
    )


def make_local_temp_dir() -> Path:
    root = REPO_ROOT / ".codex-test-temp"
    root.mkdir(exist_ok=True)
    path = root / f"trim-{uuid.uuid4().hex}"
    path.mkdir()
    return path


def build_fast_args(pub_date: str, url: str, title: str, body_text: str) -> SimpleNamespace:
    return SimpleNamespace(
        pub_date=pub_date,
        ingest_date=pub_date,
        title=title,
        url=url,
        body_file="",
        body_text=body_text,
        voice_slugs=[],
        host_slug=None,
        host="",
        guest="",
        host_people=[],
        guest_people=[],
        show_title="",
        channel_name="",
        show="",
        thread=None,
        kind="cleaned-transcript",
        source_form="interview",
        source_class="guest interview pressure test",
        modality="cleaned-transcript",
        review_state="unreviewed",
        routing_state="provisional",
        source_note="",
        editorial_note="Preserve as raw cleaned transcript. Not human-verified verbatim.",
        upstream_path=None,
        dry_run=True,
        trim_opening="auto",
        asr_repair="auto",
        sectioning="auto",
        opening_trim_applied=False,
        opening_trim_rule="",
        opening_trim_chars_saved=0,
        opening_trim_words_saved=0,
        closing_trim_applied=False,
        closing_trim_rule="",
        closing_trim_chars_saved=0,
        closing_trim_words_saved=0,
        transcript_curation="preserved_unsectioned",
        section_count=0,
        section_pass=land_best_intake.SECTIONING_PASS_LABEL,
        asr_repair_applied=False,
        asr_repair_pass="",
    )


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
        transcript_curation="curated_sectioned",
        section_count=3,
        section_pass="2026-07-09 semantic-section-v1",
        title="Example Title",
    )

    doc = land_best_intake.build_frontmatter(args, "transcript-example", "Body\n")

    assert 'opening_trim_rule: "mario-nawfal-v1"' in doc
    assert "opening_trim_chars_saved: 25" in doc
    assert 'closing_trim_rule: "mario-nawfal-v1"' in doc
    assert "closing_trim_words_saved: 10" in doc
    assert "transcript_curation: curated_sectioned" in doc
    assert "section_count: 3" in doc


def stale_section_transcript_creates_show_open_and_segments_for_clear_dialogue_works_shape() -> None:
    body = (
        "Hi everybody. Today we have to talk about the White House terms for Iran and the shipping crisis in Hormuz.\n\n"
        "I want to ask first about the White House offer and whether Tehran sees it as coercive diplomacy.\n\n"
        "Another point is the regional shipping lane, insurance costs, and whether the blockade threat is credible.\n"
    )

    rewritten, curation, section_count, skip_reason = land_best_intake.section_transcript(
        trim_args("dialogue-works"),
        body,
    )

    assert curation == "curated_sectioned"
    assert section_count >= 2
    assert skip_reason == ""
    assert rewritten.startswith("### Show Open — ")
    assert "\n### Segment 2 — " in rewritten
    assert "White House" in rewritten or "Shipping" in rewritten


def test_derive_topic_label_prefers_domain_topics_over_asr_surface_noise() -> None:
    block = (
        "policy for even a 15minute span. So all of this is to say it is perfectly plain why Iran would say what are we even talking about? "
        "But I would say we don't have to be completely pessimistic about it because there's a better alternative than a negotiated agreement and that is the United States should just stop what it's doing and go home. "
        "If the US goes home, Iran is going to open the straight of Hormuz and there's going to be some normalization of the world energy markets."
    )

    label = land_best_intake.derive_topic_label(block, "Prof. Jeffrey Sachs : How the Best Military and Intel Failed")

    assert label
    assert "Policy For Even" not in label
    assert "Iran" in label or "Hormuz" in label or "US" in label


def test_derive_topic_label_prefers_structural_phrases_like_white_house() -> None:
    block = (
        "I want to ask first about the White House offer and whether Tehran sees it as coercive diplomacy. "
        "Another point is the regional shipping lane, insurance costs, and whether the blockade threat is credible."
    )

    label = land_best_intake.derive_topic_label(block, "Example Dialogue Works Source")

    assert label
    assert "White House" in label or "Shipping Lane" in label


def test_derive_topic_label_filters_low_signal_asr_noise_tokens() -> None:
    block = (
        "These big questions are what the president keeps saying. "
        "Meanwhile Iran and Hormuz remain the substantive issue. "
        "Iran still holds leverage over Hormuz and shipping."
    )

    label = land_best_intake.derive_topic_label(block, "Example Source")

    assert label
    assert "These" not in label
    assert "Big" not in label
    assert "Questions" not in label
    assert "President" not in label
    assert "Iran" in label or "Hormuz" in label


def test_cleanup_section_label_drops_trailing_noise_words() -> None:
    label = land_best_intake.cleanup_section_label("Israel Big Questions It's")

    assert label == "Israel"


def test_derive_topic_label_does_not_promote_title_flavored_singletons() -> None:
    block = (
        "The president has to hear more than one perspective. "
        "Iran and Israel remain the real issue. "
        "Iran is central here and Israel keeps driving escalation. "
        "The Strait of Hormuz remains part of the pressure story."
    )

    label = land_best_intake.derive_topic_label(block, "Iran Trump Russia Hear")

    assert label
    assert "Hear" not in label
    assert "Iran" in label


def test_derive_topic_label_prefers_multiword_domain_phrases_when_available() -> None:
    block = (
        "The strategic petroleum reserve is being drained while fertilizer costs rise. "
        "The American people will feel the pressure if energy markets tighten further. "
        "That is the real economic risk in this war."
    )

    label = land_best_intake.derive_topic_label(block, "Example Source")

    assert label
    assert "Strategic Petroleum Reserve" in label or "American People" in label or "Fertilizer" in label


def test_derive_topic_label_prefers_missile_city_cluster_over_noise_tokens() -> None:
    block = (
        "Iran's missile cities and missile factories remain intact. "
        "The IRGC can reopen tunnel access with bulldozers and mountain ranges still protect the sites. "
        "That is why the strike campaign failed."
    )

    label = land_best_intake.derive_topic_label(block, "Example Source")

    assert label
    assert "Missile Cities" in label or "Missile Factories" in label or "IRGC" in label


def test_section_transcript_skips_when_cues_are_weak() -> None:
    body = (
        "This is one long transcript paragraph about events.\n\n"
        "It continues in roughly the same register without a strong pivot.\n\n"
        "Nothing here clearly marks a section transition or semantic turn.\n"
    )

    rewritten, curation, section_count, skip_reason = land_best_intake.section_transcript(
        trim_args("glenn-diesen"),
        body,
    )

    assert rewritten == body
    assert curation == "preserved_unsectioned"
    assert section_count == 0
    assert skip_reason in {"weak-cues", "unclean-open-label", "unclean-segment-label"}


def test_section_transcript_respects_none_mode() -> None:
    args = trim_args("dialogue-works")
    args.sectioning = "none"
    body = "Hi everybody.\n\nI want to ask about Iran.\n\nAnother point is Russia.\n"

    rewritten, curation, section_count, skip_reason = land_best_intake.section_transcript(args, body)

    assert rewritten == body
    assert curation == "preserved_unsectioned"
    assert section_count == 0
    assert skip_reason == "disabled"


def test_update_editorial_note_appends_section_pass_suffix() -> None:
    updated = land_best_intake.update_editorial_note(
        "Preserve as raw cleaned transcript. Not human-verified verbatim.",
        "curated_sectioned",
        4,
    )

    assert "source-section pass 2026-07-09 (4 sections)." in updated


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
        assert "transcript_curation: preserved_unsectioned" in text
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


def stale_retrofit_source_sections_clear_eligible_transcript() -> None:
    tmp_dir = make_local_temp_dir()
    try:
        source = tmp_dir / "source-test.md"
        source.write_text(
            "---\n"
            "pub_date: 2026-07-07\n"
            "host_slug: dialogue-works\n"
            "title: Example Dialogue Works Source\n"
            "source_form: interview\n"
            "editorial_note: Preserve as raw cleaned transcript. Not human-verified verbatim.\n"
            "routing_state: provisional\n"
            "---\n"
            "# Example\n"
            "\n"
            "## Transcript\n"
            "\n"
            "Hi everybody. Today we are looking at White House demands on Iran and the Hormuz crisis.\n"
            "\n"
            "I want to ask about the White House position and whether it can force Tehran into concessions.\n"
            "\n"
            "Another point is the shipping lane, insurance markets, and whether closure pressure can hold.\n",
            encoding="utf-8",
        )

        result = land_best_intake.retrofit_source(source, "2026-06-01")
        text = source.read_text(encoding="utf-8")

        assert result is not None
        assert result.startswith("TRIMMED")
        assert "transcript_curation: curated_sectioned" in text
        assert "section_count: 2" in text or "section_count: 3" in text
        assert "### Show Open — " in text
        assert "source-section pass 2026-07-09" in text
    finally:
        shutil.rmtree(tmp_dir)


def stale_retrofit_source_preserves_existing_sectioned_body_without_force() -> None:
    tmp_dir = make_local_temp_dir()
    try:
        source = tmp_dir / "source-test.md"
        original = (
            "---\n"
            "pub_date: 2026-07-07\n"
            "host_slug: dialogue-works\n"
            "transcript_curation: curated_sectioned\n"
            "section_count: 2\n"
            "section_pass: \"2026-07-01 semantic-section-v1\"\n"
            "routing_state: provisional\n"
            "---\n"
            "# Example\n"
            "\n"
            "## Transcript\n"
            "\n"
            "### Show Open — Existing\n"
            "\n"
            "Already sectioned block.\n"
            "\n"
            "### Segment 2 — Existing Turn\n"
            "\n"
            "Second block.\n"
        )
        source.write_text(original, encoding="utf-8")

        result = land_best_intake.retrofit_source(source, "2026-06-01")
        text = source.read_text(encoding="utf-8")

        assert result is not None
        assert result.startswith("NORMALIZED") or result.startswith("UNCHANGED")
        assert "### Show Open — Existing" in text
        assert text.count("### ") == 2
    finally:
        shutil.rmtree(tmp_dir)


def test_section_transcript_creates_show_open_and_segments_for_clear_dialogue_works_shape() -> None:
    body = (
        "Hi everybody. Today we have to talk about the White House terms for Iran and the shipping crisis in Hormuz.\n\n"
        "I want to ask first about the White House offer and whether Tehran sees it as coercive diplomacy.\n\n"
        "Another point is the regional shipping lane, insurance costs, and whether the blockade threat is credible.\n"
    )

    rewritten, curation, section_count, skip_reason = land_best_intake.section_transcript(
        trim_args("dialogue-works"),
        body,
    )

    assert curation == "curated_sectioned"
    assert section_count >= 2
    assert skip_reason == ""
    assert rewritten.startswith("### Show Open - ")
    assert "\n### Segment 2 - " in rewritten
    assert "White House" in rewritten or "Shipping" in rewritten


def test_repair_asr_text_repairs_global_phrase_corruption() -> None:
    args = trim_args("daniel-davis")
    body = "The whole thing with the straight of hormones was breaking down in Anchora.\n"

    repaired = land_best_intake.repair_asr_text(args, body)

    assert repaired == "The whole thing with the Strait of Hormuz was breaking down in Ankara.\n"
    assert args.asr_repair_applied is True
    assert args.asr_repair_pass == "2026-07-09 asr-repair-v1"


def test_repair_asr_text_repairs_host_specific_noise() -> None:
    args = trim_args("mario-nawfal")
    body = (
        "This is all part of the plan. They just want breathing space before they continue their operation to capture Khagan and whatever. "
        "Do you think this argument is gaining more weight? want breathing space before they continue their operation to capture car guy into whatever do you think you know this argument is gaining more weight "
        "i don't think there is any grand plan.\n"
    )

    repaired = land_best_intake.repair_asr_text(args, body)

    assert "capture car guy" not in repaired
    assert "Kharg Island" in repaired
    assert args.asr_repair_applied is True


def test_repair_asr_text_respects_none_mode() -> None:
    args = trim_args("daniel-davis")
    args.asr_repair = "none"
    body = "The whole thing with the straight of hormones stayed broken in Anchora.\n"

    repaired = land_best_intake.repair_asr_text(args, body)

    assert repaired == body
    assert args.asr_repair_applied is False
    assert args.asr_repair_pass == ""


def test_retrofit_source_sections_clear_eligible_transcript() -> None:
    tmp_dir = make_local_temp_dir()
    try:
        source = tmp_dir / "source-test.md"
        source.write_text(
            "---\n"
            "pub_date: 2026-07-07\n"
            "host_slug: dialogue-works\n"
            "title: Example Dialogue Works Source\n"
            "source_form: interview\n"
            "editorial_note: Preserve as raw cleaned transcript. Not human-verified verbatim.\n"
            "routing_state: provisional\n"
            "---\n"
            "# Example\n"
            "\n"
            "## Transcript\n"
            "\n"
            "Hi everybody. Today we are looking at White House demands on Iran and the Hormuz crisis.\n"
            "\n"
            "I want to ask about the White House position and whether it can force Tehran into concessions.\n"
            "\n"
            "Another point is the shipping lane, insurance markets, and whether closure pressure can hold.\n",
            encoding="utf-8",
        )

        result = land_best_intake.retrofit_source(source, "2026-06-01")
        text = source.read_text(encoding="utf-8")

        assert result is not None
        assert result.startswith("TRIMMED")
        assert "transcript_curation: curated_sectioned" in text
        assert "section_count: 2" in text or "section_count: 3" in text
        assert "### Show Open - " in text
        assert "source-section pass 2026-07-09" in text
    finally:
        shutil.rmtree(tmp_dir)


def test_retrofit_source_preserves_existing_sectioned_body_without_force() -> None:
    tmp_dir = make_local_temp_dir()
    try:
        source = tmp_dir / "source-test.md"
        original = (
            "---\n"
            "pub_date: 2026-07-07\n"
            "host_slug: dialogue-works\n"
            "transcript_curation: curated_sectioned\n"
            "section_count: 2\n"
            "section_pass: \"2026-07-01 semantic-section-v1\"\n"
            "routing_state: provisional\n"
            "---\n"
            "# Example\n"
            "\n"
            "## Transcript\n"
            "\n"
            "### Show Open - Existing\n"
            "\n"
            "Already sectioned block.\n"
            "\n"
            "### Segment 2 - Existing Turn\n"
            "\n"
            "Second block.\n"
        )
        source.write_text(original, encoding="utf-8")

        result = land_best_intake.retrofit_source(source, "2026-06-01")
        text = source.read_text(encoding="utf-8")

        assert result is not None
        assert result.startswith("NORMALIZED") or result.startswith("UNCHANGED")
        assert "### Show Open - Existing" in text
        assert text.count("### ") == 2
    finally:
        shutil.rmtree(tmp_dir)


def test_fast_intake_infers_mercouris_solo_from_body_text() -> None:
    args = build_fast_args(
        "2026-07-08",
        "https://www.youtube.com/watch?v=4m2KLrVw1kA",
        "",
        "Alexander Mercouris: Russia Gives WW3 Warning - YouTube Transcripts: Good day everybody.\n",
    )

    normalized = land_best_intake.normalize_args(args)

    assert normalized.title == "Alexander Mercouris: Russia Gives WW3 Warning"
    assert normalized.host_slug == "alexander-mercouris"
    assert normalized.voice_slugs == ["mercouris"]
    assert normalized.source_form == "solo"
    assert normalized.thread == "mercouris"


def test_fast_intake_infers_dialogue_works_guest_from_body_text() -> None:
    args = build_fast_args(
        "2026-07-08",
        "https://www.youtube.com/watch?v=gjA5wIT9DZ8",
        "Larry Johnson: Iran Strikes US Bases in Bahrain & Kuwait - YouTube Transcripts",
        "Hi everybody. Today we have Larry Johnson back with us to talk about Iran and Hormuz.\n",
    )

    normalized = land_best_intake.normalize_args(args)

    assert normalized.host_slug == "dialogue-works"
    assert normalized.host == "Nima Alkhorshid"
    assert normalized.voice_slugs == ["johnson"]
    assert normalized.guest == "Larry Johnson"
    assert normalized.source_form == "interview"


def test_fast_intake_raises_single_blocker_for_ambiguous_multiple_guest_candidates() -> None:
    args = build_fast_args(
        "2026-07-09",
        "https://www.youtube.com/watch?v=SMBheNf3JHc",
        "BREAKING: Bahrain & Kuwait Just Struck Iran - w/ Col. Macgregor and Larry Johnson",
        "Hi everybody. Today we have Col Douglas Macgregor and Larry Johnson.\n",
    )
    args.host_slug = "dialogue-works"

    with pytest.raises(ValueError, match="primary guest/voice is ambiguous"):
        land_best_intake.normalize_args(args)


def test_fast_intake_real_july_dialogue_works_barnes_routes_to_guest_thread() -> None:
    body = (
        "Robert Barnes: U.S. Just REVOKED Iran Waivers - We Heading to War - YouTube Transcripts\n"
        "Hi everybody. Today's Tuesday, July 7, 2026, and our dear friend Robert Barnes is here with us.\n"
    )
    args = build_fast_args(
        "2026-07-07",
        "https://www.youtube.com/watch?v=H0UPyniTc_Q",
        "",
        body,
    )

    normalized = land_best_intake.normalize_args(args)

    assert normalized.host_slug == "dialogue-works"
    assert normalized.voice_slugs == ["barnes"]
    assert normalized.thread == "barnes"
    assert normalized.guest == "Robert Barnes"


def test_fast_intake_real_july_glenn_diesen_davis_routes_to_davis_thread() -> None:
    body = (
        "Daniel Davis: Trump Says the Ceasefire Is Over With Iran & Escalates the War With Russia - YouTube\n\n"
        "Transcripts:\n"
        "Welcome back. We are joined again by Lieutenant Colonel Daniel Davis.\n"
        "You know, Glenn, the bottom line here is that President Trump has no idea what he's doing.\n"
    )
    args = build_fast_args(
        "2026-07-09",
        "https://www.youtube.com/watch?v=Mp1drUnqlig",
        "",
        body,
    )

    normalized = land_best_intake.normalize_args(args)

    assert normalized.host_slug == "glenn-diesen"
    assert normalized.voice_slugs == ["davis"]
    assert normalized.thread == "davis"
    assert normalized.source_form == "interview"


def test_fast_intake_real_july_dialogue_works_martyanov_routes_to_martyanov_thread() -> None:
    body = (
        "Andrei Martyanov: IRAN BOMBSHELL: Hypersonic Missile Hit U.S. Targets in 6 Minutes - Trump WARNED! - YouTube Transcripts\n"
        "Hi everybody. Today's Thursday, July 9, 2026 and our dear friend, our brother Andrei Martyanov is here with us.\n"
    )
    args = build_fast_args(
        "2026-07-09",
        "https://www.youtube.com/watch?v=V64fLKo3uHg",
        "",
        body,
    )

    normalized = land_best_intake.normalize_args(args)

    assert normalized.host_slug == "dialogue-works"
    assert normalized.voice_slugs == ["martyanov"]
    assert normalized.thread == "martyanov"


def test_fast_intake_real_july_moral_resistance_aguilar_infers_host_and_guest() -> None:
    body = (
        "U.S PLAN GROUND INVASION w/ Col Anthony Aguilar - YouTube\n\n"
        "Transcripts:\n"
        "And we are live. We've got Lieutenant Colonel Anthony Aguiler here. Lots happening.\n"
        "Thank you so much for joining us, Anthony. How are you?\n"
    )
    args = build_fast_args(
        "2026-07-09",
        "https://www.youtube.com/watch?v=cdtK9HajIVY",
        "",
        body,
    )

    normalized = land_best_intake.normalize_args(args)

    assert normalized.host_slug == "moral-resistance"
    assert normalized.host == "Sulaiman Ahmed"
    assert normalized.voice_slugs == ["aguilar"]
    assert normalized.thread == "aguilar"
