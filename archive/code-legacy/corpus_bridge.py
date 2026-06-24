#!/usr/bin/env python3
"""
corpus_bridge.py — Bridge ingest master CSV → corpus-data.json.

Creates skeleton corpus items from ingested files, assigns IDs following
the {COUNTRY}-{NNN} pattern, and merges them into corpus-data.json
without duplicating existing items.

Mapping logic:
  - source_institution → country code → corpus ID prefix
  - year_detected → year field
  - renamed_filename → title (humanized)
  - detected_language, OCR metadata → preserved as ingest_metadata
  - Analysis fields (indicadores, panofsky) left empty for IconoCode

Usage:
    python -m modules.corpus_bridge                           # dry run
    python -m modules.corpus_bridge --write                   # write to corpus
    python -m modules.corpus_bridge --csv output/custom.csv   # custom CSV path
"""

from __future__ import annotations

import csv
import json
import logging
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

logger = logging.getLogger("corpus-bridge")

# ── Paths ───────────────────────────────────────────────────────────────────
INGEST_DIR = Path(__file__).resolve().parent.parent
REPO_ROOT = INGEST_DIR.parent
CORPUS_JSON = REPO_ROOT / "corpus" / "corpus-data.json"
DEFAULT_CSV = INGEST_DIR / "output" / "iconocracy_master.csv"

# ── Institution → Country mapping ───────────────────────────────────────────
# Maps ingest source codes to corpus country prefixes (ISO 2-letter).
INSTITUTION_TO_COUNTRY = {
    "BND": "BR",
    "CAM": "BR",
    "SEN": "BR",
    "GAL": "FR",
    "BNF": "FR",
    "BL": "UK",
    "BM": "UK",
    "LOC": "US",
    "BSB": "DE",
    "DDB": "DE",
    "KBR": "BE",
    "EUR": "EU",
    "NUM": "EU",
    "COL": "EU",
    "IA": "US",    # Internet Archive — default to US; override manually if needed
}

# Country prefix → full name (Portuguese)
COUNTRY_NAMES_PT = {
    "BR": "Brasil",
    "FR": "França",
    "UK": "Reino Unido",
    "US": "Estados Unidos",
    "DE": "Alemanha",
    "BE": "Bélgica",
    "EU": "Europa",
    "IT": "Itália",
    "ES": "Espanha",
    "PT": "Portugal",
    "NL": "Países Baixos",
    "AT": "Áustria",
    "AR": "Argentina",
    "MX": "México",
    "UY": "Uruguai",
}

COUNTRY_NAMES_EN = {
    "BR": "Brazil",
    "FR": "France",
    "UK": "United Kingdom",
    "US": "United States",
    "DE": "Germany",
    "BE": "Belgium",
    "EU": "Europe",
    "IT": "Italy",
    "ES": "Spain",
    "PT": "Portugal",
    "NL": "Netherlands",
    "AT": "Austria",
    "AR": "Argentina",
    "MX": "Mexico",
    "UY": "Uruguay",
}

# Institution code → full institution name
INSTITUTION_NAMES = {
    "BND": "Biblioteca Nacional Digital",
    "CAM": "Câmara dos Deputados",
    "SEN": "Senado Federal",
    "GAL": "Gallica / BnF",
    "BNF": "Bibliothèque nationale de France",
    "BL": "British Library",
    "BM": "British Museum",
    "LOC": "Library of Congress",
    "BSB": "Bayerische Staatsbibliothek",
    "DDB": "Deutsche Digitale Bibliothek",
    "KBR": "KBR — Bibliothèque royale de Belgique",
    "EUR": "Europeana",
    "NUM": "Numista",
    "COL": "Colnect",
    "IA": "Internet Archive",
}

# Language code → detected_language display
LANG_NAMES = {
    "pt": "Portuguese",
    "es": "Spanish",
    "fr": "French",
    "it": "Italian",
    "en": "English",
    "de": "German",
    "la": "Latin",
}

# Empty analysis template
EMPTY_INDICADORES = {
    "desincorporacao": 0,
    "rigidez_postural": 0,
    "dessexualizacao": 0,
    "uniformizacao_facial": 0,
    "heraldizacao": 0,
    "enquadramento_arquitetonico": 0,
    "apagamento_narrativo": 0,
    "monocromatizacao": 0,
    "serialidade": 0,
    "inscricao_estatal": 0,
}

