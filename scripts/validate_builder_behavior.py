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

    builder = data.get("checks", {}).get("live_scenarios", {}).get("builder", {})

    ok = True
    errors: list[str] = []

    checks = builder.get("checks", {})

    required_checks = [
        "capability_has_output",
        "capability_validate",
        "capability_update",
        "capability_version_incremented",
        "capability_output_changed",
        "capability_evidence_present",
        "capability_registry_fetch",
        "capability_registry_contains_item",
    ]

    for key in required_checks:
        if not checks.get(key, {}).get("ok"):
            ok = False
            errors.append(f"{key} failed")

    result = {"ok": ok, "errors": errors}
    print(json.dumps(result, indent=2))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
