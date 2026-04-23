from __future__ import annotations

from copy import deepcopy
from typing import Any


def pause_run(job: dict[str, Any], run_id: str) -> dict[str, Any]:
    updated = deepcopy(job)
    for run in updated.get("runs", []):
        if run.get("id") == run_id:
            run["status"] = "paused"
            run.setdefault("events", []).append({"type": "paused"})
            return updated
    raise KeyError(run_id)


def resume_run(job: dict[str, Any], run_id: str) -> dict[str, Any]:
    updated = deepcopy(job)
    for run in updated.get("runs", []):
        if run.get("id") == run_id:
            run["status"] = "running"
            run.setdefault("events", []).append({"type": "resumed"})
            return updated
    raise KeyError(run_id)


def retry_run(job: dict[str, Any], run_id: str, max_attempts: int = 3) -> dict[str, Any]:
    updated = deepcopy(job)
    for run in updated.get("runs", []):
        if run.get("id") == run_id:
            attempts = int(run.get("attempt_count", 1) or 1)
            if attempts >= max_attempts:
                run.setdefault("events", []).append({"type": "retry_blocked"})
                return updated
            run["attempt_count"] = attempts + 1
            run["status"] = "running"
            run.setdefault("events", []).append({"type": "retried", "attempt_count": run["attempt_count"]})
            return updated
    raise KeyError(run_id)


def restore_runs(job: dict[str, Any]) -> dict[str, Any]:
    restored = deepcopy(job)
    for run in restored.get("runs", []):
        status = run.get("status")
        if status in {"running", "paused"}:
            run["restored"] = True
            run.setdefault("events", []).append({"type": "restored"})
    return restored
