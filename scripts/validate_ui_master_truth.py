from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

MASTER_DOC = ROOT / "docs" / "ui" / "NEXUS_UI_MASTER_TRUTH.md"
DOCTRINE_DOC = ROOT / "docs" / "ui" / "NEXUS_UI_DOCTRINE.md"
README = ROOT / "README.md"
REPORT = ROOT / "docs" / "release" / "evidence" / "ui" / "ui_master_truth_report.json"

REQUIRED_MASTER_TERMS = [
    "hover-native",
    "workspace primacy",
    "chat bar",
    "quick action",
    "keyboard",
    "pin",
    "adaptive",
    "curated",
    "operational truth",
]

REQUIRED_DOCTRINE_TERMS = [
    "hover-native ambient command os",
    "chat bar",
    "quick actions",
    "curated",
    "pinned",
]

README_DRIFT_PATTERNS = [
    "dashboard-first",
    "always-visible pane walls",
    "static dashboard",
]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def main() -> int:
    result: dict[str, object] = {
        "ok": True,
        "checks": {},
        "errors": [],
    }

    def fail(message: str) -> None:
        result["ok"] = False
        errors = result["errors"]
        assert isinstance(errors, list)
        errors.append(message)

    if not MASTER_DOC.exists():
        fail(f"Missing file: {MASTER_DOC}")
    else:
        text = read_text(MASTER_DOC).lower()
        missing = [term for term in REQUIRED_MASTER_TERMS if term not in text]
        result["checks"]["master_doc"] = {
            "ok": not missing,
            "missing_terms": missing,
        }
        if missing:
            fail(f"Master UI truth missing required terms: {missing}")

    if not DOCTRINE_DOC.exists():
        fail(f"Missing file: {DOCTRINE_DOC}")
    else:
        text = read_text(DOCTRINE_DOC).lower()
        missing = [term for term in REQUIRED_DOCTRINE_TERMS if term not in text]
        result["checks"]["doctrine_doc"] = {
            "ok": not missing,
            "missing_terms": missing,
        }
        if missing:
            fail(f"UI doctrine missing required terms: {missing}")

    if README.exists():
        readme_text = read_text(README).lower()
        drift_hits = [pattern for pattern in README_DRIFT_PATTERNS if pattern in readme_text]
        result["checks"]["readme_drift"] = {
            "ok": not drift_hits,
            "hits": drift_hits,
        }
        if drift_hits:
            fail(f"README drift detected against UI master truth: {drift_hits}")

    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(result, indent=2), encoding="utf-8")

    print(json.dumps(result, indent=2))
    return 0 if bool(result["ok"]) else 1


if __name__ == "__main__":
    raise SystemExit(main())
