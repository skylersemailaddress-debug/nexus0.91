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

    mem_payload = {
        "project_id": "default",
        "content": "behavioral memory probe",
        "tags": ["behavioral_test"],
    }
    status, upsert_body = _request_json("POST", f"{base_url.rstrip('/')}/memory/upsert", mem_payload, token)
    upsert_ok = 200 <= status < 300
    result["checks"]["memory_upsert"] = {"ok": upsert_ok, "status": status, "body": upsert_body}
    if not upsert_ok:
        result["ok"] = False
        result["errors"].append("/memory/upsert failed")
        return result

    search_payload = {"query": "behavioral memory probe", "top_k": 5}
    status, search_body = _request_json("POST", f"{base_url.rstrip('/')}/memory/search", search_payload, token)
    search_ok = 200 <= status < 300
    result["checks"]["memory_search"] = {"ok": search_ok, "status": status, "body": search_body}
    if not search_ok:
        result["ok"] = False
        result["errors"].append("/memory/search failed")
        return result

    body_text = json.dumps(search_body).lower()
    contains_probe = "behavioral memory probe" in body_text
    result["checks"]["memory_present_in_results"] = {"ok": contains_probe}
    if not contains_probe:
        result["ok"] = False
        result["errors"].append("memory not influencing retrieval results")

    context_payload = {"query": "behavioral memory probe"}
    status, context_body = _request_json("POST", f"{base_url.rstrip('/')}/projects/default/context", context_payload, token)
    context_ok = 200 <= status < 300
    result["checks"]["context_build"] = {"ok": context_ok, "status": status, "body": context_body}
    if not context_ok:
        result["ok"] = False
        result["errors"].append("/projects/default/context failed")
        return result

    selected_memories = context_body.get("selected_memories", [])
    filtered_memories = context_body.get("filtered_memories", [])
    influence_trace = context_body.get("influence_trace", [])
    decision = context_body.get("decision", {})
    next_step = str(decision.get("next_step", ""))

    has_selected_memory = len(selected_memories) > 0
    has_score = any("score" in item for item in selected_memories)
    has_filtering_surface = isinstance(filtered_memories, list)
    has_influence_trace = len(influence_trace) > 0
    decision_changed = "use" in next_step.lower() and "selected memories" in next_step.lower()

    result["checks"]["selected_memory_present"] = {"ok": has_selected_memory}
    result["checks"]["selected_memory_scored"] = {"ok": has_score}
    result["checks"]["filtering_surface_present"] = {"ok": has_filtering_surface}
    result["checks"]["influence_trace_present"] = {"ok": has_influence_trace}
    result["checks"]["decision_changed_by_memory"] = {"ok": decision_changed, "next_step": next_step}

    for key, message in [
        ("selected_memory_present", "no selected memories in context"),
        ("selected_memory_scored", "selected memories are not ranked"),
        ("filtering_surface_present", "filtered memories surface missing"),
        ("influence_trace_present", "memory influence trace missing"),
        ("decision_changed_by_memory", "decision did not change based on memory"),
    ]:
        if not result["checks"][key]["ok"]:
            result["ok"] = False
            result["errors"].append(message)

    return result
