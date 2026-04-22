from __future__ import annotations

from .infra_models import DeployTarget


def default_targets() -> list[DeployTarget]:
    return [
        DeployTarget(name="local-docker", target_type="docker"),
        DeployTarget(name="local-service", target_type="service"),
    ]
