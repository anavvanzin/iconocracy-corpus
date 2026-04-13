#!/usr/bin/env python3
"""Build the ARGOS acquisition manifest.

Scans ``corpus/corpus-data.json`` for pending items (those lacking
``thumbnail_url`` or missing from ``data/raw/drive-manifest.json``),
classifies each by source domain protocol, and writes
``data/raw/argos/manifest.json``.

Usage:
    python tools/scripts/argos_build_manifest.py [--dry-run]
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

# Allow running from repo root without PYTHONPATH tweaks.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from argos import manifest as argos_manifest


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print summary without writing manifest.json",
    )
    args = parser.parse_args()

    data = argos_manifest.build_manifest(dry_run=args.dry_run)
    protocol_counts = Counter(entry["protocol"] for entry in data["items"])
    domain_counts = Counter(entry["source_domain"] or "(unknown)" for entry in data["items"])

    print(f"ARGOS manifest — {data['total_items']} pending items")
    print(f"  storage_tier: {data['storage_tier']}")
    print(f"  storage_root: {data['storage_root']}")
    print()
    print("Protocols:")
    for proto, n in protocol_counts.most_common():
        print(f"  {proto:<22} {n}")
    print()
    print("Top domains:")
    for domain, n in domain_counts.most_common(10):
        print(f"  {domain:<40} {n}")
    if args.dry_run:
        print("\n(dry-run — manifest.json NOT written)")
    else:
        print(f"\nWrote: {argos_manifest.MANIFEST_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
