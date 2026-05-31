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
ID_MAPPING = REPO / "data" / "processed" / "id-mapping.json"

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

# Fallback country derivation from the corpus_id prefix (e.g. "AT-001" -> "Austria").
# Used only when input.place_hint is missing and no existing entry carries country.
# NOTE: imperfect — a few ids (e.g. DE-prefixed items physically held in IT/CH)
# do not match their country, so place_hint always takes precedence.
COUNTRY_BY_PREFIX: dict[str, str] = {
    "FR": "France",
    "BR": "Brazil",
    "US": "United States",
    "DE": "Germany",
    "UK": "United Kingdom",
    "GB": "United Kingdom",
    "BE": "Belgium",
    "NL": "Netherlands",
    "PT": "Portugal",
    "IT": "Italy",
    "AT": "Austria",
    "ES": "Spain",
    "CH": "Switzerland",
    "UY": "Uruguay",
    "MX": "Mexico",
    "AR": "Argentina",
}


def _item_uuid(corpus_id: str) -> str:
    """Reconstruct the deterministic item UUID used by csv_to_records.py."""
    return str(uuid.uuid5(_NS, f"iconocracy-corpus-{corpus_id}"))


def _country_from_corpus_id(corpus_id: str) -> str:
    """Derive a country name from the leading prefix of a corpus_id (best-effort)."""
    if not corpus_id or "-" not in corpus_id:
        return ""
    return COUNTRY_BY_PREFIX.get(corpus_id.split("-", 1)[0].upper(), "")


def _load_id_mapping() -> dict[str, str]:
    """Return {record item_id -> public corpus_id} from id-mapping.json.

    This is the canonical source of the public ``id`` field that corpus-data.json
    items must carry (issue #56). records.jsonl itself does not store corpus_id.
    """
    if not ID_MAPPING.exists():
        return {}
    try:
        data = json.loads(ID_MAPPING.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return {
        e["item_id"]: e["corpus_id"]
        for e in data.get("mapping", [])
        if e.get("item_id") and e.get("corpus_id")
    }


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


def _corpus_entry_from_record(
    record: dict, existing: dict | None, corpus_id: str = ""
) -> dict:
    """Build a corpus-data.json entry from a master record, merging with existing.

    ``corpus_id`` is the public id resolved from id-mapping.json (issue #56).
    """
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
    if exports.get("audit_flags") and not entry.get("audit_flags"):
        entry["audit_flags"] = exports["audit_flags"]

    # ── Export contract identity/classification fields (issue #56) ──────────
    # These were dropped in a prior regression. records.jsonl does not store
    # them, so they are restored from:
    #   id      -> id-mapping.json (record item_id -> corpus_id)
    #   country -> curated value preserved from the existing entry; derived from
    #              input.place_hint (corpus_id prefix as fallback) only when the
    #              existing entry has none (i.e. the records-only path).
    #   support -> curated; preserved from the existing corpus entry only
    #   year    -> curated; preserved from the existing corpus entry only
    if corpus_id:
        entry["id"] = corpus_id

    # Never overwrite a curated country with a raw place_hint (some hints are
    # malformed, e.g. "['FR']"). Derive only when nothing curated is present.
    if not entry.get("country"):
        place_hint = (inp.get("place_hint") or "").strip()
        country = ""
        if place_hint and place_hint.lower() != "unknown":
            country = COUNTRY_MAP_REVERSE.get(place_hint, place_hint)
        if not country:
            country = _country_from_corpus_id(corpus_id)
        if country:
            entry["country"] = country

    # support/year are curated enrichments held only in corpus-data.json.
    if existing and existing.get("support"):
        entry["support"] = existing["support"]
    if existing and existing.get("year") is not None:
        entry["year"] = existing["year"]

    return entry


def export_corpus(
    records: list[dict],
    existing_corpus: dict[str, dict],
    replace: bool = False,
    id_mapping: dict[str, str] | None = None,
) -> list[dict]:
    """
    Build corpus-data.json list.

    In merge mode (default): existing entries are kept and enriched with
    records data; records without a corpus match are added at the end.
    In replace mode: only records entries are used (may lose rich fields).

    ``id_mapping`` maps record item_id -> public corpus_id and is used to
    restore the export contract ``id`` field (issue #56).
    """
    id_mapping = id_mapping or {}
    result: list[dict] = []

    # Index records by deterministic item_id first (canonical), URL as fallback.
    records_by_item_id: dict[str, dict] = {}
    records_by_url: dict[str, dict] = {}
    for rec in records:
        rec_item_id = rec.get("item_id", "")
        if rec_item_id:
            records_by_item_id[rec_item_id] = rec
        sr = rec.get("webscout", {}).get("search_results", [{}])
        url = sr[0].get("url", "") if sr else ""
        if url:
            records_by_url[url] = rec

    # Process existing corpus entries
    matched_urls: set[str] = set()
    matched_item_ids: set[str] = set()

    if not replace:
        for item_id, item in existing_corpus.items():
            expected_record_item_id = _item_uuid(item_id)
            item_url = item.get("url", "")
            rec = records_by_item_id.get(expected_record_item_id)
            if not rec and item_url:
                rec = records_by_url.get(item_url)
            if rec:
                # Prefer the existing corpus id; fall back to the mapping.
                resolved_id = item_id or id_mapping.get(rec.get("item_id", ""), "")
                entry = _corpus_entry_from_record(rec, item, resolved_id)
                matched_item_ids.add(rec.get("item_id", ""))
                matched_urls.add(item_url)
            else:
                entry = dict(item)
            result.append(entry)

    # Add records not matched to existing corpus
    for rec in records:
        rec_item_id = rec.get("item_id", "")
        sr = rec.get("webscout", {}).get("search_results", [{}])
        url = sr[0].get("url", "") if sr else ""
        if rec_item_id in matched_item_ids or url in matched_urls:
            continue
        if replace or url not in {i.get("url", "") for i in result}:
            resolved_id = id_mapping.get(rec_item_id, "")
            entry = _corpus_entry_from_record(rec, None, resolved_id)
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
    id_mapping = _load_id_mapping()

    if args.diff:
        show_diff(records, existing)
        return

    result = export_corpus(
        records, existing, replace=args.replace, id_mapping=id_mapping
    )

    if args.dry_run:
        print(f"[DRY-RUN] Geraria {len(result)} itens em {args.output}")
        print(f"  Registros de origem: {len(records)}")
        print(f"  Corpus existente: {len(existing)}")
        return

    _atomic_write_json(args.output, result)
    print(f"OK: {len(result)} itens escritos em {args.output}")


if __name__ == "__main__":
    main()
