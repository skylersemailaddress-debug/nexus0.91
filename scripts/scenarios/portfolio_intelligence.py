from __future__ import annotations

import json
import urllib.request


def run(base_url: str, token=None):
    result = {"ok": True, "checks": {}, "errors": []}

    # create
    data = json.dumps({"name": "test_project"}).encode()
    req = urllib.request.Request(f"{base_url}/portfolio/projects/create", data=data, headers={"Content-Type": "application/json"}, method="POST")
    resp = urllib.request.urlopen(req)
    project = json.loads(resp.read().decode())["project"]
    pid = project["id"]

    # score
    urllib.request.urlopen(urllib.request.Request(f"{base_url}/portfolio/projects/{pid}/score", method="POST"))

    # list
    with urllib.request.urlopen(f"{base_url}/portfolio/projects") as r:
        data = json.loads(r.read().decode())

    checks = {
        "has_project": len(data.get("projects", [])) > 0,
    }

    for k, v in checks.items():
        result["checks"][k] = {"ok": v}
        if not v:
            result["ok"] = False

    return result
