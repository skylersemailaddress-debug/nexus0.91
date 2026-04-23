from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCENARIO_REPORT = ROOT / "docs" / "release" / "evidence" / "behavioral_runtime" / "behavioral_scenarios_report.json"
RUNTIME_REPORT = ROOT / "docs" / "release" / "evidence" / "behavioral_runtime" / "behavioral_runtime_report.json"
OUT = ROOT / "docs" / "release" / "evidence" / "behavioral_gate" / "behavioral_ten_ten_report.json"


def _read(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    errors: list[str] = []
    checks: dict[str, object] = {}

    if not SCENARIO_REPORT.exists():
        errors.append("missing behavioral_scenarios_report.json")
    if not RUNTIME_REPORT.exists():
        errors.append("missing behavioral_runtime_report.json")

    scenario_ok = False
    runtime_ok = False

    if SCENARIO_REPORT.exists():
        scenario = _read(SCENARIO_REPORT)
        scenario_ok = bool(scenario.get("ok", False))
        checks["scenarios"] = {"ok": scenario_ok, "path": str(SCENARIO_REPORT)}
        if not scenario_ok:
            errors.append("behavioral scenarios failed")

    if RUNTIME_REPORT.exists():
        runtime = _read(RUNTIME_REPORT)
        runtime_ok = bool(runtime.get("ok", False))
        checks["runtime"] = {"ok": runtime_ok, "path": str(RUNTIME_REPORT)}
        if not runtime_ok:
            errors.append("behavioral runtime validation failed")

    result = {
        "ok": not errors and scenario_ok and runtime_ok,
        "source": "generated",
        "checks": checks,
        "errors": errors,
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
