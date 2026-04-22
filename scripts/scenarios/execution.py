from __future__ import annotations

import json
import urllib.error
import urllib.request
from typing import Any


def _request_json(method: str, url: str, payload: dict[str, Any] | None = None, token: str | None = None) -> tuple[int, Any]:
    data = None
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            body = resp.read().decode("utf-8")
            return resp.status, json.loads(body) if body else {}
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="ignore")
        parsed: Any = {"raw": body}
        try:
            parsed = json.loads(body) if body else {}
        except Exception:
            pass
        return exc.code, parsed
    except Exception as exc:
        return 0, {"error": str(exc)}


def run(base_url: str, token: str | None = None) -> dict[str, Any]:
    result: dict[str, Any] = {"ok": True, "checks": {}, "errors": []}

    run_payload = {"goal": "behavioral execution probe"}
    status, run_body = _request_json("POST", f"{base_url.rstrip('/')}/runs/create", run_payload, token)
    create_ok = 200 <= status < 300
    result["checks"]["run_create"] = {"ok": create_ok, "status": status, "body": run_body}
    if not create_ok:
        result["ok"] = False
        result["errors"].append("/runs/create failed")
        return result

    run_id = run_body.get("run_id") or run_body.get("id")
    if not run_id:
        result["ok"] = False
        result["errors"].append("run id missing")
        return result

    created_attempt_count = int((run_body.get("run") or {}).get("attempt_count", 0))

    status, pause_body = _request_json("POST", f"{base_url.rstrip('/')}/runs/{run_id}/pause", None, token)
    pause_ok = 200 <= status < 300 and pause_body.get("status") == "paused"
    result["checks"]["run_pause"] = {"ok": pause_ok, "status": status, "body": pause_body}

    status, resume_body = _request_json("POST", f"{base_url.rstrip('/')}/runs/{run_id}/resume", None, token)
    resume_ok = 200 <= status < 300 and resume_body.get("status") == "running"
    result["checks"]["run_resume"] = {"ok": resume_ok, "status": status, "body": resume_body}

    status, retry_body = _request_json("POST", f"{base_url.rstrip('/')}/runs/{run_id}/retry", None, token)
    retry_ok = 200 <= status < 300 and retry_body.get("status") == "running"
    result["checks"]["run_retry"] = {"ok": retry_ok, "status": status, "body": retry_body}

    retry_attempt_count = int(retry_body.get("attempt_count", 0))
    attempts_incremented = retry_attempt_count > created_attempt_count
    result["checks"]["attempt_count_incremented"] = {
        "ok": attempts_incremented,
        "before": created_attempt_count,
        "after": retry_attempt_count,
    }

    status, artifact_body = _request_json(
        "POST",
        f"{base_url.rstrip('/')}/runs/{run_id}/artifacts",
        {"type": "evidence", "content": "behavioral execution artifact"},
        token,
    )
    artifact_bind_ok = 200 <= status < 300
    result["checks"]["artifact_bind"] = {"ok": artifact_bind_ok, "status": status, "body": artifact_body}

    status, state_body = _request_json("GET", f"{base_url.rstrip('/')}/runs/{run_id}", None, token)
    state_ok = 200 <= status < 300
    result["checks"]["run_state_fetch"] = {"ok": state_ok, "status": status, "body": state_body}
    if not state_ok:
        result["ok"] = False
        result["errors"].append("/runs/{id} fetch failed")
        return result

    has_status = isinstance(state_body.get("status"), str) and len(state_body.get("status", "")) > 0
    has_artifacts = isinstance(state_body.get("artifacts"), list) and len(state_body.get("artifacts")) > 0
    has_events = isinstance(state_body.get("events"), list) and len(state_body.get("events")) >= 3

    result["checks"]["run_has_status"] = {"ok": has_status}
    result["checks"]["run_has_artifacts"] = {"ok": has_artifacts}
    result["checks"]["run_has_events"] = {"ok": has_events}

    for key, message in [
        ("run_pause", "pause transition failed"),
        ("run_resume", "resume transition failed"),
        ("run_retry", "retry transition failed"),
        ("attempt_count_incremented", "retry did not increment attempt count"),
        ("artifact_bind", "artifact binding failed"),
        ("run_has_status", "run state missing status"),
        ("run_has_artifacts", "run state missing artifacts"),
        ("run_has_events", "run state missing lifecycle events"),
    ]:
        if not result["checks"][key]["ok"]:
            result["ok"] = False
            result["errors"].append(message)

    return result
