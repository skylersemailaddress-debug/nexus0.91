from __future__ import annotations

from nexus_os.persistence.store import load_state, save_state
from nexus_os.observability.runtime_audit import append_audit_event
from .approvals import build_approval_prompt
from .capability_cards import build_context_cards
from .continuity import infer_continuity_label
from .state_inference import (
    compute_active_intelligence_line,
    compute_next_best_move,
    infer_work_state,
)


def _get_ui(runtime: dict) -> dict:
    return runtime.get("ui_state", {})


def _save(runtime: dict) -> None:
    save_state(runtime)


def build_frame(runtime: dict) -> dict:
    messages = runtime.get("messages", [])
    memories = runtime.get("memories", [])
    runs = runtime.get("runs", {})
    ui = _get_ui(runtime)

    history = [m.get("text", "") for m in messages]
    mission = history[-1] if history else "No mission set"

    return {
        "header": {
            "mission": mission,
            "state": infer_work_state(history, mission),
            "continuity": infer_continuity_label(history),
            "signal": compute_active_intelligence_line(history, mission),
        },
        "primary": {
            "log": history[-5:],
            "next": compute_next_best_move(history, mission),
        },
        "context": {
            "cards": build_context_cards(history),
            "memories": memories[:3],
            "runs": list(runs.values())[:3],
        },
        "controls": ui,
    }


def render_frame(frame: dict) -> None:
    print("=" * 72)
    print(f"Mission: {frame['header']['mission']}")
    print(f"State: {frame['header']['state']} | {frame['header']['continuity']}")
    print(f"Signal: {frame['header']['signal']}")

    print("-" * 72)
    print("PRIMARY")
    for line in frame["primary"]["log"]:
        print(f"> {line}")
    print(f"Next: {frame['primary']['next']}")

    print("-" * 72)
    print("CONTEXT")
    for card in frame["context"]["cards"]:
        print(f"[{card.title}] {card.summary}")

    print("-" * 72)
    print("MEMORY")
    for m in frame["context"]["memories"]:
        print(f"- {m.get('content')}")

    print("-" * 72)
    print("RUNS")
    for r in frame["context"]["runs"]:
        print(f"- {r.get('run_id')} | {r.get('status')}")

    print("-" * 72)
    print(f"Controls: {frame['controls']}")
    print("=" * 72)


def run_shell() -> None:
    while True:
        runtime = load_state()
        frame = build_frame(runtime)
        render_frame(frame)

        cmd = input("nexus> ").strip()
        ui = _get_ui(runtime)

        if cmd in {"exit", "quit"}:
            return

        if cmd.startswith("pin "):
            ui.setdefault("pinned_sections", []).append(cmd.split(" ", 1)[1])

        elif cmd.startswith("hover "):
            ui["hover_target"] = cmd.split(" ", 1)[1]

        elif cmd.startswith("mode "):
            ui["mode"] = cmd.split(" ", 1)[1]

        elif cmd.startswith("density "):
            ui["density"] = cmd.split(" ", 1)[1]

        else:
            msg = {
                "id": f"msg:{len(runtime.get('messages', [])) + 1}",
                "role": "user",
                "text": cmd,
                "meta": {},
            }
            runtime.setdefault("messages", []).append(msg)
            append_audit_event("message_append", msg)

        runtime["ui_state"] = ui
        _save(runtime)
