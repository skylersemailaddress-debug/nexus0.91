from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "docs" / "release" / "evidence" / "behavioral_gate" / "behavioral_ten_ten_report.json"

REQUIRED_FILES = {
    "ui_master_truth": ROOT / "docs" / "ui" / "NEXUS_UI_MASTER_TRUTH.md",
    "ui_doctrine": ROOT / "docs" / "ui" / "NEXUS_UI_DOCTRINE.md",
    "ui_validator": ROOT / "scripts" / "validate_ui_master_truth.py",
    "ui_tests": ROOT / "tests" / "test_ui_master_truth.py",
}

PROOF_MARKERS = {
    "continuity": [
        "continuity",
        "resume",
        "message append",
        "restart",
        "re-entry",
        "objective",
        "next step",
    ],
    "memory": [
        "memory influence",
        "relevance",
        "traceability",
        "context build",
        "quality controls",
    ],
    "execution": [
        "run lifecycle",
        "pause/resume/restore",
        "retry",
        "repair",
        "artifact",
        "evidence binding",
    ],
    "ui_truth": [
        "approvals backed by state",
        "mission backed by state",
        "memory backed by state",
        "progress backed by jobs",
        "no decorative core surfaces",
        "hover-native",
    ],
}

CANDIDATE_DOCS = [
    ROOT / "README.md",
    ROOT / "docs" / "ui" / "NEXUS_UI_MASTER_TRUTH.md",
    ROOT / "docs" / "ui" / "NEXUS_UI_DOCTRINE.md",
    ROOT / "docs" / "release" / "BEHAVIORAL_TEN_TEN_WORK_PLAN.md",
]


def read_if_exists(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="ignore")


def main() -> int:
    result: dict[str, object] = {"ok": True, "checks": {}, "errors": []}

    def fail(msg: str) -> None:
        result["ok"] = False
        errors = result["errors"]
        assert isinstance(errors, list)
        errors.append(msg)

    file_checks: dict[str, object] = {}
    for key, path in REQUIRED_FILES.items():
        exists = path.exists()
        file_checks[key] = {"ok": exists, "path": str(path)}
        if not exists:
            fail(f"Missing required behavioral gate dependency: {path}")
    result["checks"]["required_files"] = file_checks

    corpus = "\n\n".join(read_if_exists(path) for path in CANDIDATE_DOCS)
    proof_checks: dict[str, object] = {}
    for category, markers in PROOF_MARKERS.items():
        missing = [marker for marker in markers if marker.lower() not in corpus.lower()]
        proof_checks[category] = {"ok": not missing, "missing_markers": missing}
        if missing:
            fail(f"Missing {category} proof markers: {missing}")
    result["checks"]["proof_markers"] = proof_checks

    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))
    return 0 if bool(result["ok"]) else 1


if __name__ == "__main__":
    raise SystemExit(main())
