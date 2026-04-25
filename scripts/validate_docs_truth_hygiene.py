from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

BANNED = [
    "Status: NO-GO",
    "Status: RED",
    "Status: OPEN",
    "DRAFT",
]

ALLOW_CONTEXT = [
    "archive",
    "historical",
    "pre_pr49",
]

SEARCH_PATHS = [ROOT / "docs"]


def is_allowed(text):
    lower = text.lower()
    return any(a in lower for a in ALLOW_CONTEXT)


def scan():
    violations = []
    for base in SEARCH_PATHS:
        for path in base.rglob("*.md"):
            if "docs/archive" in str(path):
                continue
            try:
                text = path.read_text(encoding="utf-8")
            except Exception:
                continue
            for b in BANNED:
                if b in text and not is_allowed(text):
                    violations.append(str(path))
    return violations


if __name__ == "__main__":
    v = scan()
    if v:
        print("DOCS_TRUTH_HYGIENE_FAIL")
        for i in v:
            print(i)
        exit(1)
    print("DOCS_TRUTH_HYGIENE_PASS")
