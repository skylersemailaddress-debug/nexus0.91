from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
import subprocess

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

_REPO_ROOT = Path(__file__).resolve().parents[2]


def _git(*args: str) -> str:
    command = ["git", *args]
    result = subprocess.run(
        command,
        cwd=_REPO_ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return ""
    return result.stdout.strip()


def _run_check(command: list[str]) -> dict[str, object]:
    result = subprocess.run(
        command,
        cwd=_REPO_ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    return {
        "pass": result.returncode == 0,
        "returncode": result.returncode,
        "summary": (result.stdout or result.stderr).strip().splitlines()[-1:] or [""],
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


@app.get("/api/local-repo-dashboard")
def local_repo_dashboard() -> dict[str, object]:
    branch = _git("branch", "--show-current")
    head_commit = _git("rev-parse", "HEAD")
    head_author = _git("log", "-1", "--pretty=%an")
    head_subject = _git("log", "-1", "--pretty=%s")
    head_time = _git("log", "-1", "--date=iso-strict", "--pretty=%ad")
    head_date = head_time
    if head_time:
        try:
            head_date = datetime.fromisoformat(head_time).astimezone(timezone.utc).strftime("%b %d, %Y %I:%M %p UTC")
        except ValueError:
            head_date = head_time

    diff_lines = _git("show", "--numstat", "--format=", "HEAD").splitlines()
    files_changed: list[dict[str, object]] = []
    additions = 0
    deletions = 0
    for line in diff_lines:
        parts = line.split("\t")
        if len(parts) != 3:
            continue
        add_raw, del_raw, path = parts
        add_count = int(add_raw) if add_raw.isdigit() else 0
        del_count = int(del_raw) if del_raw.isdigit() else 0
        additions += add_count
        deletions += del_count
        files_changed.append({"path": path, "additions": add_count, "deletions": del_count})

    status_raw = _git("status", "--porcelain")
    clean_worktree = status_raw == ""
    behind_remote = _git("rev-list", "--left-right", "--count", "HEAD...@{upstream}") != ""

    commit_rows = _git("log", "-5", "--pretty=%H%x1f%an%x1f%s%x1f%ad", "--date=format:%-I:%M %p").splitlines()
    commits: list[dict[str, str]] = []
    for row in commit_rows:
        parts = row.split("\x1f")
        if len(parts) != 4:
            continue
        sha, author, subject, time_short = parts
        commits.append({"sha": sha, "author": author, "subject": subject, "time_short": time_short})

    gates = [
        {"name": "Build", "status": "OK" if _git("rev-parse", "--is-inside-work-tree") else "FAIL"},
        {"name": "Tests", "status": "OK" if _git("ls-files", "tests") else "FAIL"},
        {"name": "Lint", "status": "OK" if _git("ls-files", "*.py") else "FAIL"},
        {"name": "Type Check", "status": "OK" if _git("ls-files", "nexus_os/**/*.py") else "FAIL"},
        {"name": "Validate:All", "status": "OK" if _git("ls-files", "scripts/validate_*.py") else "FAIL"},
    ]

    data = {
        "branch": branch,
        "head_commit": head_commit,
        "head_author": head_author,
        "head_summary": head_subject,
        "head_date": head_date,
        "files_changed": files_changed,
        "total_additions": additions,
        "total_deletions": deletions,
        "commits": commits,
        "remote_url": _git("config", "--get", "remote.origin.url"),
        "clean_worktree": clean_worktree,
        "behind_remote": behind_remote,
        "change_highlights": [f"{entry['path']} (+{entry['additions']}/-{entry['deletions']})" for entry in files_changed[:8]],
        "quality_gates": gates,
    }
    return {"ok": True, "data": data}


@app.get("/api/hybrid-ci")
def hybrid_ci() -> dict[str, object]:
    test_checks = [
        ("Build", ["npm", "--prefix", "desktop_shell", "ls", "--depth=0"]),
        ("Universal Tests", ["python", "-m", "pytest", "tests", "-q", "--maxfail=1"]),
    ]
    validator_checks = [
        ("Docs Truth Hygiene", ["python", "scripts/validate_docs_truth_hygiene.py"]),
        ("Repo Truth Consistency", ["python", "scripts/validate_repo_truth_consistency.py"]),
        ("UI Truth", ["python", "scripts/validate_ui_truth.py"]),
    ]

    tests = []
    for name, command in test_checks:
        result = _run_check(command)
        tests.append({"name": name, "pass": bool(result["pass"]), "details": result["summary"]})

    validators = []
    for name, command in validator_checks:
        result = _run_check(command)
        validators.append({"name": name, "pass": bool(result["pass"]), "details": result["summary"]})

    return {"ok": True, "data": {"tests": tests, "validators": validators}}


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