EMPTY_PANOFSKY = {
    "pre_iconographic": "",
    "iconographic": {
        "motivo_alegorico": "",
        "iconclass": [],
        "tradicao": "",
        "pathosformel": "",
    },
    "iconological": {
        "regime": "",
        "funcao": "",
        "contrato_sexual_visual": "",
        "colonialidade_do_ver": "",
    },
    "analyst_notes": "Awaiting IconoCode analysis",
}


def load_corpus() -> list[dict]:
    """Load existing corpus-data.json."""
    if CORPUS_JSON.exists():
        return json.loads(CORPUS_JSON.read_text(encoding="utf-8"))
    return []


def get_existing_ids(corpus: list[dict]) -> set[str]:
    """Return set of existing corpus IDs."""
    return {item["id"] for item in corpus}


def get_existing_hashes(corpus: list[dict]) -> set[str]:
    """Return set of file_id hashes already in corpus (via ingest_metadata)."""
    hashes = set()
    for item in corpus:
        meta = item.get("ingest_metadata", {})
        if "file_id" in meta:
            hashes.add(meta["file_id"])
    return hashes


def next_id_for_country(country: str, existing_ids: set[str]) -> str:
    """Generate the next available ID for a country prefix (e.g., BR-012)."""
    max_num = 0
    prefix = f"{country}-"
    for cid in existing_ids:
        if cid.startswith(prefix):
            try:
                num = int(cid[len(prefix):])
                max_num = max(max_num, num)
            except ValueError:
                pass
    return f"{country}-{max_num + 1:03d}"


def humanize_filename(renamed: str) -> str:
    """Convert a renamed filename to a human-readable title."""
    # Strip extension
    stem = Path(renamed).stem
    # Remove the SOURCE_YEAR_SEQ_ prefix
    parts = stem.split("_", 3)
    if len(parts) >= 4:
        title_part = parts[3]
    else:
        title_part = stem
    # Convert hyphens to spaces, title case
    title = title_part.replace("-", " ").strip()
    return title.title() if title else renamed


def csv_row_to_corpus_item(
    row: dict,
    corpus_id: str,
    country: str,
) -> dict:
    """Convert a single CSV row to a corpus-data.json skeleton item."""
    institution_code = row.get("source_institution", "UNKNOWN")
    year_str = row.get("year_detected", "")
    year = int(year_str) if year_str and year_str.isdigit() else None

    return {
        "id": corpus_id,
        "title": humanize_filename(row.get("renamed_filename", row.get("original_filename", ""))),
        "date": year_str or "",
        "period": "",
        "creator": "",
        "institution": INSTITUTION_NAMES.get(institution_code, institution_code),
        "source_archive": INSTITUTION_NAMES.get(institution_code, ""),
        "country": COUNTRY_NAMES_EN.get(country, country),
        "medium": "",
        "motif": [],
        "description": "",
        "url": "",
        "thumbnail_url": "",
        "rights": "",
        "citation_abnt": "",
        "citation_chicago": "",
        "tags": [],
        "year": year,
        "medium_norm": "",
        "country_pt": COUNTRY_NAMES_PT.get(country, country),
        "period_norm": "",
        "motif_str": "",
        "tags_str": "",
        "regime": "",
        "endurecimento_score": 0.0,
        "indicadores": dict(EMPTY_INDICADORES),
        "coded_by": "",
        "coded_at": "",
        "support": "",
        "in_scope": True,
        "scope_note": "Imported from ingest pipeline — awaiting review",
        "panofsky": json.loads(json.dumps(EMPTY_PANOFSKY)),  # deep copy
        # Ingest-specific metadata preserved for traceability
        "ingest_metadata": {
            "file_id": row.get("file_id", ""),
            "original_filename": row.get("original_filename", ""),
            "renamed_filename": row.get("renamed_filename", ""),
            "detected_language": row.get("detected_language", ""),
            "ocr_language_used": row.get("ocr_language_used", ""),
            "total_pages": int(row["total_pages"]) if row.get("total_pages") else 0,
            "mean_confidence": float(row["mean_confidence"]) if row.get("mean_confidence") else 0.0,
            "min_confidence": float(row["min_confidence"]) if row.get("min_confidence") else 0.0,
            "low_conf_pages": row.get("low_conf_pages", ""),
            "caption_count": int(row["caption_count"]) if row.get("caption_count") else 0,
            "has_figures": row.get("has_figures", "") == "True",
            "ingestion_timestamp": row.get("ingestion_timestamp", ""),
            "input_folder": row.get("input_folder", ""),
            "notes": row.get("notes", ""),
        },
    }


