"""Hover-native UI primitives for Nexus P0-2.

Plain dataclasses — no external dependencies required.
"""
from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Any


# ---------------------------------------------------------------------------
# Edge Reveal Zone
# ---------------------------------------------------------------------------

@dataclass
class EdgeRevealZone:
    id: str
    edge: str          # left | right | top | bottom
    label: str
    intent: str
    enabled: bool
    reason: str
    keyboard_shortcut: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


# ---------------------------------------------------------------------------
# Bottom Command Rail State
# ---------------------------------------------------------------------------

@dataclass
class BottomCommandRailState:
    visible: bool
    mode: str          # idle | command | review | blocked
    primary_action: str
    secondary_actions: list[str] = field(default_factory=list)
    disabled_reason: str = ""
    keyboard_shortcuts: dict[str, str] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


# ---------------------------------------------------------------------------
# Pinned Item
# ---------------------------------------------------------------------------

@dataclass
class PinnedItem:
    id: str
    item_type: str
    title: str
    source: str
    persistence_key: str
    created_at: str
    reason: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


# ---------------------------------------------------------------------------
# Adaptive Opening Group
# ---------------------------------------------------------------------------

@dataclass
class AdaptiveOpeningGroup:
    id: str
    title: str
    relevance_score: float
    items: list[dict[str, Any]] = field(default_factory=list)
    reason: str = ""
    enabled: bool = True

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


# ---------------------------------------------------------------------------
# Explain Why Entry
# ---------------------------------------------------------------------------

@dataclass
class ExplainWhyEntry:
    id: str
    target: str
    explanation: str
    evidence_ids: list[str] = field(default_factory=list)
    confidence: float = 1.0
    limited: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


# ---------------------------------------------------------------------------
# Undo / Recovery State
# ---------------------------------------------------------------------------

@dataclass
class UndoRecoveryState:
    can_undo: bool
    last_action: str
    recovery_options: list[str] = field(default_factory=list)
    disabled_reason: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


# ---------------------------------------------------------------------------
# Keyboard Parity Contract
# ---------------------------------------------------------------------------

@dataclass
class KeyboardParityContract:
    shortcuts: dict[str, str] = field(default_factory=dict)
    missing_shortcuts: list[str] = field(default_factory=list)
    passed: bool = True

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


# ---------------------------------------------------------------------------
# Builder helper
# ---------------------------------------------------------------------------

REQUIRED_SHORTCUTS = [
    "open_command_rail",
    "focus_edge_nav",
    "pin_current_item",
    "show_explain_why",
    "close_recover_escape",
]


