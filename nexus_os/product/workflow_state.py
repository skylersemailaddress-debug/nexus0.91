from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict


@dataclass
class WorkflowProgress:
    current_step: str = ""
    completed_steps: list[str] = field(default_factory=list)
    failed_steps: list[str] = field(default_factory=list)


@dataclass
class WorkflowState:
    name: str
    progress: WorkflowProgress = field(default_factory=WorkflowProgress)
    metadata: Dict[str, str] = field(default_factory=dict)
