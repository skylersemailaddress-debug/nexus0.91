from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    report = ROOT / "docs" / "release" / "evidence" / "behavioral_runtime" / "behavioral_scenarios_report.json"

    if not report.exists():
        print("missing report")
        return 1

    data = json.loads(report.read_text())

    ui = data.get("checks", {}).get("live_scenarios", {}).get("ui_truth", {})
    checks = ui.get("checks", {})

    required = [
        "mission_backed",
        "approvals_backed",
        "memory_present",
        "memory_influence",
        "progress_runs",
        "proof_artifacts",
        "proof_ids",
    ]

    ok = True
    errors = []

    for r in required:
        if not checks.get(r, {}).get("ok"):
            ok = False
            errors.append(r)

    print(json.dumps({"ok": ok, "errors": errors}, indent=2))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
