from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from nexus_os.persistence.store import reset_state, load_state, save_state


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def audit_log_path() -> Path:
    return repo_root() / "docs" / "release" / "evidence" / "runtime" / "audit_log.jsonl"


def replay_report_path() -> Path:
    return repo_root() / "docs" / "release" / "evidence" / "runtime" / "replay_report.json"


def _read_lines(path: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    if not path.exists():
        return records
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        records.append(json.loads(line))
    return records


def replay_audit_log() -> dict[str, Any]:
    records = _read_lines(audit_log_path())
    state = reset_state()
    applied = 0

    for record in records:
        event_type = record.get("event_type")
        payload = record.get("payload", {})
        if event_type == "message_append":
            state["messages"].append(payload)
            applied += 1
        elif event_type == "memory_upsert":
            memory_id = payload.get("id")
            existing = next((m for m in state["memories"] if m.get("id") == memory_id), None)
            if existing is None:
                state["memories"].append(payload)
            else:
                existing.update(payload)
            applied += 1
        elif event_type == "run_create":
            run_id = payload.get("run_id")
            if run_id:
                state["runs"][run_id] = payload
                applied += 1
        elif event_type in {"run_pause", "run_resume", "run_retry"}:
            run_id = payload.get("run_id")
            run = state["runs"].get(run_id)
            if run is not None:
                if event_type == "run_pause":
                    run["status"] = "paused"
                elif event_type == "run_resume":
                    run["status"] = "running"
                elif event_type == "run_retry":
                    run["status"] = "retrying"
                    run["attempt_count"] = int(run.get("attempt_count", 1)) + 1
                applied += 1

    save_state(state)
    final_state = load_state()
    report = {
        "ok": True,
        "records_seen": len(records),
        "records_applied": applied,
        "messages": len(final_state.get("messages", [])),
        "memories": len(final_state.get("memories", [])),
        "runs": len(final_state.get("runs", {})),
    }
    replay_report_path().parent.mkdir(parents=True, exist_ok=True)
    replay_report_path().write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    return report
