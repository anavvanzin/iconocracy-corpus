#!/usr/bin/env python3
"""build_purification_manifest.py — Identify corpus entries lacking purification coding.

Produces a JSON manifest listing every entry in corpus/corpus-data.json that has
no matching record in data/processed/purification.jsonl, with id (when available),
URL, title hint, and the reason it is queued.

Per ADR 007 / Issue #57, these entries remain in the public corpus with an
`uncoded-purification` audit flag; this manifest is the authoritative work queue.

Usage:
    python tools/scripts/build_purification_manifest.py
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent
CORPUS = REPO / "corpus" / "corpus-data.json"
PURIF = REPO / "data" / "processed" / "purification.jsonl"
OUT = REPO / "data" / "processed" / "purification-manifest.json"


def _load_coded_ids() -> set[str]:
    """Return the set of corpus IDs that have purification entries."""
    coded: set[str] = set()
    if not PURIF.exists():
        return coded
    with PURIF.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            rec = json.loads(line)
            item_id = rec.get("id", "")
            if item_id:
                coded.add(item_id)
    return coded


def main() -> None:
    corpus: list[dict] = json.loads(CORPUS.read_text(encoding="utf-8"))
    coded_ids = _load_coded_ids()

    queued: list[dict] = []
    for entry in corpus:
        entry_id = entry.get("id", "")
        # An entry is coded if it has an id that appears in purification.jsonl
        if entry_id and entry_id in coded_ids:
            continue

        # Determine reason
        if not entry_id:
            reason = "no corpus id assigned"
        else:
            reason = "missing purification entry"

        queued.append(
            {
                "corpus_id": entry_id,
                "url": entry.get("url", ""),
                "title_hint": (entry.get("title") or "")[:120],
                "country": entry.get("country", ""),
                "reason": reason,
            }
        )

    queued.sort(key=lambda x: (x["corpus_id"] or "\xff", x["title_hint"]))

    total_records = len(corpus)
    total_coded = total_records - len(queued)

    payload = {
        "version": "1.0",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "total_records": total_records,
        "total_coded": total_coded,
        "total_queued": len(queued),
        "queued": queued,
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"OK: {len(queued)} queued records written to {OUT}")
    print(f"    coded: {total_coded} / {total_records}")
    no_id = sum(1 for q in queued if not q["corpus_id"])
    if no_id:
        print(f"    entries without corpus id: {no_id}")


if __name__ == "__main__":
    main()
