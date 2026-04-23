from __future__ import annotations

from dataclasses import dataclass, field
from typing import List

from nexus_os.persistence.store import load_state, save_state
from nexus_os.observability.runtime_audit import append_audit_event
from .approvals import build_approval_prompt
from .capability_cards import build_context_cards
from .continuity import infer_continuity_label
from .runtime_adapter import get_gate_execution_summary
from .state_inference import (
    compute_active_intelligence_line,
    compute_next_best_move,
    infer_work_state,
)
from .surface_model import MissionHeader, PrimarySurface, ShellFrame, UIControls
from .trust_layer import build_trust_panel


@dataclass
class ShellState:
    mode: str = "focus"
    density: str = "comfortable"
    pinned: List[str] = field(default_factory=list)
    hover: str = "mission"


def _load_runtime():
    state = load_state()
    return state


def build_frame(state: ShellState) -> ShellFrame:
    runtime = _load_runtime()
    messages = runtime.get("messages", [])
    memories = runtime.get("memories", [])
    runs = runtime.get("runs", {})

    history = [m.get("text", "") for m in messages]
    mission = history[-1] if history else "No mission set"

    work_state = infer_work_state(history, mission)
    continuity = infer_continuity_label(history)
    active_line = compute_active_intelligence_line(history, mission)
    next_move = compute_next_best_move(history, mission)

    header = MissionHeader(mission, continuity, work_state, active_line)
    primary = PrimarySurface(history[-5:], next_move)

    controls = UIControls(
        mode=state.mode,
        density=state.density,
        pinned_sections=state.pinned,
        hover_target=state.hover,
        palette_commands=["mission", "approve", "rollback", "monitor"],
        quick_actions=["approve", "pause", "resume"],
    )

    frame = ShellFrame(header=header, primary=primary, controls=controls)
    frame.cards = build_context_cards(history)
    frame.approval_prompt = build_approval_prompt(history)
    frame.trust_panel = build_trust_panel(history)
    return frame


def render_frame(frame: ShellFrame) -> None:
    print("=" * 72)
    print(f"Mission: {frame.header.mission_title}")
    print(f"State: {frame.header.work_state} | {frame.header.continuity_label}")
    print(f"Signal: {frame.header.active_intelligence_line}")
    print(f"Next: {frame.primary.next_best_move}")

    print(f"Mode: {frame.controls.mode} | Density: {frame.controls.density} | Hover: {frame.controls.hover_target}")

    print("-" * 72)
    for line in frame.primary.log_lines:
        print(f"> {line}")

    if frame.cards:
        print("-" * 72)
        for c in frame.cards:
            if c.title in frame.controls.pinned_sections or frame.controls.hover_target == c.title:
                print(f"[{c.title}] {c.summary}")

    if frame.approval_prompt:
        print("-" * 72)
        print(f"APPROVAL: {frame.approval_prompt.title}")

    print("=" * 72)


def run_shell() -> None:
    state = ShellState()

    while True:
        frame = build_frame(state)
        render_frame(frame)

        cmd = input("nexus> ").strip()

        if cmd in {"exit", "quit"}:
            return

        runtime = load_state()

        if cmd.startswith("pin "):
            state.pinned.append(cmd.split(" ", 1)[1])

        elif cmd.startswith("unpin "):
            section = cmd.split(" ", 1)[1]
            if section in state.pinned:
                state.pinned.remove(section)

        elif cmd.startswith("hover "):
            state.hover = cmd.split(" ", 1)[1]

        elif cmd.startswith("mode "):
            state.mode = cmd.split(" ", 1)[1]

        elif cmd.startswith("density "):
            state.density = cmd.split(" ", 1)[1]

        elif cmd == "palette":
            print("Commands:", frame.controls.palette_commands)

        else:
            msg = {
                "id": f"msg:{len(runtime.get('messages', [])) + 1}",
                "role": "user",
                "text": cmd,
                "meta": {"trace": {}},
            }
            runtime.setdefault("messages", []).append(msg)
            save_state(runtime)
            append_audit_event("message_append", msg)
