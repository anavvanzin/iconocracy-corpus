#!/usr/bin/env python3
"""Create timestamped local vault backups outside normal git history."""

from __future__ import annotations

import argparse
import json
import tarfile
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
VAULT = REPO / "vault"
DEFAULT_DEST = REPO / "tmp" / "vault-backups"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create a timestamped tar.gz backup of vault/ outside git history."
    )
    parser.add_argument(
        "--dest",
        type=Path,
        default=DEFAULT_DEST,
        help=f"Destination directory (default: {DEFAULT_DEST})",
    )
    parser.add_argument(
        "--note",
        default="",
        help="Optional note to store next to the backup manifest.",
    )
    parser.add_argument(
        "--keep",
        type=int,
        default=20,
        help="Number of most recent backups to keep per destination (default: 20).",
    )
    return parser.parse_args()


def prune_old_backups(dest: Path, keep: int) -> list[Path]:
    if keep <= 0:
        return []
    archives = sorted(dest.glob("vault-*.tar.gz"))
    stale = archives[:-keep]
    for path in stale:
        path.unlink(missing_ok=True)
        manifest = path.with_suffix("").with_suffix(".json")
        manifest.unlink(missing_ok=True)
    return stale


def main() -> None:
    args = parse_args()
    if not VAULT.exists():
        raise SystemExit(f"Vault not found: {VAULT}")

    args.dest.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%SZ")
    archive_path = args.dest / f"vault-{stamp}.tar.gz"
    manifest_path = args.dest / f"vault-{stamp}.json"

    with tarfile.open(archive_path, "w:gz") as tar:
        tar.add(VAULT, arcname="vault")

    manifest = {
        "created_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "source": str(VAULT),
        "archive": str(archive_path),
        "note": args.note,
    }
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    pruned = prune_old_backups(args.dest, args.keep)
    print(f"Backup created: {archive_path}")
    print(f"Manifest created: {manifest_path}")
    if pruned:
        print(f"Pruned {len(pruned)} older backup(s).")


if __name__ == "__main__":
    main()
