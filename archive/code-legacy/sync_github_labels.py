#!/usr/bin/env python3
"""Sync the repository's small label set to GitHub using gh CLI."""

from __future__ import annotations

import argparse
import json
import re
import shlex
import shutil
import subprocess
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
LABELS_FILE = REPO / ".github" / "labels.json"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Sync labels defined in .github/labels.json using gh.")
    parser.add_argument(
        "--repo",
        default="",
        help="GitHub repository in OWNER/REPO form. Defaults to origin remote.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print gh commands without executing them.",
    )
    return parser.parse_args()


def detect_repo() -> str:
    try:
        remote = subprocess.run(
            ["git", "-C", str(REPO), "remote", "get-url", "origin"],
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
    except subprocess.CalledProcessError as exc:
        raise SystemExit("Could not detect origin remote; pass --repo explicitly.") from exc

    patterns = [
        r"github\.com[:/](?P<repo>[^/]+/[^/.]+)(?:\.git)?$",
    ]
    for pattern in patterns:
        match = re.search(pattern, remote)
        if match:
            return match.group("repo")
    raise SystemExit(f"Could not parse GitHub repo from origin remote: {remote}")


def load_labels() -> list[dict]:
    return json.loads(LABELS_FILE.read_text(encoding="utf-8"))


def main() -> None:
    args = parse_args()
    if shutil.which("gh") is None:
        raise SystemExit("gh CLI is not installed or not on PATH.")

    repo = args.repo or detect_repo()
    labels = load_labels()

    for label in labels:
        cmd = [
            "gh",
            "label",
            "create",
            label["name"],
            "--color",
            label["color"],
            "--description",
            label["description"],
            "--force",
            "-R",
            repo,
        ]
        if args.dry_run:
            print(shlex.join(cmd))
            continue
        subprocess.run(cmd, check=True)
        print(f"Synced label: {label['name']}")


if __name__ == "__main__":
    main()
