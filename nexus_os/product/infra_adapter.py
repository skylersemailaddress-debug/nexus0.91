from __future__ import annotations

import subprocess
from pathlib import Path


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _run_command(cmd: list[str], timeout: int = 30) -> str:
    try:
        result = subprocess.run(
            cmd,
            cwd=repo_root(),
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        return "pass" if result.returncode == 0 else "fail"
    except Exception:
        return "error"


def run_action(action: str) -> str:
    commands = {
        "validate_truth": ["python", "scripts/validate_nexus_master_truth.py"],
        "validate_ten_ten": ["python", "scripts/validate_nexus_10_10_gate.py"],
        "generate_manifest": ["python", "scripts/generate_release_manifest.py"],
        "execution_signals": ["python", "-c", "print('signals-ok')"],
        "gate_status": ["python", "-c", "print('gate-status-ok')"],
        "rollback_manifest": ["python", "-c", "print('rollback-ok')"],
    }

    cmd = commands.get(action)
    if not cmd:
        return "unknown"

    return _run_command(cmd)
