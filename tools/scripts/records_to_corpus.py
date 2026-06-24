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
import tempfile
import uuid
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent
RECORDS = REPO / "data" / "processed" / "records.jsonl"
CORPUS_OUT = REPO / "corpus" / "corpus-data.json"

# Stable namespace shared with csv_to_records.py for corpus-id -> UUID5 mapping.
_NS = uuid.UUID("6ba7b810-9dad-11d1-80b4-00c04fd430c8")

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


def _item_uuid(corpus_id: str) -> str:
    """Reconstruct the deterministic item UUID used by csv_to_records.py."""
    return str(uuid.uuid5(_NS, f"iconocracy-corpus-{corpus_id}"))


def _atomic_write_json(path: Path, payload: list[dict]) -> None:
    """Atomically write JSON to disk to avoid half-written corpus files."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        "w", encoding="utf-8", dir=path.parent, delete=False, suffix=".tmp"
    ) as tmp:
        tmp.write(json.dumps(payload, indent=2, ensure_ascii=False) + "\n")
        tmp_path = Path(tmp.name)
    tmp_path.replace(path)


def _record_diff_key(record: dict) -> str:
    """Normalize diff comparison keys so placeholders align with empty-URL corpus items."""
    sr = record.get("webscout", {}).get("search_results", [{}])
    url = sr[0].get("url", "") if sr else ""
    item_id = record.get("item_id", "(sem-item-id)")
    prefix = "https://iconocracy.corpus/placeholder/"
    if url.startswith(prefix):
        corpus_id = url.removeprefix(prefix)
        return f"(sem URL)::{corpus_id}"
    return url or f"(sem URL)::{item_id}"


def _corpus_diff_key(item_id: str, item: dict) -> str:
    url = item.get("url", "")
    prefix = "https://iconocracy.corpus/placeholder/"
    if url.startswith(prefix):
        corpus_id = url.removeprefix(prefix)
        return f"(sem URL)::{corpus_id}"
    return url or f"(sem URL)::{item_id}"


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


def _corpus_entry_from_record(record: dict, existing: dict | None, corpus_id: str | None = None) -> dict:
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

    # Set ID and Country for new entries
    if not entry.get("id"):
        entry["id"] = corpus_id or record.get("item_id", "")
    
    if not entry.get("country"):
        place_hint = inp.get("place_hint", "")
        if isinstance(place_hint, list) and place_hint:
            place_hint = place_hint[0]
        elif isinstance(place_hint, str):
            place_hint = place_hint.replace("[", "").replace("]", "").replace("'", "").replace('"', "").strip()
        
        country = COUNTRY_MAP_REVERSE.get(place_hint, "")
        if not country:
            if place_hint in ["BR", "Brazil"]:
                country = "Brazil"
            elif place_hint in ["FR", "France"]:
                country = "France"
            elif place_hint in ["US", "United States"]:
                country = "United States"
            elif place_hint in ["UK", "United Kingdom"]:
                country = "United Kingdom"
            elif place_hint in ["DE", "Germany"]:
                country = "Germany"
            elif place_hint in ["BE", "Belgium"]:
                country = "Belgium"
            elif place_hint in ["NL", "Netherlands"]:
                country = "Netherlands"
            elif place_hint in ["PT", "Portugal"]:
                country = "Portugal"
            elif place_hint in ["IT", "Italy"]:
                country = "Italy"
            else:
                country = place_hint or "Brazil"
        entry["country"] = country

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
        "date": inp.get("date_hint") or entry.get("date", ""),
    })

    if indicadores:
        entry["indicadores"] = indicadores

    if abnt and not entry.get("citation_abnt"):
        entry["citation_abnt"] = abnt

    # Tags from exports audit_flags
    if exports.get("audit_flags") and not entry.get("audit_flags"):
        entry["audit_flags"] = exports["audit_flags"]

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
    
    # Load explicit id mapping from id-mapping.json
    id_mapping = {}
    mapping_file = REPO / "data" / "processed" / "id-mapping.json"
    if mapping_file.exists():
        try:
            data = json.loads(mapping_file.read_text(encoding="utf-8"))
            for entry in data.get("mapping", []):
                c_id = entry.get("corpus_id")
                item_id = entry.get("item_id")
                if c_id and item_id:
                    id_mapping[c_id] = item_id
        except Exception as e:
            print(f"AVISO: Falha ao carregar id-mapping.json: {e}", file=sys.stderr)

    # Index records by item_id
    records_by_item_id: dict[str, dict] = {}
    for rec in records:
        rec_item_id = rec.get("item_id", "")
        if rec_item_id:
            records_by_item_id[rec_item_id] = rec

    # Process existing corpus entries
    matched_item_ids: set[str] = set()
    assigned_corpus_ids: set[str] = set()

    if not replace:
        for item_id, item in existing_corpus.items():
            expected_record_item_id = id_mapping.get(item_id) or _item_uuid(item_id)
            rec = records_by_item_id.get(expected_record_item_id)
            if not rec:
                item_url = item.get("url", "")
                if item_url:
                    # Find candidate records matching this URL
                    candidates = [
                        r for r in records
                        if (r.get("webscout", {}).get("search_results", [{}])[0].get("url") or
                            r.get("input", {}).get("input_url", "")) == item_url
                    ]
                    if candidates:
                        if len(candidates) > 1:
                            # Tie-break using title similarity
                            item_title = item.get("title", "").lower()
                            best_candidate = candidates[0]
                            for cand in candidates:
                                cand_title = (cand.get("input", {}).get("title_hint", "") or "").lower()
                                if cand_title == item_title:
                                    best_candidate = cand
                                    break
                            rec = best_candidate
                        else:
                            rec = candidates[0]
            if rec:
                entry = _corpus_entry_from_record(rec, item, corpus_id=item_id)
                matched_item_ids.add(rec.get("item_id", ""))
            else:
                entry = dict(item)
                
            c_id = entry.get("id")
            if c_id:
                assigned_corpus_ids.add(c_id)
            result.append(entry)

    # Add records not matched to existing corpus
    item_to_corpus = {v: k for k, v in id_mapping.items() if v}

    for rec in records:
        rec_item_id = rec.get("item_id", "")
        if rec_item_id in matched_item_ids:
            continue
            
        c_id = item_to_corpus.get(rec_item_id)
        if not c_id:
            for existing_id in existing_corpus.keys():
                if _item_uuid(existing_id) == rec_item_id:
                    c_id = existing_id
                    break
                    
        if c_id in assigned_corpus_ids:
            c_id = None
            
        entry = _corpus_entry_from_record(rec, None, corpus_id=c_id)
        actual_id = entry.get("id")
        if actual_id:
            assigned_corpus_ids.add(actual_id)
            
        if entry.get("title"):
            result.append(entry)

    result.sort(key=lambda item: (str(item.get("id", "")), str(item.get("url", ""))))
    return result


def show_diff(records: list[dict], existing_corpus: dict[str, dict]) -> None:
    """Show a summary of differences between records.jsonl and corpus-data.json."""
    rec_items: dict[str, str] = {}
    for rec in records:
        key = _record_diff_key(rec)
        rec_items[key] = key

    corpus_items = {}
    for item_id, item in existing_corpus.items():
        key = _corpus_diff_key(item_id, item)
        corpus_items[key] = {"id": item_id, "url": item.get("url", "") or "(sem URL)"}

    only_in_records = set(rec_items.keys()) - set(corpus_items.keys())
    only_in_corpus = set(corpus_items.keys()) - set(rec_items.keys())

    print(f"records.jsonl items:   {len(records)}")
    print(f"corpus-data.json items:{len(existing_corpus)}")
    print()

    if only_in_records:
        print(f"Only in records.jsonl ({len(only_in_records)}):")
        for key in sorted(only_in_records)[:10]:
            print(f"  + {rec_items[key][:80]}")
        if len(only_in_records) > 10:
            print(f"  ... and {len(only_in_records) - 10} more")

    if only_in_corpus:
        print(f"\nOnly in corpus-data.json ({len(only_in_corpus)}):")
        for key in sorted(only_in_corpus)[:10]:
            payload = corpus_items[key]
            print(f"  - [{payload['id']}] {payload['url'][:80]}")
        if len(only_in_corpus) > 10:
            print(f"  ... and {len(only_in_corpus) - 10} more")

    if not only_in_records and not only_in_corpus:
        print("Em sincronização (por URL).")


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

    _atomic_write_json(args.output, result)
    print(f"OK: {len(result)} itens escritos em {args.output}")


if __name__ == "__main__":
    main()
