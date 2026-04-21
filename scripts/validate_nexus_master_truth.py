from __future__ import annotations
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from nexus_os.governance.master_truth_gate import run_master_truth_gate

def main() -> int:
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
    checks = run_master_truth_gate(root)
    failed = [c for c in checks if not c.passed]

    for c in checks:
        print(f"[{'PASS' if c.passed else 'FAIL'}] {c.name} :: {c.details}")

    if failed:
        print(f"\nMASTER_TRUTH_GATE=FAIL ({len(failed)} failing checks)")
        return 1

    print("\nMASTER_TRUTH_GATE=PASS")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
