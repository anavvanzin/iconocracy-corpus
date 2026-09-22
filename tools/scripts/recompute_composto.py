#!/usr/bin/env python3
"""Recompute purificacao_composto against the canonical formula.

Canonical formula (tools/scripts/code_purification.py, line 281):
    composite = round(sum(scores) / len(scores), 2)

Some rows in data/processed/purification.jsonl carry a composto that
diverges from the mean of their own indicator vector (e.g. SCOUT-562:
vector mean 1.7, stored composto 3.0). Per METHOD_CONTRACT_2026-07-31,
purificacao_composto is deprecated as probatory value and kept only for
backward compatibility — but where it exists, it must equal the mean of
its own vector, or every consumer that trusts it inherits a bug.

Usage:
    python tools/scripts/recompute_composto.py           # audit only
    python tools/scripts/recompute_composto.py --fix     # rewrite divergent rows

The fix rewrites ONLY the purificacao_composto field of divergent rows
(all other fields are byte-preserved) and reports old -> new per item.
"""
from __future__ import annotations

import argparse
import json
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent
PURIFICATION = REPO / "data" / "processed" / "purification.jsonl"

INDICATORS = [
    "desincorporacao", "rigidez_postural", "dessexualizacao",
    "uniformizacao_facial", "heraldizacao", "enquadramento_arquitetonico",
    "apagamento_narrativo", "monocromatizacao", "serialidade",
    "inscricao_estatal",
]

TOLERANCE = 0.005  # float noise only; real divergences are >= 0.01


def canonical_composto(row: dict) -> float | None:
    vals = [row.get(k) for k in INDICATORS]
    if any(not isinstance(v, int) for v in vals):
        return None  # incomplete/non-integer vector: leave untouched
    return round(sum(vals) / len(vals), 2)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--fix", action="store_true",
                    help="rewrite divergent purificacao_composto values")
    args = ap.parse_args()

    rows = [json.loads(l) for l in PURIFICATION.read_text().splitlines() if l.strip()]
    divergent = []
    for r in rows:
        canon = canonical_composto(r)
        if canon is None:
            continue
        c = r.get("purificacao_composto")
        if not isinstance(c, (int, float)) or abs(c - canon) > TOLERANCE:
            divergent.append((r, c, canon))

    print(f"rows read: {len(rows)}")
    print(f"divergent composto (vs. own vector mean): {len(divergent)}")
    for r, old, new in divergent:
        print(f"  {r.get('id')}: stored={old} -> canonical={new}")

    if not args.fix:
        if divergent:
            print("\naudit only — run with --fix to rewrite")
        return 0

    if not divergent:
        print("nothing to fix")
        return 0

    fixed = {r.get("id"): new for r, _, new in divergent}
    for r in rows:
        if r.get("id") in fixed:
            r["purificacao_composto"] = fixed[r["id"]]

    # atomic rewrite preserving key order and one-JSON-per-line format
    tmp = tempfile.NamedTemporaryFile(
        "w", dir=PURIFICATION.parent, delete=False, encoding="utf-8")
    with tmp:
        for r in rows:
            tmp.write(json.dumps(r, ensure_ascii=False) + "\n")
    tmp_path = Path(tmp.name)
    tmp_path.replace(PURIFICATION)

    print(f"\nrewrote {len(divergent)} rows in {PURIFICATION.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())