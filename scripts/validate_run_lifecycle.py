from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT_PATH = ROOT / "docs" / "release" / "evidence" / "execution" / "run_lifecycle_report.json"


def main() -> int:
    if not REPORT_PATH.exists():
        print("Missing run lifecycle report")
        return 1

    data = json.loads(REPORT_PATH.read_text(encoding="utf-8"))

    if not data.get("passed"):
        print("Run lifecycle failed")
        return 1

    print("Run lifecycle validated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
