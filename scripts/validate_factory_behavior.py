import json
from pathlib import Path

p = Path("docs/release/evidence/behavioral_runtime/behavioral_scenarios_report.json")
data = json.loads(p.read_text())
f = data["checks"]["live_scenarios"].get("factory", {})
ok = f.get("ok", False)
print(json.dumps({"ok": ok}, indent=2))
exit(0 if ok else 1)
