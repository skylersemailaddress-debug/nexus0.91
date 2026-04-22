from __future__ import annotations

import json
import urllib.request


def run(base_url: str, token=None):
    result = {"ok": True, "checks": {}, "errors": []}

    # ingest
    payload = json.dumps({"title": "ai dev tools", "source": "test", "weight": 0.9}).encode()
    try:
        req = urllib.request.Request(f"{base_url}/market/intelligence/ingest", data=payload, headers={"Content-Type": "application/json"}, method="POST")
        urllib.request.urlopen(req)
    except Exception as e:
        return {"ok": False, "errors": [str(e)], "checks": {}}

    # fetch
    try:
        with urllib.request.urlopen(f"{base_url}/market/intelligence/opportunities") as resp:
            data = json.loads(resp.read().decode())
    except Exception as e:
        return {"ok": False, "errors": [str(e)], "checks": {}}

    checks = {
        "has_opportunities": len(data.get("opportunities", [])) > 0,
        "has_score": "score" in data.get("opportunities", [{}])[0],
    }

    for k, v in checks.items():
        result["checks"][k] = {"ok": v}
        if not v:
            result["ok"] = False
            result["errors"].append(k)

    return result
