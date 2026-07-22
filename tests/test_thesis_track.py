from scripts.thesis_track import classify, evidence_spans


def test_forecast_classification_is_deterministic():
    claim_type, confidence, basis = classify("Odessa will become the final battle", "Russia could eventually capture the city.")
    assert claim_type == "forecast"
    assert confidence == "medium"
    assert basis == "forecast-language"


def test_evidence_span_is_bounded_and_line_addressable():
    text = "\n".join(["noise"] * 3 + ["Russia may blockade Odessa port and cut maritime access to Ukraine." ] + ["tail"] * 3)
    spans = evidence_spans(text, ["odessa", "port"])
    assert spans
    assert spans[0]["line_start"] <= spans[0]["line_end"]
    assert len(spans[0]["excerpt"]) <= 480


def test_title_only_candidate_is_not_accepted_by_closeout_guard():
    # The production closeout rejects low-confidence accepted candidates;
    # this test locks the classification boundary used by that guard.
    claim_type, confidence, basis = classify("Odessa", "Odessa")
    assert claim_type == "descriptive"
    assert confidence == "low"
    assert basis == "keyword-only"
