from __future__ import annotations

from datetime import UTC, datetime
from typing import Any
from uuid import uuid4

_CAPABILITIES: dict[str, dict[str, Any]] = {}


def _now() -> str:
    return datetime.now(UTC).isoformat()


def create_capability(goal: str) -> dict[str, Any]:
    capability_id = str(uuid4())
    capability = {
        "id": capability_id,
        "goal": goal,
        "title": f"Capability: {goal}",
        "output": f"Generated capability for: {goal}",
        "validated": False,
        "version": 1,
        "evidence": [],
        "created_at": _now(),
        "updated_at": _now(),
    }
    _CAPABILITIES[capability_id] = capability
    return capability


def get_capability(capability_id: str) -> dict[str, Any] | None:
    return _CAPABILITIES.get(capability_id)


def validate_capability(capability_id: str) -> dict[str, Any] | None:
    capability = _CAPABILITIES.get(capability_id)
    if capability is None:
        return None
    capability["validated"] = True
    capability["evidence"].append({"type": "validation", "detail": "Capability validated", "ts": _now()})
    capability["updated_at"] = _now()
    return capability


def update_capability(capability_id: str, content: str) -> dict[str, Any] | None:
    capability = _CAPABILITIES.get(capability_id)
    if capability is None:
        return None
    capability["output"] = content
    capability["version"] = int(capability.get("version", 1)) + 1
    capability["evidence"].append({"type": "update", "detail": "Capability updated", "ts": _now()})
    capability["updated_at"] = _now()
    return capability


def list_capabilities() -> list[dict[str, Any]]:
    return list(_CAPABILITIES.values())
