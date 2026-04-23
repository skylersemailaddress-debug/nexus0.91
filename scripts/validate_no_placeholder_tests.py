from __future__ import annotations

from pathlib import Path

try:
    from _release_common import REPO_ROOT, fail
except ModuleNotFoundError:  # pragma: no cover
    from scripts._release_common import REPO_ROOT, fail

BANNED_PATTERNS = (
    'assert False',
    'Replace this placeholder',
    'TODO',
    'DRAFT UNTIL IMPLEMENTED',
)


def main() -> None:
    tests_root = REPO_ROOT / "tests"
    violations = []

    for path in sorted(tests_root.rglob("test_*.py")):
        text = path.read_text(encoding="utf-8")
        if any(p in text for p in BANNED_PATTERNS):
            violations.append(str(path.relative_to(REPO_ROOT)))

    if violations:
        fail(f"Placeholder tests detected: {violations}")

    print("placeholder check: PASS")


if __name__ == "__main__":
    main()
