"""Build and print a tiny narrative system."""

from narrative_systems import NarrativeRelation, NarrativeSystem, NarrativeUnit


def build_system() -> NarrativeSystem:
    system = NarrativeSystem("arrival scene")
    system.add_unit(NarrativeUnit("door", "The locked door", "A boundary appears."))
    system.add_unit(NarrativeUnit("key", "The found key", "A possible passage appears."))
    system.add_relation(
        NarrativeRelation(
            source_id="key",
            target_id="door",
            kind="unlocks",
            note="The second unit changes what the first one means.",
        )
    )
    return system


if __name__ == "__main__":
    print(build_system().summary())
