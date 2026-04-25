from __future__ import annotations
import sys
from pathlib import Path

try:
    import _repo_bootstrap  # noqa: F401
except ModuleNotFoundError:  # pragma: no cover
    from scripts import _repo_bootstrap  # noqa: F401
from nexus_os.governance.ten_ten_gate import run_ten_ten_gate

def main() -> int:
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
    checks = run_ten_ten_gate(root)
    failed = [c for c in checks if not c.passed]

    for c in checks:
        print(f"[{'PASS' if c.passed else 'FAIL'}] {c.name} :: {c.details}")

    if failed:
        print(f"\nTEN_TEN_GATE=FAIL ({len(failed)} failing checks)")
        return 1

    print("\nTEN_TEN_GATE=PASS")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
