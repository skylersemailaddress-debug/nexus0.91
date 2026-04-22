from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    report_path = ROOT / "docs" / "release" / "evidence" / "behavioral_runtime" / "behavioral_scenarios_report.json"

    if not report_path.exists():
        print("Missing behavioral runtime report")
        return 1

    data = json.loads(report_path.read_text())

    mem = data.get("checks", {}).get("live_scenarios", {}).get("memory", {})

    ok = True
    errors: list[str] = []

    checks = mem.get("checks", {})

    # Require influence-related signals
    if "memory_present_in_results" not in checks:
        ok = False
        errors.append("missing memory_present_in_results check")

    # Future: extend with influence trace, ranking, filtering

    result = {"ok": ok, "errors": errors}
    print(json.dumps(result, indent=2))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
