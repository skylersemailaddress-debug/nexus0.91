from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT_PATH = ROOT / "docs" / "release" / "evidence" / "execution" / "job_persistence_report.json"


def main() -> int:
    if not REPORT_PATH.exists():
        print("Missing job persistence report")
        return 1

    data = json.loads(REPORT_PATH.read_text(encoding="utf-8"))

    if not data.get("passed"):
        print("Job persistence failed")
        return 1

    print("Job persistence validated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
