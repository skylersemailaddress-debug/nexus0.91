from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE_DIR = ROOT / "docs" / "release" / "evidence" / "ui"
REPORT_PATH = EVIDENCE_DIR / "ui_validation_report.json"

REQUIRED = [
    "mission_surface_matches_runtime.json",
    "approval_surface_matches_runtime.json",
    "progress_surface_matches_run_state.json",
    "memory_surface_matches_influence_trace.json",
    "proof_surface_matches_evidence.json",
]

ALLOWED_SURFACE_KEYS = {
    "mission_surface_matches_runtime": {"objective", "next_step", "trajectory"},
    "approval_surface_matches_runtime": {"approvals"},
    "progress_surface_matches_run_state": {"run_status", "jobs"},
    "memory_surface_matches_influence_trace": {"memory", "suppressed", "reasoning"},
    "proof_surface_matches_evidence": {"evidence"},
}


def _details_for(name: str, data: dict[str, Any]) -> list[str]:
    details: list[str] = []
    scenario = name.replace(".json", "")
    surface = data.get("surface")
    runtime = data.get("runtime_source")
    reasoning = data.get("reasoning")
    if data.get("scenario") != scenario:
        details.append("scenario_mismatch")
    if not isinstance(surface, dict) or not surface:
        details.append("missing_surface")
        surface = {}
    if not isinstance(runtime, dict) or not runtime:
        details.append("missing_runtime_source")
        runtime = {}
    if not isinstance(reasoning, list) or not reasoning:
        details.append("missing_reasoning")
    allowed = ALLOWED_SURFACE_KEYS.get(scenario, set())
    extra = set(surface.keys()).difference(allowed)
    if extra:
        details.append(f"hallucinated_surface_fields:{','.join(sorted(extra))}")

    if scenario == "mission_surface_matches_runtime":
        for key in ("objective", "next_step", "trajectory"):
            if surface.get(key) != runtime.get(key):
                details.append(f"mission_mismatch_{key}")
    elif scenario == "approval_surface_matches_runtime":
        if surface.get("approvals") != list(runtime.get("approvals") or []):
            details.append("approvals_mismatch")
    elif scenario == "progress_surface_matches_run_state":
        if surface.get("run_status") != runtime.get("status"):
            details.append("run_status_mismatch")
        if surface.get("jobs") != list(runtime.get("jobs") or []):
            details.append("jobs_mismatch")
    elif scenario == "memory_surface_matches_influence_trace":
        memory_context = runtime.get("memory_context") or {}
        if surface.get("memory") != list(memory_context.get("items") or []):
            details.append("memory_items_mismatch")
        if surface.get("suppressed") != list(memory_context.get("suppressed") or []):
            details.append("memory_suppressed_mismatch")
        if surface.get("reasoning") != list(memory_context.get("reasoning") or []):
            details.append("memory_reasoning_mismatch")
    elif scenario == "proof_surface_matches_evidence":
        if surface.get("evidence") != list(runtime.get("evidence") or []):
            details.append("evidence_mismatch")
    return details


def main() -> int:
    EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)
    results = []
    for name in REQUIRED:
        path = EVIDENCE_DIR / name
        if not path.exists():
            results.append({"name": name, "passed": False, "details": ["missing"]})
            continue
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            results.append({"name": name, "passed": False, "details": ["invalid_json"]})
            continue
        details = sorted(set(_details_for(name, data)))
        results.append({"name": name, "passed": not details, "details": details})
    report = {"passed": all(r["passed"] for r in results), "checks": results}
    REPORT_PATH.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
