from __future__ import annotations
from dataclasses import dataclass
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

def run_ten_ten_gate(repo_root: str | Path) -> list[GateCheck]:
    root = Path(repo_root)
    checks: list[GateCheck] = []

    for rel in REQUIRED_PATHS:
        p = root / rel
        checks.append(GateCheck(
            name=f"path:{rel}",
            passed=p.exists(),
            details="required file/package path must exist",
        ))

    for rel in REQUIRED_TESTS:
        p = root / rel
        checks.append(GateCheck(
            name=f"test:{rel}",
            passed=p.exists(),
            details="required proof test must exist",
        ))

    roadmap = root / "docs/roadmaps/NEXUS_10_10_MASTER_ROADMAP.md"
    checklist = root / "docs/checklists/NEXUS_10_10_MASTER_CHECKLIST.md"

    checks.append(GateCheck(
        name="roadmap_nonempty",
        passed=roadmap.exists() and len(roadmap.read_text(encoding="utf-8").strip()) > 500,
        details="roadmap must be substantive",
    ))
    checks.append(GateCheck(
        name="checklist_nonempty",
        passed=checklist.exists() and len(checklist.read_text(encoding="utf-8").strip()) > 200,
        details="checklist must be substantive",
    ))

    return checks

def all_ten_ten_checks_pass(repo_root: str | Path) -> bool:
    return all(c.passed for c in run_ten_ten_gate(repo_root))
