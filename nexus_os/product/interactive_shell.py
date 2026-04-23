from __future__ import annotations

from nexus_os.persistence.store import load_state, save_state
from nexus_os.observability.runtime_audit import append_audit_event
from .capability_cards import build_context_cards
from .continuity import infer_continuity_label
from .state_inference import (
    compute_active_intelligence_line,
    compute_next_best_move,
    infer_work_state,
)


DEFAULT_QUICK_ACTIONS = ["approve", "pause", "resume", "mission"]


def _get_ui(runtime: dict) -> dict:
    ui = runtime.get("ui_state", {})
    ui.setdefault("mode", "focus")
    ui.setdefault("density", "comfortable")
    ui.setdefault("pinned_sections", [])
    ui.setdefault("hover_target", "mission")
    ui.setdefault("saved_layout", "default")
    ui.setdefault("quick_actions", list(DEFAULT_QUICK_ACTIONS))
    return ui


def _save(runtime: dict) -> None:
    save_state(runtime)


def _density_limits(density: str) -> tuple[int, int, int]:
    if density == "compact":
        return (3, 2, 2)
    if density == "expanded":
        return (8, 5, 5)
    return (5, 3, 3)


def _section_weight(section: str, ui: dict) -> int:
    weight = 0
    if section == ui.get("hover_target"):
        weight += 2
    if section in ui.get("pinned_sections", []):
        weight += 3
    return weight


def build_frame(runtime: dict) -> dict:
    messages = runtime.get("messages", [])
    memories = runtime.get("memories", [])
    runs = runtime.get("runs", {})
    ui = _get_ui(runtime)

    history = [m.get("text", "") for m in messages]
    mission = history[-1] if history else "No mission set"
    log_limit, memory_limit, run_limit = _density_limits(ui["density"])

    context_cards = build_context_cards(history)
    weighted_cards = sorted(
        context_cards,
        key=lambda card: _section_weight(card.title, ui),
        reverse=True,
    )

    weighted_memories = sorted(
        memories,
        key=lambda m: _section_weight("memory", ui) + (1 if m.get("kind") == "note" else 0),
        reverse=True,
    )
    weighted_runs = sorted(
        list(runs.values()),
        key=lambda r: _section_weight("runs", ui) + (1 if r.get("status") in {"running", "retrying"} else 0),
        reverse=True,
    )

    return {
        "header": {
            "mission": mission,
            "state": infer_work_state(history, mission),
            "continuity": infer_continuity_label(history),
            "signal": compute_active_intelligence_line(history, mission),
        },
        "primary": {
            "log": history[-log_limit:],
            "next": compute_next_best_move(history, mission),
        },
        "context": {
            "cards": weighted_cards,
            "memories": weighted_memories[:memory_limit],
            "runs": weighted_runs[:run_limit],
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


def _apply_quick_action(cmd: str, runtime: dict) -> bool:
    ui = _get_ui(runtime)
    if cmd == "approve":
        runtime.setdefault("approvals", []).append({"approval_id": f"approval:{len(runtime.get('approvals', [])) + 1}", "status": "approved"})
        append_audit_event("quick_action_approve", {"source": "ui_shell"})
        return True
    if cmd == "pause":
        runs = runtime.get("runs", {})
        if runs:
            last_key = sorted(runs.keys())[-1]
            runs[last_key]["status"] = "paused"
            append_audit_event("quick_action_pause", {"run_id": last_key})
        return True
    if cmd == "resume":
        runs = runtime.get("runs", {})
        if runs:
            last_key = sorted(runs.keys())[-1]
            runs[last_key]["status"] = "running"
            append_audit_event("quick_action_resume", {"run_id": last_key})
        return True
    if cmd.startswith("layout "):
        ui["saved_layout"] = cmd.split(" ", 1)[1]
        runtime["ui_state"] = ui
        append_audit_event("ui_layout_change", {"layout": ui["saved_layout"]})
        return True
    return False


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
            section = cmd.split(" ", 1)[1]
            if section not in ui["pinned_sections"]:
                ui["pinned_sections"].append(section)

        elif cmd.startswith("unpin "):
            section = cmd.split(" ", 1)[1]
            if section in ui["pinned_sections"]:
                ui["pinned_sections"].remove(section)

        elif cmd.startswith("hover "):
            ui["hover_target"] = cmd.split(" ", 1)[1]

        elif cmd.startswith("mode "):
            ui["mode"] = cmd.split(" ", 1)[1]

        elif cmd.startswith("density "):
            ui["density"] = cmd.split(" ", 1)[1]

        elif cmd == "palette":
            print("Commands:", ui["quick_actions"] + ["layout <name>"])

        elif _apply_quick_action(cmd, runtime):
            pass

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
