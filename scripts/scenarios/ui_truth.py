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

    status, surface_body = _request_json("GET", f"{base_url.rstrip('/')}/operator/surface", None, token)
    surface_ok = 200 <= status < 300
    result["checks"]["surface_fetch"] = {"ok": surface_ok, "status": status, "body": surface_body}
    if not surface_ok:
        result["ok"] = False
        result["errors"].append("operator surface fetch failed")
        return result

    mission = surface_body.get("mission", {})
    approvals = surface_body.get("approvals", {})
    memory = surface_body.get("memory", {})
    progress = surface_body.get("progress", {})
    proof = surface_body.get("proof", {})

    mission_backed = bool(mission.get("runtime_backed") and mission.get("objective") and mission.get("next_step"))
    approvals_backed = bool(approvals.get("runtime_backed"))
    memory_present = int(memory.get("count", 0)) > 0
    memory_influence = len(memory.get("influence_trace", [])) > 0
    progress_runs = int(progress.get("run_count", 0)) > 0
    proof_artifacts = len(proof.get("artifacts", [])) > 0
    proof_ids = len(proof.get("proof_ids", [])) > 0

    result["checks"]["mission_backed"] = {"ok": mission_backed, "mission": mission}
    result["checks"]["approvals_backed"] = {"ok": approvals_backed, "approvals": approvals}
    result["checks"]["memory_present"] = {"ok": memory_present, "count": memory.get("count", 0)}
    result["checks"]["memory_influence"] = {"ok": memory_influence, "influence_trace": memory.get("influence_trace", [])}
    result["checks"]["progress_runs"] = {"ok": progress_runs, "run_count": progress.get("run_count", 0)}
    result["checks"]["proof_artifacts"] = {"ok": proof_artifacts, "artifact_count": len(proof.get("artifacts", []))}
    result["checks"]["proof_ids"] = {"ok": proof_ids, "proof_ids": proof.get("proof_ids", [])}

    for key, message in [
        ("mission_backed", "mission not runtime-backed"),
        ("approvals_backed", "approvals not runtime-backed"),
        ("memory_present", "memory not surfaced"),
        ("memory_influence", "memory influence not surfaced"),
        ("progress_runs", "progress not backed by runs"),
        ("proof_artifacts", "proof artifacts missing"),
        ("proof_ids", "proof ids missing"),
    ]:
        if not result["checks"][key]["ok"]:
            result["ok"] = False
            result["errors"].append(message)

    return result
