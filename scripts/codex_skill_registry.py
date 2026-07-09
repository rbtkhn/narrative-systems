from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
SKILL_DRAFT_ROOT = REPO_ROOT / "docs" / "skill-drafts"
CODEX_SKILLS_ROOT = Path.home() / ".codex" / "skills"


@dataclass(frozen=True)
class SkillEntry:
    name: str
    source: Path
    dest: Path


def discover_repo_skill_names() -> list[str]:
    if not SKILL_DRAFT_ROOT.exists():
        return []
    names: list[str] = []
    for path in SKILL_DRAFT_ROOT.glob("*/SKILL.md"):
        if path.parent.name not in names:
            names.append(path.parent.name)
    return sorted(names)


def discover_codex_skill_names() -> list[str]:
    if not CODEX_SKILLS_ROOT.exists():
        return []
    names: list[str] = []
    for path in CODEX_SKILLS_ROOT.iterdir():
        if not path.is_dir():
            continue
        if path.name == ".system":
            continue
        names.append(path.name)
    return sorted(names)


def build_registry(names: list[str] | None = None) -> dict[str, SkillEntry]:
    chosen = names or discover_repo_skill_names()
    return {
        name: SkillEntry(
            name=name,
            source=SKILL_DRAFT_ROOT / name / "SKILL.md",
            dest=CODEX_SKILLS_ROOT / name / "SKILL.md",
        )
        for name in chosen
    }


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")
