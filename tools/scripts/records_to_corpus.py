#!/usr/bin/env python3
"""
records_to_corpus.py — Exporta data/processed/records.jsonl → corpus/corpus-data.json

Reconstrói corpus-data.json a partir do arquivo canônico records.jsonl.
Para campos enriquecidos (panofsky, indicadores) que existem no corpus-data.json
mas não são cobertos pelo schema master-record, mantém os dados do arquivo
existente como fallback (modo --merge, padrão).

Uso:
    python tools/scripts/records_to_corpus.py              # merge com corpus existente
    python tools/scripts/records_to_corpus.py --replace    # substitui completamente
    python tools/scripts/records_to_corpus.py --dry-run    # preview sem escrever
    python tools/scripts/records_to_corpus.py --diff       # mostra diferenças
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict, deque
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent
RECORDS = REPO / "data" / "processed" / "records.jsonl"
CORPUS_OUT = REPO / "corpus" / "corpus-data.json"
PLACEHOLDER_PREFIX = "https://iconocracy.corpus/placeholder/"

# Map master-record country strings (from input.place_hint) back to corpus names
COUNTRY_MAP_REVERSE: dict[str, str] = {
    "France": "France",
    "Brazil": "Brazil",
    "United States": "United States",
    "Germany": "Germany",
    "United Kingdom": "United Kingdom",
    "Belgium": "Belgium",
    "Netherlands": "Netherlands",
    "Portugal": "Portugal",
    "Italy": "Italy",
    "Austria": "Austria",
    "Spain": "Spain",
    "Switzerland": "Switzerland",
    "Uruguay": "Uruguay",
    "Mexico": "Mexico",
    "Argentina": "Argentina",
}


def _load_records() -> list[dict]:
    if not RECORDS.exists():
        print(f"ERRO: records.jsonl não encontrado: {RECORDS}", file=sys.stderr)
        sys.exit(1)
    records = []
    with RECORDS.open(encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError as e:
                print(f"AVISO: linha {line_num} JSON inválido: {e}", file=sys.stderr)
    return records


def _load_existing_corpus() -> dict[str, dict]:
    """Return {item_id: corpus_entry} for existing corpus-data.json."""
    if not CORPUS_OUT.exists():
        return {}
    try:
        items = json.loads(CORPUS_OUT.read_text(encoding="utf-8"))
        return {item["id"]: item for item in items if "id" in item}
    except Exception:
        return {}


def _match_key(url: str | None, fallback_id: str = "") -> str:
    text = str(url or "")
    if text.startswith(PLACEHOLDER_PREFIX):
        return f"(sem URL)::{text.removeprefix(PLACEHOLDER_PREFIX)}"
    return text or f"(sem URL)::{fallback_id}"


def _display_url(url: str | None) -> str:
    text = str(url or "")
    return "(sem URL)" if text.startswith(PLACEHOLDER_PREFIX) else (text or "(sem URL)")


def _record_match_url(rec: dict) -> str:
    sr = rec.get("webscout", {}).get("search_results", [{}])
    url = sr[0].get("url", "") if sr else ""
    input_url = rec.get("input", {}).get("input_url", "")
    return url or input_url


def _duplicate_keys_from_values(values: list[str]) -> dict[str, int]:
    counts = Counter(v for v in values if v)
    return {k: v for k, v in counts.items() if v > 1}


def _corpus_entry_from_record(record: dict, existing: dict | None) -> dict:
    """Build a corpus-data.json entry from a master record, merging with existing."""
    inp = record.get("input", {})
    webscout = record.get("webscout", {})
    iconocode = record.get("iconocode", {})
    purif = record.get("purificacao") or {}
    exports = record.get("exports", {})

    # Primary result
    sr = webscout.get("search_results", [{}])[0] if webscout.get("search_results") else {}
    url = sr.get("url") or inp.get("input_url", "")
    abnt = sr.get("abnt_citation") or (exports.get("abnt_citations") or [""])[0]
    title = inp.get("title_hint") or sr.get("title") or ""
    description = webscout.get("summary_evidence") or ""
    iconclass = sr.get("iconclass_candidates") or []

    # Motifs from pre_iconographic
    motifs = [
        m["motif"]
        for m in iconocode.get("pre_iconographic", [])
        if m.get("observed", True)
    ]

    # Regime from purification block or interpretation
    regime = purif.get("regime_iconocratico", "")
    if not regime:
        for claim in iconocode.get("interpretation", []):
            ct = claim.get("claim_text", "")
            if ct.startswith("Regime iconocrático:"):
                regime = ct.split(":", 1)[1].strip().lower()
                break

    # Indicadores dict from purificacao
    indicator_cols = [
        "desincorporacao", "rigidez_postural", "dessexualizacao",
        "uniformizacao_facial", "heraldizacao", "enquadramento_arquitetonico",
        "apagamento_narrativo", "monocromatizacao", "serialidade", "inscricao_estatal",
    ]
    indicadores = {col: purif[col] for col in indicator_cols if col in purif} or None

    coded_by = purif.get("coded_by") or ""
    coded_at = purif.get("coded_at") or record.get("timestamps", {}).get("updated_at", "")
    endurecimento = purif.get("purificacao_composto") or 0.0

    # Start from existing entry for rich fields (panofsky, institution, etc.)
    entry: dict = dict(existing) if existing else {}

    # Overwrite with authoritative fields from records.jsonl
    entry.update({
        "url": url if url and not url.startswith("https://iconocracy.corpus/placeholder/") else entry.get("url", url),
        "title": title or entry.get("title", ""),
        "description": description or entry.get("description", ""),
        "motif": motifs or entry.get("motif", []),
        "regime": regime or entry.get("regime", ""),
        "endurecimento_score": endurecimento or entry.get("endurecimento_score", 0.0),
        "coded_by": coded_by or entry.get("coded_by", ""),
        "coded_at": coded_at or entry.get("coded_at", ""),
    })

    if indicadores:
        entry["indicadores"] = indicadores

    if abnt and not entry.get("citation_abnt"):
        entry["citation_abnt"] = abnt

    # Tags from exports audit_flags
    audit_flags = exports.get("audit_flags") or []
    if audit_flags and not entry.get("audit_flags"):
        entry["audit_flags"] = audit_flags

    if not entry.get("id"):
        source_note_flag = next((flag for flag in audit_flags if isinstance(flag, str) and flag.startswith("source-note-id:")), "")
        if source_note_flag:
            entry["id"] = source_note_flag.split(":", 1)[1].strip()

    return entry


def export_corpus(
    records: list[dict],
    existing_corpus: dict[str, dict],
    replace: bool = False,
) -> list[dict]:
    """
    Build corpus-data.json list.

    In merge mode (default): existing entries are kept and enriched with
    records data; records without a corpus match are added at the end.
    In replace mode: only records entries are used (may lose rich fields).
    """
    result: list[dict] = []

    # Index records by URL or placeholder-derived corpus id for matching.
    # Use queues to preserve multiplicity instead of silently overwriting duplicates.
    records_by_key: dict[str, deque[dict]] = defaultdict(deque)
    for rec in records:
        match_key = _match_key(_record_match_url(rec))
        if match_key:
            records_by_key[match_key].append(rec)

    # Process existing corpus entries
    matched_record_ids: set[str] = set()

    if not replace:
        for item_id, item in existing_corpus.items():
            item_url = item.get("url", "")
            item_key = _match_key(item_url, item_id)
            rec_queue = records_by_key.get(item_key)
            rec = None
            if rec_queue:
                while rec_queue and rec_queue[0].get("item_id") in matched_record_ids:
                    rec_queue.popleft()
                if rec_queue:
                    rec = rec_queue.popleft()
            if rec:
                entry = _corpus_entry_from_record(rec, item)
                matched_record_ids.add(rec.get("item_id", ""))
            else:
                entry = dict(item)
            result.append(entry)

    # Add records not matched to existing corpus
    existing_keys = [_match_key(i.get("url", ""), i.get("id", "")) for i in result]
    existing_key_counts = Counter(existing_keys)
    for rec in records:
        rec_item_id = rec.get("item_id", "")
        match_key = _match_key(_record_match_url(rec))
        if rec_item_id in matched_record_ids:
            continue
        current_count = sum(1 for r in result if _match_key(r.get("url", ""), r.get("id", "")) == match_key)
        target_count = existing_key_counts.get(match_key, 0)
        if not replace and current_count < target_count:
            continue
        entry = _corpus_entry_from_record(rec, None)
        if entry.get("title"):
            result.append(entry)
            matched_record_ids.add(rec_item_id)

    return result


def show_diff(records: list[dict], existing_corpus: dict[str, dict]) -> None:
    """Show a summary of differences between records.jsonl and corpus-data.json."""
    rec_items: dict[str, list[str]] = defaultdict(list)
    rec_keys_raw: list[str] = []
    for rec in records:
        match_url = _record_match_url(rec)
        key = _match_key(match_url)
        rec_items[key].append(_display_url(match_url))
        rec_keys_raw.append(key)

    corpus_items: dict[str, list[dict]] = defaultdict(list)
    corpus_keys_raw: list[str] = []
    for item_id, item in existing_corpus.items():
        url = item.get("url", "")
        key = _match_key(url, item_id)
        corpus_items[key].append({"id": item_id, "url": _display_url(url)})
        corpus_keys_raw.append(key)

    only_in_records = set(rec_items.keys()) - set(corpus_items.keys())
    only_in_corpus = set(corpus_items.keys()) - set(rec_items.keys())
    duplicate_record_keys = _duplicate_keys_from_values(rec_keys_raw)
    duplicate_corpus_keys = _duplicate_keys_from_values(corpus_keys_raw)

    print(f"records.jsonl items:   {len(records)}")
    print(f"corpus-data.json items:{len(existing_corpus)}")
    print()

    if duplicate_record_keys:
        print(f"AVISO: chaves duplicadas em records.jsonl ({len(duplicate_record_keys)}):")
        for key, count in sorted(duplicate_record_keys.items())[:10]:
            print(f"  ! {count}x {_display_url(key)}")
        if len(duplicate_record_keys) > 10:
            print(f"  ... and {len(duplicate_record_keys) - 10} more")
        print()

    if duplicate_corpus_keys:
        print(f"AVISO: chaves duplicadas em corpus-data.json ({len(duplicate_corpus_keys)}):")
        for key, count in sorted(duplicate_corpus_keys.items())[:10]:
            print(f"  ! {count}x {_display_url(key)}")
        if len(duplicate_corpus_keys) > 10:
            print(f"  ... and {len(duplicate_corpus_keys) - 10} more")
        print()

    if only_in_records:
        print(f"Only in records.jsonl ({len(only_in_records)}):")
        for key in sorted(only_in_records)[:10]:
            print(f"  + {rec_items[key][0][:80]}")
        if len(only_in_records) > 10:
            print(f"  ... and {len(only_in_records) - 10} more")

    if only_in_corpus:
        print(f"\nOnly in corpus-data.json ({len(only_in_corpus)}):")
        for key in sorted(only_in_corpus)[:10]:
            payload = corpus_items[key][0]
            print(f"  - [{payload['id']}] {payload['url'][:80]}")
        if len(only_in_corpus) > 10:
            print(f"  ... and {len(only_in_corpus) - 10} more")

    if not only_in_records and not only_in_corpus:
        print("Em sincronização (por URL/chave de correspondência).")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Exporta records.jsonl → corpus-data.json"
    )
    parser.add_argument(
        "--output", "-o", type=Path, default=CORPUS_OUT,
        help=f"Arquivo de saída (padrão: {CORPUS_OUT})",
    )
    parser.add_argument(
        "--replace", action="store_true",
        help="Substituir completamente (não fazer merge com corpus existente)",
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Preview sem escrever arquivo",
    )
    parser.add_argument(
        "--diff", action="store_true",
        help="Mostrar diferenças entre records.jsonl e corpus-data.json",
    )
    args = parser.parse_args()

    records = _load_records()
    existing = _load_existing_corpus()

    if args.diff:
        show_diff(records, existing)
        return

    result = export_corpus(records, existing, replace=args.replace)

    if args.dry_run:
        print(f"[DRY-RUN] Geraria {len(result)} itens em {args.output}")
        print(f"  Registros de origem: {len(records)}")
        print(f"  Corpus existente: {len(existing)}")
        return

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(result, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"OK: {len(result)} itens escritos em {args.output}")


if __name__ == "__main__":
    main()
