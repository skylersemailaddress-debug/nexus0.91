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

    create_payload = {"goal": "behavioral builder probe"}
    status, create_body = _request_json("POST", f"{base_url.rstrip('/')}/capabilities/create", create_payload, token)
    create_ok = 200 <= status < 300
    result["checks"]["capability_create"] = {"ok": create_ok, "status": status, "body": create_body}
    if not create_ok:
        result["ok"] = False
        result["errors"].append("/capabilities/create failed")
        return result

    capability = create_body.get("capability", {})
    capability_id = capability.get("id")
    initial_output = str(capability.get("output", ""))
    initial_version = int(capability.get("version", 0))

    has_output = len(initial_output.strip()) > 0
    result["checks"]["capability_has_output"] = {"ok": has_output, "output": initial_output}

    if not capability_id:
        result["ok"] = False
        result["errors"].append("capability id missing")
        return result

    status, validate_body = _request_json("POST", f"{base_url.rstrip('/')}/capabilities/{capability_id}/validate", None, token)
    validate_ok = 200 <= status < 300 and bool(validate_body.get("capability", {}).get("validated"))
    result["checks"]["capability_validate"] = {"ok": validate_ok, "status": status, "body": validate_body}

    updated_content = "Updated capability output for behavioral builder probe"
    status, update_body = _request_json(
        "POST",
        f"{base_url.rstrip('/')}/capabilities/{capability_id}/update",
        {"content": updated_content},
        token,
    )
    update_ok = 200 <= status < 300
    result["checks"]["capability_update"] = {"ok": update_ok, "status": status, "body": update_body}

    updated_capability = update_body.get("capability", {})
    version_incremented = int(updated_capability.get("version", 0)) > initial_version
    output_changed = str(updated_capability.get("output", "")) == updated_content
    evidence_present = isinstance(updated_capability.get("evidence"), list) and len(updated_capability.get("evidence")) >= 2
    result["checks"]["capability_version_incremented"] = {"ok": version_incremented, "before": initial_version, "after": updated_capability.get("version")}
    result["checks"]["capability_output_changed"] = {"ok": output_changed}
    result["checks"]["capability_evidence_present"] = {"ok": evidence_present, "evidence_count": len(updated_capability.get("evidence", [])) if isinstance(updated_capability.get("evidence"), list) else 0}

    status, list_body = _request_json("GET", f"{base_url.rstrip('/')}/capabilities", None, token)
    list_ok = 200 <= status < 300
    result["checks"]["capability_registry_fetch"] = {"ok": list_ok, "status": status, "body": list_body}
    registry = list_body.get("capabilities", []) if isinstance(list_body, dict) else []
    registry_contains = any(item.get("id") == capability_id for item in registry if isinstance(item, dict))
    result["checks"]["capability_registry_contains_item"] = {"ok": registry_contains}

    for key, message in [
        ("capability_has_output", "capability output is empty"),
        ("capability_validate", "capability validation failed"),
        ("capability_update", "capability update failed"),
        ("capability_version_incremented", "capability version did not increment"),
        ("capability_output_changed", "capability output did not change"),
        ("capability_evidence_present", "capability evidence missing"),
        ("capability_registry_fetch", "capability registry fetch failed"),
        ("capability_registry_contains_item", "capability missing from registry"),
    ]:
        if not result["checks"][key]["ok"]:
            result["ok"] = False
            result["errors"].append(message)

    return result
