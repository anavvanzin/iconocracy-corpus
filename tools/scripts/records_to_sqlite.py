#!/usr/bin/env python3
"""
records_to_sqlite.py — Parses records.jsonl and purification.jsonl to build
a normalized, high-performance SQLite database representation of the corpus.

Usage:
    python tools/scripts/records_to_sqlite.py
"""

import json
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
]

INDEXES = [
    "CREATE INDEX IF NOT EXISTS \"idx_items_corpus_id\" ON \"items\" (\"corpus_id\")",
    "CREATE INDEX IF NOT EXISTS \"idx_purification_regime\" ON \"purification\" (\"regime_iconocratico\")",
    "CREATE INDEX IF NOT EXISTS \"idx_purification_composite\" ON \"purification\" (\"purificacao_composto\")",
    "CREATE INDEX IF NOT EXISTS \"idx_evidence_item\" ON \"evidence\" (\"item_id\")",
    "CREATE INDEX IF NOT EXISTS \"idx_iconclass_item\" ON \"item_iconclass\" (\"item_id\")",
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

def build_database():
    print(f"Connecting to SQLite database: {SQLITE_DB}")
    # Remove existing db to ensure clean import
    if SQLITE_DB.exists():
        SQLITE_DB.unlink()
        
    db = sqlite3.connect(str(SQLITE_DB))
    cursor = db.cursor()
    
    # Enable foreign keys
    cursor.execute("PRAGMA foreign_keys = ON;")
    
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
            
            # 1. Insert into items
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
            medium_norm = meta.get("medium_norm") or rec.get("purificacao", {}).get("medium_norm")
            created_at = rec.get("timestamps", {}).get("created_at")
            updated_at = rec.get("timestamps", {}).get("updated_at")
            
            cursor.execute(
                """INSERT INTO items (item_id, corpus_id, title, country, year, period, medium_norm, created_at, updated_at) 
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (item_id, corpus_id, title, country, year, period, medium_norm, created_at, updated_at)
            )
            items_count += 1
            
            # 2. Insert into purification
            purif = rec.get("purificacao")
            if purif:
                cursor.execute(
                    """INSERT INTO purification (
                        item_id, desincorporacao, rigidez_postural, dessexualizacao, uniformizacao_facial,
                        heraldizacao, enquadramento_arquitetonico, apagamento_narrativo, monocromatizacao,
                        serialidade, inscricao_estatal, purificacao_composto, regime_iconocratico,
                        coded_by, coded_at, notes
                       ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    (
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
                    )
                )
                purification_count += 1
                
            # 3. Insert evidence
            webscout = rec.get("webscout", {})
            for result in webscout.get("search_results", []):
                evidence_id = result.get("evidence_id")
                if not evidence_id:
                    continue
                # Make sure evidence_id is unique
                cursor.execute("SELECT 1 FROM evidence WHERE evidence_id = ?", (evidence_id,))
                if cursor.fetchone():
                    continue
                cursor.execute(
                    """INSERT INTO evidence (evidence_id, item_id, source_type, title, url, abnt_citation, notes)
                       VALUES (?, ?, ?, ?, ?, ?, ?)""",
                    (
                        evidence_id,
                        item_id,
                        result.get("source_type"),
                        result.get("title"),
                        result.get("url"),
                        result.get("abnt_citation"),
                        result.get("notes")
                    )
                )
                evidence_count += 1
                
            # 4. Insert item_iconclass codes
            iconocode = rec.get("iconocode", {})
            for code_entry in iconocode.get("codes", []):
                notation = code_entry.get("notation")
                if not notation:
                    continue
                cursor.execute(
                    """INSERT OR IGNORE INTO item_iconclass (item_id, notation, confidence)
                       VALUES (?, ?, ?)""",
                    (
                        item_id,
                        notation,
                        code_entry.get("confidence")
                    )
                )
                iconclass_count += 1
                
    # Create indexes
    for idx_ddl in INDEXES:
        cursor.execute(idx_ddl)
        
    db.commit()
    db.close()
    
    print("\nImport Complete:")
    print(f"  Items loaded:        {items_count}")
    print(f"  Purification records:{purification_count}")
    print(f"  Evidence sources:    {evidence_count}")
    print(f"  Iconclass mappings:  {iconclass_count}")
    print(f"Database successfully saved to {SQLITE_DB}\n")
    
    # Quick verification query
    verify_database()

def verify_database():
    db = sqlite3.connect(str(SQLITE_DB))
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
    db.close()

if __name__ == "__main__":
    import re  # needed for year regex fallback
    build_database()
