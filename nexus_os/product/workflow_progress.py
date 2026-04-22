from __future__ import annotations

from .workflow_state import WorkflowState


def update_progress(state: WorkflowState, step: str, status: str) -> None:
    state.progress.current_step = step
    if status == "pass":
        state.progress.completed_steps.append(step)
    else:
        state.progress.failed_steps.append(step)
