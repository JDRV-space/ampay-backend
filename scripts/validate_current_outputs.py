#!/usr/bin/env python3
"""Run validation checks for the committed AMPAY outputs."""

from validate_ampay_traceability import main as validate_traceability


def main() -> int:
    return validate_traceability()


if __name__ == "__main__":
    raise SystemExit(main())
