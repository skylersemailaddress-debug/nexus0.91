from __future__ import annotations

from .workflows import WorkflowDefinition
from .infra_adapter import run_action


def run_workflow(defn: WorkflowDefinition) -> list[str]:
    results: list[str] = []
    for step in defn.steps:
        outcome = run_action(step.action)
        results.append(f"{step.name}: {outcome}")
    return results
