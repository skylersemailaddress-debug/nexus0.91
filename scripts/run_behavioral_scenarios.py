from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

from scripts.scenarios import continuity, execution, memory, ui_truth

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "docs" / "release" / "evidence" / "behavioral_runtime" / "behavioral_scenarios_report.json"

REQUIRED_VALIDATORS = [
    ROOT / "scripts" / "validate_ui_master_truth.py",
    ROOT / "scripts" / "validate_behavioral_ten_ten_gate.py",
    ROOT / "scripts" / "validate_behavioral_runtime.py",
]

SCENARIOS = {
    "continuity": {
        "required_markers": [
            "durable message append",
            "restart + resume correctness",
            "objective and next step resolution",
        ],
        "status": "live_when_runtime_surface_exists",
    },
    "memory": {
        "required_markers": [
            "memory influences output",
            "memory relevance ranking works",
            "bad memory is filtered",
        ],
        "status": "live_when_runtime_surface_exists",
    },
    "execution": {
        "required_markers": [
            "jobs persist across time",
            "jobs resume after interruption",
            "retries and repair loops work",
        ],
        "status": "live_when_runtime_surface_exists",
    },
    "ui_truth": {
        "required_markers": [
            "ui reflects real system state",
            "no decorative panels",
            "approvals and jobs are real",
        ],
        "status": "live_when_runtime_surface_exists",
    },
}

CANDIDATE_DOCS = [
    ROOT / "docs" / "release" / "BEHAVIORAL_TEN_TEN_WORK_PLAN.md",
    ROOT / "docs" / "ui" / "NEXUS_UI_MASTER_TRUTH.md",
    ROOT / "docs" / "ui" / "NEXUS_UI_DOCTRINE.md",
]


def read_if_exists(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="ignore")


def detect_runtime_surface() -> dict[str, Any]:
    base_url = os.environ.get("NEXUS_RUNTIME_BASE_URL", "").strip()
    auth_token = os.environ.get("NEXUS_RUNTIME_AUTH_TOKEN", "").strip()
    return {
        "available": bool(base_url),
        "base_url": base_url,
        "auth_token": auth_token,
        "has_auth_token": bool(auth_token),
    }


def main() -> int:
    result: dict[str, Any] = {
        "ok": True,
        "checks": {},
        "errors": [],
        "notes": [],
    }

    def fail(message: str) -> None:
        result["ok"] = False
        result["errors"].append(message)

    validator_checks: dict[str, Any] = {}
    for path in REQUIRED_VALIDATORS:
        exists = path.exists()
        validator_checks[str(path)] = {"ok": exists}
        if not exists:
            fail(f"Missing required validator: {path}")
    result["checks"]["validators"] = validator_checks

    corpus = "\n\n".join(read_if_exists(path) for path in CANDIDATE_DOCS)
    scenario_checks: dict[str, Any] = {}
    for name, config in SCENARIOS.items():
        missing = [marker for marker in config["required_markers"] if marker.lower() not in corpus.lower()]
        scenario_checks[name] = {
            "ok": not missing,
            "missing_markers": missing,
            "status": config["status"],
        }
        if missing:
            fail(f"Scenario {name} is missing required markers: {missing}")
    result["checks"]["scenario_contract"] = scenario_checks

    runtime_surface = detect_runtime_surface()
    result["checks"]["runtime_surface"] = {
        "available": runtime_surface["available"],
        "base_url": runtime_surface["base_url"],
        "has_auth_token": runtime_surface["has_auth_token"],
    }

    if not runtime_surface["available"]:
        result["notes"].append(
            "Runtime surface not configured. Set NEXUS_RUNTIME_BASE_URL (and optionally NEXUS_RUNTIME_AUTH_TOKEN) to activate live scenario execution."
        )
    else:
        live_results = {
            "continuity": continuity.run(runtime_surface["base_url"], runtime_surface["auth_token"] or None),
            "memory": memory.run(runtime_surface["base_url"], runtime_surface["auth_token"] or None),
            "execution": execution.run(runtime_surface["base_url"], runtime_surface["auth_token"] or None),
            "ui_truth": ui_truth.run(runtime_surface["base_url"], runtime_surface["auth_token"] or None),
        }
        result["checks"]["live_scenarios"] = live_results

        for name, live_result in live_results.items():
            if not live_result.get("ok", False):
                fail(f"{name} scenario failed")

    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))
    return 0 if bool(result["ok"]) else 1


if __name__ == "__main__":
    raise SystemExit(main())
