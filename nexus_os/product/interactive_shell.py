from __future__ import annotations

from dataclasses import dataclass, field
from typing import List

from .approvals import build_approval_prompt
from .capability_cards import build_context_cards
from .continuity import infer_continuity_label
from .post_approval import run_post_approval_actions
from .runtime_adapter import get_gate_execution_summary
from .state_inference import (
    compute_active_intelligence_line,
    compute_next_best_move,
    infer_need_state,
    infer_work_state,
)
from .surface_model import MissionHeader, PrimarySurface, ShellFrame
from .trust_layer import build_trust_panel


@dataclass
class ShellState:
    mode: str = "product"
    history: List[str] = field(default_factory=list)
    mission: str = "No mission set"


WELCOME = """Nexus Adaptive Shell\n\nCommands:\n  help              Show commands\n  status            Show shell status\n  mission <text>    Set current mission\n  history           Show entered commands\n  why               Show reasoning surface\n  approve           Approve current decision\n  hold              Hold current decision\n  quit              Exit shell\n"""


def auto_detect_decision(state: ShellState):
    gates = get_gate_execution_summary()
    if all(v == "pass" for v in gates.values()):
        state.history.append("auto-ready-for-release")
    elif any(v == "fail" for v in gates.values()):
        state.history.append("auto-blocked-release")


def build_frame(state: ShellState) -> ShellFrame:
    auto_detect_decision(state)

    work_state = infer_work_state(state.history, state.mission)
    continuity = infer_continuity_label(state.history)
    active_line = compute_active_intelligence_line(state.history, state.mission)
    next_move = compute_next_best_move(state.history, state.mission)

    header = MissionHeader(
        mission_title=state.mission,
        continuity_label=continuity,
        work_state=work_state,
        active_intelligence_line=active_line,
    )
    primary = PrimarySurface(
        log_lines=state.history[-5:],
        next_best_move=next_move,
        composer_prompt="nexus> ",
    )

    frame = ShellFrame(header=header, primary=primary)

    frame.cards = build_context_cards(state.history)
    frame.approval_prompt = build_approval_prompt(state.history)

    return frame


def render_frame(frame: ShellFrame, state: ShellState) -> None:
    need_state = infer_need_state(state.history, state.mission)

    print()
    print("=" * 72)
    print(f"Mission   : {frame.header.mission_title}")
    print(f"Continuity: {frame.header.continuity_label}")
    print(f"Work State: {frame.header.work_state}")
    print(f"Need State: {need_state}")
    print(f"Signal    : {frame.header.active_intelligence_line}")
    print(f"Next Move : {frame.primary.next_best_move}")
    print("-" * 72)

    if frame.primary.log_lines:
        print("Recent Thread:")
        for item in frame.primary.log_lines:
            print(f"  - {item}")
    else:
        print("Recent Thread:")
        print("  - No prior commands")

    if frame.cards:
        print("-" * 72)
        print("Context Signals:")
        for c in frame.cards:
            print(f"  * {c.title}: {c.summary}")

    if frame.approval_prompt:
        print("-" * 72)
        print(f"[Decision] {frame.approval_prompt.title}")
        print(f"  {frame.approval_prompt.summary}")
        print(f"  Action: {frame.approval_prompt.action_label} / hold")

    print("=" * 72)


def run_shell(mode: str = "product") -> None:
    state = ShellState(mode=mode)

    print(WELCOME)
    render_frame(build_frame(state), state)

    while True:
        try:
            raw = input("nexus> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n[Nexus] Exiting shell")
            return

        if not raw:
            continue

        if raw in {"quit", "exit"}:
            print("[Nexus] Goodbye")
            return

        if raw == "help":
            print(WELCOME)
            continue

        if raw.startswith("mission"):
            parts = raw.split(maxsplit=1)
            if len(parts) == 1:
                print(f"[Nexus] Current mission: {state.mission}")
            else:
                state.mission = parts[1]
                print(f"[Nexus] Mission set: {state.mission}")
                state.history.append(raw)
                render_frame(build_frame(state), state)
            continue

        if raw == "history":
            if not state.history:
                print("[Nexus] No history yet")
            else:
                for idx, item in enumerate(state.history, start=1):
                    print(f"{idx}. {item}")
            continue

        if raw == "status":
            render_frame(build_frame(state), state)
            continue

        if raw == "why":
            panel = build_trust_panel(state.history)
            print(f"[Nexus] {panel.title}")
            for line in panel.lines:
                print(f"  - {line}")
            continue

        if raw == "approve":
            print("[Nexus] Decision approved — executing post-actions")
            results = run_post_approval_actions()
            for r in results:
                print(f"  {r}")
            state.history.append("approve")
            render_frame(build_frame(state), state)
            continue

        if raw == "hold":
            print("[Nexus] Decision held")
            state.history.append("hold")
            render_frame(build_frame(state), state)
            continue

        state.history.append(raw)
        print(f"[Nexus] Received: {raw}")
        render_frame(build_frame(state), state)
