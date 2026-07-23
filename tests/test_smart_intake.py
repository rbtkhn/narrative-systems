from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = spec_from_file_location("smart_intake", ROOT / "scripts" / "smart_intake.py")
MODULE = module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


def test_known_voice_alias_is_canonicalized():
    args, aliases = MODULE.normalize_voice_args(
        ["--voice-slug", "jeffrey-sachs", "--host-slug", "breaking-points"]
    )
    assert args[1] == "sachs"
    assert aliases == [("jeffrey-sachs", "sachs")]


def test_canonical_voice_is_unchanged():
    args, aliases = MODULE.normalize_voice_args(["--voice-slug", "sachs"])
    assert args == ["--voice-slug", "sachs"]
    assert aliases == []
