from __future__ import annotations

import json
from pathlib import Path

from scripts._release_common import REPO_ROOT, utc_now_iso, write_json


def main() -> None:
    pyproject = REPO_ROOT / "pyproject.toml"
    version = "unknown"
    for line in pyproject.read_text(encoding="utf-8").splitlines():
        if line.startswith("version = "):
            version = line.split("=", 1)[1].strip().strip('"')
            break

    dist_dir = REPO_ROOT / "dist"
    artifacts = []
    if dist_dir.exists():
        for path in sorted(dist_dir.iterdir()):
            if path.is_file():
                artifacts.append({"name": path.name, "size_bytes": path.stat().st_size})

    manifest = {
        "schema_version": "1.0",
        "release_version": version,
        "generated_at_utc": utc_now_iso(),
        "artifacts": artifacts,
    }

    write_json(REPO_ROOT / "docs" / "release" / "RELEASE_MANIFEST.json", manifest)


if __name__ == "__main__":
    main()
