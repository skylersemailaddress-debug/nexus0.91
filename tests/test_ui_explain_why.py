from nexus_os.product.ui_state import build_hover_native_ui_state


def test_explain_why_entries_have_explanation_and_evidence() -> None:
    state = build_hover_native_ui_state(runtime_state={}, user_state={})
    entries = state["explain_why"]

    assert entries
    for entry in entries:
        assert entry["explanation"]
        assert isinstance(entry["evidence_ids"], list)


def test_explain_why_marks_limited_when_runtime_is_minimal() -> None:
    state = build_hover_native_ui_state(runtime_state={"workspace": {"run_state": "idle"}}, user_state={})
    entries = state["explain_why"]

    assert any(entry.get("limited") for entry in entries)
