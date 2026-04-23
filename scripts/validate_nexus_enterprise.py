from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List

ROOT = Path(__file__).resolve().parents[1]
RELEASE_DIR = ROOT / "docs" / "release"
EVIDENCE_DIR = RELEASE_DIR / "evidence"

CONSTITUTION_PATH = RELEASE_DIR / "NEXUS_TRUTH_CONSTITUTION.md"
MATURITY_PATH = RELEASE_DIR / "NEXUS_MATURITY_LABELS.md"
SCORECARD_PATH = RELEASE_DIR / "NEXUS_SCORECARD.json"
PROOF_MATRIX_PATH = RELEASE_DIR / "NEXUS_PROOF_MATRIX.md"
REPORT_PATH = EVIDENCE_DIR / "enterprise_gate" / "enterprise_gate_report.json"

REQUIRED_SCORECARD_KEYS = {
    "enterprise_launchable_ai_os": [
        "system_truth",
        "continuity",
        "memory",
        "execution",
        "approvals_control",
        "ui_truth",
        "readiness",
        "behavioral_proof",
        "release_hardening",
        "no_overclaim",
        "enterprise_standard",
        "security_governance",
        "observability",
    ],
    "final_nexus_ten_ten": [
        "adaptive_learning",
        "max_power_feature_completion",
        "full_system_wiring",
        "final_configuration_correctness",
    ],
}

REQUIRED_CONSTITUTION_SECTIONS = [
    "## Core Rule",
    "## 1. System Truth",
    "## 2. Continuity",
    "## 3. Memory",
    "## 4. Execution",
    "## 5. Approvals and Control",
    "## 6. UI Truth",
    "## 7. Readiness",
    "## 8. Adaptive Learning",
    "## 9. Behavioral Proof",
    "## 10. Release Hardening",
    "## 11. No Overclaim",
    "## 12. Enterprise Standard",
    "## 13. Security and Governance",
    "## 14. Observability",
]

REQUIRED_MATURITY_LABELS = [
    "Prototype",
    "Architecture-complete",
    "Behavior-complete",
    "Enterprise-Launchable AI OS",
    "10/10 Final Nexus",
]

REQUIRED_PROOF_SCENARIOS = {
    "Continuity": "restart_active_mission",
    "Memory": "same_input_different_memory",
    "Execution": "interrupt_and_resume_run",
    "Approvals": "approval_blocks_execution",
    "UI Truth": "ui_reflects_runtime_state",
    "Readiness": "readiness_ranking_correctness",
    "Release": "clean_install_and_boot",
}


@dataclass
class CheckResult:
    name: str
    passed: bool
    details: List[str]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def ensure_exists(path: Path, label: str) -> CheckResult:
    exists = path.exists()
    return CheckResult(
        name=f"exists:{label}",
        passed=exists,
        details=[] if exists else [f"Missing required file: {path}"]
    )


def validate_constitution() -> CheckResult:
    text = read_text(CONSTITUTION_PATH)
    missing = [section for section in REQUIRED_CONSTITUTION_SECTIONS if section not in text]
    return CheckResult(
        name="constitution",
        passed=not missing,
        details=[f"Missing constitution section: {section}" for section in missing],
    )


def validate_maturity_labels() -> CheckResult:
    text = read_text(MATURITY_PATH)
    missing = [label for label in REQUIRED_MATURITY_LABELS if label not in text]
    return CheckResult(
        name="maturity_labels",
        passed=not missing,
        details=[f"Missing maturity label: {label}" for label in missing],
    )


def validate_scorecard() -> CheckResult:
    data = json.loads(read_text(SCORECARD_PATH))
    details: List[str] = []
    passed = True
    for top_level, required_keys in REQUIRED_SCORECARD_KEYS.items():
        if top_level not in data:
            passed = False
            details.append(f"Missing scorecard section: {top_level}")
            continue
        actual_keys = set(data[top_level].keys())
        missing = [key for key in required_keys if key not in actual_keys]
        extras = sorted(actual_keys.difference(required_keys))
        if missing:
            passed = False
            details.extend([f"Missing score key in {top_level}: {key}" for key in missing])
        if extras:
            passed = False
            details.extend([f"Unexpected score key in {top_level}: {key}" for key in extras])
    return CheckResult(name="scorecard", passed=passed, details=details)


def validate_proof_matrix() -> CheckResult:
    text = read_text(PROOF_MATRIX_PATH)
    details: List[str] = []
    passed = True
    for section, scenario in REQUIRED_PROOF_SCENARIOS.items():
        if f"## {section}" not in text:
            passed = False
            details.append(f"Missing proof matrix section: {section}")
        if scenario not in text:
            passed = False
            details.append(f"Missing proof matrix scenario: {scenario}")
    return CheckResult(name="proof_matrix", passed=passed, details=details)


def validate_evidence_tree() -> CheckResult:
    required_dirs = [
        EVIDENCE_DIR / "constitution",
        EVIDENCE_DIR / "scorecard",
        EVIDENCE_DIR / "proof_matrix",
        EVIDENCE_DIR / "enterprise_gate",
    ]
    missing = [str(path) for path in required_dirs if not path.exists()]
    return CheckResult(
        name="evidence_tree",
        passed=not missing,
        details=[f"Missing evidence directory: {path}" for path in missing],
    )


def build_report(results: List[CheckResult]) -> Dict[str, object]:
    return {
        "passed": all(result.passed for result in results),
        "checks": [
            {
                "name": result.name,
                "passed": result.passed,
                "details": result.details,
            }
            for result in results
        ],
    }


def main() -> int:
    EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)
    (EVIDENCE_DIR / "enterprise_gate").mkdir(parents=True, exist_ok=True)

    results = [
        ensure_exists(CONSTITUTION_PATH, "constitution"),
        ensure_exists(MATURITY_PATH, "maturity_labels"),
        ensure_exists(SCORECARD_PATH, "scorecard"),
        ensure_exists(PROOF_MATRIX_PATH, "proof_matrix"),
    ]

    if all(result.passed for result in results):
        results.extend([
            validate_constitution(),
            validate_maturity_labels(),
            validate_scorecard(),
            validate_proof_matrix(),
            validate_evidence_tree(),
        ])

    report = build_report(results)
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(json.dumps(report, indent=2), encoding="utf-8")

    print(json.dumps(report, indent=2))
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
