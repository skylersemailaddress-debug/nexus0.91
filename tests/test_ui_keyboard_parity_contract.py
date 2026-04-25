from nexus_os.product.ui_primitives import KeyboardParityContract
from nexus_os.product.ui_state import build_hover_native_ui_state


def test_keyboard_parity_passes_with_required_shortcuts() -> None:
    state = build_hover_native_ui_state(runtime_state={}, user_state={})
    parity = state["keyboard_parity"]

    assert parity["passed"] is True
    assert parity["missing_shortcuts"] == []


def test_keyboard_parity_fail_shape() -> None:
    contract = KeyboardParityContract(
        shortcuts={"open_command_rail": "Ctrl+K"},
        missing_shortcuts=["pin_current_item"],
        passed=False,
    )

    as_dict = contract.to_dict()
    assert as_dict["passed"] is False
    assert "pin_current_item" in as_dict["missing_shortcuts"]
