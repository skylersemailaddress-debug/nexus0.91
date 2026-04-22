from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Any
import json


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def manifest_path() -> Path:
    return repo_root() / "docs" / "release" / "RELEASE_MANIFEST.json"


def snapshot_pre_approval_state() -> dict[str, Any]:
    manifest = manifest_path()
    return {
        "manifest_exists": manifest.exists(),
        "manifest_content": manifest.read_text(encoding="utf-8") if manifest.exists() else None,
    }


def run_post_approval_actions() -> tuple[list[str], dict[str, Any]]:
    actions: list[str] = []
    snapshot = snapshot_pre_approval_state()

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

    return actions, snapshot


def rollback_post_approval_actions(snapshot: dict[str, Any]) -> list[str]:
    results: list[str] = []
    manifest = manifest_path()

    if snapshot.get("manifest_exists"):
        manifest.parent.mkdir(parents=True, exist_ok=True)
        manifest.write_text(snapshot.get("manifest_content") or "", encoding="utf-8")
        results.append("release manifest: restored")
    else:
        if manifest.exists():
            manifest.unlink()
            results.append("release manifest: removed")
        else:
            results.append("release manifest: unchanged")

    return results
