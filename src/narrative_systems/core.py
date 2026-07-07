"""Core narrative-system primitives."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class NarrativeUnit:
    """A named unit of meaning, action, or event."""

    id: str
    name: str
    note: str = ""

    def __post_init__(self) -> None:
        if not self.id.strip():
            raise ValueError("NarrativeUnit id cannot be blank.")
        if not self.name.strip():
            raise ValueError("NarrativeUnit name cannot be blank.")


@dataclass(frozen=True, slots=True)
class NarrativeRelation:
    """A typed link between two narrative units."""

    source_id: str
    target_id: str
    kind: str
    note: str = ""

    def __post_init__(self) -> None:
        if not self.source_id.strip():
            raise ValueError("NarrativeRelation source_id cannot be blank.")
        if not self.target_id.strip():
            raise ValueError("NarrativeRelation target_id cannot be blank.")
        if not self.kind.strip():
            raise ValueError("NarrativeRelation kind cannot be blank.")


@dataclass(slots=True)
class NarrativeSystem:
    """A small container for narrative units and their relations."""

    name: str
    units: dict[str, NarrativeUnit] = field(default_factory=dict)
    relations: list[NarrativeRelation] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError("NarrativeSystem name cannot be blank.")

    def add_unit(self, unit: NarrativeUnit) -> NarrativeUnit:
        """Add a unit to the system and return it."""
        if unit.id in self.units:
            raise ValueError(f"NarrativeUnit id already exists: {unit.id}")
        self.units[unit.id] = unit
        return unit

    def add_relation(self, relation: NarrativeRelation) -> NarrativeRelation:
        """Add a relation after confirming both referenced units exist."""
        missing_ids = [
            unit_id
            for unit_id in (relation.source_id, relation.target_id)
            if unit_id not in self.units
        ]
        if missing_ids:
            missing = ", ".join(missing_ids)
            raise ValueError(f"NarrativeRelation references unknown unit id(s): {missing}")
        self.relations.append(relation)
        return relation

    def summary(self) -> dict[str, object]:
        """Return a small serializable summary of the system."""
        relation_kinds = sorted({relation.kind for relation in self.relations})
        return {
            "name": self.name,
            "unit_count": len(self.units),
            "relation_count": len(self.relations),
            "relation_kinds": relation_kinds,
        }
