from __future__ import annotations

from dataclasses import dataclass, field
from typing import List

from .approvals import build_approval_prompt
from .capability_cards import build_context_cards
from .continuity import infer_continuity_label
from .runtime_adapter import get_gate_execution_summary
from .state_inference import (
    compute_active_intelligence_line,
    compute_next_best_move,
    infer_need_state,
    infer_work_state,
)
from .surface_model import MissionHeader, PrimarySurface, ShellFrame
from .trust_layer import build_trust_panel
from .workflow_runner import run_workflow
from .workflows import deploy_workflow, monitor_workflow, rollback_workflow


@dataclass
class ShellState:
    mode: str = "product"
    history: List[str] = field(default_factory=list)
    mission: str = "No mission set"
    auto_state: str = "idle"
    last_execution_results: List[str] = field(default_factory=list)
    live_workflow_results: List[str] = field(default_factory=list)
    workflow_state_summary: List[str] = field(default_factory=list)


def detect_auto_state() -> str:
    gates = get_gate_execution_summary()
    if all(v == "pass" for v in gates.values()):
        return "ready"
    if any(v == "fail" for v in gates.values()):
        return "blocked"
    return "idle"


def build_frame(state: ShellState) -> ShellFrame:
    state.auto_state = detect_auto_state()

    reasoning_history = state.history.copy()
    if state.auto_state in {"ready", "blocked"}:
        reasoning_history.append(state.auto_state)

    work_state = infer_work_state(reasoning_history, state.mission)
    continuity = infer_continuity_label(state.history)
    active_line = compute_active_intelligence_line(reasoning_history, state.mission)
    next_move = compute_next_best_move(reasoning_history, state.mission)

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
    frame.cards = build_context_cards(reasoning_history)
    frame.approval_prompt = build_approval_prompt(reasoning_history)
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
    print(f"Auto State: {state.auto_state}")
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
        print(f"  Action: {frame.approval_prompt.action_label} / hold / rollback")

    if state.live_workflow_results:
        print("-" * 72)
        print("Live Workflow View:")
        for item in state.live_workflow_results:
            print(f"  > {item}")

    if state.workflow_state_summary:
        print("-" * 72)
        print("Workflow State:")
        for item in state.workflow_state_summary:
            print(f"  * {item}")

    if state.last_execution_results:
        print("-" * 72)
        print("Last Execution Results:")
        for item in state.last_execution_results:
            print(f"  - {item}")

    print("=" * 72)


def run_shell(mode: str = "product") -> None:
    state = ShellState(mode=mode)

    print(f"[Nexus] Starting interactive shell in {mode} mode")
    print("Nexus Adaptive Shell")

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

        if raw.startswith("mission"):
            parts = raw.split(maxsplit=1)
            if len(parts) > 1:
                state.mission = parts[1]
                state.history.append(raw)

        elif raw == "approve":
            results, wf_state = run_workflow(deploy_workflow())
            state.live_workflow_results = results
            state.last_execution_results = results.copy()
            state.workflow_state_summary = [
                f"current: {wf_state.progress.current_step}",
                f"completed: {len(wf_state.progress.completed_steps)}",
                f"failed: {len(wf_state.progress.failed_steps)}",
            ]

        elif raw == "monitor":
            results, wf_state = run_workflow(monitor_workflow())
            state.live_workflow_results = results
            state.workflow_state_summary = [
                f"current: {wf_state.progress.current_step}"
            ]

        elif raw == "rollback":
            results, wf_state = run_workflow(rollback_workflow())
            state.live_workflow_results = results
            state.last_execution_results = results.copy()

        elif raw == "why":
            panel = build_trust_panel(state.history if state.history else [state.auto_state])
            print(f"[Nexus] {panel.title}")
            for line in panel.lines:
                print(f"  - {line}")
            continue

        else:
            state.history.append(raw)

        render_frame(build_frame(state), state)
