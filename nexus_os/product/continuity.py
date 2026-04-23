from __future__ import annotations

from typing import Any, Dict


def infer_continuity_label(history: list[str]) -> str:
    if not history:
        return "New session"
    return "Resumed thread"


def resolve_objective(state: Dict[str, Any]) -> str:
    objective = state.get("objective") or state.get("mission") or "No objective resolved"
    return str(objective)


def resolve_next_step(state: Dict[str, Any]) -> str:
    next_step = state.get("next_step")
    if next_step:
        return str(next_step)

    runs = state.get("runs") or []
    if runs:
        active = runs[0]
        if isinstance(active, dict) and active.get("current_step"):
            return str(active["current_step"])

    approvals = state.get("approvals") or []
    if approvals:
        return "Review pending approval"

    return "No next step resolved"


def build_resume_snapshot(state: Dict[str, Any]) -> Dict[str, Any]:
    history = state.get("history") or []
    snapshot = {
        "objective": resolve_objective(state),
        "next_step": resolve_next_step(state),
        "trajectory": state.get("trajectory") or "Trajectory unresolved",
        "approvals": list(state.get("approvals") or []),
        "runs": list(state.get("runs") or []),
        "artifacts": list(state.get("artifacts") or []),
        "continuity_label": infer_continuity_label(history),
        "passed": False,
    }
    return snapshot
