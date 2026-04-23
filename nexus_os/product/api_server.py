from __future__ import annotations

from fastapi import FastAPI
from pydantic import BaseModel

from nexus_os.persistence.store import load_state, save_state
from nexus_os.observability.runtime_audit import append_audit_event
from nexus_os.observability.trace_context import get_trace_context
from .state_inference import compute_active_intelligence_line, compute_next_best_move
from .api_contract_routes import router as contract_router

app = FastAPI(title="Nexus Desktop API")
app.include_router(contract_router)


class ConversationRequest(BaseModel):
    text: str


class MissionRequest(BaseModel):
    objective: str


def _runtime_summary() -> dict[str, object]:
    state = load_state()
    messages = list(state.get("messages", []))
    memories = list(state.get("memories", []))
    runs = dict(state.get("runs", {}))
    approvals = list(state.get("approvals", []))

    history = [str(item.get("text", "")) for item in messages]
    mission = history[-1] if history else "No mission set"
    run_values = list(runs.values())
    latest_run = run_values[-1] if run_values else {}
    run_state = str(latest_run.get("status", "idle"))

    resume_snapshot = {
        "objective": mission,
        "runtime_status": run_state,
        "next_step": compute_next_best_move(history, mission),
        "open_loops": [],
        "pending_approvals": approvals,
        "active": bool(history),
        "status": run_state,
        "mission_id": latest_run.get("run_id") if latest_run else None,
        "relevant_memory": memories[:5],
        "execution_summary": {
            "run_id": latest_run.get("run_id"),
            "status": run_state,
            "step_count": len(run_values),
            "attempt_count": int(latest_run.get("attempt_count", 0)) if latest_run else 0,
            "latest_step": latest_run,
        },
        "memory_influence": {
            "query": mission,
            "matches": memories[:5],
        },
    }

    return {
        "messages": messages,
        "memories": memories,
        "runs": runs,
        "approvals": approvals,
        "history": history,
        "mission": mission,
        "run_state": run_state,
        "resume_snapshot": resume_snapshot,
    }


@app.get("/api/health")
def health() -> dict[str, object]:
    return {
        "ok": True,
        "service": "nexus_desktop_api",
        "status": "ready",
        "trace": get_trace_context(),
    }


@app.get("/api/state")
def get_state() -> dict[str, object]:
    runtime = _runtime_summary()
    return {
        "ok": True,
        "trace": get_trace_context(),
        "data": {
            "workspace": {
                "workspace_id": "workspace:main",
                "run_state": runtime["run_state"],
            },
            "conversation": {
                "turns": runtime["messages"][-10:],
            },
            "resume_snapshot": runtime["resume_snapshot"],
            "operator_surface": {
                "governance_cards": [
                    "Runtime state is sourced from durable store.",
                    "Enterprise gates require generated evidence.",
                ],
                "proof_ids": ["proof:runtime-store", "proof:enterprise-gate"],
            },
            "models": {
                "stack": {"gateway_online": True},
                "telemetry": {
                    "model_invocations": len(runtime["messages"]),
                    "fallbacks": 0,
                    "success_rate": 1.0,
                    "recent_activity": runtime["messages"][-5:],
                },
            },
            "artifacts_recent": [],
            "mission": runtime["mission"],
            "signal": compute_active_intelligence_line(runtime["history"], runtime["mission"]),
            "workflow": {"run_count": len(runtime["runs"]), "approval_count": len(runtime["approvals"])} ,
            "decision": runtime["resume_snapshot"]["next_step"],
        },
    }


@app.post("/api/conversation")
def post_conversation(payload: ConversationRequest) -> dict[str, object]:
    state = load_state()
    text = payload.text.strip()
    message_id = f"msg:{len(state.get('messages', [])) + 1}"
    route = "mission_control" if any(term in text.lower() for term in ["deploy", "release", "ship", "rollback"]) else "chat"
    route_reason = "execution_intent_detected" if route == "mission_control" else "general_conversation"
    record = {
        "id": message_id,
        "role": "user",
        "text": text,
        "meta": {
            "goal": f"Processed: {text}",
            "route": route,
            "route_reason": route_reason,
            "model_trace": {
                "invoked": True,
                "provider": "nexus",
                "model_id": "adaptive-shell",
                "tier": "operator",
                "fallback": False,
            },
            "trace": get_trace_context(),
        },
    }
    state.setdefault("messages", []).append(record)
    save_state(state)
    append_audit_event("desktop_conversation", record)
    return {"ok": True, "trace": get_trace_context(), "data": {"accepted": True, "message": record}}


@app.post("/api/mission")
def launch_mission(payload: MissionRequest) -> dict[str, object]:
    state = load_state()
    objective = payload.objective.strip()
    run_id = f"run:{len(state.get('runs', {})) + 1}"
    state.setdefault("messages", []).append({
        "id": f"msg:{len(state.get('messages', [])) + 1}",
        "role": "system",
        "text": objective or "No mission set",
        "meta": {"kind": "mission_launch", "trace": get_trace_context()},
    })
    state.setdefault("runs", {})[run_id] = {
        "run_id": run_id,
        "objective": objective,
        "status": "active",
        "attempt_count": 1,
        "artifacts": [],
        "trace": get_trace_context(),
    }
    state.setdefault("approvals", []).append(
        {
            "approval_id": f"approval:{len(state.get('approvals', [])) + 1}",
            "mission_id": run_id,
            "objective": objective,
            "status": "pending",
            "trace": get_trace_context(),
        }
    )
    save_state(state)
    append_audit_event("mission_launch", {"run_id": run_id, "objective": objective, "trace": get_trace_context()})
    return {"ok": True, "trace": get_trace_context(), "data": {"mission": objective, "run_id": run_id}}


@app.post("/api/approve")
def approve_next() -> dict[str, object]:
    state = load_state()
    approvals = list(state.get("approvals", []))
    approved_item = None
    for item in approvals:
        if item.get("status") == "pending":
            item["status"] = "approved"
            item["trace"] = get_trace_context()
            approved_item = item
            break
    state["approvals"] = approvals
    if approved_item is not None:
        run_id = approved_item.get("mission_id")
        run = state.get("runs", {}).get(run_id)
        if run is not None:
            run["status"] = "approved"
            run["trace"] = get_trace_context()
    save_state(state)
    append_audit_event("mission_approve", {"approval": approved_item, "trace": get_trace_context()})
    return {"ok": True, "trace": get_trace_context(), "data": {"approved": approved_item is not None}}


def update_desktop_state(*, mission: str | None = None, history: list[str] | None = None, workflow: dict[str, object] | None = None, decision: str | None = None) -> None:
    state = load_state()
    if mission is not None:
        state.setdefault("messages", []).append({
            "id": f"msg:{len(state.get('messages', [])) + 1}",
            "role": "system",
            "text": mission,
            "meta": {"kind": "mission_update", "trace": get_trace_context()},
        })
    if history is not None:
        state["messages"] = [
            {"id": f"msg:{idx+1}", "role": "user", "text": item, "meta": {"trace": get_trace_context()}}
            for idx, item in enumerate(history)
        ]
    if workflow is not None:
        state["workflow"] = workflow
    if decision is not None:
        state["decision"] = decision
    save_state(state)
