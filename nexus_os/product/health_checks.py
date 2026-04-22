from __future__ import annotations

from .infra_models import HealthCheckResult


def basic_health_checks() -> list[HealthCheckResult]:
    return [
        HealthCheckResult("service", "unknown"),
        HealthCheckResult("endpoint", "unknown"),
    ]
