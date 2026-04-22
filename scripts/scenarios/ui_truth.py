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

    status, resume_body = _request_json("GET", f"{base_url.rstrip('/')}/projects/default/resume", None, token)
    ok = 200 <= status < 300
    result["checks"]["resume"] = {"ok": ok, "status": status, "body": resume_body}
    if not ok:
        result["ok"] = False
        result["errors"].append("resume endpoint failed")
        return result

    text = json.dumps(resume_body).lower()

    no_placeholders = "null" not in text and "placeholder" not in text
    has_activity = any(k in text for k in ["job", "run", "objective", "message"])

    result["checks"]["no_placeholders"] = {"ok": no_placeholders}
    result["checks"]["has_activity"] = {"ok": has_activity}

    if not no_placeholders:
        result["ok"] = False
        result["errors"].append("ui contains placeholders/nulls")
    if not has_activity:
        result["ok"] = False
        result["errors"].append("ui not backed by runtime activity")

    return result
