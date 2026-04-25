from pathlib import Path
import sys

# Compute repo root from this file (scripts/ directory)
ROOT = Path(__file__).resolve().parents[1]

# Prepend repo root to sys.path if not already present
root_str = str(ROOT)
if root_str not in sys.path:
    sys.path.insert(0, root_str)
