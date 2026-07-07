import pytest

from narrative_systems import NarrativeRelation, NarrativeSystem, NarrativeUnit


def test_system_summary_counts_units_and_relations() -> None:
    system = NarrativeSystem("threshold")
    system.add_unit(NarrativeUnit("call", "The call"))
    system.add_unit(NarrativeUnit("answer", "The answer"))

    system.add_relation(NarrativeRelation("call", "answer", "invites"))

    assert system.summary() == {
        "name": "threshold",
        "unit_count": 2,
        "relation_count": 1,
        "relation_kinds": ["invites"],
    }


def test_unit_ids_must_be_unique() -> None:
    system = NarrativeSystem("threshold")
    system.add_unit(NarrativeUnit("call", "The call"))

    with pytest.raises(ValueError, match="already exists"):
        system.add_unit(NarrativeUnit("call", "The second call"))


def test_relation_must_reference_known_units() -> None:
    system = NarrativeSystem("threshold")
    system.add_unit(NarrativeUnit("call", "The call"))

    with pytest.raises(ValueError, match="unknown unit"):
        system.add_relation(NarrativeRelation("call", "answer", "invites"))


def test_blank_names_are_rejected() -> None:
    with pytest.raises(ValueError, match="name cannot be blank"):
        NarrativeSystem(" ")
