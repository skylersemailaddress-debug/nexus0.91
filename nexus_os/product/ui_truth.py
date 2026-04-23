from __future__ import annotations

from typing import Any, Dict, List


def mission_surface_from_runtime(snapshot: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "objective": snapshot.get("objective"),
        "next_step": snapshot.get("next_step"),
        "trajectory": snapshot.get("trajectory"),
    }


def approval_surface_from_runtime(run_state: Dict[str, Any]) -> Dict[str, Any]:
    approvals = list(run_state.get("approvals") or [])
    return {"approvals": approvals}


def progress_surface_from_runtime(run_state: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "run_status": run_state.get("status"),
        "jobs": list(run_state.get("jobs") or []),
    }


def memory_surface_from_runtime(snapshot: Dict[str, Any]) -> Dict[str, Any]:
    memory_context = snapshot.get("memory_context") or {}
    return {
        "memory": list(memory_context.get("items") or []),
        "suppressed": list(memory_context.get("suppressed") or []),
        "reasoning": list(memory_context.get("reasoning") or []),
    }


def proof_surface_from_runtime(evidence: List[str]) -> Dict[str, Any]:
    return {"evidence": list(evidence)}
