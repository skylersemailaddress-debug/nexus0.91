from __future__ import annotations

try:
    from _release_common import run
except ModuleNotFoundError:  # pragma: no cover
    from scripts._release_common import run


COMMANDS = [
    ["python", "scripts/validate_no_placeholder_tests.py"],
    ["python", "scripts/validate_nexus_master_truth.py"],
    ["python", "scripts/validate_nexus_10_10_gate.py"],
    ["python", "scripts/validate_enterprise_gate_coverage.py"],
    [
        "python",
        "-m",
        "pytest",
        "-q",
        "tests/test_no_placeholder_tests.py",
        "tests/test_package_build_smoke.py",
        "tests/test_runtime_health_smoke.py",
        "tests/test_launch_scripts_smoke.py",
        "tests/test_installed_entrypoint_smoke.py",
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
    ["python", "scripts/security_baseline.py"],
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
