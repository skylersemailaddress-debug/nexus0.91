from __future__ import annotations

import json
import urllib.request
from typing import Any


def run(base_url: str, token: str | None = None) -> dict[str, Any]:
    result: dict[str, Any] = {"ok": True, "checks": {}, "errors": []}

    try:
        req = urllib.request.Request(
            f"{base_url.rstrip('/')}/intelligence/plan",
            data=b"{}",
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=20) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except Exception as exc:
        return {"ok": False, "checks": {}, "errors": [str(exc)]}

    checks = {
        "has_context": bool(data.get("context_summary")),
        "has_action": bool(data.get("recommended_action")),
        "has_next_step": bool(data.get("next_step")),
        "has_trace": isinstance(data.get("trace"), dict),
    }

    for k, v in checks.items():
        result["checks"][k] = {"ok": v}
        if not v:
            result["ok"] = False
            result["errors"].append(k)

    return result
