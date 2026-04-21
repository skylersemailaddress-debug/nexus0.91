from __future__ import annotations

from typing import Iterable

REQUIRED_SECURITY_FLAGS = ("rbac", "secrets", "runtime_enforcement")


def security_runtime_check(enabled_flags: Iterable[str]) -> dict[str, object]:
    enabled = set(enabled_flags)
    missing = [flag for flag in REQUIRED_SECURITY_FLAGS if flag not in enabled]
    return {
        "valid": not missing,
        "missing": missing,
        "enabled": sorted(enabled),
    }
