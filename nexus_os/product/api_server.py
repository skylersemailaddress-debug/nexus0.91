from __future__ import annotations

from fastapi import FastAPI

from .state_inference import compute_active_intelligence_line

app = FastAPI(title="Nexus Desktop API")

_GLOBAL_STATE: dict[str, object] = {
    "mission": "No mission set",
    "history": [],
    "workflow": {},
    "decision": "",
}


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

    return {
        "mission": mission,
        "signal": compute_active_intelligence_line(history, mission),
        "workflow": workflow,
        "decision": decision,
    }


def update_desktop_state(*, mission: str | None = None, history: list[str] | None = None, workflow: dict[str, object] | None = None, decision: str | None = None) -> None:
    if mission is not None:
        _GLOBAL_STATE["mission"] = mission
    if history is not None:
        _GLOBAL_STATE["history"] = history
    if workflow is not None:
        _GLOBAL_STATE["workflow"] = workflow
    if decision is not None:
        _GLOBAL_STATE["decision"] = decision
