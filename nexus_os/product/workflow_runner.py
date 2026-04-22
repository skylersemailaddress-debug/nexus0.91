from __future__ import annotations

from .workflows import WorkflowDefinition
from .infra_adapter import run_action
from .workflow_state import WorkflowState
from .workflow_progress import update_progress
from .workflow_branching import should_continue, branch_on_failure


def run_workflow(defn: WorkflowDefinition) -> tuple[list[str], WorkflowState, dict]:
    state = WorkflowState(name=defn.name)
    results: list[str] = []
    total = len(defn.steps)

    for idx, step in enumerate(defn.steps, start=1):
        outcome = run_action(step.action)
        update_progress(state, step.name, outcome)

        progress_pct = int((idx / total) * 100)

        results.append(f"{step.name}: {outcome}")

        if not should_continue(outcome):
            branch = branch_on_failure(step.name)
            results.append(branch)
            state.metadata["branch"] = branch
            return results, state, {
                "progress": progress_pct,
                "current": step.name,
                "status": "failed",
            }

    return results, state, {
        "progress": 100,
        "current": state.progress.current_step,
        "status": "complete",
    }
