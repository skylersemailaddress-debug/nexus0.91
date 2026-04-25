#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"

if [ -f "$ROOT/.venv/bin/activate" ]; then
  # shellcheck disable=SC1091
  source "$ROOT/.venv/bin/activate"
else
  echo "Missing .venv. Create it with:"
  echo "python -m venv .venv && source .venv/bin/activate && pip install -e ."
  exit 1
fi

python - <<'PY'
missing = []
for mod in ["fastapi", "uvicorn", "nexus_os.product.api_server"]:
    try:
        __import__(mod)
    except Exception as exc:
        missing.append(f"{mod}: {exc}")
if missing:
    print("Missing API dependencies:")
    print("Run: pip install -e . && pip install fastapi uvicorn")
    raise SystemExit(1)
PY

if [ ! -d "$ROOT/desktop_shell/node_modules" ]; then
  echo "Missing desktop dependencies."
  echo "Run: cd desktop_shell && npm install"
  exit 1
fi

API_AUTH_TOKEN="${API_AUTH_TOKEN:-dev-api-token}"
API_URL="${NEXUS_API_URL:-http://127.0.0.1:8765}"
API_PID=""

cleanup() {
  if [ -n "${API_PID:-}" ]; then
    kill "$API_PID" >/dev/null 2>&1 || true
  fi
}
trap cleanup EXIT

api_ready() {
  curl -fsS "$API_URL/api/state" -H "Authorization: Bearer $API_AUTH_TOKEN" >/dev/null 2>&1
}

if api_ready; then
  echo "Nexus API already running at $API_URL"
else
  echo "Starting Nexus API at $API_URL"
  API_AUTH_TOKEN="$API_AUTH_TOKEN" uvicorn nexus_os.product.api_server:app --host 127.0.0.1 --port 8765 >/tmp/nexus-api.log 2>&1 &
  API_PID="$!"

  for _ in $(seq 1 30); do
    if api_ready; then
      break
    fi
    sleep 0.5
  done

  if ! api_ready; then
    echo "Nexus API did not become ready. Last API log:"
    tail -n 80 /tmp/nexus-api.log || true
    exit 1
  fi
fi

cd "$ROOT/desktop_shell"

if [ -n "${DISPLAY:-}" ]; then
  echo "Launching Nexus Desktop: graphical mode"
  npm run desktop
else
  if ! command -v xvfb-run >/dev/null 2>&1; then
    echo "No DISPLAY and xvfb-run is not installed."
    echo "In Codespaces run:"
    echo "sudo apt-get update && sudo apt-get install -y xvfb libatk1.0-0t64 libatk-bridge2.0-0t64 libgtk-3-0t64 libnss3 libxss1 libasound2t64 libx11-xcb1 libxcomposite1 libxdamage1 libxrandr2 libgbm1"
    exit 1
  fi

  echo "Launching Nexus Desktop: headless Codespaces mode via xvfb-run"
  ELECTRON_DISABLE_GPU=1 xvfb-run -a ./node_modules/.bin/electron electron/main.js --disable-gpu --disable-software-rasterizer --no-sandbox
fi
