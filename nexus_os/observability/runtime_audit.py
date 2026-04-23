from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from nexus_os.observability.trace_context import get_trace_context


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def audit_log_path() -> Path:
    return repo_root() / "docs" / "release" / "evidence" / "runtime" / "audit_log.jsonl"


def utc_now_iso() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat()


def append_audit_event(event_type: str, payload: dict[str, Any]) -> None:
    path = audit_log_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    trace = get_trace_context()
    record = {
        "ts": utc_now_iso(),
        "event_type": event_type,
        "trace": trace,
        "payload": payload,
    }
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, sort_keys=True) + "\n")
