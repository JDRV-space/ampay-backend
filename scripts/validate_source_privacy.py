#!/usr/bin/env python3
"""Reject national identity numbers in committed source text."""

from pathlib import Path
import re


SOURCE_TEXT = Path(__file__).resolve().parents[1] / "data/01_input/pdfs/text"
DNI_VALUE = re.compile(r"\bDNI\b\s*:?\s*\d{7,8}\b", re.IGNORECASE)


def main() -> int:
    findings: list[str] = []
    for path in sorted(SOURCE_TEXT.glob("*.txt")):
        for line_number, line in enumerate(
            path.read_text(encoding="utf-8").splitlines(), start=1
        ):
            if DNI_VALUE.search(line):
                findings.append(f"{path.relative_to(SOURCE_TEXT.parent.parent.parent)}:{line_number}")

    if findings:
        print("FAIL: unredacted DNI values")
        print("\n".join(findings))
        return 1

    print("PASS: source DNI values are redacted")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
