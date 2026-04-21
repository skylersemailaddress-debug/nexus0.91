from __future__ import annotations

from scripts._release_common import run


COMMANDS = [
    ["python", "scripts/validate_no_placeholder_tests.py"],
    ["python", "-m", "pytest", "-q", "tests/test_no_placeholder_tests.py", "tests/test_package_build_smoke.py", "tests/test_runtime_health_smoke.py", "tests/test_launch_scripts_smoke.py", "tests/test_installed_entrypoint_smoke.py"],
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
