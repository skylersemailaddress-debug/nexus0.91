from __future__ import annotations

from typing import Any, Dict, List


def infer_continuity_label(history: list[str]) -> str:
    if not history:
        return "New session"
    return "Resumed thread"


def resolve_objective(state: Dict[str, Any]) -> str:
    objective = state.get("objective") or state.get("mission")
    if objective:
        return str(objective)

    history = list(state.get("history") or [])
    if history:
        last_meaningful = str(history[-1]).strip()
        if last_meaningful:
            return last_meaningful

    return "No objective resolved"


def get_ranked_memory_context(state: Dict[str, Any], objective: str, current_step: str) -> Dict[str, Any]:
    memory_items = list(state.get("memory") or [])
    ranked: List[Dict[str, Any]] = []
    suppressed: List[Dict[str, Any]] = []
    reasoning: List[str] = []

    objective_l = objective.lower()
    current_step_l = current_step.lower()

    for item in memory_items:
        if not isinstance(item, dict):
            continue

        text = str(item.get("text") or item.get("value") or "")
        text_l = text.lower()
        trust = int(item.get("trust", 1) or 1)
        recency = int(item.get("recency", 1) or 1)
        contradictory = bool(item.get("contradictory", False))
        stale = bool(item.get("stale", False))

        score = 0
        if objective_l and objective_l in text_l:
            score += 3
        if current_step_l and current_step_l in text_l:
            score += 2
        score += trust
        score += recency

        enriched = {
            **item,
            "score": score,
            "text": text,
        }

        if contradictory or stale:
            suppressed.append(enriched)
            reason = "suppressed as contradictory" if contradictory else "suppressed as stale"
            reasoning.append(f"{text or 'memory item'} {reason}")
        else:
            ranked.append(enriched)
            reasoning.append(f"{text or 'memory item'} ranked with score {score}")

    ranked.sort(key=lambda item: item.get("score", 0), reverse=True)

    return {
        "items": ranked,
        "suppressed": suppressed,
        "reasoning": reasoning,
    }


def resolve_next_step(state: Dict[str, Any], memory_context: Dict[str, Any] | None = None) -> str:
    next_step = state.get("next_step")
    if next_step:
        return str(next_step)

    memory_context = memory_context or {"items": []}
    ranked_items = memory_context.get("items") or []
    if ranked_items:
        top = ranked_items[0]
        suggestion = top.get("suggested_next_step")
        if suggestion:
            return str(suggestion)

    runs = state.get("runs") or []
    if runs:
        active = runs[0]
        if isinstance(active, dict) and active.get("current_step"):
            return str(active["current_step"])

    approvals = state.get("approvals") or []
    if approvals:
        return "Review pending approval"

    history = list(state.get("history") or [])
    if history:
        latest = str(history[-1]).strip()
        if latest:
            return f"Continue: {latest}"

    return "No next step resolved"


def build_resume_snapshot(state: Dict[str, Any]) -> Dict[str, Any]:
    history = state.get("history") or []
    objective = resolve_objective(state)
    preliminary_step = str(state.get("next_step") or "")
    memory_context = get_ranked_memory_context(state, objective, preliminary_step)
    resolved_step = resolve_next_step(state, memory_context)

    snapshot = {
        "objective": objective,
        "next_step": resolved_step,
        "trajectory": state.get("trajectory") or "Trajectory unresolved",
        "approvals": list(state.get("approvals") or []),
        "runs": list(state.get("runs") or []),
        "artifacts": list(state.get("artifacts") or []),
        "memory_context": memory_context,
        "continuity_label": infer_continuity_label(history),
        "passed": False,
    }
    return snapshot
