#!/usr/bin/env python3
# tools/scripts/e1_append_batch.py
"""Validated atomic append of coded E1 batches to pathosformel_index.jsonl.

Input: a JSON file with a LIST of coded RESULTS (one per subagent output).
Each result carries the coding (10 indicators 0-3 + regime) OR a fora_escopo
flag with motivo_exclusao. Identity and metadata (item_id, title, place, date,
url, image_source) are taken from the WORKLIST — the source of truth — not from
the model output, which sometimes hallucinates the long UUID. Results are matched
to the worklist by item_id, falling back to sigla_id.

Strategy B (fora_escopo): items the coder judged out of scope (e.g. a male
effigy) are kept in the index with fora_escopo=True + motivo_exclusao, their 10
indicators / regime / composto set to null, and excluded from the analytic N.

Computes purificacao_composto for in-scope items. Rejects invalid items whole
(no partial rows). Marks corresponding worklist entries as done.

Usage:
    python tools/scripts/e1_append_batch.py batch_NN_results.json
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


def resolve_worklist_entry(result: dict, by_item: dict[str, dict],
                           by_sigla: dict[str, dict]) -> dict | None:
    """Match a coded result to its authoritative worklist entry.

    Prefer the item_id; fall back to sigla_id, because subagents sometimes
    hallucinate the long UUID but get the short catalog sigla right.
    """
    iid = result.get("item_id")
    if iid in by_item:
        return by_item[iid]
    sig = result.get("sigla_id")
    if sig in by_sigla:
        return by_sigla[sig]
    return None


def build_row(result: dict, wl_entry: dict) -> dict:
    """Compose an index row: identity+metadata from the worklist (authoritative),
    coding from the result. fora_escopo rows get nulled indicators/regime/composto.
    """
    row = {
        "item_id": wl_entry["item_id"],
        "sigla_id": wl_entry.get("sigla_id") or result.get("sigla_id"),
        "title": wl_entry.get("title", ""),
        "place": wl_entry.get("place", ""),
        "date": wl_entry.get("date", ""),
        "url": wl_entry.get("url", ""),
        "coded_by": result.get("coded_by"),
        "coded_at": result.get("coded_at"),
        "coded_from": result.get("coded_from"),
        "image_source": wl_entry.get("image_source") or result.get("image_source"),
        "fora_escopo": bool(result.get("fora_escopo", False)),
        "motivo_exclusao": result.get("motivo_exclusao"),
        "confidence": result.get("confidence"),
        "notes": result.get("notes"),
    }
    if row["fora_escopo"]:
        for ind in INDICATORS:
            row[ind] = None
        row["regime_iconocratico"] = None
        row["purificacao_composto"] = None
    else:
        for ind in INDICATORS:
            row[ind] = result.get(ind)
        row["regime_iconocratico"] = result.get("regime_iconocratico")
        # purificacao_composto computed after validation, in append_batch
    return row


def validate_item(row: dict, known_ids: set[str],
                  indexed_ids: set[str]) -> list[str]:
    """Validate a composed index row (post worklist-enrichment)."""
    errs: list[str] = []
    if not row.get("item_id"):
        errs.append("item_id ausente")
    if not row.get("sigla_id"):
        errs.append("sigla_id ausente")
    for f in ("coded_by", "coded_at", "coded_from"):
        if not row.get(f):
            errs.append(f"campo ausente: {f}")

    if row.get("fora_escopo"):
        if not row.get("motivo_exclusao"):
            errs.append("fora_escopo=True exige motivo_exclusao")
        # indicators / regime intentionally null — not validated
    else:
        for ind in INDICATORS:
            v = row.get(ind)
            if isinstance(v, bool) or not isinstance(v, int) or not 0 <= v <= 3:
                errs.append(f"{ind}={v!r} fora de 0-3")
        if row.get("regime_iconocratico") not in REGIMES:
            errs.append(f"regime invalido: {row.get('regime_iconocratico')!r}")

    if row.get("item_id") not in known_ids:
        errs.append(f"item_id {row.get('item_id')!r} nao existe em records.jsonl")
    if row.get("item_id") in indexed_ids:
        errs.append(f"item_id {row.get('item_id')!r} duplicado no index")
    return errs


def _atomic_append_lines(path: Path, lines: list[str]) -> None:
    # Read-then-rewrite proposital: open("a") nao e atomico em crash;
    # para o tamanho deste index (<10k linhas) o full-read e aceitavel.
    existing = path.read_text(encoding="utf-8") if path.exists() else ""
    fd, tmp = tempfile.mkstemp(dir=str(path.parent), suffix=".tmp")
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        f.write(existing)
        for line in lines:
            f.write(line + "\n")
    os.replace(tmp, path)


def append_batch(results: list[dict], index_path: Path, worklist_path: Path,
                 known_ids: set[str]) -> tuple[int, list[str]]:
    indexed_ids: set[str] = set()
    if index_path.exists():
        for line in index_path.open(encoding="utf-8"):
            if line.strip():
                indexed_ids.add(json.loads(line)["item_id"])

    wl = json.loads(worklist_path.read_text(encoding="utf-8"))
    by_item = {w["item_id"]: w for w in wl}
    by_sigla = {w["sigla_id"]: w for w in wl if w.get("sigla_id")}

    errors: list[str] = []
    valid_rows: list[dict] = []
    for res in results:
        entry = resolve_worklist_entry(res, by_item, by_sigla)
        if entry is None:
            label = res.get("sigla_id") or res.get("item_id", "?")
            errors.append(f"{label}: nao corresponde a nenhuma entrada da worklist")
            continue
        row = build_row(res, entry)
        errs = validate_item(row, known_ids, indexed_ids)
        if errs:
            errors.append(f"{row.get('sigla_id', '?')}: " + "; ".join(errs))
            continue
        if not row["fora_escopo"]:
            row["purificacao_composto"] = round(
                sum(row[ind] for ind in INDICATORS) / len(INDICATORS), 2)
        valid_rows.append(row)
        indexed_ids.add(row["item_id"])

    if valid_rows:
        _atomic_append_lines(
            index_path,
            [json.dumps(r, ensure_ascii=False) for r in valid_rows])
        done_ids = {r["item_id"] for r in valid_rows}
        wl = [{**w, "status": "done"} if w["item_id"] in done_ids else w
              for w in wl]
        worklist_path.write_text(
            json.dumps(wl, ensure_ascii=False, indent=1), encoding="utf-8")
    return len(valid_rows), errors


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("batch_file", type=Path)
    ap.add_argument("--index", type=Path, default=INDEX_PATH)
    ap.add_argument("--worklist", type=Path, default=WORKLIST_PATH)
    args = ap.parse_args()

    results = json.loads(args.batch_file.read_text(encoding="utf-8"))
    known_ids = {json.loads(line)["item_id"]
                 for line in RECORDS_PATH.open(encoding="utf-8") if line.strip()}
    ok, errors = append_batch(results, args.index, args.worklist, known_ids)
    print(f"gravados: {ok}/{len(results)}")
    for e in errors:
        print(f"  REJEITADO {e}")
    raise SystemExit(0 if not errors else 1)


if __name__ == "__main__":
    main()
