from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any


def make_log_event(level: str, event: str, **fields: Any) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "level": level,
        "event": event,
    }
    payload.update(fields)
    return payload


def render_log_event(level: str, event: str, **fields: Any) -> str:
    return json.dumps(make_log_event(level, event, **fields), sort_keys=True)
