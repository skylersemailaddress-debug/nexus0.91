from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT_PATH = ROOT / "docs" / "release" / "evidence" / "execution" / "artifact_lineage_report.json"


def main() -> int:
    if not REPORT_PATH.exists():
        print("Missing artifact lineage report")
        return 1

    data = json.loads(REPORT_PATH.read_text(encoding="utf-8"))

    if not data.get("passed"):
        print("Artifact lineage failed")
        return 1

    if data.get("artifact_count", 0) == 0:
        print("No artifacts recorded")
        return 1

    print("Artifact lineage validated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
