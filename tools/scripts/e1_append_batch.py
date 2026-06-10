#!/usr/bin/env python3
# tools/scripts/e1_append_batch.py
"""Validated atomic append of coded E1 batches to pathosformel_index.jsonl.

Input: a JSON file with a LIST of coded items (one per subagent output).
Each item must carry the 10 indicators (int 0-3), regime, provenance fields.
Computes purificacao_composto. Rejects invalid items whole (no partial rows).
Marks corresponding worklist entries as done.

Usage:
    python tools/scripts/e1_append_batch.py batch_NN.json
"""
from __future__ import annotations

import argparse
import json
import os
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent
RECORDS_PATH = REPO / "data" / "processed" / "records.jsonl"
INDEX_PATH = REPO / "data" / "processed" / "pathosformel_index.jsonl"
WORKLIST_PATH = REPO / "data" / "processed" / "e1_worklist.json"

INDICATORS = [
    "desincorporacao", "rigidez_postural", "dessexualizacao",
    "uniformizacao_facial", "heraldizacao", "enquadramento_arquitetonico",
    "apagamento_narrativo", "monocromatizacao", "serialidade",
    "inscricao_estatal",
]
REGIMES = {"fundacional", "normativo", "militar", "contra-alegoria"}
REQUIRED = {"item_id", "sigla_id", "coded_by", "coded_at", "coded_from",
            "image_source", "regime_iconocratico"}


def validate_item(item: dict, known_ids: set[str],
                  indexed_ids: set[str]) -> list[str]:
    errs: list[str] = []
    missing = REQUIRED - item.keys()
    if missing:
        errs.append(f"campos ausentes: {sorted(missing)}")
    for ind in INDICATORS:
        v = item.get(ind)
        if not isinstance(v, int) or not 0 <= v <= 3:
            errs.append(f"{ind}={v!r} fora de 0-3")
    if item.get("regime_iconocratico") not in REGIMES:
        errs.append(f"regime invalido: {item.get('regime_iconocratico')!r}")
    if item.get("item_id") not in known_ids:
        errs.append(f"item_id {item.get('item_id')!r} nao existe em records.jsonl")
    if item.get("item_id") in indexed_ids:
        errs.append(f"item_id {item.get('item_id')!r} duplicado no index")
    return errs


def _atomic_append_lines(path: Path, lines: list[str]) -> None:
    existing = path.read_text(encoding="utf-8") if path.exists() else ""
    fd, tmp = tempfile.mkstemp(dir=str(path.parent), suffix=".tmp")
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        f.write(existing)
        for line in lines:
            f.write(line + "\n")
    os.replace(tmp, path)


def append_batch(items: list[dict], index_path: Path, worklist_path: Path,
                 known_ids: set[str]) -> tuple[int, list[str]]:
    indexed_ids: set[str] = set()
    if index_path.exists():
        for line in index_path.open(encoding="utf-8"):
            if line.strip():
                indexed_ids.add(json.loads(line)["item_id"])

    errors: list[str] = []
    valid: list[dict] = []
    for it in items:
        errs = validate_item(it, known_ids, indexed_ids)
        if errs:
            errors.append(f"{it.get('sigla_id', it.get('item_id', '?'))}: "
                          + "; ".join(errs))
            continue
        it = dict(it)  # nao mutar o input
        it["purificacao_composto"] = round(
            sum(it[ind] for ind in INDICATORS) / len(INDICATORS), 2)
        valid.append(it)
        indexed_ids.add(it["item_id"])

    if valid:
        _atomic_append_lines(
            index_path,
            [json.dumps(v, ensure_ascii=False) for v in valid])
        done_ids = {v["item_id"] for v in valid}
        wl = json.loads(worklist_path.read_text(encoding="utf-8"))
        wl = [{**w, "status": "done"} if w["item_id"] in done_ids else w
              for w in wl]
        worklist_path.write_text(
            json.dumps(wl, ensure_ascii=False, indent=1), encoding="utf-8")
    return len(valid), errors


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("batch_file", type=Path)
    ap.add_argument("--index", type=Path, default=INDEX_PATH)
    ap.add_argument("--worklist", type=Path, default=WORKLIST_PATH)
    args = ap.parse_args()

    items = json.loads(args.batch_file.read_text(encoding="utf-8"))
    known_ids = {json.loads(l)["item_id"]
                 for l in RECORDS_PATH.open(encoding="utf-8") if l.strip()}
    ok, errors = append_batch(items, args.index, args.worklist, known_ids)
    print(f"gravados: {ok}/{len(items)}")
    for e in errors:
        print(f"  REJEITADO {e}")
    raise SystemExit(0 if not errors else 1)


if __name__ == "__main__":
    main()
