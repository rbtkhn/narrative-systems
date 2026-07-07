"""Represent Predictive History as the first research target."""

from narrative_systems import NarrativeRelation, NarrativeSystem, NarrativeUnit


def build_predictive_history_system() -> NarrativeSystem:
    system = NarrativeSystem("Predictive History")

    system.add_unit(
        NarrativeUnit(
            "start-here",
            "START-HERE.md",
            "LLM bootloader and first-response contract.",
        )
    )
    system.add_unit(
        NarrativeUnit(
            "catalog",
            "Namespace catalog hub",
            "Machine and human indexes for the public chapter corpus.",
        )
    )
    system.add_unit(
        NarrativeUnit(
            "cards",
            "Public cards",
            "Single source of truth for public chapter metadata.",
        )
    )
    system.add_unit(
        NarrativeUnit(
            "first-tour",
            "First tour",
            "Default 10-stop guided reader experience.",
        )
    )
    system.add_unit(
        NarrativeUnit(
            "source-lattice",
            "Source-lattice",
            "Traversal discipline from doorway to source floor to interpretation.",
        )
    )

    system.add_relation(
        NarrativeRelation("start-here", "catalog", "opens")
    )
    system.add_relation(
        NarrativeRelation("cards", "catalog", "generates")
    )
    system.add_relation(
        NarrativeRelation("start-here", "first-tour", "defaults-to")
    )
    system.add_relation(
        NarrativeRelation("source-lattice", "first-tour", "constrains")
    )
    system.add_relation(
        NarrativeRelation("source-lattice", "catalog", "governs-traversal")
    )

    return system


if __name__ == "__main__":
    print(build_predictive_history_system().summary())
