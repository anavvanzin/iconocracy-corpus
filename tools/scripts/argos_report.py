#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from tools.argos.report import write_report

DEFAULT_MANIFEST_PATH = REPO_ROOT / "data" / "raw" / "argos" / "manifest.json"
DEFAULT_OUTPUT_PATH = REPO_ROOT / "data" / "raw" / "argos" / "report.md"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate an ARGOS markdown acquisition report from a manifest.")
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST_PATH, help="Path to ARGOS manifest.json")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT_PATH, help="Path to write report.md")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    write_report(args.manifest, args.output)
    print(f"Report written to {args.output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
