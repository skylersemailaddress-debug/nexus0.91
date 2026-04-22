from __future__ import annotations

import subprocess
from pathlib import Path


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def run_post_approval_actions() -> list[str]:
    actions: list[str] = []

    commands = [
        (["python", "scripts/validate_nexus_master_truth.py"], "master truth gate"),
        (["python", "scripts/validate_nexus_10_10_gate.py"], "10/10 gate"),
        (["python", "scripts/generate_release_manifest.py"], "release manifest"),
    ]

    for command, label in commands:
        try:
            result = subprocess.run(
                command,
                cwd=repo_root(),
                capture_output=True,
                text=True,
                timeout=30,
            )
            status = "pass" if result.returncode == 0 else "fail"
        except Exception:
            status = "error"
        actions.append(f"{label}: {status}")

    return actions