def load_csv(csv_path: Path) -> list[dict]:
    """Load the ingest master CSV."""
    if not csv_path.exists():
        logger.error("CSV not found: %s", csv_path)
        return []
    with open(csv_path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def bridge(
    csv_path: Optional[Path] = None,
    write: bool = False,
    country_override: Optional[str] = None,
) -> list[dict]:
    """
    Main bridge function: read CSV, create skeleton items, merge into corpus.

    Args:
        csv_path: Path to master CSV (default: output/iconocracy_master.csv)
        write: If True, write updated corpus-data.json
        country_override: Force all items to this country prefix (e.g., "FR")

    Returns:
        List of new items created.
    """
    csv_path = csv_path or DEFAULT_CSV
    rows = load_csv(csv_path)
    if not rows:
        logger.warning("No rows in CSV.")
        return []

    corpus = load_corpus()
    existing_ids = get_existing_ids(corpus)
    existing_hashes = get_existing_hashes(corpus)

    new_items = []
    for row in rows:
        file_id = row.get("file_id", "")

        # Skip if already bridged
        if file_id in existing_hashes:
            logger.debug("Skipping already-bridged: %s", row.get("original_filename"))
            continue

        # Determine country
        institution = row.get("source_institution", "UNKNOWN")
        country = country_override or INSTITUTION_TO_COUNTRY.get(institution, "EU")

        # Generate ID
        corpus_id = next_id_for_country(country, existing_ids)
        existing_ids.add(corpus_id)

        # Create item
        item = csv_row_to_corpus_item(row, corpus_id, country)
        new_items.append(item)

        logger.info(
            "  %s  ←  %s  [%s, %s]",
            corpus_id,
            row.get("original_filename", "?"),
            institution,
            row.get("year_detected", "????"),
        )

    if not new_items:
        logger.info("No new items to bridge. Corpus is up to date.")
        return []

    logger.info("%d new items to add to corpus.", len(new_items))

    if write:
        corpus.extend(new_items)
        CORPUS_JSON.write_text(
            json.dumps(corpus, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        logger.info("Wrote %d items to %s (total: %d)", len(new_items), CORPUS_JSON, len(corpus))
    else:
        logger.info("Dry run — no changes written. Use --write to persist.")

    return new_items


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Bridge ingest master CSV → corpus-data.json",
    )
    parser.add_argument(
        "--csv",
        type=Path,
        default=None,
        help=f"Path to master CSV (default: {DEFAULT_CSV})",
    )
    parser.add_argument(
        "--write",
        action="store_true",
        help="Write changes to corpus-data.json (default: dry run)",
    )
    parser.add_argument(
        "--country",
        type=str,
        default=None,
        help="Override country prefix for all items (e.g., FR, BR)",
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable debug logging.",
    )

    args = parser.parse_args()

    level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%H:%M:%S",
    )

    new_items = bridge(
        csv_path=args.csv,
        write=args.write,
        country_override=args.country,
    )

    if new_items:
        print(f"\n{'=' * 60}")
        print(f"  CORPUS BRIDGE — {'Written' if args.write else 'Dry Run'}")
        print(f"{'=' * 60}")
        print(f"  New items:  {len(new_items)}")
        for item in new_items:
            meta = item.get("ingest_metadata", {})
            print(f"    {item['id']}  {item['title'][:50]}")
            print(f"           {item['institution']} | {item['date']} | conf={meta.get('mean_confidence', 0)}")
        print(f"{'=' * 60}\n")


if __name__ == "__main__":
    main()
