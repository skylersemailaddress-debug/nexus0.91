from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def audit_log_path() -> Path:
    return repo_root() / "docs" / "release" / "evidence" / "runtime" / "audit_log.jsonl"


def timeline_path() -> Path:
    return repo_root() / "docs" / "release" / "evidence" / "runtime" / "run_timeline.json"


def _read_records() -> list[dict[str, Any]]:
    path = audit_log_path()
    if not path.exists():
        return []
    out: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            out.append(json.loads(line))
    return out


def build_run_timeline() -> dict[str, Any]:
    records = _read_records()
    timeline: dict[str, list[dict[str, Any]]] = {}
    for record in records:
        event_type = record.get("event_type")
        payload = record.get("payload", {})
        trace = record.get("trace", {})
        run_id = payload.get("run_id") if isinstance(payload, dict) else None
        if event_type == "run_create" and not run_id:
            run_id = payload.get("run_id")
        if not run_id:
            continue
        timeline.setdefault(run_id, []).append(
            {
                "ts": record.get("ts"),
                "event_type": event_type,
                "trace": trace,
                "payload": payload,
            }
        )

    report = {
        "ok": True,
        "runs": timeline,
        "run_count": len(timeline),
    }
    path = timeline_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    return report
