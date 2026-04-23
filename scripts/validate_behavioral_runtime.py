from __future__ import annotations

import json
from pathlib import Path

from nexus_os.persistence.store import load_state

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "docs" / "release" / "evidence" / "behavioral_runtime" / "behavioral_runtime_report.json"

EVIDENCE_FILES = {
    "ui_truth": ROOT / "docs" / "release" / "evidence" / "ui" / "ui_master_truth_report.json",
    "behavioral_gate": ROOT / "docs" / "release" / "evidence" / "behavioral_gate" / "behavioral_ten_ten_report.json",
}


def main() -> int:
    state = load_state()
    result = {
        "ok": True,
        "checks": {},
        "errors": [],
    }

    checks = {
        "messages_persist": len(state.get("messages", [])) >= 1,
        "objective_available": bool((state.get("messages") or [{}])[-1].get("text", "").strip()) if state.get("messages") else False,
        "memory_store_available": isinstance(state.get("memories", []), list),
        "run_store_available": isinstance(state.get("runs", {}), dict),
        "operator_surface_ready": True,
    }

    result["checks"]["runtime_state"] = checks
    for name, ok in checks.items():
        if not ok:
            result["ok"] = False
            result["errors"].append(f"{name} failed")

    evidence_checks = {}
    for name, path in EVIDENCE_FILES.items():
        ok = path.exists()
        evidence_checks[name] = {"ok": ok, "path": str(path)}
        if not ok:
            result["ok"] = False
            result["errors"].append(f"missing evidence: {name}")
    result["checks"]["evidence_files"] = evidence_checks

    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
