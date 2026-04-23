from __future__ import annotations

from pathlib import Path

BANNED_PATTERNS = (
    "assert" + " False",
    "Replace this" + " placeholder",
    "TO" + "DO",
    "DRAFT UNTIL" + " IMPLEMENTED",
)


def test_required_tests_have_no_placeholder_content() -> None:
    root = Path(__file__).resolve().parents[1]
    violations: list[str] = []

    for path in sorted((root / "tests").glob("test_*.py")):
        text = path.read_text(encoding="utf-8")
        for pattern in BANNED_PATTERNS:
            if pattern in text:
                rel = path.relative_to(root)
                violations.append(f"{rel}:{pattern}")

    assert not violations, f"Placeholder tests detected: {violations}"
