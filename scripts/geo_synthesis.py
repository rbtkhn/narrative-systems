from __future__ import annotations

# Backward-compatible shim for the renamed operator-facing entrypoint.
from process_daily_stack import main


if __name__ == "__main__":
    main()
