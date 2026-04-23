from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Body, HTTPException
from pydantic import BaseModel

from .context_builder import build_context
from .state_inference import compute_next_best_move

router = APIRouter(prefix="/api", tags=["contracts"])


_RUNTIME: dict[str, Any] = {
    "messages": [],
    "memories": [],
    "runs": {},
    "approvals": [],
}


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
    return {
        "ok": True,
        "contracts": "active",
        "runtime": {
            "messages": len(_RUNTIME["messages"]),
            "memories": len(_RUNTIME["memories"]),
            "runs": len(_RUNTIME["runs"]),
            "approvals": len(_RUNTIME["approvals"]),
        },
    }


@router.post("/messages/append")
def append_message(payload: MessageAppendRequest) -> dict[str, Any]:
    message_id = f"msg:{len(_RUNTIME['messages']) + 1}"
    record = {
        "id": message_id,
        "role": payload.role,
        "text": payload.text.strip(),
        "meta": dict(payload.meta),
    }
    _RUNTIME["messages"].append(record)
    return {"ok": True, "message": record}


@router.get("/projects/default/resume")
def project_resume() -> dict[str, Any]:
    messages = list(_RUNTIME["messages"])
    latest_text = messages[-1]["text"] if messages else ""
    objective = latest_text or "No active objective"
    next_step = compute_next_best_move([m["text"] for m in messages], objective)
    return {
        "ok": True,
        "project_id": "default",
        "objective": objective,
        "next_step": next_step,
        "recent_messages": messages[-10:],
        "approvals": list(_RUNTIME["approvals"]),
        "run_count": len(_RUNTIME["runs"]),
        "memory_count": len(_RUNTIME["memories"]),
    }


@router.post("/memory/upsert")
def memory_upsert(payload: MemoryUpsertRequest) -> dict[str, Any]:
    existing = next((m for m in _RUNTIME["memories"] if m["id"] == payload.id), None)
    record = {
        "id": payload.id,
        "content": payload.content,
        "kind": payload.kind,
        "meta": dict(payload.meta),
    }
    if existing is None:
        _RUNTIME["memories"].append(record)
    else:
        existing.update(record)
    return {"ok": True, "memory": record}


@router.post("/memory/search")
def memory_search(payload: MemorySearchRequest) -> dict[str, Any]:
    context = build_context(query=payload.query, memories=list(_RUNTIME["memories"]))
    return {"ok": True, **context}


@router.post("/state/build_context")
def state_build_context(payload: BuildContextRequest) -> dict[str, Any]:
    context = build_context(query=payload.query, memories=list(_RUNTIME["memories"]))
    context["messages"] = list(_RUNTIME["messages"][-10:])
    return {"ok": True, **context}


@router.post("/runs/create")
def runs_create(payload: RunCreateRequest) -> dict[str, Any]:
    run_id = f"run:{len(_RUNTIME['runs']) + 1}"
    run = {
        "run_id": run_id,
        "objective": payload.objective,
        "status": "created",
        "attempt_count": 1,
        "artifacts": [],
    }
    _RUNTIME["runs"][run_id] = run
    return {"ok": True, "run": run}


@router.get("/runs/{run_id}")
def runs_get(run_id: str) -> dict[str, Any]:
    run = _RUNTIME["runs"].get(run_id)
    if run is None:
        raise HTTPException(status_code=404, detail="run not found")
    return {"ok": True, "run": run}


@router.post("/runs/{run_id}/pause")
def runs_pause(run_id: str) -> dict[str, Any]:
    run = _RUNTIME["runs"].get(run_id)
    if run is None:
        raise HTTPException(status_code=404, detail="run not found")
    run["status"] = "paused"
    return {"ok": True, "run": run}


@router.post("/runs/{run_id}/resume")
def runs_resume(run_id: str) -> dict[str, Any]:
    run = _RUNTIME["runs"].get(run_id)
    if run is None:
        raise HTTPException(status_code=404, detail="run not found")
    run["status"] = "running"
    return {"ok": True, "run": run}


@router.post("/runs/{run_id}/retry")
def runs_retry(run_id: str) -> dict[str, Any]:
    run = _RUNTIME["runs"].get(run_id)
    if run is None:
        raise HTTPException(status_code=404, detail="run not found")
    run["status"] = "retrying"
    run["attempt_count"] = int(run.get("attempt_count", 1)) + 1
    return {"ok": True, "run": run}


@router.get("/operator/surface")
def operator_surface() -> dict[str, Any]:
    messages = list(_RUNTIME["messages"])
    objective = messages[-1]["text"] if messages else "No active objective"
    return {
        "ok": True,
        "objective": objective,
        "next_step": compute_next_best_move([m["text"] for m in messages], objective),
        "approvals": list(_RUNTIME["approvals"]),
        "runs": list(_RUNTIME["runs"].values()),
        "memory_highlights": list(_RUNTIME["memories"][:5]),
        "proof": {
            "messages": len(_RUNTIME["messages"]),
            "memories": len(_RUNTIME["memories"]),
            "runs": len(_RUNTIME["runs"]),
        },
    }
