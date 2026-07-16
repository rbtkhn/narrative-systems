from __future__ import annotations

import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_ROOT = REPO_ROOT / "scripts"
if str(SCRIPTS_ROOT) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_ROOT))

from runtime_bootstrap import BootstrapUnavailable, resolve_validation_python


def main() -> int:
    try:
        python = resolve_validation_python(REPO_ROOT)
    except BootstrapUnavailable as error:
        print(f"validation unavailable: {error}", file=sys.stderr)
        return 1
    commands = (
        [str(python), "scripts/validate_repository.py"],
        [str(python), "-m", "pytest", "-q", "-p", "no:cacheprovider"],
    )
    returncode = 0
    for command in commands:
        result = subprocess.run(command, cwd=REPO_ROOT)
        if result.returncode and not returncode:
            returncode = result.returncode
    return returncode


if __name__ == "__main__":
    raise SystemExit(main())
