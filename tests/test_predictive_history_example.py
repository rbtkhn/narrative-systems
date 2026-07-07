from examples.predictive_history_system import build_predictive_history_system


def test_predictive_history_target_summary() -> None:
    system = build_predictive_history_system()

    assert system.summary() == {
        "name": "Predictive History",
        "unit_count": 5,
        "relation_count": 5,
        "relation_kinds": [
            "constrains",
            "defaults-to",
            "generates",
            "governs-traversal",
            "opens",
        ],
    }
