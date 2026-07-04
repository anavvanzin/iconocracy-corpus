#!/usr/bin/env python3
"""
records_to_sqlite.py — Parses records.jsonl and purification.jsonl to build
a normalized, high-performance SQLite database representation of the corpus.

Usage:
    python tools/scripts/records_to_sqlite.py
    python tools/scripts/records_to_sqlite.py --output /tmp/corpus.sqlite
"""

import argparse
import json
import re
import sqlite3
import sys
import uuid
from pathlib import Path

# Paths (relative to repo root)
REPO_ROOT = Path(__file__).resolve().parent.parent.parent
RECORDS_FILE = REPO_ROOT / "data" / "processed" / "records.jsonl"
MAPPING_FILE = REPO_ROOT / "data" / "processed" / "id-mapping.json"
CORPUS_JSON = REPO_ROOT / "corpus" / "corpus-data.json"
SQLITE_DB = REPO_ROOT / "data" / "processed" / "corpus.sqlite"

INDICATOR_COLUMNS = (
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
)

DIRECT_ICONOCODE_INSTRUMENTS = frozenset(
    {
        "iconocode-opus",
        "iconocode-opus-4.6-metadata-refined",
        "iconocode-opus-4.6-image",
        "iconocode-sonnet5",
    }
)
CURATORIAL_INSTRUMENTS = frozenset({"ana"})
LEGACY_OR_IMPORTED_INSTRUMENTS = frozenset(
    {"vault-import", "migration", "manual-entry", "hermes-auto"}
)
TENTATIVE_INSTRUMENTS = frozenset({"batch-tentative-2026-04-25"})
# opus-4.8 stays a separate instrument (audit_required) until IRR against the
# IconoCode-direct instruments or an explicit pooling decision.
OPUS48_INSTRUMENTS = frozenset({"opus-4.8"})

INSTRUMENT_FAMILIES = frozenset(
    {
        "uncoded",
        "iconocode_direct",
        "curatorial",
        "legacy_or_imported",
        "tentative",
        "opus48_pending",
        "other",
    }
)
VALIDITY_STRATA = frozenset(
    {
        "S0_UNCODED",
        "S1_ICONOCODE_DIRECT",
        "S2_CURATORIAL",
        "S3_LEGACY_OR_IMPORTED",
        "S4_TENTATIVE",
        "S5_OPUS48_PENDING",
        "S9_OTHER_CODED",
    }
)
QUANTITATIVE_STATUSES = frozenset(
    {"excluded_uncoded", "excluded_scope", "core_candidate", "audit_required"}
)
SCOPE_STATUSES = frozenset({"core_1800_2000", "extended_or_out_of_scope"})


def _nullable_bool(value):
    """Store optional booleans as SQLite-friendly 0/1/NULL values."""
    if value is None:
        return None
    return 1 if bool(value) else 0


def _has_complete_indicators(purification):
    """Return True when all 10 ordinal indicators are present and bounded."""
    return all(
        isinstance(purification.get(col), int) and 0 <= purification[col] <= 3
        for col in INDICATOR_COLUMNS
    )


def _instrument_family(coded_by):
    """Map raw coded_by values into stable method families."""
    if not coded_by:
        return "uncoded"
    if coded_by in DIRECT_ICONOCODE_INSTRUMENTS:
        return "iconocode_direct"
    if coded_by in CURATORIAL_INSTRUMENTS:
        return "curatorial"
    if coded_by in LEGACY_OR_IMPORTED_INSTRUMENTS:
        return "legacy_or_imported"
    if coded_by in TENTATIVE_INSTRUMENTS:
        return "tentative"
    if coded_by in OPUS48_INSTRUMENTS:
        return "opus48_pending"
    return "other"


