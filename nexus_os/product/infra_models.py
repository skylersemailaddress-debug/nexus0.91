from __future__ import annotations

from dataclasses import dataclass


@dataclass
class DeployTarget:
    name: str
    target_type: str
    endpoint: str = ""


@dataclass
class HealthCheckResult:
    name: str
    status: str
    detail: str = ""
