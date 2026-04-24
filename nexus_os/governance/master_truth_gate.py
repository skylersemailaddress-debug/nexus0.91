from __future__ import annotations

import ast
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class TruthCheck:
    name: str
    passed: bool
    details: str


REQUIRED_PATHS = [
    "docs/specs/NEXUS_MASTER_TRUTH_AND_WORK_SYSTEM.md",
    "docs/checklists/NEXUS_10_10_EXECUTION_CHECKLIST.md",
    "docs/roadmaps/NEXUS_10_10_PHASE_GATED_MASTER_ROADMAP.md",
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
    "nexus_os/governance/master_truth_gate.py",
    "scripts/validate_nexus_master_truth.py",
    "tests/test_master_truth_system.py",
]

REQUIRED_IMPLEMENTATION_DOMAINS = [
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

PLACEHOLDER_PATTERNS = [
    "assert False",
    "Replace this placeholder",
    "TODO",
    "DRAFT UNTIL IMPLEMENTED",
]

TRUTH_DRIFT_PATTERNS = [
    "Status: NO-GO",
    "GitHub Actions: RED",
    "NOT MERGE READY",
    "PR #48",
]


def _parse_python(path: Path) -> ast.Module | None:
    try:
        return ast.parse(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def _has_executable_symbol(path: Path) -> bool:
    tree = _parse_python(path)
    if tree is None:
        return False
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)) and not node.name.startswith("_"):
            return True
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == "__all__":
                    return True
    return False


def _test_has_real_assertion(path: Path) -> bool:
    tree = _parse_python(path)
    if tree is None:
        return False
    has_test = any(
        isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name.startswith("test_")
        for node in tree.body
    )
    has_assert = any(isinstance(node, ast.Assert) for node in ast.walk(tree))
    has_call = any(isinstance(node, ast.Call) for node in ast.walk(tree))
    return has_test and has_assert and has_call


def _doc_has_required_sections(path: Path, keywords: list[str]) -> bool:
    if not path.exists():
        return False
    text = path.read_text(encoding="utf-8", errors="ignore").lower()
    return all(keyword.lower() in text for keyword in keywords)


def run_master_truth_gate(repo_root: str | Path) -> list[TruthCheck]:
    root = Path(repo_root)
    checks: list[TruthCheck] = []

    for rel in REQUIRED_PATHS:
        p = root / rel
        checks.append(TruthCheck(
            name=f"path:{rel}",
            passed=p.exists(),
            details="required master-truth path must exist",
        ))

    for rel in REQUIRED_IMPLEMENTATION_DOMAINS:
        p = root / rel
        checks.append(TruthCheck(
            name=f"impl:{rel}",
            passed=p.exists(),
            details="required implementation domain must exist before 10/10 completion",
        ))
        checks.append(TruthCheck(
            name=f"impl_symbol:{rel}",
            passed=p.exists() and _has_executable_symbol(p),
            details="required implementation domain must expose at least one public executable symbol",
        ))

    for rel in REQUIRED_TESTS:
        p = root / rel
        checks.append(TruthCheck(
            name=f"test:{rel}",
            passed=p.exists(),
            details="required proof test must exist",
        ))
        checks.append(TruthCheck(
            name=f"test_depth:{rel}",
            passed=p.exists() and _test_has_real_assertion(p),
            details="required proof test must contain real test functions, assertions, and calls",
        ))

    for rel, min_len, keywords in [
        ("docs/specs/NEXUS_MASTER_TRUTH_AND_WORK_SYSTEM.md", 2000, ["truth", "work", "system"]),
        ("docs/checklists/NEXUS_10_10_EXECUTION_CHECKLIST.md", 500, ["check", "gate"]),
        ("docs/roadmaps/NEXUS_10_10_PHASE_GATED_MASTER_ROADMAP.md", 500, ["phase", "gate"]),
    ]:
        p = root / rel
        checks.append(TruthCheck(
            name=f"substantive:{rel}",
            passed=p.exists() and len(p.read_text(encoding="utf-8").strip()) >= min_len,
            details="canonical truth doc must be substantive",
        ))
        checks.append(TruthCheck(
            name=f"semantic_doc:{rel}",
            passed=_doc_has_required_sections(p, keywords),
            details="canonical truth doc must include required semantic keywords",
        ))

    for rel in REQUIRED_TESTS + ["tests/test_master_truth_system.py"]:
        p = root / rel
        if p.exists():
            text = p.read_text(encoding="utf-8", errors="ignore")
            for pattern in PLACEHOLDER_PATTERNS:
                checks.append(TruthCheck(
                    name=f"placeholder_free:{rel}:{pattern}",
                    passed=pattern not in text,
                    details="required proof tests must not remain placeholder scaffolding",
                ))

    for base in [root / "docs"]:
        if base.exists():
            for p in base.rglob("*.md"):
                text = p.read_text(encoding="utf-8", errors="ignore")
                for pattern in TRUTH_DRIFT_PATTERNS:
                    checks.append(TruthCheck(
                        name=f"truth_drift:{p.relative_to(root)}:{pattern}",
                        passed=pattern not in text,
                        details="documentation must not contain stale red/no-go/old-PR claims outside archive context",
                    ))

    return checks


def all_master_truth_checks_pass(repo_root: str | Path) -> bool:
    return all(c.passed for c in run_master_truth_gate(repo_root))