def classify_record_stratum(record):
    """Classify a canonical record for derived SQL/data-model projections."""
    purif = record.get("purificacao") or {}
    exports = record.get("exports") or {}
    audit_flags = set(exports.get("audit_flags") or [])

    coded_by = (purif.get("coded_by") or "").strip()
    has_coded_by = bool(coded_by)
    has_regime = bool((purif.get("regime_iconocratico") or "").strip())
    has_complete_indicators = _has_complete_indicators(purif)
    family = _instrument_family(coded_by)

    if not has_coded_by or not has_regime or not has_complete_indicators:
        validity_stratum = "S0_UNCODED"
        quantitative_status = "excluded_uncoded"
    elif family == "iconocode_direct":
        validity_stratum = "S1_ICONOCODE_DIRECT"
        quantitative_status = "core_candidate"
    elif family == "curatorial":
        validity_stratum = "S2_CURATORIAL"
        quantitative_status = "audit_required"
    elif family == "legacy_or_imported":
        validity_stratum = "S3_LEGACY_OR_IMPORTED"
        quantitative_status = "audit_required"
    elif family == "tentative":
        validity_stratum = "S4_TENTATIVE"
        quantitative_status = "audit_required"
    elif family == "opus48_pending":
        validity_stratum = "S5_OPUS48_PENDING"
        quantitative_status = "audit_required"
    else:
        validity_stratum = "S9_OTHER_CODED"
        quantitative_status = "audit_required"

    out_of_scope = (
        purif.get("analytic_eligible") is False
        or purif.get("period_extended") is True
        or "fora-do-escopo" in audit_flags
    )
    scope_status = "extended_or_out_of_scope" if out_of_scope else "core_1800_2000"
    if out_of_scope and quantitative_status != "excluded_uncoded":
        quantitative_status = "excluded_scope"

    return {
        "coded_by": coded_by or None,
        "instrument_family": family,
        "validity_stratum": validity_stratum,
        "quantitative_status": quantitative_status,
        "scope_status": scope_status,
        "has_complete_indicators": int(has_complete_indicators),
        "has_regime": int(has_regime),
        "has_coded_by": int(has_coded_by),
        "analytic_eligible": _nullable_bool(purif.get("analytic_eligible")),
        "period_extended": _nullable_bool(purif.get("period_extended")),
        "cohort": purif.get("cohort"),
    }


