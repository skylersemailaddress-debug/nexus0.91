from __future__ import annotations

try:
    from _release_common import run
except ModuleNotFoundError:  # pragma: no cover
    from scripts._release_common import run

COMMANDS = [
    ["python", "scripts/run_security_governance_scenarios.py"],
    ["python", "scripts/validate_security_governance.py"],
    ["python", "scripts/run_observability_scenarios.py"],
    ["python", "scripts/validate_observability.py"],
]


def main() -> int:
    for command in COMMANDS:
        result = run(command)
        print(f"$ {' '.join(command)}")
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(result.stderr)
        if result.returncode != 0:
            return result.returncode
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
