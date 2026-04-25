from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

CANONICAL_FILES = [
    ROOT / "docs/release/CURRENT_STATUS.md",
    ROOT / "docs/release/ENTERPRISE_BLOCKERS.md",
    ROOT / "docs/ui/NEXUS_UI_MASTER_TRUTH.md",
]

CURRENT_STATUS = ROOT / "docs/release/CURRENT_STATUS.md"

ACTIVE_STALE_PATTERNS = [
    "Status: NO-GO",
    "Status: RED",
    "Status: OPEN",
    "GitHub Actions: RED",
    "NOT MERGE READY",
]

DRAFT_PATTERNS = [
    "DRAFT UNTIL IMPLEMENTED",
    "Status: DRAFT",
]

ALLOW_TERMS = [
    "archived",
    "archive",
    "historical",
    "stale",
    "superseded",
    "example",
    "quoted",
    "pre-pr #49",
    "pre_pr49",
    "non-blocking",
]

SEARCH_ROOTS = [ROOT / "docs"]


def is_archive_path(path: Path) -> bool:
    try:
        path.relative_to(ROOT / "docs/archive")
        return True
    except ValueError:
        return False


def nearby_context(lines: list[str], index: int) -> str:
    start = max(0, index - 1)
    end = min(len(lines), index + 2)
    return "\n".join(lines[start:end]).lower()


def allowed_by_context(lines: list[str], index: int) -> bool:
    context = nearby_context(lines, index)
    return any(term in context for term in ALLOW_TERMS)


def validate_required_files() -> list[str]:
    violations: list[str] = []
    for path in CANONICAL_FILES:
        if not path.exists():
            violations.append(f"missing canonical file: {path.relative_to(ROOT)}")
    if CURRENT_STATUS.exists():
        text = CURRENT_STATUS.read_text(encoding="utf-8")
        for required in ["CERTIFIED_BY_EVIDENCE", "GREEN"]:
            if required not in text:
                violations.append(
                    f"{CURRENT_STATUS.relative_to(ROOT)}: missing required current status token {required!r}"
                )
    return violations


def validate_markdown_truth() -> list[str]:
    violations: list[str] = []
    patterns = ACTIVE_STALE_PATTERNS + DRAFT_PATTERNS
    for root in SEARCH_ROOTS:
        for path in root.rglob("*.md"):
            if is_archive_path(path):
                continue
            try:
                lines = path.read_text(encoding="utf-8").splitlines()
            except Exception as exc:
                violations.append(f"{path.relative_to(ROOT)}: could not read file: {exc}")
                continue
            for index, line in enumerate(lines):
                for pattern in patterns:
                    if pattern in line and not allowed_by_context(lines, index):
                        violations.append(
                            f"{path.relative_to(ROOT)}:{index + 1}: active stale truth claim: {pattern}"
                        )
    return violations


def main() -> int:
    violations = []
    violations.extend(validate_required_files())
    violations.extend(validate_markdown_truth())
    if violations:
        print("DOCS_TRUTH_HYGIENE_FAIL")
        for violation in violations:
            print(violation)
        return 1
    print("DOCS_TRUTH_HYGIENE_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