SCHEMA = [
    # 1. Main items table
    """CREATE TABLE IF NOT EXISTS "items" (
        "item_id" TEXT PRIMARY KEY,
        "corpus_id" TEXT UNIQUE,
        "title" TEXT NOT NULL,
        "country" TEXT,
        "year" INTEGER,
        "period" TEXT,
        "medium_norm" TEXT,
        "created_at" TEXT,
        "updated_at" TEXT
    )""",

    # 2. Purification indicators (1:1 with items)
    """CREATE TABLE IF NOT EXISTS "purification" (
        "item_id" TEXT PRIMARY KEY,
        "desincorporacao" INTEGER CHECK (desincorporacao BETWEEN 0 AND 3),
        "rigidez_postural" INTEGER CHECK (rigidez_postural BETWEEN 0 AND 3),
        "dessexualizacao" INTEGER CHECK (dessexualizacao BETWEEN 0 AND 3),
        "uniformizacao_facial" INTEGER CHECK (uniformizacao_facial BETWEEN 0 AND 3),
        "heraldizacao" INTEGER CHECK (heraldizacao BETWEEN 0 AND 3),
        "enquadramento_arquitetonico" INTEGER CHECK (enquadramento_arquitetonico BETWEEN 0 AND 3),
        "apagamento_narrativo" INTEGER CHECK (apagamento_narrativo BETWEEN 0 AND 3),
        "monocromatizacao" INTEGER CHECK (monocromatizacao BETWEEN 0 AND 3),
        "serialidade" INTEGER CHECK (serialidade BETWEEN 0 AND 3),
        "inscricao_estatal" INTEGER CHECK (inscricao_estatal BETWEEN 0 AND 3),
        "purificacao_composto" REAL,
        "regime_iconocratico" TEXT,
        "coded_by" TEXT,
        "coded_at" TEXT,
        "notes" TEXT,
        FOREIGN KEY("item_id") REFERENCES "items"("item_id") ON DELETE CASCADE
    )""",

    # 3. Webscout evidence (1:N with items)
    """CREATE TABLE IF NOT EXISTS "evidence" (
        "evidence_id" TEXT PRIMARY KEY,
        "item_id" TEXT,
        "source_type" TEXT,
        "title" TEXT,
        "url" TEXT,
        "abnt_citation" TEXT,
        "notes" TEXT,
        FOREIGN KEY("item_id") REFERENCES "items"("item_id") ON DELETE CASCADE
    )""",

    # 4. Iconclass codes associated with items (N:M mapping)
    """CREATE TABLE IF NOT EXISTS "item_iconclass" (
        "item_id" TEXT,
        "notation" TEXT,
        "confidence" REAL,
        PRIMARY KEY ("item_id", "notation"),
        FOREIGN KEY("item_id") REFERENCES "items"("item_id") ON DELETE CASCADE
    )""",

    # 5. Analytic data-model strata (derived from canonical records)
    """CREATE TABLE IF NOT EXISTS "corpus_strata" (
        "item_id" TEXT PRIMARY KEY,
        "corpus_id" TEXT,
        "coded_by" TEXT,
        "instrument_family" TEXT NOT NULL CHECK (instrument_family IN (
            'uncoded', 'iconocode_direct', 'curatorial',
            'legacy_or_imported', 'tentative', 'opus48_pending', 'other'
        )),
        "validity_stratum" TEXT NOT NULL CHECK (validity_stratum IN (
            'S0_UNCODED', 'S1_ICONOCODE_DIRECT', 'S2_CURATORIAL',
            'S3_LEGACY_OR_IMPORTED', 'S4_TENTATIVE', 'S5_OPUS48_PENDING',
            'S9_OTHER_CODED'
        )),
        "quantitative_status" TEXT NOT NULL CHECK (quantitative_status IN (
            'excluded_uncoded', 'excluded_scope', 'core_candidate', 'audit_required'
        )),
        "scope_status" TEXT NOT NULL CHECK (scope_status IN (
            'core_1800_2000', 'extended_or_out_of_scope'
        )),
        "has_complete_indicators" INTEGER NOT NULL CHECK (has_complete_indicators IN (0, 1)),
        "has_regime" INTEGER NOT NULL CHECK (has_regime IN (0, 1)),
        "has_coded_by" INTEGER NOT NULL CHECK (has_coded_by IN (0, 1)),
        "analytic_eligible" INTEGER CHECK (analytic_eligible IN (0, 1)),
        "period_extended" INTEGER CHECK (period_extended IN (0, 1)),
        "cohort" TEXT,
        FOREIGN KEY("item_id") REFERENCES "items"("item_id") ON DELETE CASCADE
    )""",

    # 6. Full-Text Search Virtual Table (FTS5)
    """CREATE VIRTUAL TABLE IF NOT EXISTS "items_fts" USING fts5(
        title, country, period, medium_norm, content="items", content_rowid="rowid"
    )""",

    # 7. Triggers to keep FTS table in sync
    """CREATE TRIGGER IF NOT EXISTS "items_ai" AFTER INSERT ON "items" BEGIN
        INSERT INTO "items_fts"(rowid, title, country, period, medium_norm)
        VALUES (new.rowid, new.title, new.country, new.period, new.medium_norm);
    END""",
    """CREATE TRIGGER IF NOT EXISTS "items_ad" AFTER DELETE ON "items" BEGIN
        INSERT INTO "items_fts"("items_fts", rowid, title, country, period, medium_norm)
        VALUES ('delete', old.rowid, old.title, old.country, old.period, old.medium_norm);
    END""",
    """CREATE TRIGGER IF NOT EXISTS "items_au" AFTER UPDATE ON "items" BEGIN
        INSERT INTO "items_fts"("items_fts", rowid, title, country, period, medium_norm)
        VALUES ('delete', old.rowid, old.title, old.country, old.period, old.medium_norm);
        INSERT INTO "items_fts"(rowid, title, country, period, medium_norm)
        VALUES (new.rowid, new.title, new.country, new.period, new.medium_norm);
    END"""
]

