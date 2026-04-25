import json

from nexus_os.product.ui_state import build_hover_native_ui_state


def test_no_dashboard_regression_in_hover_native_state() -> None:
    state = build_hover_native_ui_state(runtime_state={}, user_state={})
    encoded = json.dumps(state).lower()

    assert "dashboard" not in encoded
