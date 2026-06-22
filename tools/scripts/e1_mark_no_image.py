#!/usr/bin/env python3
"""
e1_mark_no_image.py — Marca itens sem imagem acessível como #no-image no
pathosformel_index.jsonl, completando o DoD E1 (265 linhas).

Lê records.jsonl, identifica itens que ainda não estão no pathosformel_index,
e acrescenta entradas #no-image com indicadores nulos (mesmo formato dos
fora_escopo). Itens já codificados ou fora_escopo não são tocados.

Uso:
    python tools/scripts/e1_mark_no_image.py --dry-run    # lista apenas
    python tools/scripts/e1_mark_no_image.py              # grava
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent
RECORDS_PATH = REPO / "data" / "processed" / "records.jsonl"
CORPUS_PATH = REPO / "corpus" / "corpus-data.json"
OUTPUT_PATH = REPO / "data" / "processed" / "pathosformel_index.jsonl"

INDICATOR_KEYS = [
    "desincorporacao",
    "rigidez_postural",
    "dessexualizacao",
    "uniformizacao_facial",
    "heraldizacao",
    "enquadramento_arquitetonico",
    "apagamento_narrativo",
    "monocromatizacao",
    "serialidade",
    "inscricao_estatal",
]


def load_records() -> list[dict]:
    with open(RECORDS_PATH) as f:
        return [json.loads(l) for l in f if l.strip()]


def load_corpus_url_map() -> dict[str, str]:
    """url -> sigla_id from corpus-data.json."""
    with open(CORPUS_PATH) as f:
        corpus = json.load(f)
    return {c.get("url", ""): c.get("id", "") for c in corpus}


def load_existing_index() -> dict[str, dict]:
    """item_id -> entry from existing pathosformel_index.jsonl."""
    if not OUTPUT_PATH.exists():
        return {}
    items: dict[str, dict] = {}
    with open(OUTPUT_PATH) as f:
        for line in f:
            if not line.strip():
                continue
            try:
                item = json.loads(line)
                items[item["item_id"]] = item
            except (json.JSONDecodeError, KeyError):
                pass
    return items


def resolve_sigla(record: dict, url_map: dict[str, str]) -> str:
    url = record.get("input", {}).get("input_url", "")
    sigla = url_map.get(url, "")
    if not sigla and "placeholder" in url:
        sigla = url.split("/")[-1]
    elif not sigla:
        sigla = record["item_id"][:12]
    return sigla


def build_no_image_entry(record: dict, sigla: str) -> dict:
    inp = record.get("input", {})
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    entry: dict = {
        "item_id": record["item_id"],
        "sigla_id": sigla,
        "title": inp.get("title_hint", "Untitled"),
        "place": inp.get("place_hint", "Unknown"),
        "date": inp.get("date_hint", ""),
        "url": inp.get("input_url", ""),
        "coded_by": "e1-no-image",
        "coded_at": now,
        "coded_from": "no_image",
        "image_source": "none",
        "fora_escopo": False,
        "motivo_exclusao": None,
        "confidence": None,
        "notes": "#no-image — sem fonte de imagem acessível para codificação visual",
        "purificacao_composto": None,
        "regime_iconocratico": None,
    }
    for key in INDICATOR_KEYS:
        entry[key] = None
    return entry


def main() -> int:
    parser = argparse.ArgumentParser(description="Mark uncoded items as #no-image")
    parser.add_argument("--dry-run", action="store_true", help="List only, don't write")
    args = parser.parse_args()

    records = load_records()
    url_map = load_corpus_url_map()
    existing = load_existing_index()

    missing = [r for r in records if r["item_id"] not in existing]
    print(f"Records: {len(records)} | Already in index: {len(existing)} | Missing: {len(missing)}")

    if not missing:
        print("Nothing to do — all records already in index.")
        return 0

    new_entries: list[dict] = []
    for r in missing:
        sigla = resolve_sigla(r, url_map)
        entry = build_no_image_entry(r, sigla)
        new_entries.append(entry)

    if args.dry_run:
        print(f"\n--- DRY RUN: {len(new_entries)} entries ---")
        for e in new_entries[:10]:
            print(f"  {e['sigla_id']:<15} {e['title'][:50]}")
        if len(new_entries) > 10:
            print(f"  ... and {len(new_entries) - 10} more")
        print(f"\nTotal would be: {len(existing) + len(new_entries)} lines")
        return 0

    # Append to index (sorted by sigla_id for stability)
    all_entries = list(existing.values()) + new_entries
    all_entries.sort(key=lambda x: x.get("sigla_id", ""))

    with open(OUTPUT_PATH, "w") as f:
        for e in all_entries:
            f.write(json.dumps(e, ensure_ascii=False) + "\n")

    print(f"Wrote {len(new_entries)} #no-image entries → {OUTPUT_PATH}")
    print(f"Total index: {len(all_entries)} lines")

    # Summary stats
    coded = sum(1 for e in all_entries if e.get("purificacao_composto") is not None)
    fora = sum(1 for e in all_entries if e.get("fora_escopo"))
    no_img = sum(1 for e in all_entries if e.get("coded_from") == "no_image")
    print(f"\nBreakdown:")
    print(f"  Coded (with score):  {coded}")
    print(f"  Fora escopo:         {fora}")
    print(f"  #no-image:           {no_img}")
    print(f"  Total:               {len(all_entries)}")

    return 0


if __name__ == "__main__":
    sys.exit(main())