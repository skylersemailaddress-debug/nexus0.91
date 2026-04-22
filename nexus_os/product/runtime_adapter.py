from __future__ import annotations

from pathlib import Path


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def get_truth_gate_state() -> str:
    path = repo_root() / "scripts" / "validate_nexus_master_truth.py"
    return "available" if path.exists() else "missing"


def get_ten_ten_gate_state() -> str:
    path = repo_root() / "scripts" / "validate_nexus_10_10_gate.py"
    return "available" if path.exists() else "missing"


def get_release_manifest_state() -> str:
    path = repo_root() / "docs" / "release" / "RELEASE_MANIFEST.json"
    return "present" if path.exists() else "not_generated"


def get_execution_signal_summary() -> dict[str, str]:
    root = repo_root()
    return {
        "truth_gate": get_truth_gate_state(),
        "ten_ten_gate": get_ten_ten_gate_state(),
        "release_manifest": get_release_manifest_state(),
        "product_entry": "available" if (root / "nexus_os" / "product" / "__main__.py").exists() else "missing",
        "ui_entry": "available" if (root / "nexus_os" / "ui" / "__main__.py").exists() else "missing",
    }