def build_hover_native_primitives(
    runtime_state: dict[str, Any] | None = None,
    user_state: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Construct all hover-native UI primitives from available state."""
    runtime_state = runtime_state or {}
    user_state = user_state or {}

    run_state = runtime_state.get("workspace", {}).get("run_state", "idle") if isinstance(runtime_state.get("workspace"), dict) else "idle"
    mission = runtime_state.get("mission", "") or ""
    has_mission = bool(mission and mission != "No mission set")
    pending = runtime_state.get("operator_surface", {}).get("governance_cards", []) if isinstance(runtime_state.get("operator_surface"), dict) else []
    has_pending = bool(pending)

    # Edge reveal zones
    edge_zones = [
        EdgeRevealZone(
            id="edge:left:nav",
            edge="left",
            label="Navigation",
            intent="open_navigation_panel",
            enabled=True,
            reason="Always available for workspace navigation",
            keyboard_shortcut="Alt+ArrowLeft",
        ),
        EdgeRevealZone(
            id="edge:right:context",
            edge="right",
            label="Context",
            intent="open_context_panel",
            enabled=has_mission,
            reason="Active mission available" if has_mission else "No active mission — context panel limited",
            keyboard_shortcut="Alt+ArrowRight",
        ),
        EdgeRevealZone(
            id="edge:top:command",
            edge="top",
            label="Command",
            intent="open_command_rail",
            enabled=True,
            reason="Command rail always accessible",
            keyboard_shortcut="Alt+ArrowUp",
        ),
        EdgeRevealZone(
            id="edge:bottom:recovery",
            edge="bottom",
            label="Recovery",
            intent="open_recovery_panel",
            enabled=run_state in ("active", "review"),
            reason="Recovery available during active run" if run_state in ("active", "review") else "Disabled — no active run",
            keyboard_shortcut="Alt+ArrowDown",
        ),
    ]

    # Bottom command rail
    mode = "idle"
    primary_action = "compose"
    disabled_reason = ""
    if has_pending:
        mode = "review"
        primary_action = "review_approvals"
    elif run_state == "active":
        mode = "command"
        primary_action = "continue_execution"
    elif run_state == "blocked":
        mode = "blocked"
        primary_action = "resolve_block"
        disabled_reason = "Execution blocked — resolve before continuing"

    rail = BottomCommandRailState(
        visible=True,
        mode=mode,
        primary_action=primary_action,
        secondary_actions=["pin_current", "show_explain_why", "undo_last"],
        disabled_reason=disabled_reason,
        keyboard_shortcuts={
            "open_command_rail": "Ctrl+K",
            "focus_edge_nav": "Alt+ArrowLeft",
            "pin_current_item": "Ctrl+Shift+P",
            "show_explain_why": "Ctrl+Shift+W",
            "close_recover_escape": "Escape",
        },
    )

    # Pinned items from user_state localStorage-backed state
    raw_pins = user_state.get("pinned_items", []) if isinstance(user_state, dict) else []
    pinned = [
        PinnedItem(
            id=p.get("id", f"pin:{i}"),
            item_type=p.get("item_type", "unknown"),
            title=p.get("title", "Untitled"),
            source=p.get("source", ""),
            persistence_key=f"nexus:pinned-items:{p.get('id', i)}",
            created_at=p.get("created_at", ""),
            reason=p.get("reason", ""),
        )
        for i, p in enumerate(raw_pins)
    ]

    # Adaptive opening groups
    groups: list[AdaptiveOpeningGroup] = []
    if has_mission:
        groups.append(AdaptiveOpeningGroup(
            id="adaptive:mission",
            title="Active Mission",
            relevance_score=1.0,
            items=[{"label": "Current mission", "value": mission}],
            reason="Mission is active and in progress",
            enabled=True,
        ))
    if has_pending:
        groups.append(AdaptiveOpeningGroup(
            id="adaptive:approvals",
            title="Pending Approvals",
            relevance_score=0.9,
            items=[{"label": c} for c in pending],
            reason="Operator approval required",
            enabled=True,
        ))
    if run_state != "idle":
        artifacts = runtime_state.get("artifacts_recent", []) or []
        if artifacts:
            groups.append(AdaptiveOpeningGroup(
                id="adaptive:artifacts",
                title="Recent Artifacts",
                relevance_score=0.7,
                items=[{"label": str(a.get("id", "")), "type": str(a.get("type", ""))} for a in artifacts[:3]],
                reason="Recent artifacts from active run",
                enabled=True,
            ))
    if not groups:
        groups.append(AdaptiveOpeningGroup(
            id="adaptive:idle",
            title="Getting Started",
            relevance_score=0.5,
            items=[{"label": "Set a mission to begin"}],
            reason="No active mission — showing default prompt",
            enabled=True,
        ))

    # Explain why entries
    explain_entries = [
        ExplainWhyEntry(
            id="explain:run-state",
            target="run_state_pill",
            explanation=f"Current run state is '{run_state}' — reflects live workspace execution status",
            evidence_ids=["workspace.run_state"],
            confidence=1.0,
            limited=False,
        ),
        ExplainWhyEntry(
            id="explain:command-rail",
            target="bottom_command_rail",
            explanation=f"Command rail is in '{mode}' mode because: {primary_action}",
            evidence_ids=["workspace.run_state", "operator_surface.governance_cards"],
            confidence=1.0,
            limited=mode == "blocked",
        ),
        ExplainWhyEntry(
            id="explain:adaptive-opening",
            target="adaptive_opening",
            explanation="Adaptive opening surface shows groups relevant to current mission and run state",
            evidence_ids=["mission", "artifacts_recent"],
            confidence=0.9,
            limited=not has_mission,
        ),
    ]

    # Undo/recovery
    undo = UndoRecoveryState(
        can_undo=run_state in ("active", "review"),
        last_action="execution_step" if run_state == "active" else "none",
        recovery_options=["abort_run", "retry_last_step"] if run_state == "active" else [],
        disabled_reason="" if run_state in ("active", "review") else "No active run to undo",
    )

    # Keyboard parity
    defined = set(rail.keyboard_shortcuts.keys())
    missing = [s for s in REQUIRED_SHORTCUTS if s not in defined]
    kb = KeyboardParityContract(
        shortcuts=rail.keyboard_shortcuts,
        missing_shortcuts=missing,
        passed=len(missing) == 0,
    )

    return {
        "edge_reveal": [z.to_dict() for z in edge_zones],
        "bottom_command_rail": rail.to_dict(),
        "pinned_items": [p.to_dict() for p in pinned],
        "adaptive_opening": [g.to_dict() for g in groups],
        "explain_why": [e.to_dict() for e in explain_entries],
        "undo_recovery": undo.to_dict(),
        "keyboard_parity": kb.to_dict(),
    }
