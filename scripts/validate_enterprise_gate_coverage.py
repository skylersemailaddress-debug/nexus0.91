from __future__ import annotations

import ast
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GATE_PATH = ROOT / "scripts" / "run_enterprise_gate.py"
REPORT_PATH = ROOT / "docs" / "release" / "evidence" / "enterprise_gate" / "enterprise_gate_coverage_report.json"

REQUIRED_TOKENS = {
    "continuity": ["validate_continuity.py"],
    "memory": ["validate_memory.py"],
    "execution": ["validate_execution.py", "validate_execution_resume.py"],
    "ui_truth": ["validate_ui_truth.py"],
    "readiness": ["validate_readiness.py"],
    "release_hardening": ["validate_release_hardening.py"],
    "security": ["security_baseline.py"],
    "observability": ["validate_observability.py"],
    "adaptive_learning": ["validate_adaptive_learning.py"],
    "max_power": ["validate_max_power.py"],
    "full_system_wiring": ["validate_full_system_wiring.py"],
    "final_configuration": ["validate_final_configuration.py"],
    "final_certification": ["validate_final_certification.py"],
    "score_label_authority": ["validate_nexus_10_10_gate.py"],
}


def _load_commands() -> list[list[str]]:
    module = ast.parse(GATE_PATH.read_text(encoding="utf-8"))
    for node in module.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == "COMMANDS":
                    value = ast.literal_eval(node.value)
                    return [[str(part) for part in command] for command in value]
    raise RuntimeError("COMMANDS list missing")


def main() -> int:
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    commands = _load_commands()
    joined = "\n".join(" ".join(command) for command in commands)

    checks = []
    for domain, required in REQUIRED_TOKENS.items():
        missing = [token for token in required if token not in joined]
        checks.append({"domain": domain, "passed": not missing, "missing": missing})

    report = {"passed": all(item["passed"] for item in checks), "checks": checks, "command_count": len(commands)}
    REPORT_PATH.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
