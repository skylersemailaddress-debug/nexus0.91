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

    append_payload = {
        "project_id": "default",
        "role": "user",
        "content": "behavioral continuity probe",
        "meta": {"source": "run_behavioral_scenarios", "scenario": "continuity"},
    }
    status, append_body = _request_json("POST", f"{base_url.rstrip('/')}/messages/append", append_payload, token)
    append_ok = 200 <= status < 300
    result["checks"]["append"] = {"ok": append_ok, "status": status, "body": append_body}
    if not append_ok:
        result["ok"] = False
        result["errors"].append("/messages/append failed")

    status, resume_body = _request_json("GET", f"{base_url.rstrip('/')}/projects/default/resume", None, token)
    resume_ok = 200 <= status < 300
    result["checks"]["resume_fetch"] = {"ok": resume_ok, "status": status, "body": resume_body}
    if not resume_ok:
        result["ok"] = False
        result["errors"].append("/projects/default/resume failed")
        return result

    resume_text = json.dumps(resume_body).lower()
    has_objective = "objective" in resume_text and "null" not in str(resume_body.get("objective", "null")).lower()
    has_next_step = "next" in resume_text
    has_message_trace = "message" in resume_text or "recent" in resume_text

    result["checks"]["resume_objective"] = {"ok": has_objective}
    result["checks"]["resume_next_step"] = {"ok": has_next_step}
    result["checks"]["resume_message_trace"] = {"ok": has_message_trace}

    for key in ["resume_objective", "resume_next_step", "resume_message_trace"]:
        if not result["checks"][key]["ok"]:
            result["ok"] = False
            result["errors"].append(f"continuity check failed: {key}")

    return result
