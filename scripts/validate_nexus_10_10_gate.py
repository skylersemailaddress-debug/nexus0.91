from __future__ import annotations
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from nexus_os.governance.ten_ten_gate import run_ten_ten_gate

REQUIRED_GENERATED_EVIDENCE = [
    Path("docs/release/evidence/ui/ui_master_truth_report.json"),
    Path("docs/release/evidence/behavioral_gate/behavioral_ten_ten_report.json"),
    Path("docs/release/evidence/behavioral_runtime/behavioral_runtime_report.json"),
]


def _check_generated_sources(root: Path) -> list[str]:
    failures: list[str] = []
    for rel in REQUIRED_GENERATED_EVIDENCE:
        path = root / rel
        if not path.exists():
            failures.append(f"missing evidence file: {rel}")
            continue
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            failures.append(f"invalid evidence json: {rel}: {exc}")
            continue
        if payload.get("source") != "generated":
            failures.append(f"evidence not generated: {rel}")
        if payload.get("ok") is not True:
            failures.append(f"evidence failing: {rel}")
    return failures


def main() -> int:
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
    checks = run_ten_ten_gate(root)
    failed = [c for c in checks if not c.passed]

    for c in checks:
        print(f"[{'PASS' if c.passed else 'FAIL'}] {c.name} :: {c.details}")

    generated_failures = _check_generated_sources(root)
    for item in generated_failures:
        print(f"[FAIL] generated_evidence :: {item}")

    if failed or generated_failures:
        total = len(failed) + len(generated_failures)
        print(f"\nTEN_TEN_GATE=FAIL ({total} failing checks)")
        return 1

    print("\nTEN_TEN_GATE=PASS")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
