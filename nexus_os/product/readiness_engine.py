from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class ReadinessPane:
    id: str
    title: str
    kind: str
    score: float
    summary: str
    actions: list[str]
    reason: str


MODE_BOOSTS: dict[str, dict[str, float]] = {
    "focus": {"now": 1.0, "prepared": 0.3, "context": 0.2},
    "build": {"in_motion": 1.0, "prepared": 0.8, "context": 0.4},
    "review": {"needs_you": 1.0, "prepared": 0.5, "context": 0.5},
    "inspect": {"context": 0.8, "in_motion": 0.5, "what_changed": 0.4},
    "decide": {"needs_you": 1.0, "now": 0.6, "prepared": 0.4},
    "war-room": {"what_changed": 1.0, "in_motion": 1.0, "needs_you": 0.8},
    "autopilot": {"in_motion": 0.8, "prepared": 0.3, "context": 0.2},
}


def _mode_boost(ui: dict[str, Any], pane_kind: str) -> float:
    mode = str(ui.get("mode", "focus"))
    return MODE_BOOSTS.get(mode, {}).get(pane_kind, 0.0)


def _learning_boost(runtime: dict[str, Any], pane_kind: str) -> float:
    learning = runtime.get("learning_state", {})
    pane_usage = learning.get("pane_usage", {})
    return 0.4 * float(pane_usage.get(pane_kind, 0))


def _action_rank(runtime: dict[str, Any], actions: list[str]) -> list[str]:
    learning = runtime.get("learning_state", {})
    action_usage = learning.get("action_usage", {})
    return sorted(actions, key=lambda a: action_usage.get(a, 0), reverse=True)


def _safe_tail(items: list[Any], count: int) -> list[Any]:
    return items[-count:] if len(items) > count else list(items)


def score_readiness_field(runtime: dict[str, Any]) -> list[ReadinessPane]:
    messages = list(runtime.get("messages", []))
    memories = list(runtime.get("memories", []))
    runs = dict(runtime.get("runs", {}))
    approvals = list(runtime.get("approvals", []))
    ui = dict(runtime.get("ui_state", {}))

    history = [str(item.get("text", "")) for item in messages]
    mission = history[-1] if history else "No active objective"
    recent = _safe_tail(history, 3)
    active_runs = [item for item in runs.values() if item.get("status") in {"running", "retrying", "active", "paused"}]
    pending_approvals = [item for item in approvals if item.get("status") in {"pending", "review", "blocked"}]
    recent_memories = _safe_tail(memories, 2)

    panes: list[ReadinessPane] = []

    now_score = 3.0 + (1.0 if history else 0.0) + _mode_boost(ui, "now") + _learning_boost(runtime, "now")
    panes.append(
        ReadinessPane(
            id="pane:now",
            title="Now",
            kind="now",
            score=now_score,
            summary=f"{mission} | waiting: {len(pending_approvals)} | active runs: {len(active_runs)}",
            actions=_action_rank(runtime, ["continue", "focus", "summarize"]),
            reason="top current objective and best next move anchor the workspace",
        )
    )

    if recent:
        changed_score = 1.5 + 0.4 * len(recent) + 0.3 * len(active_runs) + _mode_boost(ui, "what_changed") + _learning_boost(runtime, "what_changed")
        panes.append(
            ReadinessPane(
                id="pane:what_changed",
                title="What Changed",
                kind="what_changed",
                score=changed_score,
                summary=" | ".join(recent),
                actions=_action_rank(runtime, ["review", "compare", "pick up"]),
                reason="recent activity and changed state should be visible on return",
            )
        )

    if active_runs:
        run_states = ", ".join(f"{item.get('run_id', 'run:?')}:{item.get('status', 'unknown')}" for item in active_runs[:3])
        motion_score = 2.0 + 0.8 * len(active_runs) + _mode_boost(ui, "in_motion") + _learning_boost(runtime, "in_motion")
        panes.append(
            ReadinessPane(
                id="pane:in_motion",
                title="In Motion",
                kind="in_motion",
                score=motion_score,
                summary=run_states,
                actions=_action_rank(runtime, ["inspect", "pause", "resume", "retry"]),
                reason="ongoing jobs and retries deserve live workspace weight",
            )
        )

    if pending_approvals:
        approval_score = 2.8 + 0.9 * len(pending_approvals) + _mode_boost(ui, "needs_you") + _learning_boost(runtime, "needs_you")
        approval_summary = ", ".join(str(item.get("objective") or item.get("approval_id") or "approval") for item in pending_approvals[:3])
        panes.append(
            ReadinessPane(
                id="pane:needs_you",
                title="Needs You",
                kind="needs_you",
                score=approval_score,
                summary=approval_summary,
                actions=_action_rank(runtime, ["approve", "inspect", "revise"]),
                reason="blocking decisions should rise above passive context",
            )
        )

    prepared_summary = mission if history else "Workspace is ready for a new command"
    prepared_score = 1.2 + 0.5 * len(messages) + _mode_boost(ui, "prepared") + _learning_boost(runtime, "prepared")
    panes.append(
        ReadinessPane(
            id="pane:prepared",
            title="Prepared For You",
            kind="prepared",
            score=prepared_score,
            summary=prepared_summary,
            actions=_action_rank(runtime, list(ui.get("quick_actions", ["continue", "branch", "launch"]))[:4]),
            reason="likely next commands and staged actions should be pre-composed",
        )
    )

    if recent_memories:
        memory_summary = " | ".join(str(item.get("content", ""))[:80] for item in recent_memories)
        context_score = 1.0 + 0.5 * len(recent_memories) + _mode_boost(ui, "context") + _learning_boost(runtime, "context")
        panes.append(
            ReadinessPane(
                id="pane:context",
                title="Context",
                kind="context",
                score=context_score,
                summary=memory_summary,
                actions=_action_rank(runtime, ["why", "expand", "debug"]),
                reason="only the few memories affecting current action should surface",
            )
        )

    return sorted(panes, key=lambda pane: pane.score, reverse=True)


def readiness_snapshot(runtime: dict[str, Any]) -> dict[str, Any]:
    panes = score_readiness_field(runtime)
    return {
        "top_pane": panes[0].title if panes else "Now",
        "pane_order": [pane.kind for pane in panes],
        "scores": {pane.kind: pane.score for pane in panes},
    }
