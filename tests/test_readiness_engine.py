from nexus_os.product.readiness_engine import readiness_snapshot, score_readiness_field


def test_needs_you_rises_with_personal_usage_and_pending_approvals() -> None:
    runtime = {
        "messages": [{"text": "Ship enterprise release"}],
        "memories": [],
        "runs": {},
        "approvals": [{"status": "pending", "objective": "Approve release"}],
        "ui_state": {
            "mode": "decide",
            "quick_actions": ["approve", "inspect"],
        },
        "learning_state": {
            "pane_usage": {"needs_you": 4, "prepared": 1},
            "action_usage": {"approve": 5},
            "mode_usage": {"decide": 3},
        },
    }

    panes = score_readiness_field(runtime)
    assert panes[0].kind == "needs_you"
    assert panes[0].score > panes[-1].score


def test_prepared_actions_adapt_to_personal_action_history() -> None:
    runtime = {
        "messages": [{"text": "Audit the repo"}],
        "memories": [],
        "runs": {},
        "approvals": [],
        "ui_state": {
            "mode": "focus",
            "quick_actions": ["continue", "branch", "launch"],
        },
        "learning_state": {
            "pane_usage": {"prepared": 2},
            "action_usage": {"resume": 4, "approve": 2, "inspect": 1},
            "mode_usage": {"focus": 2},
        },
    }

    panes = score_readiness_field(runtime)
    prepared = [pane for pane in panes if pane.kind == "prepared"][0]
    assert prepared.actions[0] == "resume"

    snapshot = readiness_snapshot(runtime)
    assert "prepared" in snapshot["pane_order"]
