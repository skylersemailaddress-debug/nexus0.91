#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="${ROOT_DIR}/.venv"

if [[ ! -d "${VENV_DIR}" ]]; then
  echo "Missing virtual environment at ${VENV_DIR}. Create it and install the project first." >&2
  echo "Expected setup:" >&2
  echo "  python3 -m venv .venv && source .venv/bin/activate && python -m pip install -e ." >&2
  exit 1
fi

# shellcheck disable=SC1091
source "${VENV_DIR}/bin/activate"

python - <<'PY'
import importlib.util
import sys

if importlib.util.find_spec("nexus_os") is None:
    sys.stderr.write("Nexus package is not installed in the active virtual environment.\n")
    sys.stderr.write("Run: python -m pip install -e .\n")
    raise SystemExit(1)
PY

exec python -m nexus_os.product "$@"
