from __future__ import annotations

from pathlib import Path


REQUIRED_LAUNCH_SCRIPTS = [
    "launch_nexus.sh",
    "launch_nexus_desktop.sh",
]


def test_launch_scripts_exist_and_are_not_empty() -> None:
    root = Path(__file__).resolve().parents[1]
    for script_name in REQUIRED_LAUNCH_SCRIPTS:
        path = root / script_name
        assert path.exists(), f"Missing launch script: {script_name}"
        assert path.stat().st_size > 0, f"Launch script is empty: {script_name}"