INDEXES = [
    "CREATE INDEX IF NOT EXISTS \"idx_items_corpus_id\" ON \"items\" (\"corpus_id\")",
    "CREATE INDEX IF NOT EXISTS \"idx_purification_regime\" ON \"purification\" (\"regime_iconocratico\")",
    "CREATE INDEX IF NOT EXISTS \"idx_purification_composite\" ON \"purification\" (\"purificacao_composto\")",
    "CREATE INDEX IF NOT EXISTS \"idx_evidence_item\" ON \"evidence\" (\"item_id\")",
    "CREATE INDEX IF NOT EXISTS \"idx_iconclass_item\" ON \"item_iconclass\" (\"item_id\")",
    "CREATE INDEX IF NOT EXISTS \"idx_strata_validity\" ON \"corpus_strata\" (\"validity_stratum\")",
    "CREATE INDEX IF NOT EXISTS \"idx_strata_quantitative\" ON \"corpus_strata\" (\"quantitative_status\")",
    "CREATE INDEX IF NOT EXISTS \"idx_strata_family\" ON \"corpus_strata\" (\"instrument_family\")",
]

def load_mapping():
    """Load UUID mapping to corpus ID."""
    mapping = {}
    if MAPPING_FILE.exists():
        with open(MAPPING_FILE, encoding="utf-8") as f:
            try:
                data = json.load(f)
                corpus_to_items = {}
                for entry in data.get("mapping", []):
                    c_id = entry.get("corpus_id")
                    item_id = entry.get("item_id")
                    if c_id and item_id:
                        corpus_to_items.setdefault(c_id, []).append(item_id)
                
                for entry in data.get("mapping", []):
                    c_id = entry.get("corpus_id")
                    item_id = entry.get("item_id")
                    if c_id and item_id:
                        items_mapped = corpus_to_items[c_id]
                        if len(items_mapped) > 1:
                            ns = uuid.UUID("6ba7b810-9dad-11d1-80b4-00c04fd430c8")
                            expected_uuid = str(uuid.uuid5(ns, f"iconocracy-corpus-{c_id}"))
                            if item_id == expected_uuid:
                                mapping[item_id] = c_id
                        else:
                            mapping[item_id] = c_id
            except Exception as e:
                print(f"Warning: Failed to load id-mapping.json: {e}")
    return mapping

def load_corpus_metadata():
    """Load metadata details from corpus-data.json for richer item fields."""
    metadata = {}
    if CORPUS_JSON.exists():
        with open(CORPUS_JSON, encoding="utf-8") as f:
            try:
                corpus = json.load(f)
                for item in corpus:
                    c_id = item.get("id")
                    if c_id:
                        metadata[c_id] = item
            except Exception as e:
                print(f"Warning: Failed to load corpus-data.json: {e}")
    return metadata

