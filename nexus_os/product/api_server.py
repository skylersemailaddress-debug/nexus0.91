from __future__ import annotations

from fastapi import FastAPI
from pydantic import BaseModel

from .state_inference import compute_active_intelligence_line
from .api_contract_routes import router as contract_router
from .ui_state import build_hover_native_ui_state

app = FastAPI(title="Nexus Desktop API")

# Attach commercial runtime contract routes
app.include_router(contract_router)

_GLOBAL_STATE: dict[str, object] = {
    "mission": "No mission set",
    "history": [],
    "conversation_turns": [],
    "workflow": {},
    "decision": "",
    "workspace_id": "workspace:main",
    "run_state": "idle",
    "pending_approvals": [],
    "open_loops": [],
    "relevant_memory": [],
    "artifacts_recent": [],
    "models": {
        "stack": {"gateway_online": True},
        "telemetry": {
            "model_invocations": 0,
            "fallbacks": 0,
            "success_rate": 1.0,
            "recent_activity": [],
        },
    },
    "operator_surface": {
        "governance_cards": [],
        "proof_ids": [],
    },
    "execution_summary": {
        "run_id": None,
        "status": "idle",
        "step_count": 0,
        "attempt_count": 0,
        "latest_step": None,
    },
}


class ConversationRequest(BaseModel):
    text: str


class MissionRequest(BaseModel):
    objective: str


@app.get("/api/health")
def health() -> dict[str, object]:
    return {
        "ok": True,
        "service": "nexus_desktop_api",
        "status": "ready",
    }


@app.get("/api/state")
def get_state() -> dict[str, object]:
    mission = str(_GLOBAL_STATE.get("mission", "No mission set"))
    history = list(_GLOBAL_STATE.get("history", []))
    workflow = dict(_GLOBAL_STATE.get("workflow", {}))
    decision = str(_GLOBAL_STATE.get("decision", ""))
    turns = list(_GLOBAL_STATE.get("conversation_turns", []))
    pending_approvals = list(_GLOBAL_STATE.get("pending_approvals", []))
    open_loops = list(_GLOBAL_STATE.get("open_loops", []))
    relevant_memory = list(_GLOBAL_STATE.get("relevant_memory", []))
    execution_summary = dict(_GLOBAL_STATE.get("execution_summary", {}))

    resume_snapshot = {
        "objective": mission,
        "runtime_status": _GLOBAL_STATE.get("run_state", "idle"),
        "next_step": decision or "Awaiting next operator action.",
        "open_loops": open_loops,
        "pending_approvals": pending_approvals,
        "active": bool(mission and mission != "No mission set"),
        "status": _GLOBAL_STATE.get("run_state", "idle"),
        "mission_id": "mission:current" if mission and mission != "No mission set" else None,
        "relevant_memory": relevant_memory,
        "execution_summary": execution_summary,
        "memory_influence": {
            "query": mission,
            "matches": relevant_memory,
        },
    }

    _data: dict[str, object] = {
        "workspace": {
            "workspace_id": _GLOBAL_STATE.get("workspace_id", "workspace:main"),
            "run_state": _GLOBAL_STATE.get("run_state", "idle"),
        },
        "conversation": {
            "turns": turns,
        },
        "resume_snapshot": resume_snapshot,
        "operator_surface": _GLOBAL_STATE.get("operator_surface", {}),
        "models": _GLOBAL_STATE.get("models", {}),
        "artifacts_recent": _GLOBAL_STATE.get("artifacts_recent", []),
        "mission": mission,
        "signal": compute_active_intelligence_line(history, mission),
        "workflow": workflow,
        "decision": decision,
    }
    _data["hover_native_ui"] = build_hover_native_ui_state(_data)
    return {"ok": True, "data": _data}


@app.post("/api/conversation")
def post_conversation(payload: ConversationRequest) -> dict[str, object]:
    text = payload.text.strip()
    history = list(_GLOBAL_STATE.get("history", []))
    history.append(text)
    _GLOBAL_STATE["history"] = history

    route = "mission_control" if any(term in text.lower() for term in ["deploy", "release", "ship", "rollback"]) else "chat"
    route_reason = "execution_intent_detected" if route == "mission_control" else "general_conversation"

    turns = list(_GLOBAL_STATE.get("conversation_turns", []))
    turns.append(
        {
            "user_text": text,
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
        }
    )
    _GLOBAL_STATE["conversation_turns"] = turns
    _GLOBAL_STATE["decision"] = f"Review next move for: {text}"
    _GLOBAL_STATE["run_state"] = "active"
    return {"ok": True, "data": {"accepted": True}}


@app.post("/api/mission")
def launch_mission(payload: MissionRequest) -> dict[str, object]:
    objective = payload.objective.strip()
    _GLOBAL_STATE["mission"] = objective or "No mission set"
    _GLOBAL_STATE["run_state"] = "active"
    _GLOBAL_STATE["decision"] = "Mission launched. Review workflow and continue."
    _GLOBAL_STATE["pending_approvals"] = [
        {
            "approval_id": "approval:1",
            "mission_id": "mission:current",
            "objective": objective,
            "status": "pending",
        }
    ]
    _GLOBAL_STATE["operator_surface"] = {
        "governance_cards": [
            "Approval required before protected execution.",
            "Operator review is active for this mission.",
        ],
        "proof_ids": ["proof:mission-launch"],
    }
    return {"ok": True, "data": {"mission": objective}}


@app.post("/api/approve")
def approve_next() -> dict[str, object]:
    pending = list(_GLOBAL_STATE.get("pending_approvals", []))
    if pending:
        item = pending.pop(0)
        item["status"] = "approved"
        artifacts = list(_GLOBAL_STATE.get("artifacts_recent", []))
        artifacts.append({
            "id": "artifact:approval",
            "mission_id": item.get("mission_id"),
            "type": "approval_receipt",
        })
        _GLOBAL_STATE["artifacts_recent"] = artifacts
    _GLOBAL_STATE["pending_approvals"] = pending
    _GLOBAL_STATE["decision"] = "Approval resolved. Continue execution."
    _GLOBAL_STATE["run_state"] = "active"
    _GLOBAL_STATE["execution_summary"] = {
        "run_id": "run:desktop",
        "status": "approved",
        "step_count": 1,
        "attempt_count": 1,
        "latest_step": {"phase": "approval"},
    }
    return {"ok": True, "data": {"approved": True}}



def update_desktop_state(*, mission: str | None = None, history: list[str] | None = None, workflow: dict[str, object] | None = None, decision: str | None = None) -> None:
    if mission is not None:
        _GLOBAL_STATE["mission"] = mission
    if history is not None:
        _GLOBAL_STATE["history"] = history
    if workflow is not None:
        _GLOBAL_STATE["workflow"] = workflow
    if decision is not None:
        _GLOBAL_STATE["decision"] = decision
