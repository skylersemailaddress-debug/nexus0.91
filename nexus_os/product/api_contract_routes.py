from __future__ import annotations

from typing import Any
from uuid import uuid4

from fastapi import APIRouter
from pydantic import BaseModel, Field

from .context_builder import build_context

router = APIRouter()

_MESSAGES: list[dict[str, Any]] = []
_MEMORIES: list[dict[str, Any]] = []
_RUNS: dict[str, dict[str, Any]] = {}
_STATE: dict[str, Any] = {
    "project_id": "default",
    "objective": "Continuity spine validation",
    "next_step": "Finish Phase 1 continuity and resume truth",
}


class AppendMessageRequest(BaseModel):
    project_id: str = "default"
    role: str
    content: str
    meta: dict[str, Any] = Field(default_factory=dict)


class MemoryUpsertRequest(BaseModel):
    project_id: str = "default"
    content: str
    tags: list[str] = Field(default_factory=list)


class MemorySearchRequest(BaseModel):
    query: str
    top_k: int = 5


class RunCreateRequest(BaseModel):
    goal: str


class ContextRequest(BaseModel):
    query: str


@router.get("/health")
def health() -> dict[str, Any]:
    return {"ok": True, "service": "nexus_api", "status": "ready"}


@router.post("/messages/append")
def append_message(payload: AppendMessageRequest) -> dict[str, Any]:
    message = {
        "id": str(uuid4()),
        "project_id": payload.project_id,
        "role": payload.role,
        "content": payload.content,
        "meta": payload.meta,
    }
    _MESSAGES.append(message)
    _STATE["last_message_id"] = message["id"]
    if not _STATE.get("objective"):
        _STATE["objective"] = "Drive Nexus runtime continuity"
    if not _STATE.get("next_step"):
        _STATE["next_step"] = "Inspect resume and resolve state"
    return {"ok": True, "message": message}


@router.get("/projects/{project_id}/resume")
def resume(project_id: str) -> dict[str, Any]:
    recent_messages = [m for m in _MESSAGES if m["project_id"] == project_id][-10:]
    return {
        "project_id": project_id,
        "objective": _STATE.get("objective"),
        "next_step": _STATE.get("next_step"),
        "recent_messages": recent_messages,
        "run_count": len(_RUNS),
        "memory_count": len(_MEMORIES),
    }


@router.post("/memory/upsert")
def memory_upsert(payload: MemoryUpsertRequest) -> dict[str, Any]:
    memory = {
        "id": str(uuid4()),
        "project_id": payload.project_id,
        "content": payload.content,
        "tags": payload.tags,
    }
    _MEMORIES.append(memory)
    return {"ok": True, "memory": memory}


@router.post("/memory/search")
def memory_search(payload: MemorySearchRequest) -> dict[str, Any]:
    query = payload.query.lower()
    results = [m for m in _MEMORIES if query in m["content"].lower()][: payload.top_k]
    return {"ok": True, "results": results}


@router.post("/projects/{project_id}/context")
def build_project_context(project_id: str, payload: ContextRequest) -> dict[str, Any]:
    project_memories = [m for m in _MEMORIES if m.get("project_id") == project_id]
    context = build_context(query=payload.query, memories=project_memories)
    return {"ok": True, **context}


@router.post("/runs/create")
def run_create(payload: RunCreateRequest) -> dict[str, Any]:
    run_id = str(uuid4())
    run = {
        "id": run_id,
        "run_id": run_id,
        "goal": payload.goal,
        "status": "created",
    }
    _RUNS[run_id] = run
    return {"ok": True, "run_id": run_id, "run": run}


@router.get("/runs/{run_id}")
def run_get(run_id: str) -> dict[str, Any]:
    run = _RUNS.get(run_id)
    if run is None:
        return {"ok": False, "error": "run_not_found", "run_id": run_id, "status": "missing"}
    return {"ok": True, **run}
