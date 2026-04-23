#!/usr/bin/env python3
"""
csv_to_records.py — Migra corpus-data.json + corpus_dataset.csv → data/processed/records.jsonl

Usa corpus/corpus-data.json como fonte primária (mais rico, 139 itens) e
corpus_dataset.csv como fonte de dados de purificação complementares.
Gera records.jsonl conforme master-record.schema.json.

Uso:
    python tools/scripts/csv_to_records.py                        # escreve records.jsonl
    python tools/scripts/csv_to_records.py --dry-run              # preview sem escrever
    python tools/scripts/csv_to_records.py --output path/out.jsonl
    python tools/scripts/csv_to_records.py --item BR-001          # apenas um item
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent
CORPUS_JSON = REPO / "corpus" / "corpus-data.json"
CORPUS_CSV = REPO / "data" / "processed" / "corpus_dataset.csv"
RECORDS_OUT = REPO / "data" / "processed" / "records.jsonl"

# Fixed batch UUID for this migration run (stable / deterministic)
MIGRATION_BATCH_ID = "00000000-1c0c-4842-8a1a-000000000002"
MIGRATION_TS = "2026-04-04T09:47:29Z"

# Namespace for deterministic UUIDs derived from item IDs
_NS = uuid.UUID("6ba7b810-9dad-11d1-80b4-00c04fd430c8")  # uuid.NAMESPACE_URL

# Valid regime values in the schema
VALID_REGIMES = {"fundacional", "normativo", "militar", "contra-alegoria"}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _item_uuid(item_id: str) -> str:
    """Generate a deterministic, stable UUID for a corpus item.

    Uses uuid5 with a fixed namespace so the same item_id always produces
    the same UUID, making migrations idempotent and records de-duplicatable.
    """
    return str(uuid.uuid5(_NS, f"iconocracy-corpus-{item_id}"))


def _item_hash(url: str | None, title: str) -> str:
    src = str(url).strip() if url else title
    return hashlib.sha256(src.encode()).hexdigest()


def _safe_int(val, default: int = 0) -> int:
    try:
        return int(float(str(val)))
    except (TypeError, ValueError):
        return default


def _safe_float(val, default: float = 0.0) -> float:
    try:
        return float(str(val))
    except (TypeError, ValueError):
        return default


def _safe_url(item_id: str, url: str | None) -> str:
    """Return a valid URI, using a placeholder for items without one."""
    if url and str(url).strip().startswith("http"):
        return str(url).strip()
    return f"https://iconocracy.corpus/placeholder/{item_id}"


# ---------------------------------------------------------------------------
# CSV index (purification data from corpus_dataset.csv)
# ---------------------------------------------------------------------------

PURIF_COLS = [
    "desincorporacao", "rigidez_postural", "dessexualizacao",
    "uniformizacao_facial", "heraldizacao", "enquadramento_arquitetonico",
    "apagamento_narrativo", "monocromatizacao", "serialidade", "inscricao_estatal",
]


def load_csv_index() -> dict[str, dict]:
    """Return {item_id: row_dict} from corpus_dataset.csv."""
    index: dict[str, dict] = {}
    if not CORPUS_CSV.exists():
        return index
    with CORPUS_CSV.open(encoding="utf-8") as f:
        for row in csv.DictReader(f):
            index[row["id"]] = row
    return index


# ---------------------------------------------------------------------------
# Field mappers
# ---------------------------------------------------------------------------

def _iconclass_from_panofsky(item: dict) -> list:
    """Extract iconclass codes from panofsky, handling both dict and str variants."""
    panofsky = item.get("panofsky") or {}
    iconographic = panofsky.get("iconographic") or {}
    if isinstance(iconographic, dict):
        return iconographic.get("iconclass") or []
    return []  # iconographic is a plain string — no machine-readable iconclass here


def _build_webscout(item: dict) -> dict:
    url = _safe_url(item["id"], item.get("url") or "")
    abnt = item.get("citation_abnt") or item.get("title", "")
    description = item.get("description") or item.get("title", "")
    panofsky = item.get("panofsky") or {}
    pre_icon_note = panofsky.get("pre_iconographic") or ""

    return {
        "search_results": [
            {
                "evidence_id": "e1",
                "source_type": "primary_image",
                "title": item.get("title", ""),
                "url": url,
                "abnt_citation": abnt,
                "iconclass_candidates": _iconclass_from_panofsky(item),
                "notes": pre_icon_note,
            }
        ],
        "summary_evidence": description,
        "gaps": [],
    }


def _build_iconocode(item: dict) -> dict:
    panofsky = item.get("panofsky") or {}
    iconographic = panofsky.get("iconographic") or {}
    # iconographic may be str or dict
    icon_dict = iconographic if isinstance(iconographic, dict) else {}
    iconological = panofsky.get("iconological") or {}

    # Pre-iconographic: one entry per motif
    motifs = item.get("motif") or []
    pre_iconographic = [{"motif": m, "observed": True} for m in motifs]
    if not pre_iconographic:
        pre_iconographic = [{"motif": "figura feminina alegórica", "observed": True}]

    # Iconclass codes (only when iconographic is a dict)
    codes = []
    for ic_code in (icon_dict.get("iconclass") or []):
        codes.append({
            "scheme": "iconclass",
            "notation": str(ic_code),
            "label": "",
            "code_role": "depicts",
            "confidence": 0.8,
            "evidence_source_id": "e1",
        })

    # Interpretation claims from iconological
    interpretation = []
    regime = iconological.get("regime") or item.get("regime", "")
    if regime:
        interpretation.append({
            "claim_text": f"Regime iconocrático: {regime.upper()}",
            "claim_type": "iconographic",
            "status": "supported",
            "confidence": 0.85,
        })
    funcao = iconological.get("funcao") or ""
    if funcao:
        interpretation.append({
            "claim_text": funcao,
            "claim_type": "legal_context",
            "status": "supported",
            "confidence": 0.75,
        })
    csv_visual = iconological.get("contrato_sexual_visual") or ""
    if csv_visual:
        interpretation.append({
            "claim_text": csv_visual,
            "claim_type": "postcolonial_marker",
            "status": "tentative",
            "confidence": 0.65,
        })
    if not interpretation:
        interpretation = [{
            "claim_text": "Figura feminina alegórica identificada",
            "claim_type": "iconographic",
            "status": "tentative",
            "confidence": 0.5,
        }]

    # Confidence from endurecimento_score (0–3 normalised to 0–1)
    raw_score = _safe_float(item.get("endurecimento_score", 1.5))
    confidence = min(1.0, max(0.0, raw_score / 3.0))

    return {
        "pre_iconographic": pre_iconographic,
        "codes": codes,
        "interpretation": interpretation,
        "validation": {"claim_ledger": []},
        "confidence": round(confidence, 3),
    }


def _build_purificacao(item: dict, csv_row: dict | None) -> dict | None:
    """Build purificacao block from corpus item or CSV row."""
    # Prefer CSV data (has string values), then corpus indicadores dict
    csv_ind: dict = {}
    if csv_row:
        csv_ind = {col: _safe_int(csv_row.get(col, 0)) for col in PURIF_COLS}

    corpus_ind: dict = item.get("indicadores") or {}

    # Merge: CSV wins on numeric purif cols; corpus fills the rest
    ind = {col: csv_ind.get(col, _safe_int(corpus_ind.get(col, 0)))
           for col in PURIF_COLS}

    if all(v == 0 for v in ind.values()) and not corpus_ind and not csv_row:
        return None  # genuinely uncoded

    # regime_iconocratico
    regime_raw = (
        (csv_row.get("regime_iconocratico") if csv_row else None)
        or item.get("regime", "")
        or ""
    ).lower()
    regime = regime_raw if regime_raw in VALID_REGIMES else "normativo"

    # purificacao_composto
    csv_comp = _safe_float(csv_row.get("purificacao_composto", 0)) if csv_row else 0
    corpus_comp = _safe_float(item.get("endurecimento_score", 0))
    composto = csv_comp if csv_comp is not None else corpus_comp

    coded_by = (csv_row.get("coded_by") if csv_row else None) or item.get("coded_by", "migration")
    coded_at = (csv_row.get("coded_at") if csv_row else None) or item.get("coded_at", MIGRATION_TS)

    purif: dict = {col: ind[col] for col in PURIF_COLS}
    purif["purificacao_composto"] = round(composto, 3)
    purif["regime_iconocratico"] = regime
    purif["coded_by"] = coded_by
    purif["coded_at"] = coded_at

    notes = (item.get("panofsky") or {}).get("analyst_notes") or ""
    if notes:
        purif["notes"] = notes

    return purif


def _build_exports(item: dict) -> dict:
    abnt = item.get("citation_abnt") or ""
    flags: list[str] = []
    if not item.get("url"):
        flags.append("sem-url")
    if not item.get("thumbnail_url"):
        flags.append("sem-thumbnail")
    if not item.get("in_scope"):
        flags.append("fora-do-escopo")
    return {
        "abnt_citations": [abnt] if abnt else [],
        "audit_flags": flags,
    }


# ---------------------------------------------------------------------------
# Main converter
# ---------------------------------------------------------------------------

def item_to_record(item: dict, csv_row: dict | None) -> dict:
    item_id_str = item["id"]
    url = item.get("url", "")

    record: dict = {
        "master_record_version": "1.0",
        "batch_id": MIGRATION_BATCH_ID,
        "item_id": _item_uuid(item_id_str),
        "item_hash": _item_hash(url, item.get("title", "")),
        "input": {
            "input_url": _safe_url(item_id_str, url),
            "title_hint": item.get("title", ""),
            "date_hint": str(item.get("date", "")),
            "place_hint": item.get("country", ""),
        },
        "webscout": _build_webscout(item),
        "iconocode": _build_iconocode(item),
        "exports": _build_exports(item),
        "timestamps": {
            "created_at": item.get("coded_at") or MIGRATION_TS,
            "updated_at": MIGRATION_TS,
        },
    }

    purif = _build_purificacao(item, csv_row)
    if purif is not None:
        record["purificacao"] = purif

    return record


def convert(
    output_path: Path = RECORDS_OUT,
    dry_run: bool = False,
    target_id: str | None = None,
) -> int:
    if not CORPUS_JSON.exists():
        print(f"ERRO: corpus-data.json não encontrado: {CORPUS_JSON}", file=sys.stderr)
        return 1

    corpus: list[dict] = json.loads(CORPUS_JSON.read_text(encoding="utf-8"))
    csv_index = load_csv_index()

    if target_id:
        corpus = [c for c in corpus if c["id"] == target_id]
        if not corpus:
            print(f"ERRO: item '{target_id}' não encontrado em corpus-data.json", file=sys.stderr)
            return 1

    records = []
    errors = []
    for item in corpus:
        try:
            csv_row = csv_index.get(item["id"])
            rec = item_to_record(item, csv_row)
            records.append(rec)
        except Exception as exc:
            errors.append(f"  {item['id']}: {exc}")

    if errors:
        print("Erros durante conversão:", file=sys.stderr)
        for e in errors:
            print(e, file=sys.stderr)

    if dry_run:
        print(f"[DRY-RUN] Geraria {len(records)} registros em {output_path}")
        if records:
            print("Amostra (primeiro registro):")
            print(json.dumps(records[0], indent=2, ensure_ascii=False)[:800])
        return 0

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as f:
        for rec in records:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")

    print(f"OK: {len(records)} registros escritos em {output_path}")
    if errors:
        print(f"AVISO: {len(errors)} erros (ver acima)")
        return 1
    return 0


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Migra corpus-data.json + corpus_dataset.csv → records.jsonl"
    )
    parser.add_argument(
        "--output", "-o", type=Path, default=RECORDS_OUT,
        help=f"Arquivo de saída (padrão: {RECORDS_OUT})",
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Preview sem escrever arquivo",
    )
    parser.add_argument(
        "--item", type=str, default=None,
        help="Converter apenas um item por ID (ex: BR-001)",
    )
    args = parser.parse_args()

    sys.exit(convert(args.output, args.dry_run, args.item))


if __name__ == "__main__":
    main()
