from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

BANNED_STRINGS = [
    "Status: NO-GO",
    "GitHub Actions: RED",
    "NOT MERGE READY",
    "PR #48",
]

SEARCH_PATHS = [
    ROOT / "docs",
    ROOT / "scripts",
]


def scan() -> list[str]:
    violations: list[str] = []
    for base in SEARCH_PATHS:
        for path in base.rglob("*"):
            if not path.is_file():
                continue
            if path.suffix not in {".md", ".py"}:
                continue
            try:
                text = path.read_text(encoding="utf-8")
            except Exception:
                continue
            for banned in BANNED_STRINGS:
                if banned in text:
                    violations.append(f"{path}: contains '{banned}'")
    return violations


def main() -> int:
    violations = scan()
    if violations:
        print("REPO_TRUTH_CONSISTENCY_FAIL")
        for v in violations:
            print(v)
        return 1
    print("REPO_TRUTH_CONSISTENCY_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
