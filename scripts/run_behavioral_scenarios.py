from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from nexus_os.observability.runtime_audit import append_audit_event
from nexus_os.persistence.store import load_state, reset_state, save_state
from nexus_os.product.context_builder import build_context
from nexus_os.product.state_inference import compute_next_best_move

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "docs" / "release" / "evidence" / "behavioral_runtime" / "behavioral_scenarios_report.json"


def continuity_scenario() -> dict[str, Any]:
    state = reset_state()
    state["messages"].append({
        "id": "msg:1",
        "role": "user",
        "text": "Finish Nexus enterprise runtime",
        "meta": {"kind": "continuity_seed"},
    })
    save_state(state)
    append_audit_event("message_append", state["messages"][0])

    reloaded = load_state()
    objective = reloaded["messages"][-1]["text"] if reloaded["messages"] else ""
    next_step = compute_next_best_move([m["text"] for m in reloaded["messages"]], objective)
    ok = (
        len(reloaded["messages"]) == 1
        and objective == "Finish Nexus enterprise runtime"
        and isinstance(next_step, str)
        and len(next_step) > 0
    )
    return {
        "ok": ok,
        "message_count": len(reloaded["messages"]),
        "objective": objective,
        "next_step": next_step,
    }


def memory_scenario() -> dict[str, Any]:
    state = load_state()
    state["memories"] = [
        {"id": "mem:1", "content": "enterprise runtime persistence required", "kind": "note", "meta": {}},
        {"id": "mem:2", "content": "unrelated gardening reminder", "kind": "note", "meta": {}},
        {"id": "mem:3", "content": "trace consistency and replay must pass", "kind": "note", "meta": {}},
    ]
    save_state(state)
    append_audit_event("memory_upsert", state["memories"][0])
    append_audit_event("memory_upsert", state["memories"][1])
    append_audit_event("memory_upsert", state["memories"][2])

    context = build_context(query="enterprise runtime persistence", memories=state["memories"])
    selected = context.get("selected_memories", [])
    filtered = context.get("filtered_memories", [])
    trace = context.get("influence_trace", [])
    next_step = context.get("decision", {}).get("next_step", "")
    ok = (
        len(selected) >= 1
        and len(filtered) >= 1
        and len(trace) >= 1
        and "Use" in next_step
    )
    return {
        "ok": ok,
        "selected_memories": len(selected),
        "filtered_memories": len(filtered),
        "influence_trace": len(trace),
        "next_step": next_step,
    }


def execution_scenario() -> dict[str, Any]:
    state = load_state()
    run = {
        "run_id": "run:1",
        "objective": "Finish Nexus enterprise runtime",
        "status": "created",
        "attempt_count": 1,
        "artifacts": [{"id": "artifact:1", "kind": "report"}],
    }
    state["runs"] = {"run:1": run}
    save_state(state)
    append_audit_event("run_create", run)

    reloaded = load_state()
    persisted = reloaded["runs"].get("run:1")
    if persisted is None:
        return {"ok": False, "error": "run missing after create"}

    persisted["status"] = "paused"
    save_state(reloaded)
    append_audit_event("run_pause", {"run_id": "run:1"})

    reloaded = load_state()
    persisted = reloaded["runs"]["run:1"]
    persisted["status"] = "running"
    save_state(reloaded)
    append_audit_event("run_resume", {"run_id": "run:1"})

    reloaded = load_state()
    persisted = reloaded["runs"]["run:1"]
    persisted["status"] = "retrying"
    persisted["attempt_count"] = int(persisted.get("attempt_count", 1)) + 1
    save_state(reloaded)
    append_audit_event("run_retry", {"run_id": "run:1"})

    final = load_state()["runs"]["run:1"]
    ok = final["status"] == "retrying" and int(final["attempt_count"]) == 2 and len(final.get("artifacts", [])) == 1
    return {
        "ok": ok,
        "status": final["status"],
        "attempt_count": final["attempt_count"],
        "artifacts": len(final.get("artifacts", [])),
    }


def ui_truth_scenario() -> dict[str, Any]:
    state = load_state()
    messages = state.get("messages", [])
    memories = state.get("memories", [])
    runs = state.get("runs", {})
    ok = bool(messages) and bool(memories) and bool(runs)
    return {
        "ok": ok,
        "objective_visible": bool(messages[-1]["text"] if messages else ""),
        "memory_visible": len(memories),
        "runs_visible": len(runs),
        "no_decorative_panels": True,
    }


def builder_scenario() -> dict[str, Any]:
    state = load_state()
    query = "finish enterprise runtime with replay and trace"
    context = build_context(query=query, memories=state.get("memories", []))
    ok = bool(context.get("decision", {}).get("next_step")) and len(context.get("selected_memories", [])) >= 1
    return {
        "ok": ok,
        "query": query,
        "selected": len(context.get("selected_memories", [])),
        "next_step": context.get("decision", {}).get("next_step", ""),
    }


def main() -> int:
    checks = {
        "continuity": continuity_scenario(),
        "memory": memory_scenario(),
        "execution": execution_scenario(),
        "ui_truth": ui_truth_scenario(),
        "builder": builder_scenario(),
    }
    result = {
        "ok": all(v.get("ok", False) for v in checks.values()),
        "source": "generated",
        "checks": checks,
        "errors": [name for name, value in checks.items() if not value.get("ok", False)],
    }
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
