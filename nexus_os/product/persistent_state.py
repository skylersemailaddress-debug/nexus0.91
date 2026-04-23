from dataclasses import dataclass, field
from pathlib import Path
from typing import Any
import json


@dataclass
class PersistentShellState:
    mission: str = "No mission set"
    history: list[str] = field(default_factory=list)
    auto_state: str = "idle"
    last_post_approval_results: list[str] = field(default_factory=list)

    messages: list[dict[str, Any]] = field(default_factory=list)
    objective: str | None = None
    next_step: str | None = None
    last_message_id: str | None = None


def state_path() -> Path:
    return Path(__file__).resolve().parents[2] / ".nexus_shell_state.json"


def load_state() -> PersistentShellState:
    path = state_path()
    if not path.exists():
        return PersistentShellState()
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return PersistentShellState(
            mission=data.get("mission", "No mission set"),
            history=data.get("history", []),
            auto_state=data.get("auto_state", "idle"),
            last_post_approval_results=data.get("last_post_approval_results", []),
            messages=data.get("messages", []),
            objective=data.get("objective"),
            next_step=data.get("next_step"),
            last_message_id=data.get("last_message_id"),
        )
    except Exception:
        return PersistentShellState()


def save_state(state: PersistentShellState) -> None:
    payload = {
        "mission": state.mission,
        "history": state.history,
        "auto_state": state.auto_state,
        "last_post_approval_results": state.last_post_approval_results,
        "messages": state.messages,
        "objective": state.objective,
        "next_step": state.next_step,
        "last_message_id": state.last_message_id,
    }
    state_path().write_text(json.dumps(payload, indent=2), encoding="utf-8")
