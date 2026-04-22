from __future__ import annotations

import subprocess
from pathlib import Path


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def run_action(action: str) -> str:
    commands = {
        "validate_truth": ["python", "scripts/validate_nexus_master_truth.py"],
        "validate_ten_ten": ["python", "scripts/validate_nexus_10_10_gate.py"],
        "generate_manifest": ["python", "scripts/generate_release_manifest.py"],
    }

    cmd = commands.get(action)
    if not cmd:
        return "unknown"

    try:
        result = subprocess.run(
            cmd,
            cwd=repo_root(),
            capture_output=True,
            text=True,
            timeout=30,
        )
        return "pass" if result.returncode == 0 else "fail"
    except Exception:
        return "error"
