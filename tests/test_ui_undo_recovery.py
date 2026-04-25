from nexus_os.product.ui_state import build_hover_native_ui_state


def test_undo_recovery_active_run() -> None:
    state = build_hover_native_ui_state(runtime_state={"workspace": {"run_state": "active"}}, user_state=None)
    undo = state["undo_recovery"]

    assert undo["can_undo"] is True
    assert undo["recovery_options"]


def test_undo_recovery_idle_honest_disabled_reason() -> None:
    state = build_hover_native_ui_state(runtime_state={"workspace": {"run_state": "idle"}}, user_state=None)
    undo = state["undo_recovery"]

    assert undo["can_undo"] is False
    assert isinstance(undo["disabled_reason"], str) and undo["disabled_reason"]
