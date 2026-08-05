#!/usr/bin/env python3
"""Reject national identity numbers in committed source text."""

from pathlib import Path
import re


SOURCE_TEXT = Path(__file__).resolve().parents[1] / "data/01_input/pdfs/text"
IDENTITY_VALUES = (
    re.compile(r"\bDNI\b\s*:?\s*\d{7,8}\b", re.IGNORECASE),
    re.compile(r"\bFIR\s+\d{7,8}\s+hard\b", re.IGNORECASE),
)


def main() -> int:
    findings: list[str] = []
    for path in sorted(SOURCE_TEXT.glob("*.txt")):
        text = path.read_text(encoding="utf-8")
        for pattern in IDENTITY_VALUES:
            for match in pattern.finditer(text):
                line_number = text.count("\n", 0, match.start()) + 1
                findings.append(
                    f"{path.relative_to(SOURCE_TEXT.parent.parent.parent)}:{line_number}"
                )

    if findings:
        print("FAIL: unredacted identity values")
        print("\n".join(findings))
        return 1

    print("PASS: source identity values are redacted")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
