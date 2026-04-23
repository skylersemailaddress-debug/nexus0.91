from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

MASTER_DOC = ROOT / "docs" / "ui" / "NEXUS_UI_MASTER_TRUTH.md"
SHELL_FILE = ROOT / "nexus_os" / "product" / "interactive_shell.py"
READINESS_FILE = ROOT / "nexus_os" / "product" / "readiness_engine.py"
REPORT = ROOT / "docs" / "release" / "evidence" / "ui" / "ui_master_truth_report.json"

REQUIRED_MASTER_TERMS = [
    "hover-native",
    "workspace",
    "chat bar",
    "curated",
    "predictive",
    "readiness",
]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def main() -> int:
    result = {"ok": True, "checks": {}, "errors": []}

    def fail(msg: str) -> None:
        result["ok"] = False
        result["errors"].append(msg)

    if MASTER_DOC.exists():
        text = read_text(MASTER_DOC).lower()
        missing = [t for t in REQUIRED_MASTER_TERMS if t not in text]
        result["checks"]["master_terms"] = {"ok": not missing, "missing": missing}
        if missing:
            fail(f"missing master truth terms: {missing}")

    if SHELL_FILE.exists():
        shell_text = read_text(SHELL_FILE)
        has_workspace = "_render_workspace" in shell_text
        has_chat = "_render_chat" in shell_text
        result["checks"]["workspace_arch"] = {"ok": has_workspace and has_chat}
        if not (has_workspace and has_chat):
            fail("workspace/chat architecture not enforced")

    if READINESS_FILE.exists():
        readiness_text = read_text(READINESS_FILE)
        has_scoring = "score_readiness_field" in readiness_text
        result["checks"]["readiness_engine"] = {"ok": has_scoring}
        if not has_scoring:
            fail("predictive readiness scoring missing")

    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(result, indent=2))

    print(json.dumps(result, indent=2))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
