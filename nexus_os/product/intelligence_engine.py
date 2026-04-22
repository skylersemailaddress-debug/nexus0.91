from __future__ import annotations

from typing import Any, List


def build_plan(
    objective: str,
    messages: List[dict[str, Any]],
    memories: List[dict[str, Any]],
    runs: List[dict[str, Any]],
    capabilities: List[dict[str, Any]],
) -> dict[str, Any]:

    context_summary = f"Messages: {len(messages)}, Memories: {len(memories)}, Runs: {len(runs)}, Capabilities: {len(capabilities)}"

    recommended_action = f"Focus on advancing objective: {objective} using current system state"

    next_step = f"Execute next step derived from {len(runs)} runs and {len(memories)} memories"

    trace = {
        "messages_used": len(messages),
        "memories_used": len(memories),
        "runs_considered": len(runs),
        "capabilities_considered": len(capabilities),
    }

    return {
        "ok": True,
        "objective": objective,
        "context_summary": context_summary,
        "recommended_action": recommended_action,
        "next_step": next_step,
        "trace": trace,
    }
