#!/usr/bin/env python3
"""Render the ARGOS run report from manifest.json.

Writes ``data/raw/argos/report.md``.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from argos import report


def main() -> int:
    path = report.write_report()
    print(f"Wrote: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
