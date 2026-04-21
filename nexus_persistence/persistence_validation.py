from __future__ import annotations

from pathlib import Path

REQUIRED_PERSISTENCE_ARTIFACTS = (
    "docs/release/ENTERPRISE_RELEASE_EVIDENCE.json",
    "docs/release/RELEASE_SCOPE.md",
    "docs/release/SUPPORT_MATRIX.md",
)


def persistence_validation(repo_root: str | Path) -> dict[str, object]:
    root = Path(repo_root)
    missing = [item for item in REQUIRED_PERSISTENCE_ARTIFACTS if not (root / item).exists()]
    return {
        "repo_root": str(root),
        "valid": not missing,
        "missing": missing,
    }
