#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from tools.argos.manifest import build_manifest, pending_item_count, protocol_breakdown
from tools.argos.storage import resolve_storage_root

DEFAULT_CORPUS_PATH = REPO_ROOT / "corpus" / "corpus-data.json"
DEFAULT_DRIVE_MANIFEST_PATH = REPO_ROOT / "data" / "raw" / "drive-manifest.json"
DEFAULT_OUTPUT_PATH = REPO_ROOT / "data" / "raw" / "argos" / "manifest.json"


def _load_json(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _print_summary(manifest: dict) -> None:
    print(f"Pending items: {manifest['summary']['pending']}")
    print("Protocol breakdown:")
    breakdown = protocol_breakdown(manifest)
    if not breakdown:
        print("  (none)")
        return

    for protocol, count in breakdown.items():
        print(f"  {protocol}: {count}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build the ARGOS pending acquisition manifest.")
    parser.add_argument("--dry-run", action="store_true", help="Print pending counts without writing the manifest")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT_PATH, help="Manifest output path")
    parser.add_argument("--limit", type=int, default=None, help="Maximum number of pending items to include")
    parser.add_argument("--corpus", type=Path, default=DEFAULT_CORPUS_PATH, help="Path to corpus/corpus-data.json")
    parser.add_argument(
        "--drive-manifest",
        type=Path,
        default=DEFAULT_DRIVE_MANIFEST_PATH,
        help="Path to data/raw/drive-manifest.json",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    corpus_items = _load_json(args.corpus)
    drive_manifest = _load_json(args.drive_manifest)
    storage_root, storage_tier = resolve_storage_root(REPO_ROOT)
    manifest = build_manifest(
        corpus_items,
        drive_manifest,
        storage_root=storage_root,
        storage_tier=storage_tier,
        limit=args.limit,
    )

    _print_summary(manifest)

    if pending_item_count(manifest) == 0:
        print("No pending items remain.")
        if not args.dry_run and args.output.exists():
            args.output.unlink()
            print(f"Removed stale manifest at {args.output}")
        return 0

    if args.dry_run:
        print("Dry run: manifest not written")
        return 0

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Manifest written to {args.output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
