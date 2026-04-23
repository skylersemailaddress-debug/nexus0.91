from __future__ import annotations

import json
from pathlib import Path
from typing import Any

DEFAULT_STATE: dict[str, Any] = {
    "messages": [],
    "memories": [],
    "runs": {},
    "approvals": [],
    "ui_state": {
        "mode": "focus",
        "density": "comfortable",
        "pinned_sections": [],
        "hover_target": "mission",
        "saved_layout": "default",
    },
}


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def state_path() -> Path:
    return repo_root() / "docs" / "release" / "evidence" / "runtime" / "state.json"


def load_state() -> dict[str, Any]:
    path = state_path()
    if not path.exists():
        return json.loads(json.dumps(DEFAULT_STATE))
    state = json.loads(path.read_text(encoding="utf-8"))
    if "ui_state" not in state:
        state["ui_state"] = json.loads(json.dumps(DEFAULT_STATE["ui_state"]))
    return state


def save_state(state: dict[str, Any]) -> None:
    path = state_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(state, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def reset_state() -> dict[str, Any]:
    state = json.loads(json.dumps(DEFAULT_STATE))
    save_state(state)
    return state
