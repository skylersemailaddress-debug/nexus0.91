"""Hover-native UI state builder for Nexus P0-2.

Produces the hover_native_ui block injected into /api/state.
"""
from __future__ import annotations

from typing import Any

from .ui_primitives import build_hover_native_primitives


def build_hover_native_ui_state(
    runtime_state: dict[str, Any] | None = None,
    user_state: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Build the full hover-native UI state dict.

    Args:
        runtime_state: The ``data`` dict from the current /api/state response,
            or None if not yet available.
        user_state: Optional user/session state (e.g. pinned items from
            localStorage passed via a future API endpoint).

    Returns:
        A dict with keys: edge_reveal, bottom_command_rail, pinned_items,
        adaptive_opening, explain_why, undo_recovery, keyboard_parity, status.
    """
    primitives = build_hover_native_primitives(runtime_state, user_state)

    # Determine overall status honestly
    kb_passed = primitives["keyboard_parity"].get("passed", False)
    rail_mode = primitives["bottom_command_rail"].get("mode", "idle")
    edge_enabled = any(z.get("enabled") for z in primitives["edge_reveal"])

    if not kb_passed:
        status = "degraded:keyboard_parity_incomplete"
    elif rail_mode == "blocked":
        status = "degraded:execution_blocked"
    elif not edge_enabled:
        status = "limited:no_edge_zones_active"
    else:
        status = "ready"

    return {
        **primitives,
        "status": status,
    }
