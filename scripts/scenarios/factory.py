from __future__ import annotations

import json
import urllib.request


def run(base_url: str, token=None):
    result = {"ok": True, "checks": {}, "errors": []}

    payload = json.dumps({"goal": "factory test"}).encode()
    req = urllib.request.Request(f"{base_url}/factory/generate", data=payload, headers={"Content-Type": "application/json"}, method="POST")
    resp = urllib.request.urlopen(req)
    data = json.loads(resp.read().decode())

    checks = {
        "has_manifest": "manifest" in data,
        "has_spec": "spec" in data,
    }

    for k, v in checks.items():
        result["checks"][k] = {"ok": v}
        if not v:
            result["ok"] = False

    return result
