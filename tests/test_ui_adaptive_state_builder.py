from nexus_os.product.ui_state import build_hover_native_ui_state


def test_hover_native_state_shape_and_status() -> None:
    state = build_hover_native_ui_state(runtime_state=None, user_state=None)

    assert set(state.keys()) >= {
        "edge_reveal",
        "bottom_command_rail",
        "pinned_items",
        "adaptive_opening",
        "explain_why",
        "undo_recovery",
        "keyboard_parity",
        "status",
    }
    assert isinstance(state["status"], str)


def test_adaptive_opening_relevance_gating() -> None:
    active = build_hover_native_ui_state(
        runtime_state={
            "workspace": {"run_state": "active"},
            "mission": "Execute objective",
            "operator_surface": {"governance_cards": []},
            "artifacts_recent": [{"id": "artifact:1", "type": "receipt"}],
        },
        user_state=None,
    )

    groups = active["adaptive_opening"]
    assert groups
    assert all("relevance_score" in group and "reason" in group for group in groups)


def test_honest_limited_state_without_runtime_refs() -> None:
    idle = build_hover_native_ui_state(runtime_state={"workspace": {"run_state": "idle"}}, user_state=None)

    undo = idle["undo_recovery"]
    assert undo["can_undo"] is False
    assert isinstance(undo["disabled_reason"], str) and undo["disabled_reason"]
