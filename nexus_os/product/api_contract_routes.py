from __future__ import annotations

from datetime import datetime, UTC
from typing import Any
from uuid import uuid4

from fastapi import APIRouter
from pydantic import BaseModel, Field

from .context_builder import build_context
from .capability_store import (
    create_capability,
    list_capabilities,
    update_capability,
    validate_capability,
)
from .intelligence_engine import build_plan

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


class ArtifactBindRequest(BaseModel):
    type: str = "log"
    content: str


class CapabilityCreateRequest(BaseModel):
    goal: str


class CapabilityUpdateRequest(BaseModel):
    content: str


def _now() -> str:
    return datetime.now(UTC).isoformat()


def _append_event(run: dict[str, Any], event_type: str, detail: str) -> None:
    events = run.setdefault("events", [])
    events.append({"type": event_type, "detail": detail, "ts": _now()})
    run["updated_at"] = _now()


def _append_artifact(run: dict[str, Any], artifact_type: str, content: str) -> None:
    artifacts = run.setdefault("artifacts", [])
    artifacts.append({"id": str(uuid4()), "type": artifact_type, "content": content, "ts": _now()})
    run["updated_at"] = _now()


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
        "attempt_count": 1,
        "artifacts": [],
        "events": [],
        "created_at": _now(),
        "updated_at": _now(),
    }
    _append_event(run, "created", f"Run created for goal: {payload.goal}")
    _RUNS[run_id] = run
    return {"ok": True, "run_id": run_id, "run": run}


@router.post("/runs/{run_id}/pause")
def run_pause(run_id: str) -> dict[str, Any]:
    run = _RUNS.get(run_id)
    if run is None:
        return {"ok": False, "error": "run_not_found", "run_id": run_id, "status": "missing"}
    run["status"] = "paused"
    _append_event(run, "paused", "Run paused")
    _append_artifact(run, "log", "pause triggered")
    return {"ok": True, **run}


@router.post("/runs/{run_id}/resume")
def run_resume(run_id: str) -> dict[str, Any]:
    run = _RUNS.get(run_id)
    if run is None:
        return {"ok": False, "error": "run_not_found", "run_id": run_id, "status": "missing"}
    run["status"] = "running"
    _append_event(run, "resumed", "Run resumed")
    _append_artifact(run, "log", "resume triggered")
    return {"ok": True, **run}


@router.post("/runs/{run_id}/retry")
def run_retry(run_id: str) -> dict[str, Any]:
    run = _RUNS.get(run_id)
    if run is None:
        return {"ok": False, "error": "run_not_found", "run_id": run_id, "status": "missing"}
    run["attempt_count"] = int(run.get("attempt_count", 0)) + 1
    run["status"] = "running"
    _append_event(run, "retried", f"Retry attempt {run['attempt_count']}")
    _append_artifact(run, "retry_evidence", f"retry attempt {run['attempt_count']}")
    return {"ok": True, **run}


@router.post("/runs/{run_id}/artifacts")
def run_bind_artifact(run_id: str, payload: ArtifactBindRequest) -> dict[str, Any]:
    run = _RUNS.get(run_id)
    if run is None:
        return {"ok": False, "error": "run_not_found", "run_id": run_id, "status": "missing"}
    _append_artifact(run, payload.type, payload.content)
    _append_event(run, "artifact_bound", f"Artifact bound: {payload.type}")
    return {"ok": True, **run}


@router.get("/operator/surface")
def operator_surface() -> dict[str, Any]:
    all_artifacts = [artifact for run in _RUNS.values() for artifact in run.get("artifacts", [])]
    active_runs = [run for run in _RUNS.values() if run.get("status") in {"running", "paused"}]
    capability_items = list_capabilities()
    latest_context = build_context(query="behavioral memory probe", memories=_MEMORIES) if _MEMORIES else {
        "query": "",
        "selected_memories": [],
        "filtered_memories": [],
        "influence_trace": [],
        "decision": {"objective": _STATE.get("objective"), "next_step": _STATE.get("next_step")},
    }

    return {
        "ok": True,
        "mission": {
            "objective": _STATE.get("objective"),
            "next_step": _STATE.get("next_step"),
            "runtime_backed": bool(_STATE.get("objective") and _STATE.get("next_step")),
        },
        "approvals": {
            "runtime_backed": True,
            "count": 1 if active_runs else 0,
            "items": [{"type": "operator_review", "state": "required"}] if active_runs else [],
        },
        "memory": {
            "runtime_backed": True,
            "count": len(_MEMORIES),
            "selected_memories": latest_context.get("selected_memories", []),
            "influence_trace": latest_context.get("influence_trace", []),
        },
        "progress": {
            "runtime_backed": True,
            "run_count": len(_RUNS),
            "active_runs": active_runs,
            "attempt_total": sum(int(run.get("attempt_count", 0)) for run in _RUNS.values()),
        },
        "proof": {
            "runtime_backed": True,
            "proof_ids": [artifact.get("id") for artifact in all_artifacts],
            "artifacts": all_artifacts,
            "capability_evidence_count": sum(len(cap.get("evidence", [])) for cap in capability_items),
        },
        "capabilities": {
            "runtime_backed": True,
            "count": len(capability_items),
        },
    }


@router.post("/intelligence/plan")
def intelligence_plan() -> dict[str, Any]:
    messages = _MESSAGES[-20:]
    memories = list(_MEMORIES)
    runs = list(_RUNS.values())
    capabilities = list_capabilities()
    objective = str(_STATE.get("objective") or "No objective set")
    return build_plan(
        objective=objective,
        messages=messages,
        memories=memories,
        runs=runs,
        capabilities=capabilities,
    )


# Phase 4 Builder Routes (additive)

@router.post("/capabilities/create")
def capability_create(payload: CapabilityCreateRequest) -> dict[str, Any]:
    capability = create_capability(payload.goal)
    return {"ok": True, "capability": capability}


@router.post("/capabilities/{capability_id}/validate")
def capability_validate_route(capability_id: str) -> dict[str, Any]:
    capability = validate_capability(capability_id)
    if capability is None:
        return {"ok": False, "error": "not_found"}
    return {"ok": True, "capability": capability}


@router.post("/capabilities/{capability_id}/update")
def capability_update_route(capability_id: str, payload: CapabilityUpdateRequest) -> dict[str, Any]:
    capability = update_capability(capability_id, payload.content)
    if capability is None:
        return {"ok": False, "error": "not_found"}
    return {"ok": True, "capability": capability}


@router.get("/capabilities")
def capability_list_route() -> dict[str, Any]:
    return {"ok": True, "capabilities": list_capabilities()}


@router.get("/runs/{run_id}")
def run_get(run_id: str) -> dict[str, Any]:
    run = _RUNS.get(run_id)
    if run is None:
        return {"ok": False, "error": "run_not_found", "run_id": run_id, "status": "missing"}
    return {"ok": True, **run}
