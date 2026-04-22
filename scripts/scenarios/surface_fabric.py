from __future__ import annotations

import json
import urllib.request


def run(base_url: str, token=None):
    result = {"ok": True, "checks": {}, "errors": []}

    resp = urllib.request.urlopen(f"{base_url}/surface/fabric/manifests")
    data = json.loads(resp.read().decode())

    checks = {
        "has_surfaces": "surfaces" in data,
        "has_mission": any(s["id"] == "mission" for s in data.get("surfaces", [])),
    }

    for k, v in checks.items():
        result["checks"][k] = {"ok": v}
        if not v:
            result["ok"] = False

    return result
