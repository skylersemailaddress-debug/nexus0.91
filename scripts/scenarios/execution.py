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

    status, state_body = _request_json("GET", f"{base_url.rstrip('/')}/runs/{run_id}", None, token)
    state_ok = 200 <= status < 300
    result["checks"]["run_state_fetch"] = {"ok": state_ok, "status": status, "body": state_body}
    if not state_ok:
        result["ok"] = False
        result["errors"].append("/runs/{id} fetch failed")

    body_text = json.dumps(state_body).lower()
    has_status = "status" in body_text

    result["checks"]["run_has_status"] = {"ok": has_status}
    if not has_status:
        result["ok"] = False
        result["errors"].append("run state missing status")

    return result
