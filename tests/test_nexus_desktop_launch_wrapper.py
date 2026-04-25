import json
import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_launcher_exists_and_executable() -> None:
    launcher = ROOT / "launch_nexus_desktop.sh"
    assert launcher.exists(), "launch_nexus_desktop.sh should exist"
    assert os.access(launcher, os.X_OK), "launch_nexus_desktop.sh should be executable"


def test_launcher_contains_required_markers() -> None:
    launcher = ROOT / "launch_nexus_desktop.sh"
    content = launcher.read_text(encoding="utf-8")

    required_markers = [
        "API_AUTH_TOKEN",
        "uvicorn nexus_os.product.api_server:app",
        "/api/state",
        "DISPLAY",
        "xvfb-run",
        "--disable-gpu",
        "--disable-software-rasterizer",
        "--no-sandbox",
        "Launching Nexus Desktop: headless Codespaces mode via xvfb-run",
    ]

    for marker in required_markers:
        assert marker in content, f"Missing marker in launcher: {marker}"


def test_smoke_script_exists_and_emits_json() -> None:
    smoke_script = ROOT / "scripts" / "smoke_nexus_launch.py"
    assert smoke_script.exists(), "scripts/smoke_nexus_launch.py should exist"

    result = subprocess.run(
        [sys.executable, str(smoke_script)],
        capture_output=True,
        text=True,
        cwd=ROOT,
        check=False,
    )

    output = result.stdout.strip()
    assert output, "Smoke script should output JSON"

    payload = json.loads(output)
    assert isinstance(payload, dict)
    assert "ok" in payload
    assert "checks" in payload
    assert isinstance(payload["checks"], list)
