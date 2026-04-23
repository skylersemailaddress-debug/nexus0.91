from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from nexus_os.persistence.store import load_state, save_state
from nexus_os.observability.runtime_audit import append_audit_event
from .context_builder import build_context
from .state_inference import compute_next_best_move

router = APIRouter(prefix="/api", tags=["contracts"])


class MessageAppendRequest(BaseModel):
    text: str
    role: str = "user"
    meta: dict[str, Any] = {}


class MemoryUpsertRequest(BaseModel):
    id: str
    content: str
    kind: str = "note"
    meta: dict[str, Any] = {}


class MemorySearchRequest(BaseModel):
    query: str


class RunCreateRequest(BaseModel):
    objective: str


class BuildContextRequest(BaseModel):
    query: str


@router.get("/contracts/status")
def contract_status() -> dict[str, Any]:
    state = load_state()
    return {
        "ok": True,
        "contracts": "active",
        "runtime": {
            "messages": len(state["messages"]),
            "memories": len(state["memories"]),
            "runs": len(state["runs"]),
            "approvals": len(state["approvals"]),
        },
    }


@router.post("/messages/append")
def append_message(payload: MessageAppendRequest) -> dict[str, Any]:
    state = load_state()
    message_id = f"msg:{len(state['messages']) + 1}"
    record = {
        "id": message_id,
        "role": payload.role,
        "text": payload.text.strip(),
        "meta": dict(payload.meta),
    }
    state["messages"].append(record)
    save_state(state)
    append_audit_event("message_append", record)
    return {"ok": True, "message": record}


@router.get("/projects/default/resume")
def project_resume() -> dict[str, Any]:
    state = load_state()
    messages = list(state["messages"])
    latest_text = messages[-1]["text"] if messages else ""
    objective = latest_text or "No active objective"
    next_step = compute_next_best_move([m["text"] for m in messages], objective)
    return {
        "ok": True,
        "project_id": "default",
        "objective": objective,
        "next_step": next_step,
        "recent_messages": messages[-10:],
        "approvals": list(state["approvals"]),
        "run_count": len(state["runs"]),
        "memory_count": len(state["memories"]),
    }


@router.post("/memory/upsert")
def memory_upsert(payload: MemoryUpsertRequest) -> dict[str, Any]:
    state = load_state()
    existing = next((m for m in state["memories"] if m["id"] == payload.id), None)
    record = {
        "id": payload.id,
        "content": payload.content,
        "kind": payload.kind,
        "meta": dict(payload.meta),
    }
    if existing is None:
        state["memories"].append(record)
    else:
        existing.update(record)
    save_state(state)
    append_audit_event("memory_upsert", record)
    return {"ok": True, "memory": record}


@router.post("/memory/search")
def memory_search(payload: MemorySearchRequest) -> dict[str, Any]:
    state = load_state()
    context = build_context(query=payload.query, memories=list(state["memories"]))
    append_audit_event("memory_search", {"query": payload.query})
    return {"ok": True, **context}


@router.post("/state/build_context")
def state_build_context(payload: BuildContextRequest) -> dict[str, Any]:
    state = load_state()
    context = build_context(query=payload.query, memories=list(state["memories"]))
    context["messages"] = list(state["messages"][-10:])
    append_audit_event("build_context", {"query": payload.query})
    return {"ok": True, **context}


@router.post("/runs/create")
def runs_create(payload: RunCreateRequest) -> dict[str, Any]:
    state = load_state()
    run_id = f"run:{len(state['runs']) + 1}"
    run = {
        "run_id": run_id,
        "objective": payload.objective,
        "status": "created",
        "attempt_count": 1,
        "artifacts": [],
    }
    state["runs"][run_id] = run
    save_state(state)
    append_audit_event("run_create", run)
    return {"ok": True, "run": run}


@router.get("/runs/{run_id}")
def runs_get(run_id: str) -> dict[str, Any]:
    state = load_state()
    run = state["runs"].get(run_id)
    if run is None:
        raise HTTPException(status_code=404, detail="run not found")
    return {"ok": True, "run": run}


@router.post("/runs/{run_id}/pause")
def runs_pause(run_id: str) -> dict[str, Any]:
    state = load_state()
    run = state["runs"].get(run_id)
    if run is None:
        raise HTTPException(status_code=404, detail="run not found")
    run["status"] = "paused"
    save_state(state)
    append_audit_event("run_pause", {"run_id": run_id})
    return {"ok": True, "run": run}


@router.post("/runs/{run_id}/resume")
def runs_resume(run_id: str) -> dict[str, Any]:
    state = load_state()
    run = state["runs"].get(run_id)
    if run is None:
        raise HTTPException(status_code=404, detail="run not found")
    run["status"] = "running"
    save_state(state)
    append_audit_event("run_resume", {"run_id": run_id})
    return {"ok": True, "run": run}


@router.post("/runs/{run_id}/retry")
def runs_retry(run_id: str) -> dict[str, Any]:
    state = load_state()
    run = state["runs"].get(run_id)
    if run is None:
        raise HTTPException(status_code=404, detail="run not found")
    run["status"] = "retrying"
    run["attempt_count"] = int(run.get("attempt_count", 1)) + 1
    save_state(state)
    append_audit_event("run_retry", {"run_id": run_id})
    return {"ok": True, "run": run}


@router.get("/operator/surface")
def operator_surface() -> dict[str, Any]:
    state = load_state()
    messages = list(state["messages"])
    objective = messages[-1]["text"] if messages else "No active objective"
    return {
        "ok": True,
        "objective": objective,
        "next_step": compute_next_best_move([m["text"] for m in messages], objective),
        "approvals": list(state["approvals"]),
        "runs": list(state["runs"].values()),
        "memory_highlights": list(state["memories"][:5]),
        "proof": {
            "messages": len(state["messages"]),
            "memories": len(state["memories"]),
            "runs": len(state["runs"]),
        },
    }
