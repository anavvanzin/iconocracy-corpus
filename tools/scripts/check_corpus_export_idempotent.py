#!/usr/bin/env python3
"""Gate: fail if corpus export drifts on authoritative fields."""

from __future__ import annotations

import math
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from tools.scripts.records_to_corpus import (
    _load_existing_corpus,
    _load_records,
    export_corpus,
)

# Keep in sync with the authoritative update block in
# tools/scripts/records_to_corpus.py::_corpus_entry_from_record().
AUTHORITATIVE_FIELDS = (
    "url",
    "title",
    "description",
    "motif",
    "regime",
    "endurecimento_score",
    "coded_by",
    "coded_at",
    "indicadores",
    "citation_abnt",
    "audit_flags",
)


def diff_authoritative_fields(generated: dict, existing: dict) -> list[str]:
    """Return human-readable diffs for any authoritative field mismatch."""
    diffs: list[str] = []
    for field in AUTHORITATIVE_FIELDS:
        g = generated.get(field)
        e = existing.get(field)
        if field == "endurecimento_score" and isinstance(g, (int, float)) and isinstance(e, (int, float)):
            if not math.isclose(g, e, abs_tol=1e-9):
                diffs.append(f"  {field}: generated={g!r} existing={e!r}")
        elif g != e:
            diffs.append(f"  {field}: generated={g!r} existing={e!r}")
    return diffs


def main() -> int:
    records = _load_records()
    existing_corpus = _load_existing_corpus()
    generated = export_corpus(records, existing_corpus, replace=False)

    id_less = [g for g in generated if "id" not in g]
    if id_less:
        print(f"corpus export NOT idempotent: {len(id_less)} generated items lack 'id'")
        for item in id_less[:5]:
            print(f"  missing id: title={item.get('title', '(no title)')!r}")
        if len(id_less) > 5:
            print(f"  ... and {len(id_less) - 5} more")
        return 1

    # Index both by id for alignment
    generated_by_id: dict[str, dict] = {g["id"]: g for g in generated if "id" in g}
    existing_by_id: dict[str, dict] = existing_corpus

    all_ids = set(generated_by_id.keys()) | set(existing_by_id.keys())
    total_diffs: list[str] = []

    for item_id in sorted(all_ids):
        g = generated_by_id.get(item_id, {})
        e = existing_by_id.get(item_id, {})
        diffs = diff_authoritative_fields(g, e)
        if diffs:
            total_diffs.append(f"[{item_id}]")
            total_diffs.extend(diffs)

    if total_diffs:
        print(f"corpus export NOT idempotent: {len(total_diffs)} difference lines")
        for line in total_diffs[:80]:
            print(line)
        if len(total_diffs) > 80:
            print(f"... and {len(total_diffs) - 80} more lines")
        return 1

    print("corpus export idempotent: authoritative fields match")
    return 0


if __name__ == "__main__":
    sys.exit(main())
