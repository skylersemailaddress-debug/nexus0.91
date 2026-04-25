from nexus_os.product.ui_state import build_hover_native_ui_state


def test_pin_persistence_key_stability() -> None:
    user_state = {
        "pinned_items": [
            {
                "id": "mission:alpha",
                "item_type": "mission",
                "title": "alpha",
                "source": "desktop_shell",
                "created_at": "2026-04-25T00:00:00Z",
                "reason": "Pinned by operator",
            }
        ]
    }

    first = build_hover_native_ui_state(runtime_state={}, user_state=user_state)
    second = build_hover_native_ui_state(runtime_state={}, user_state=user_state)

    key_one = first["pinned_items"][0]["persistence_key"]
    key_two = second["pinned_items"][0]["persistence_key"]

    assert key_one == key_two
    assert key_one == "nexus:pinned-items:mission:alpha"
