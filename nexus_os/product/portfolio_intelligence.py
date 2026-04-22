from __future__ import annotations

from typing import Dict, Any
import uuid

PROJECTS: Dict[str, Dict[str, Any]] = {}


def create_project(name: str) -> dict:
    pid = str(uuid.uuid4())
    project = {
        "id": pid,
        "name": name,
        "score": 0.0,
        "status": "active",
        "recommended_action": "none",
        "reasons": [],
        "evidence": [],
    }
    PROJECTS[pid] = project
    return project


def score_project(pid: str) -> dict:
    p = PROJECTS.get(pid)
    if not p:
        return {}

    score = 0.8
    action = "scale" if score > 0.7 else "kill"

    p["score"] = score
    p["recommended_action"] = action
    p["reasons"] = ["baseline scoring"]
    return p


def kill_project(pid: str) -> dict:
    p = PROJECTS.get(pid)
    if not p:
        return {}
    p["status"] = "killed"
    return p


def clone_project(pid: str) -> dict:
    p = PROJECTS.get(pid)
    if not p:
        return {}
    return create_project(p["name"] + "_clone")


def bundle_project(pid: str) -> dict:
    p = PROJECTS.get(pid)
    if not p:
        return {}
    p["status"] = "bundled"
    return p


def list_projects() -> dict:
    return {"ok": True, "projects": list(PROJECTS.values())}
