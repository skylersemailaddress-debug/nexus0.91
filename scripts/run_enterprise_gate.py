from __future__ import annotations

try:
    from _release_common import run
except ModuleNotFoundError:
    from scripts._release_common import run

COMMANDS = [
    ["python", "scripts/generate_ui_truth_evidence.py"],
    ["python", "scripts/validate_no_placeholder_tests.py"],
    ["python", "scripts/validate_nexus_master_truth.py"],
    ["python", "scripts/validate_nexus_10_10_gate.py"],
    ["python", "scripts/run_behavioral_scenarios.py"],
    ["python", "scripts/validate_behavioral_runtime.py"],
    ["python", "scripts/generate_behavioral_gate_evidence.py"],
    ["python", "scripts/security_baseline.py"],
    ["python", "scripts/validate_replay_consistency.py"],
    ["python", "scripts/validate_trace_consistency.py"],
    [
        "python",
        "-m",
        "pytest",
        "-q",
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
    ],
    ["python", "scripts/generate_release_manifest.py"],
]


def main() -> None:
    for command in COMMANDS:
        result = run(command)
        print(f"$ {' '.join(command)}")
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(result.stderr)
        if result.returncode != 0:
            raise SystemExit(result.returncode)


if __name__ == "__main__":
    main()
