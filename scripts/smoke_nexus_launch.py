#!/usr/bin/env python3
import importlib
import json
import os
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def check_import(name: str) -> tuple[bool, str]:
    try:
        importlib.import_module(name)
        return True, f"import {name}"
    except Exception as exc:
        return False, f"import {name}: {exc}"


def main() -> int:
    checks: list[dict[str, object]] = []

    for module in ["fastapi", "uvicorn", "nexus_os.product.api_server"]:
        ok, detail = check_import(module)
        checks.append({"name": f"module:{module}", "ok": ok, "detail": detail})

    launcher = ROOT / "launch_nexus_desktop.sh"
    checks.append(
        {
            "name": "launcher_exists",
            "ok": launcher.exists(),
            "detail": str(launcher),
        }
    )
    checks.append(
        {
            "name": "launcher_executable",
            "ok": launcher.exists() and os.access(launcher, os.X_OK),
            "detail": str(launcher),
        }
    )

    package_json = ROOT / "desktop_shell" / "package.json"
    checks.append(
        {
            "name": "desktop_package_json_exists",
            "ok": package_json.exists(),
            "detail": str(package_json),
        }
    )

    electron_main = ROOT / "desktop_shell" / "electron" / "main.js"
    checks.append(
        {
            "name": "desktop_electron_main_exists",
            "ok": electron_main.exists(),
            "detail": str(electron_main),
        }
    )

    node_modules = ROOT / "desktop_shell" / "node_modules"
    checks.append(
        {
            "name": "desktop_node_modules_exists",
            "ok": node_modules.exists(),
            "detail": str(node_modules),
        }
    )

    display_set = bool(os.environ.get("DISPLAY"))
    checks.append(
        {
            "name": "display_set",
            "ok": True,
            "detail": f"DISPLAY={'set' if display_set else 'missing'}",
        }
    )

    if not display_set:
        xvfb_exists = shutil.which("xvfb-run") is not None
        checks.append(
            {
                "name": "xvfb_run_available",
                "ok": xvfb_exists,
                "detail": "xvfb-run found" if xvfb_exists else "xvfb-run missing",
            }
        )

    payload = {
        "ok": all(bool(item["ok"]) for item in checks),
        "checks": checks,
    }
    print(json.dumps(payload))
    return 0 if payload["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
