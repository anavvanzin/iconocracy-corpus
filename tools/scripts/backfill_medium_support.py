#!/usr/bin/env python3
"""
backfill_medium_support.py — Repovoa purificacao.record_metadata.medium no ledger

Contexto: ``records_to_corpus.py`` trata ``purificacao.record_metadata.medium``
como a única fonte canônica do campo ``support`` do export (corpus-data.json).
Até 2026-07, porém, só 15/328 registros de records.jsonl carregavam esse campo,
então a regeneração do export derrubava ``support`` em 313 itens e o gate de
idempotência (check_corpus_export_idempotent.py, job Validate Schemas) falhava
na main desde 2026-07-24.

Este script copia o ``support`` atual de corpus-data.json para o ledger — uma
única vez, de forma idempotente — usando o mesmo alinhamento do export
(id-mapping.json → uuid5(item_id) → casamento por URL). Valores são copiados
como estão (inclui '?' e texto livre); a normalização de vocabulário é tarefa
de ``normalize_supports.py``, não deste backfill.

Registros que já possuem record_metadata.medium NÃO são alterados.

Uso:
    python tools/scripts/backfill_medium_support.py --dry-run   # preview
    python tools/scripts/backfill_medium_support.py             # escreve
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from tools.scripts.csv_to_records import _atomic_write_jsonl, _item_uuid

RECORDS = REPO / "data" / "processed" / "records.jsonl"
CORPUS = REPO / "corpus" / "corpus-data.json"
ID_MAPPING = REPO / "data" / "processed" / "id-mapping.json"


def _load_id_mapping() -> dict[str, str]:
    """corpus_id -> item_id, igual ao export."""
    if not ID_MAPPING.exists():
        return {}
    data = json.loads(ID_MAPPING.read_text(encoding="utf-8"))
    return {
        e["corpus_id"]: e["item_id"]
        for e in data.get("mapping", [])
        if e.get("corpus_id") and e.get("item_id")
    }


def _record_url(rec: dict) -> str:
    return (
        rec.get("webscout", {}).get("search_results", [{}])[0].get("url")
        or rec.get("input", {}).get("input_url", "")
    )


def build_support_lookup(records: list[dict]) -> dict[str, str]:
    """Map record item_id -> support, seguindo o alinhamento do export."""
    id_mapping = _load_id_mapping()
    records_by_item_id = {r["item_id"]: r for r in records if r.get("item_id")}
    records_by_url = {_record_url(r): r for r in records if _record_url(r)}

    items = json.loads(CORPUS.read_text(encoding="utf-8"))
    lookup: dict[str, str] = {}
    for item in items:
        corpus_id = item.get("id")
        support = item.get("support")
        if not corpus_id or not (isinstance(support, str) and support.strip()):
            continue
        # O corpus_id pode ser o próprio item_id do record (exports antigos),
        # um id mapeado em id-mapping.json, ou derivável via uuid5.
        rec = (
            records_by_item_id.get(corpus_id)
            or records_by_item_id.get(id_mapping.get(corpus_id) or _item_uuid(corpus_id))
        )
        if rec is None:
            rec = records_by_url.get(item.get("url", ""))
        if rec is not None and rec.get("item_id"):
            lookup[rec["item_id"]] = support.strip()
    return lookup


def backfill(records: list[dict], lookup: dict[str, str]) -> tuple[list[dict], int]:
    """Retorna (records, n_alterados). Preserva record_metadata existente."""
    changed = 0
    for rec in records:
        support = lookup.get(rec.get("item_id", ""))
        if not support:
            continue
        purif = rec.get("purificacao")
        if not isinstance(purif, dict):
            continue
        rm = purif.setdefault("record_metadata", {})
        if not (isinstance(rm.get("medium"), str) and rm["medium"].strip()):
            rm["medium"] = support
            changed += 1
    return records, changed


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true", help="preview sem escrever")
    args = parser.parse_args()

    records = [json.loads(line) for line in RECORDS.read_text(encoding="utf-8").splitlines() if line.strip()]
    lookup = build_support_lookup(records)
    records, changed = backfill(records, lookup)

    print(f"records: {len(records)} | supports mapeados do export: {len(lookup)} | backfilled: {changed}")
    if args.dry_run:
        print("dry-run: nada escrito")
        return 0
    if changed:
        _atomic_write_jsonl(RECORDS, records)
        print(f"escrito: {RECORDS}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