def build_database(sqlite_db=SQLITE_DB):
    print(f"Connecting to SQLite database: {sqlite_db}")
    # Remove existing db to ensure clean import
    sqlite_db.parent.mkdir(parents=True, exist_ok=True)
    if sqlite_db.exists():
        sqlite_db.unlink()
        
    db = sqlite3.connect(str(sqlite_db))
    cursor = db.cursor()
    
    # Enable performance and security PRAGMAs
    cursor.execute("PRAGMA foreign_keys = ON;")
    cursor.execute("PRAGMA journal_mode = WAL;")
    cursor.execute("PRAGMA synchronous = NORMAL;")
    cursor.execute("PRAGMA temp_store = MEMORY;")
    cursor.execute("PRAGMA mmap_size = 30000000000;")
    cursor.execute("PRAGMA page_size = 4096;")
    
    # Create tables
    for ddl in SCHEMA:
        cursor.execute(ddl)
        
    # Load auxiliary data
    uuid_to_corpus = load_mapping()
    corpus_metadata = load_corpus_metadata()
    
    # Process records
    items_count = 0
    purification_count = 0
    evidence_count = 0
    iconclass_count = 0
    
    # Batch arrays
    items_batch = []
    purification_batch = []
    evidence_batch = []
    iconclass_batch = []
    strata_batch = []
    
    seen_evidence = set()
    seen_iconclass = set()
    
    if not RECORDS_FILE.exists():
        print(f"Error: {RECORDS_FILE} not found. Cannot load data.")
        sys.exit(1)
        
    with open(RECORDS_FILE, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
                
            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                continue
                
            item_id = rec.get("item_id")
            if not item_id:
                continue
                
            corpus_id = uuid_to_corpus.get(item_id)
            if not corpus_id or corpus_id.strip() == "":
                corpus_id = None
            meta = corpus_metadata.get(corpus_id, {}) if corpus_id else {}
            
            # 1. Gather for items
            title = meta.get("title") or rec.get("input", {}).get("title_hint") or "Unknown Title"
            country = meta.get("country") or rec.get("input", {}).get("place_hint")
            year = meta.get("year")
            if year is None:
                try:
                    # Fallback parsing for year hint
                    year_hint = rec.get("input", {}).get("date_hint", "")
                    # Extract first 4-digit number
                    year_match = re.search(r'\b\d{4}\b', str(year_hint))
                    year = int(year_match.group(0)) if year_match else None
                except Exception:
                    year = None
                    
            period = meta.get("period") or rec.get("purificacao", {}).get("period")
            medium_norm = (
                meta.get("support")
                or rec.get("purificacao", {}).get("medium_norm")
                or rec.get("purificacao", {}).get("record_metadata", {}).get("medium")
            )
            created_at = rec.get("timestamps", {}).get("created_at")
            updated_at = rec.get("timestamps", {}).get("updated_at")
            
            items_batch.append((item_id, corpus_id, title, country, year, period, medium_norm, created_at, updated_at))
            items_count += 1

            stratum = classify_record_stratum(rec)
            strata_batch.append((
                item_id,
                corpus_id,
                stratum["coded_by"],
                stratum["instrument_family"],
                stratum["validity_stratum"],
                stratum["quantitative_status"],
                stratum["scope_status"],
                stratum["has_complete_indicators"],
                stratum["has_regime"],
                stratum["has_coded_by"],
                stratum["analytic_eligible"],
                stratum["period_extended"],
                stratum["cohort"],
            ))
            
            # 2. Gather for purification
            purif = rec.get("purificacao")
            if purif:
                purification_batch.append((
                    item_id,
                    purif.get("desincorporacao"),
                    purif.get("rigidez_postural"),
                    purif.get("dessexualizacao"),
                    purif.get("uniformizacao_facial"),
                    purif.get("heraldizacao"),
                    purif.get("enquadramento_arquitetonico"),
                    purif.get("apagamento_narrativo"),
                    purif.get("monocromatizacao"),
                    purif.get("serialidade"),
                    purif.get("inscricao_estatal"),
                    purif.get("purificacao_composto"),
                    purif.get("regime_iconocratico"),
                    purif.get("coded_by"),
                    purif.get("coded_at"),
                    purif.get("notes")
                ))
                purification_count += 1
                
            # 3. Gather evidence
            webscout = rec.get("webscout", {})
            for result in webscout.get("search_results", []):
                evidence_id = result.get("evidence_id")
                if not evidence_id or evidence_id in seen_evidence:
                    continue
                seen_evidence.add(evidence_id)
                evidence_batch.append((
                    evidence_id,
                    item_id,
                    result.get("source_type"),
                    result.get("title"),
                    result.get("url"),
                    result.get("abnt_citation"),
                    result.get("notes")
                ))
                evidence_count += 1
                
            # 4. Gather item_iconclass codes
            iconocode = rec.get("iconocode", {})
            for code_entry in iconocode.get("codes", []):
                notation = code_entry.get("notation")
                if not notation or (item_id, notation) in seen_iconclass:
                    continue
                seen_iconclass.add((item_id, notation))
                iconclass_batch.append((
                    item_id,
                    notation,
                    code_entry.get("confidence")
                ))
                iconclass_count += 1

    # Execute batched inserts
    cursor.executemany(
        """INSERT INTO items (item_id, corpus_id, title, country, year, period, medium_norm, created_at, updated_at) 
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        items_batch
    )
    
    cursor.executemany(
        """INSERT INTO purification (
            item_id, desincorporacao, rigidez_postural, dessexualizacao, uniformizacao_facial,
            heraldizacao, enquadramento_arquitetonico, apagamento_narrativo, monocromatizacao,
            serialidade, inscricao_estatal, purificacao_composto, regime_iconocratico,
            coded_by, coded_at, notes
           ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        purification_batch
    )

    cursor.executemany(
        """INSERT INTO evidence (evidence_id, item_id, source_type, title, url, abnt_citation, notes)
           VALUES (?, ?, ?, ?, ?, ?, ?)""",
        evidence_batch
    )

    cursor.executemany(
        """INSERT OR IGNORE INTO item_iconclass (item_id, notation, confidence)
           VALUES (?, ?, ?)""",
        iconclass_batch
    )

    cursor.executemany(
        """INSERT INTO corpus_strata (
            item_id, corpus_id, coded_by, instrument_family, validity_stratum,
            quantitative_status, scope_status, has_complete_indicators,
            has_regime, has_coded_by, analytic_eligible, period_extended, cohort
           ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        strata_batch
    )
                
    # Create indexes
    for idx_ddl in INDEXES:
        cursor.execute(idx_ddl)
        
    # Database Maintenance
    cursor.execute("PRAGMA optimize;")
    db.commit()
    cursor.execute("ANALYZE;")
    cursor.execute("VACUUM;")
    
    db.close()
    
    print("\nImport Complete:")
    print(f"  Items loaded:        {items_count}")
    print(f"  Purification records:{purification_count}")
    print(f"  Evidence sources:    {evidence_count}")
    print(f"  Iconclass mappings:  {iconclass_count}")
    print(f"  Strata rows:         {len(strata_batch)}")
    print(f"Database successfully saved to {sqlite_db}\n")
    
    # Quick verification query
    verify_database(sqlite_db)

def verify_database(sqlite_db=SQLITE_DB):
    db = sqlite3.connect(str(sqlite_db))
    cursor = db.cursor()
    
    print("Verifying database with test query:")
    cursor.execute("""
        SELECT 
            i.country,
            p.regime_iconocratico,
            COUNT(i.item_id) as total_items,
            ROUND(AVG(p.purificacao_composto), 2) as avg_composite
        FROM items i
        JOIN purification p ON i.item_id = p.item_id
        GROUP BY i.country, p.regime_iconocratico
        ORDER BY avg_composite DESC
        LIMIT 5;
    """)
    rows = cursor.fetchall()
    print("  Country    | Regime      | Count | Avg Composite")
    print("  -----------+-------------+-------+--------------")
    for r in rows:
        print(f"  {r[0]:<10} | {str(r[1]).upper():<11} | {r[2]:<5} | {r[3]:.2f}")

    print("\nAnalytic strata summary:")
    cursor.execute("""
        SELECT validity_stratum, quantitative_status, COUNT(*) AS total_items
        FROM corpus_strata
        GROUP BY validity_stratum, quantitative_status
        ORDER BY validity_stratum, quantitative_status;
    """)
    print("  Validity stratum       | Quantitative status | Count")
    print("  -----------------------+---------------------+------")
    for validity, status, count in cursor.fetchall():
        print(f"  {validity:<22} | {status:<19} | {count}")
    db.close()

def main():
    parser = argparse.ArgumentParser(
        description="Build a derived SQLite query/index layer from records.jsonl"
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=SQLITE_DB,
        help=f"SQLite output path (default: {SQLITE_DB})",
    )
    args = parser.parse_args()
    build_database(args.output)


if __name__ == "__main__":
    main()
