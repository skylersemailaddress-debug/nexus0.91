import json
from pathlib import Path

p = Path("docs/release/evidence/behavioral_runtime/behavioral_scenarios_report.json")
data = json.loads(p.read_text())
mi = data["checks"]["live_scenarios"].get("market_intelligence", {})
checks = mi.get("checks", {})
ok = checks.get("has_opportunities", {}).get("ok") and checks.get("has_score", {}).get("ok")
print(json.dumps({"ok": ok}, indent=2))
exit(0 if ok else 1)
