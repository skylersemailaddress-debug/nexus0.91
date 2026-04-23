from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT_PATH = ROOT / "docs" / "release" / "evidence" / "memory" / "memory_context_integration_report.json"


def main() -> int:
    if not REPORT_PATH.exists():
        print("Missing memory context report")
        return 1

    data = json.loads(REPORT_PATH.read_text(encoding="utf-8"))

    if not data.get("behavior_changed"):
        print("Memory did not influence behavior")
        return 1

    if not data.get("passed"):
        print("Memory scenario failed")
        return 1

    print("Memory context integration validated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
