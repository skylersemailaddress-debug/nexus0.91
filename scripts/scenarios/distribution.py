from __future__ import annotations

import json
import urllib.request


def run(base_url: str, token=None):
    result = {"ok": True, "checks": {}, "errors": []}

    payload = json.dumps({
        "content": "distribution test",
        "channel": "internal"
    }).encode()

    req = urllib.request.Request(
        f"{base_url}/distribution/publish",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    resp = urllib.request.urlopen(req)
    data = json.loads(resp.read().decode())

    logs_resp = urllib.request.urlopen(f"{base_url}/distribution/logs")
    logs = json.loads(logs_resp.read().decode())

    checks = {
        "published": data.get("ok") is True,
        "logs_present": len(logs.get("logs", [])) > 0,
    }

    for k, v in checks.items():
        result["checks"][k] = {"ok": v}
        if not v:
            result["ok"] = False

    return result
