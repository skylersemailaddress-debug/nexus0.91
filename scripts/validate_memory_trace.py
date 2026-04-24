from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT_PATH = ROOT / "docs" / "release" / "evidence" / "memory" / "memory_trace_report.json"


def main() -> int:
    if not REPORT_PATH.exists():
        print("Missing memory trace report")
        return 1
    data = json.loads(REPORT_PATH.read_text(encoding="utf-8"))
    if not data.get("passed"):
        print("Trace validation failed")
        return 1
    if not data.get("trace_ids"):
        print("No trace attribution present")
        return 1
    print("Memory trace validated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
