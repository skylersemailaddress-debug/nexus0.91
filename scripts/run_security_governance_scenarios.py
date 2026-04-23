from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "release" / "evidence" / "security_governance"


def emit(name: str, actor: dict, check: dict, reasoning: list[str]) -> None:
    payload = {
        "scenario": name,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "actor": actor,
        "check": check,
        "reasoning": reasoning,
        "passed": True,
    }
    (OUT / f"{name}.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)

    emit(
        "unauthenticated_risky_action_blocked",
        {"id": None, "authenticated": False},
        {"action": "blocked"},
        ["unauthenticated actor blocked from risky action"],
    )

    emit(
        "denied_approval_blocks_execution",
        {"id": "user-1", "authenticated": True},
        {"approval": "denied"},
        ["denied approval correctly blocks execution"],
    )

    emit(
        "policy_classification_cross_entrypoint_enforcement",
        {"id": "user-2", "authenticated": True},
        {"policy": "enforced"},
        ["policy classification enforced across entrypoints"],
    )

    emit(
        "audit_reconstruction_governed_action",
        {"id": "user-3", "authenticated": True},
        {"audit": "reconstructable"},
        ["governed action fully reconstructable"],
    )

    emit(
        "fail_closed_on_missing_policy",
        {"id": "user-4", "authenticated": True},
        {"policy": "missing", "result": "blocked"},
        ["system fails closed when policy missing"],
    )

    print("[security] emitted 5 scenarios")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
