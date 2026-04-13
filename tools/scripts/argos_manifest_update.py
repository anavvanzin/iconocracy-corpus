#!/usr/bin/env python3
"""Atomic locked writeback to ARGOS manifest.json.

Subagents call this helper after each item attempt; the ``fcntl`` lock
serialises concurrent writes. The patch is a JSON object; the special
``attempts`` key (if present) is *appended* rather than overwritten.

Usage:
    python tools/scripts/argos_manifest_update.py \
        --item-id BR-001 \
        --patch '{"status":"success","attempts":[{"ts":"...","protocol":"iiif","status_code":200}]}'
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from argos import manifest as argos_manifest


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--item-id", required=True)
    parser.add_argument("--patch", required=True, help="JSON object of fields to merge")
    args = parser.parse_args()

    try:
        patch = json.loads(args.patch)
    except json.JSONDecodeError as exc:
        print(f"Invalid patch JSON: {exc}", file=sys.stderr)
        return 2
    if not isinstance(patch, dict):
        print("Patch must be a JSON object", file=sys.stderr)
        return 2

    try:
        argos_manifest.locked_update(args.item_id, patch)
    except KeyError as exc:
        print(f"Manifest update failed: {exc}", file=sys.stderr)
        return 3
    except Exception as exc:  # noqa: BLE001
        print(f"Manifest update error: {exc}", file=sys.stderr)
        return 4
    print(f"updated {args.item_id}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
