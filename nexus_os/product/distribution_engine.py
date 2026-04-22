from __future__ import annotations

from typing import Any, Dict, List
from uuid import uuid4
from datetime import datetime, UTC

_LOGS: List[Dict[str, Any]] = []


def _now() -> str:
    return datetime.now(UTC).isoformat()


def publish(payload: dict) -> dict:
    record = {
        "id": str(uuid4()),
        "content": payload.get("content"),
        "channel": payload.get("channel", "internal"),
        "status": "delivered",
        "ts": _now(),
    }
    _LOGS.append(record)
    return {"ok": True, "record": record}


def logs() -> dict:
    return {"ok": True, "logs": _LOGS}
