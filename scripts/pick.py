#!/usr/bin/env python3
"""pick — choose an ICONOCRACY prompt from vault/prompts.

Usage:
    pick
    pick <query>
    pick -n|--number N
    pick -d|--domain dominio

Output:
    Prints the chosen prompt content to stdout.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent
INDEX_PATH = REPO_ROOT / "vault" / "prompts" / "INDEX.md"
PROMPTS_DIR = REPO_ROOT / "vault" / "prompts"

INDEX_FALLBACK = Path("/Users/ana/vault/prompts/INDEX.md")
PROMPTS_FALLBACK = Path("/Users/ana/vault/prompts")


def load_index(index_path: Path):
    entries = []
    for line in index_path.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*(`[^`]+`)\s*\|$", line)
        if not m:
            continue
        pid, title, domain, lang, path_ref = [x.strip() for x in m.groups()]
        entries.append({
            "id": pid,
            "title": title,
            "domain": domain,
            "language": lang,
            "path": path_ref.strip("`"),
        })
    return entries


def resolve_path(relpath: str) -> Path | None:
    for base in (PROMPTS_DIR / relpath, PROMPTS_FALLBACK / relpath):
        if base.exists():
            return base
    return None


def render_table(entries):
    print(f"{'#':<5} {'Domain':<14} {'Lang':<5} {'Title'}")
    print("-" * 75)
    for idx, entry in enumerate(entries, start=1):
        print(f"{idx:<5} {entry['domain']:<14} {entry['language']:<5} {entry['title']}")


def filter_entries(entries, query: str | None, domain: str | None):
    q = (query or "").lower().strip()
    domain_q = (domain or "").lower().strip()
    out = []
    for entry in entries:
        haystack = " ".join([
            entry["id"], entry["title"], entry["domain"], entry["language"], entry["path"],
        ]).lower()
        if q and q not in haystack:
            continue
        if domain_q and entry["domain"].lower() != domain_q:
            continue
        out.append(entry)
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description="Pick an ICONOCRACY prompt.")
    ap.add_argument("query", nargs="?", help="Search title/domain/id/path")
    ap.add_argument("-n", "--number", type=int, help="Pick by menu number")
    ap.add_argument("-d", "--domain", help="Filter by domain folder")
    ap.add_argument("-l", "--list", action="store_true", help="List and exit")
    args = ap.parse_args()

    index_path = INDEX_PATH if INDEX_PATH.exists() else INDEX_FALLBACK
    if not index_path.exists():
        print("INDEX.md not found for vault/prompts.", file=sys.stderr)
        return 1

    entries = load_index(index_path)
    filtered = filter_entries(entries, args.query, args.domain)

    if not filtered:
        print("No matching prompts.")
        return 0

    if args.number is not None:
        idx = args.number - 1
        if idx < 0 or idx >= len(filtered):
            print(f"Number out of range (1..{len(filtered)}).")
            return 1
        entry = filtered[idx]
    elif len(filtered) == 1 and not args.list and not args.query:
        entry = filtered[0]
    else:
        render_table(filtered)
        if len(filtered) == 1 and not args.query:
            entry = filtered[0]
            print(f"\nOnly one match: #{filtered.index(entry)+1}")
        else:
            return 0

    path = resolve_path(entry["path"])
    if path is None or not path.exists():
        print(f"Prompt file missing: {entry['path']}", file=sys.stderr)
        return 1
    print(f"# Prompt: {entry['id']} | {entry['title']} | {entry['domain']}\n")
    print(path.read_text(encoding="utf-8"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
