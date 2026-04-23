from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "docs" / "release" / "evidence" / "security" / "security_baseline_report.json"

REQUIRED = {
    "pyproject": ROOT / "pyproject.toml",
    "api_server": ROOT / "nexus_os" / "product" / "api_server.py",
    "contract_routes": ROOT / "nexus_os" / "product" / "api_contract_routes.py",
}

FORBIDDEN_SNIPPETS = [
    "<FULL FILE WITH MARKET ROUTES>",
    "assert False",
]


def main() -> int:
    result = {"ok": True, "checks": {}, "errors": []}

    for name, path in REQUIRED.items():
        ok = path.exists()
        result["checks"][name] = {"ok": ok, "path": str(path)}
        if not ok:
            result["ok"] = False
            result["errors"].append(f"missing required file: {name}")
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        forbidden_hits = [snippet for snippet in FORBIDDEN_SNIPPETS if snippet in text]
        if forbidden_hits:
            result["ok"] = False
            result["errors"].append(f"forbidden placeholder content in {name}: {forbidden_hits}")

    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
