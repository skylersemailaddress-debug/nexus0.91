from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Panel:
    name: str
    components: list[str]
    actions: list[str]
    state_bindings: list[str]


@dataclass(frozen=True)
class Surface:
    name: str
    panels: list[Panel] = field(default_factory=list)
    layout: list[str] = field(default_factory=list)
    evidence_views: list[str] = field(default_factory=list)


def _panel(name: str, comps: list[str], actions: list[str], bindings: list[str]) -> Panel:
    return Panel(name=name, components=comps, actions=actions, state_bindings=bindings)


def build_surface(product_name: str, workflows: list[str]) -> Surface:
    name = product_name

    panels = [
        _panel(
            "mission_control",
            ["status_header", "priority_queue", "alerts"],
            ["refresh", "filter", "drill_down"],
            ["workflow_state", "priority"],
        ),
        _panel(
            "work_queue",
            ["task_list", "assignment", "status_badge"],
            ["assign", "complete", "escalate"],
            ["task_state", "owner"],
        ),
        _panel(
            "proof_panel",
            ["audit_log", "decision_trace", "evidence_cards"],
            ["export", "inspect"],
            ["audit_events"],
        ),
    ]

    if any("churn" in w for w in workflows):
        panels.append(
            _panel(
                "retention_panel",
                ["customer_health", "risk_score", "intervention"],
                ["trigger_playbook", "log_outcome"],
                ["customer_state", "risk_score"],
            )
        )

    if any("approval" in w or "policy" in w for w in workflows):
        panels.append(
            _panel(
                "approval_console",
                ["pending_requests", "decision_buttons", "policy_view"],
                ["approve", "reject"],
                ["policy_state"],
            )
        )

    layout = [p.name for p in panels]

    evidence_views = [
        "decision_trace",
        "workflow_execution_log",
        "policy_evaluation",
    ]

    return Surface(
        name=name,
        panels=panels,
        layout=layout,
        evidence_views=evidence_views,
    )


def create_surface(product_name: str, workflows: list[str]) -> Surface:
    return build_surface(product_name, workflows)


__all__ = ["Surface", "Panel", "build_surface", "create_surface"]
