from __future__ import annotations

import json
from pathlib import Path

from nexus_os.observability.run_timeline import build_run_timeline

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "release" / "evidence" / "runtime" / "run_timeline_report.json"


def main() -> int:
    report = build_run_timeline()
    OUT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
