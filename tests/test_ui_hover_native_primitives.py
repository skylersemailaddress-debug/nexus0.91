from nexus_os.product.ui_primitives import (
    EdgeRevealZone,
    KeyboardParityContract,
    PinnedItem,
    build_hover_native_primitives,
)


def test_primitive_to_dict_serialization() -> None:
    zone = EdgeRevealZone(
        id="edge:left:nav",
        edge="left",
        label="Navigation",
        intent="open_navigation_panel",
        enabled=True,
        reason="Always available",
        keyboard_shortcut="Alt+ArrowLeft",
    )
    pin = PinnedItem(
        id="mission:alpha",
        item_type="mission",
        title="alpha",
        source="desktop_shell",
        persistence_key="nexus:pinned-items:mission:alpha",
        created_at="2026-04-25T00:00:00Z",
        reason="Pinned by operator",
    )
    parity = KeyboardParityContract(shortcuts={"open_command_rail": "Ctrl+K"}, missing_shortcuts=[], passed=True)

    assert zone.to_dict()["edge"] == "left"
    assert pin.to_dict()["persistence_key"].startswith("nexus:pinned-items:")
    assert parity.to_dict()["passed"] is True


def test_build_hover_native_primitives_shape() -> None:
    data = build_hover_native_primitives(runtime_state={}, user_state={})

    assert "edge_reveal" in data
    assert "bottom_command_rail" in data
    assert "pinned_items" in data
    assert "adaptive_opening" in data
    assert "explain_why" in data
    assert "undo_recovery" in data
    assert "keyboard_parity" in data
