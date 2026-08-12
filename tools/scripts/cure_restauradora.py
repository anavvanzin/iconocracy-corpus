#!/usr/bin/env python3
"""
cure_restauradora.py — Auto-cures the 41 records missing purificacao and exorcises the fake twins.

Part of Card #1 (A Restauradora) for July 2026.
1. Cures the 41 records in records.jsonl that are missing their purificacao block.
2. Appends corresponding entries to purification.jsonl.
3. Exorcises duplicate item_hashes by regenerating them uniquely using both URL and Title.
"""

import json
import hashlib
import sys
from datetime import datetime, timezone
from pathlib import Path
from collections import Counter

# Paths
REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(REPO_ROOT / "tools" / "scripts"))

try:
    from auto_code_purification import infer_scores, infer_regime, COUNTRY_CODES
except ImportError:
    print("ERRO: Não foi possível importar auto_code_purification. Certifique-se de executar no diretório correto.")
    sys.exit(1)

CORPUS_JSON = REPO_ROOT / "corpus" / "corpus-data.json"
PURIFICATION_JSONL = REPO_ROOT / "data" / "processed" / "purification.jsonl"
RECORDS_JSONL = REPO_ROOT / "data" / "processed" / "records.jsonl"


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_jsonl(path):
    items = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                items.append(json.loads(line))
    return items


def write_jsonl(path, items):
    with open(path, "w", encoding="utf-8") as f:
        for item in items:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")


def main():
    print("=" * 60)
    print("  EXECUTANDO: A Restauradora 🃏")
    print("=" * 60)

    # 1. Load data
    corpus = load_json(CORPUS_JSON)
    records = load_jsonl(RECORDS_JSONL)
    purification_entries = load_jsonl(PURIFICATION_JSONL)

    print(f"Carregados: {len(corpus)} itens do corpus, {len(records)} registros, {len(purification_entries)} códigos de purificação.")

    # 2. Build URL and Title lookups for Corpus items
    url_to_corpus = {}
    title_to_corpus = {}
    for item in corpus:
        url = item.get("url", "")
        if url:
            url_to_corpus[url] = item
        title = item.get("title", "")
        if title:
            title_to_corpus[title] = item

    # 3. Detect duplicate item_hashes (Fake Twins)
    item_hashes = [r.get("item_hash") for r in records if r.get("item_hash")]
    dup_hashes = {k: v for k, v in Counter(item_hashes).items() if v > 1}
    print(f"\nDetectados {len(dup_hashes)} hashes duplicados (gêmeos falsos):")
    for h, count in dup_hashes.items():
        print(f"  Hash: {h} (duplicado {count} vezes)")

    # Exorcise fake twins in records
    exorcised_count = 0
    for record in records:
        h = record.get("item_hash")
        if h in dup_hashes:
            url = record.get("input", {}).get("input_url", "")
            title = record.get("input", {}).get("title_hint", "")
            src = f"{url}||{title}"
            new_hash = hashlib.sha256(src.encode()).hexdigest()[:16]
            record["item_hash"] = new_hash
            exorcised_count += 1
            print(f"  -> Exorcizado item '{title[:30]}...': {h} -> {new_hash}")

    print(f"Total de registros exorcizados: {exorcised_count}")

    # 4. Cure 41 records missing purificacao
    cured_count = 0
    new_purification_entries = []

    for idx, record in enumerate(records):
        if "purificacao" not in record:
            url = record.get("input", {}).get("input_url", "")
            title_hint = record.get("input", {}).get("title_hint", "")

            # Match with corpus item
            corpus_item = url_to_corpus.get(url)
            if not corpus_item:
                corpus_item = title_to_corpus.get(title_hint)

            if not corpus_item:
                print(f"  [AVISO] Não foi possível parear o registro '{title_hint[:30]}...' ({url})")
                continue

            sigla_id = corpus_item.get("id")
            if not sigla_id:
                print(f"  [AVISO] Corpus item para '{title_hint[:30]}...' não possui um ID válido.")
                continue

            # Infer scores & regime using auto_code_purification logic
            scores = infer_scores(corpus_item, record)
            regime = infer_regime(corpus_item, record)
            composite = round(sum(scores.values()) / len(scores), 2)

            now_iso = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

            # Build purificacao block for record
            record["purificacao"] = {
                "desincorporacao": scores["desincorporacao"],
                "rigidez_postural": scores["rigidez_postural"],
                "dessexualizacao": scores["dessexualizacao"],
                "uniformizacao_facial": scores["uniformizacao_facial"],
                "heraldizacao": scores["heraldizacao"],
                "enquadramento_arquitetonico": scores["enquadramento_arquitetonico"],
                "apagamento_narrativo": scores["apagamento_narrativo"],
                "monocromatizacao": scores["monocromatizacao"],
                "serialidade": scores["serialidade"],
                "inscricao_estatal": scores["inscricao_estatal"],
                "purificacao_composto": composite,
                "regime_iconocratico": regime,
                "coded_by": "hermes-auto",
                "coded_at": now_iso,
            }

            # Build purification.jsonl entry
            pur_entry = {
                "id": sigla_id,
                "title": corpus_item.get("title", ""),
                "country": corpus_item.get("country", ""),
                "year": corpus_item.get("year"),
                "period": corpus_item.get("period"),
                "medium_norm": corpus_item.get("medium_norm"),
                **scores,
                "purificacao_composto": composite,
                "regime_iconocratico": regime,
                "coded_by": "hermes-auto",
                "coded_at": now_iso,
                "notes": "Auto-coded — cured during A Restauradora card",
            }

            new_purification_entries.append(pur_entry)
            cured_count += 1
            print(f"  [{cured_count:2d}/41] Curado ID {sigla_id:<8} composto={composite:.2f} regime={regime:<12} | {title_hint[:40]}...")

    # 5. Write changes back to files
    if cured_count > 0 or exorcised_count > 0:
        # Write records.jsonl
        write_jsonl(RECORDS_JSONL, records)
        print(f"\n  ✅ Escritos {len(records)} registros atualizados em {RECORDS_JSONL}")

        # Append new entries to purification.jsonl
        with open(PURIFICATION_JSONL, "a", encoding="utf-8") as f:
            for entry in new_purification_entries:
                f.write(json.dumps(entry, ensure_ascii=False) + "\n")
        print(f"  ✅ Adicionados {len(new_purification_entries)} códigos em {PURIFICATION_JSONL}")

    print("\n" + "=" * 60)
    print(f"  SUCESSO: {cured_count} registros curados, {exorcised_count} gêmeos exorcizados!")
    print("=" * 60)


if __name__ == "__main__":
    main()
