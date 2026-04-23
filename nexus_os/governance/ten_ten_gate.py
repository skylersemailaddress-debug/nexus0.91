from __future__ import annotations
from dataclasses import dataclass
import json
from pathlib import Path

@dataclass(frozen=True)
class GateCheck:
    name: str
    passed: bool
    details: str

REQUIRED_PATHS = [
    "docs/roadmaps/NEXUS_10_10_MASTER_ROADMAP.md",
    "docs/checklists/NEXUS_10_10_MASTER_CHECKLIST.md",
    "docs/specs/NEXUS_PRODUCT_COMPANY_MASTER_SPEC.md",
    "docs/specs/NEXUS_MARKET_INTELLIGENCE_SPEC.md",
    "docs/specs/NEXUS_PORTFOLIO_ENGINE_SPEC.md",
    "docs/specs/NEXUS_FACTORY_SPEC.md",
    "docs/specs/NEXUS_SURFACE_FABRIC_SPEC.md",
    "docs/specs/NEXUS_DISTRIBUTION_OPS_SPEC.md",
    "docs/specs/NEXUS_ECONOMICS_SPEC.md",
    "docs/specs/NEXUS_FLEET_MAINTENANCE_SPEC.md",
    "docs/specs/NEXUS_AUTONOMY_POLICY_SPEC.md",
    "docs/specs/NEXUS_CUSTOMER_OPS_SPEC.md",
    "docs/specs/NEXUS_BENCHMARKING_SPEC.md",
    "nexus_os/models/product.py",
    "nexus_os/models/opportunity.py",
    "nexus_os/models/portfolio.py",
    "nexus_os/models/economics.py",
    "nexus_os/market_intelligence/__init__.py",
    "nexus_os/portfolio/__init__.py",
    "nexus_os/factory/__init__.py",
    "nexus_os/surface_fabric/__init__.py",
    "nexus_os/distribution/__init__.py",
    "nexus_os/economics/__init__.py",
    "nexus_os/fleet_maintenance/__init__.py",
    "nexus_os/autonomy_policy/__init__.py",
    "nexus_os/customer_ops/__init__.py",
    "nexus_os/benchmarking/__init__.py",
    "nexus_os/operator/portfolio_projection.py",
    "nexus_os/operator/market_projection.py",
    "nexus_os/operator/product_fleet_projection.py",
    "nexus_os/operator/economics_projection.py",
]

REQUIRED_TESTS = [
    "tests/test_ten_ten_gate.py",
    "tests/test_market_intelligence.py",
    "tests/test_portfolio_engine.py",
    "tests/test_factory_generation.py",
    "tests/test_surface_fabric.py",
    "tests/test_distribution_ops.py",
    "tests/test_economics.py",
    "tests/test_fleet_maintenance.py",
    "tests/test_autonomy_policy.py",
    "tests/test_customer_ops.py",
    "tests/test_benchmarking.py",
]

REQUIRED_JSON_EVIDENCE = [
    "docs/release/evidence/ui/ui_master_truth_report.json",
    "docs/release/evidence/behavioral_gate/behavioral_ten_ten_report.json",
    "docs/release/evidence/behavioral_runtime/behavioral_runtime_report.json",
    "docs/release/evidence/behavioral_runtime/behavioral_scenarios_report.json",
    "docs/release/evidence/runtime/replay_consistency_report.json",
    "docs/release/evidence/runtime/trace_consistency_report.json",
]

REQUIRED_FILE_EVIDENCE = [
    "docs/release/evidence/runtime/audit_log.jsonl",
]

REQUIRED_CHECKLISTS = [
    "docs/checklists/NEXUS_10_10_MASTER_CHECKLIST.md",
    "docs/checklists/NEXUS_10_10_EXECUTION_CHECKLIST.md",
]


def _count_checked_boxes(path: Path) -> int:
    if not path.exists():
        return 0
    text = path.read_text(encoding="utf-8", errors="ignore")
    return text.count("- [x]") + text.count("- [X]")


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def run_ten_ten_gate(repo_root: str | Path) -> list[GateCheck]:
    root = Path(repo_root)
    checks: list[GateCheck] = []

    for rel in REQUIRED_PATHS:
        p = root / rel
        checks.append(GateCheck(f"path:{rel}", p.exists(), "required file/package path must exist"))

    for rel in REQUIRED_TESTS:
        p = root / rel
        checks.append(GateCheck(f"test:{rel}", p.exists(), "required proof test must exist"))

    for rel in REQUIRED_FILE_EVIDENCE:
        p = root / rel
        checks.append(GateCheck(f"evidence_file:{rel}", p.exists() and p.stat().st_size > 0 if p.exists() else False, "required evidence file must exist and be non-empty"))

    for rel in REQUIRED_JSON_EVIDENCE:
        p = root / rel
        ok = False
        details = "required generated evidence must exist and pass"
        if p.exists():
            try:
                payload = _load_json(p)
                ok = payload.get("source") == "generated" and payload.get("ok") is True
            except Exception:
                ok = False
        checks.append(GateCheck(f"evidence_json:{rel}", ok, details))

    roadmap = root / "docs/roadmaps/NEXUS_10_10_MASTER_ROADMAP.md"
    checklist = root / "docs/checklists/NEXUS_10_10_MASTER_CHECKLIST.md"
    checks.append(GateCheck("roadmap_nonempty", roadmap.exists() and len(roadmap.read_text(encoding="utf-8").strip()) > 500, "roadmap must be substantive"))
    checks.append(GateCheck("checklist_nonempty", checklist.exists() and len(checklist.read_text(encoding="utf-8").strip()) > 200, "checklist must be substantive"))

    for rel in REQUIRED_CHECKLISTS:
        p = root / rel
        checks.append(GateCheck(f"checklist_progress:{rel}", _count_checked_boxes(p) > 0, "checklist must show real completed work"))

    scenario_report = root / "docs/release/evidence/behavioral_runtime/behavioral_scenarios_report.json"
    if scenario_report.exists():
        try:
            data = _load_json(scenario_report)
            scenario_checks = data.get("checks", {})
            for name in ["continuity", "memory", "execution"]:
                ok = bool(scenario_checks.get(name, {}).get("ok", False))
                checks.append(GateCheck(f"scenario:{name}", ok, "behavioral scenario must pass"))
        except Exception:
            for name in ["continuity", "memory", "execution"]:
                checks.append(GateCheck(f"scenario:{name}", False, "behavioral scenario report unreadable"))
    else:
        for name in ["continuity", "memory", "execution"]:
            checks.append(GateCheck(f"scenario:{name}", False, "behavioral scenario report missing"))

    return checks


def all_ten_ten_checks_pass(repo_root: str | Path) -> bool:
    return all(c.passed for c in run_ten_ten_gate(repo_root))
