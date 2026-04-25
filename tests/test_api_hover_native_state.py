from nexus_os.product import api_server


def test_api_state_includes_hover_native_ui() -> None:
    payload = api_server.get_state()

    assert payload["ok"] is True
    assert "data" in payload
    data = payload["data"]
    assert "hover_native_ui" in data

    hover = data["hover_native_ui"]
    assert "edge_reveal" in hover
    assert "bottom_command_rail" in hover
    assert "keyboard_parity" in hover
