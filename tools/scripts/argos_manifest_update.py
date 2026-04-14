#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from tools.argos.manifest import locked_update_manifest

DEFAULT_MANIFEST_PATH = REPO_ROOT / "data" / "raw" / "argos" / "manifest.json"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Atomically update a single ARGOS manifest item.")
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST_PATH, help="Path to manifest.json")
    parser.add_argument("--item-id", required=True, help="Manifest item_id to update")
    parser.add_argument("--patch", required=True, help="JSON object patch to merge into the matching item")
    parser.add_argument("--lock-path", type=Path, default=None, help="Optional explicit lock file path")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        patch = json.loads(args.patch)
    except json.JSONDecodeError as exc:
        print(f"Invalid patch JSON: {exc}", file=sys.stderr)
        return 1

    if not isinstance(patch, dict):
        print("Patch must decode to a JSON object", file=sys.stderr)
        return 1

    try:
        locked_update_manifest(args.manifest, args.item_id, patch, lock_path=args.lock_path)
    except (KeyError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        return 1

    print(f"Updated manifest item {args.item_id} in {args.manifest}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
