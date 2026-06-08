#!/usr/bin/env python3
"""tag_uncoded_purification.py — Add `uncoded-purification` audit flag to corpus
entries that appear in the purification manifest's queued list.

Idempotent: running twice does not duplicate the flag.

Prerequisites:
    Run build_purification_manifest.py first to generate the manifest.

Usage:
    python tools/scripts/tag_uncoded_purification.py
"""

from __future__ import annotations

import json
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent
CORPUS = REPO / "corpus" / "corpus-data.json"
MANIFEST = REPO / "data" / "processed" / "purification-manifest.json"
FLAG = "uncoded-purification"


def main() -> None:
    if not MANIFEST.exists():
        print(f"ERROR: manifest not found at {MANIFEST}")
        print("       Run build_purification_manifest.py first.")
        raise SystemExit(1)

    corpus: list[dict] = json.loads(CORPUS.read_text(encoding="utf-8"))
    manifest: dict = json.loads(MANIFEST.read_text(encoding="utf-8"))

    # Build lookup sets from manifest
    queued_corpus_ids: set[str] = {q["corpus_id"] for q in manifest["queued"] if q["corpus_id"]}
    queued_urls: set[str] = {q["url"] for q in manifest["queued"] if not q["corpus_id"] and q["url"]}

    tagged = 0
    already_tagged = 0
    for entry in corpus:
        entry_id = entry.get("id", "")
        entry_url = entry.get("url", "")

        is_queued = (entry_id and entry_id in queued_corpus_ids) or (
            not entry_id and entry_url and entry_url in queued_urls
        )
        if not is_queued:
            continue

        flags: list[str] = list(entry.get("audit_flags") or [])
        if FLAG in flags:
            already_tagged += 1
        else:
            flags.append(FLAG)
            entry["audit_flags"] = flags
            tagged += 1

    CORPUS.write_text(
        json.dumps(corpus, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )

    total_flagged = tagged + already_tagged
    print(f"OK: tagged {tagged} entries with `{FLAG}` ({already_tagged} already had the flag)")
    print(f"    total entries now carrying flag: {total_flagged}")
    # Note: total_flagged may exceed manifest's total_queued when corpus-data.json
    # contains duplicate entries (same URL, no id) — both duplicates get flagged.
    print(f"    manifest total_queued: {manifest['total_queued']}")


if __name__ == "__main__":
    main()
