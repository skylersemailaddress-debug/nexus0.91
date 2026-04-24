from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_LOCKED_PATHS = [
    "scripts/run_enterprise_gate.py",
    "scripts/validate_final_certification.py",
    "scripts/validate_nexus_master_truth.py",
    "scripts/validate_nexus_10_10_gate.py",
    "docs/specs/NEXUS_MASTER_TRUTH_AND_WORK_SYSTEM.md",
    "docs/checklists/NEXUS_10_10_EXECUTION_CHECKLIST.md",
]


def test_locked_paths_exist() -> None:
    missing = [path for path in REQUIRED_LOCKED_PATHS if not (ROOT / path).exists()]
    assert not missing, f"Missing locked enterprise paths: {missing}"


def test_enterprise_gate_contains_final_certification_and_full_tests() -> None:
    text = (ROOT / "scripts" / "run_enterprise_gate.py").read_text(encoding="utf-8")
    assert "scripts/validate_final_certification.py" in text
    assert '"-m", "pytest", "-q", "tests"' in text
    assert "scripts/generate_release_manifest.py" in text


def test_final_certification_keeps_overclaim_guard() -> None:
    text = (ROOT / "scripts" / "validate_final_certification.py").read_text(encoding="utf-8")
    assert "CERTIFIED_BY_EVIDENCE" in text
    assert "No 10/10, enterprise-ready, or launch-ready label" in text
