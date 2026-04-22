from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, List


@dataclass
class WorkflowStep:
    name: str
    action: str


@dataclass
class WorkflowDefinition:
    name: str
    steps: List[WorkflowStep] = field(default_factory=list)


def deploy_workflow() -> WorkflowDefinition:
    return WorkflowDefinition(
        name="deploy",
        steps=[
            WorkflowStep("validate master truth", "validate_truth"),
            WorkflowStep("validate 10/10 gate", "validate_ten_ten"),
            WorkflowStep("generate release manifest", "generate_manifest"),
        ],
    )


def monitor_workflow() -> WorkflowDefinition:
    return WorkflowDefinition(
        name="monitor",
        steps=[
            WorkflowStep("read execution signals", "execution_signals"),
            WorkflowStep("read gate status", "gate_status"),
        ],
    )


def rollback_workflow() -> WorkflowDefinition:
    return WorkflowDefinition(
        name="rollback",
        steps=[
            WorkflowStep("rollback manifest", "rollback_manifest"),
        ],
    )
