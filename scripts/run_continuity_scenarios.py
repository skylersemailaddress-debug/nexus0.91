from __future__ import annotations

import json
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE_DIR = ROOT / "docs" / "release" / "evidence" / "continuity"

SCENARIOS = [
    "restart_active_mission",
    "restart_with_pending_approval",
    "restart_with_active_run",
    "resume_summary_completeness",
]


def emit_stub(name: str) -> None:
    path = EVIDENCE_DIR / f"{name}.json"
    payload = {
        "scenario": name,
        "timestamp": datetime.utcnow().isoformat(),
        "objective": "UNIMPLEMENTED",
        "next_step": "UNIMPLEMENTED",
        "trajectory": "UNIMPLEMENTED",
        "approvals": [],
        "runs": [],
        "artifacts": [],
        "passed": False,
        "note": "Continuity scenario not yet implemented",
    }
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def main() -> int:
    EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)

    for scenario in SCENARIOS:
        emit_stub(scenario)

    print(f"[continuity] emitted {len(SCENARIOS)} stub scenarios")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
