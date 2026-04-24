from __future__ import annotations

try:
    from _release_common import run
except ModuleNotFoundError:  # pragma: no cover
    from scripts._release_common import run


COMMANDS = [
    ["python", "scripts/run_continuity_scenarios.py"],
    ["python", "scripts/validate_continuity.py"],
    ["python", "scripts/run_memory_context_scenarios.py"],
    ["python", "scripts/validate_memory_context_integration.py"],
    ["python", "scripts/run_memory_trace_scenarios.py"],
    ["python", "scripts/validate_memory_trace.py"],
    ["python", "scripts/run_memory_behavior_scenarios.py"],
    ["python", "scripts/validate_memory_behavior.py"],
    ["python", "scripts/validate_memory.py"],
    ["python", "scripts/run_execution_scenarios.py"],
    ["python", "scripts/validate_execution.py"],
    ["python", "scripts/validate_execution_resume.py"],
    ["python", "scripts/run_ui_truth_scenarios.py"],
    ["python", "scripts/validate_ui_truth.py"],
    ["python", "scripts/run_readiness_scenarios.py"],
    ["python", "scripts/validate_readiness.py"],
    ["python", "scripts/run_release_hardening.py"],
    ["python", "scripts/validate_release_hardening.py"],
    ["python", "scripts/security_baseline.py"],
    ["python", "scripts/validate_observability.py"],
    ["python", "scripts/run_adaptive_learning_scenarios.py"],
    ["python", "scripts/validate_adaptive_learning.py"],
    ["python", "scripts/run_max_power_scenarios.py"],
    ["python", "scripts/validate_max_power.py"],
    ["python", "scripts/run_full_system_wiring_scenarios.py"],
    ["python", "scripts/validate_full_system_wiring.py"],
    ["python", "scripts/run_final_configuration_scenarios.py"],
    ["python", "scripts/validate_final_configuration.py"],
    ["python", "scripts/validate_no_placeholder_tests.py"],
    ["python", "scripts/validate_repo_truth_consistency.py"],
    ["python", "scripts/validate_nexus_master_truth.py"],
    ["python", "scripts/validate_nexus_10_10_gate.py"],
    ["python", "scripts/validate_enterprise_gate_coverage.py"],
    ["python", "scripts/run_release_hardening.py"],
    ["python", "scripts/validate_release_hardening.py"],
    ["python", "scripts/run_final_certification_scenarios.py"],
    ["python", "scripts/validate_final_certification.py"],
    ["python", "-m", "pytest", "-q", "tests"],
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
