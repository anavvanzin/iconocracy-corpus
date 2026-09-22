#!/usr/bin/env python3
"""Build a disposable SQLite projection from the canonical JSONL ledgers.

The database is never authoritative.  Item and evidence metadata comes from
``records.jsonl``; coding observations come from ``purification.jsonl``.
"""

from __future__ import annotations

import json
import re
import sqlite3
import tempfile
import uuid
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
RECORDS_FILE = REPO_ROOT / "data" / "processed" / "records.jsonl"
PURIFICATION_FILE = REPO_ROOT / "data" / "processed" / "purification.jsonl"
MAPPING_FILE = REPO_ROOT / "data" / "processed" / "id-mapping.json"
SQLITE_DB = REPO_ROOT / "data" / "processed" / "corpus.sqlite"

_NS = uuid.UUID("6ba7b810-9dad-11d1-80b4-00c04fd430c8")
INDICATOR_FIELDS = (
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

SCHEMA = (
    """CREATE TABLE items (
        item_id TEXT PRIMARY KEY,
        corpus_id TEXT UNIQUE,
        title TEXT NOT NULL,
        country TEXT,
        year INTEGER,
        period TEXT,
        medium_norm TEXT,
        created_at TEXT,
        updated_at TEXT
    )""",
    """CREATE TABLE purification (
        coding_id TEXT PRIMARY KEY,
        item_id TEXT NOT NULL,
        source_id TEXT NOT NULL,
        desincorporacao INTEGER CHECK (desincorporacao BETWEEN 0 AND 3),
        rigidez_postural INTEGER CHECK (rigidez_postural BETWEEN 0 AND 3),
        dessexualizacao INTEGER CHECK (dessexualizacao BETWEEN 0 AND 3),
        uniformizacao_facial INTEGER CHECK (uniformizacao_facial BETWEEN 0 AND 3),
        heraldizacao INTEGER CHECK (heraldizacao BETWEEN 0 AND 3),
        enquadramento_arquitetonico INTEGER CHECK (enquadramento_arquitetonico BETWEEN 0 AND 3),
        apagamento_narrativo INTEGER CHECK (apagamento_narrativo BETWEEN 0 AND 3),
        monocromatizacao INTEGER CHECK (monocromatizacao BETWEEN 0 AND 3),
        serialidade INTEGER CHECK (serialidade BETWEEN 0 AND 3),
        inscricao_estatal INTEGER CHECK (inscricao_estatal BETWEEN 0 AND 3),
        purificacao_composto REAL,
        regime_iconocratico TEXT,
        coded_by TEXT NOT NULL,
        coded_at TEXT NOT NULL,
        coding_round INTEGER NOT NULL DEFAULT 1,
        prompt_version TEXT,
        adjudication_status TEXT,
        notes TEXT,
        FOREIGN KEY(item_id) REFERENCES items(item_id) ON DELETE CASCADE
    )""",
    """CREATE TABLE evidence (
        item_id TEXT NOT NULL,
        evidence_id TEXT NOT NULL,
        source_type TEXT,
        title TEXT,
        url TEXT,
        abnt_citation TEXT,
        notes TEXT,
        PRIMARY KEY(item_id, evidence_id),
        FOREIGN KEY(item_id) REFERENCES items(item_id) ON DELETE CASCADE
    )""",
    """CREATE TABLE item_iconclass (
        item_id TEXT NOT NULL,
        notation TEXT NOT NULL,
        confidence REAL,
        PRIMARY KEY(item_id, notation),
        FOREIGN KEY(item_id) REFERENCES items(item_id) ON DELETE CASCADE
    )""",
    """CREATE VIRTUAL TABLE items_fts USING fts5(
        title, country, period, medium_norm, content='items', content_rowid='rowid'
    )""",
    """CREATE TRIGGER items_ai AFTER INSERT ON items BEGIN
        INSERT INTO items_fts(rowid, title, country, period, medium_norm)
        VALUES (new.rowid, new.title, new.country, new.period, new.medium_norm);
    END""",
    """CREATE TRIGGER items_ad AFTER DELETE ON items BEGIN
        INSERT INTO items_fts(items_fts, rowid, title, country, period, medium_norm)
        VALUES ('delete', old.rowid, old.title, old.country, old.period, old.medium_norm);
    END""",
    """CREATE TRIGGER items_au AFTER UPDATE ON items BEGIN
        INSERT INTO items_fts(items_fts, rowid, title, country, period, medium_norm)
        VALUES ('delete', old.rowid, old.title, old.country, old.period, old.medium_norm);
        INSERT INTO items_fts(rowid, title, country, period, medium_norm)
        VALUES (new.rowid, new.title, new.country, new.period, new.medium_norm);
    END""",
)

INDEXES = (
    "CREATE INDEX idx_items_corpus_id ON items(corpus_id)",
    "CREATE INDEX idx_purification_item ON purification(item_id)",
    "CREATE INDEX idx_purification_regime ON purification(regime_iconocratico)",
    "CREATE INDEX idx_purification_coder ON purification(coded_by)",
    "CREATE INDEX idx_evidence_item ON evidence(item_id)",
    "CREATE INDEX idx_iconclass_item ON item_iconclass(item_id)",
)


def _load_jsonl(path: Path) -> list[dict]:
    rows: list[dict] = []
    with path.open(encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, 1):
            if not line.strip():
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError as error:
                raise ValueError(f"Invalid JSON in {path}:{line_number}: {error}") from error
    return rows


def _load_mapping(path: Path) -> tuple[dict[str, str], dict[str, str]]:
    if not path.exists():
        return {}, {}
    payload = json.loads(path.read_text(encoding="utf-8"))
    grouped: dict[str, list[str]] = {}
    for entry in payload.get("mapping", []):
        corpus_id = entry.get("corpus_id")
        item_id = entry.get("item_id")
        if corpus_id and item_id:
            grouped.setdefault(corpus_id, []).append(item_id)

    corpus_to_item: dict[str, str] = {}
    item_to_corpus: dict[str, str] = {}
    for corpus_id, item_ids in grouped.items():
        deterministic = _deterministic_item_id(corpus_id)
        if deterministic in item_ids:
            chosen = deterministic
        elif len(item_ids) == 1:
            chosen = item_ids[0]
        else:
            # An ambiguous historical crosswalk must not assign the same
            # public identity to multiple canonical records.
            continue
        corpus_to_item[corpus_id] = chosen
        item_to_corpus[chosen] = corpus_id
    return corpus_to_item, item_to_corpus


def _deterministic_item_id(corpus_id: str) -> str:
    return str(uuid.uuid5(_NS, f"iconocracy-corpus-{corpus_id}"))


def _resolve_item_id(source_id: str, corpus_to_item: dict[str, str], known: set[str]) -> str:
    candidate = corpus_to_item.get(source_id, source_id)
    if candidate in known:
        return candidate
    deterministic = _deterministic_item_id(source_id)
    if deterministic in known:
        return deterministic
    raise ValueError(f"Coding row {source_id!r} has no matching canonical record")


def _year(value: object) -> int | None:
    match = re.search(r"\b(1[0-9]{3}|20[0-9]{2})\b", str(value or ""))
    return int(match.group(1)) if match else None


def _place(value: object) -> str | None:
    if isinstance(value, list):
        return str(value[0]) if value else None
    if value is None:
        return None
    normalized = str(value).strip()
    return normalized or None


def _coding_id(row: dict, item_id: str) -> str:
    identity = "|".join(
        str(row.get(field, ""))
        for field in ("id", "coded_by", "coded_at", "coding_round", "prompt_version")
    )
    return str(uuid.uuid5(_NS, f"iconocracy-coding-{item_id}-{identity}"))


def build_database(
    *,
    records_file: Path = RECORDS_FILE,
    purification_file: Path = PURIFICATION_FILE,
    mapping_file: Path = MAPPING_FILE,
    sqlite_db: Path = SQLITE_DB,
    verify: bool = True,
) -> dict[str, int]:
    """Rebuild *sqlite_db* atomically and return projected row counts."""
    records = _load_jsonl(records_file)
    codings = _load_jsonl(purification_file)
    corpus_to_item, item_to_corpus = _load_mapping(mapping_file)
    known_item_ids = {row["item_id"] for row in records}

    sqlite_db.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        dir=sqlite_db.parent, prefix=f".{sqlite_db.name}.", suffix=".tmp", delete=False
    ) as temporary:
        temporary_path = Path(temporary.name)

    stats = {"items": 0, "purification": 0, "evidence": 0, "iconclass": 0}
    try:
        with sqlite3.connect(temporary_path) as db:
            db.execute("PRAGMA foreign_keys = ON")
            # This is a one-shot atomic rebuild in a temporary file. DELETE
            # mode avoids WAL sidecars; FULL sync protects the committed file
            # before its final atomic replacement.
            db.execute("PRAGMA journal_mode = DELETE")
            db.execute("PRAGMA synchronous = FULL")
            db.execute("PRAGMA temp_store = MEMORY")
            for statement in SCHEMA:
                db.execute(statement)

            items: list[tuple] = []
            evidence: list[tuple] = []
            iconclass: list[tuple] = []
            seen_evidence: set[tuple[str, str]] = set()
            seen_iconclass: set[tuple[str, str]] = set()

            for record in records:
                item_id = record["item_id"]
                input_data = record.get("input") or {}
                embedded = record.get("purificacao") or {}
                metadata = embedded.get("record_metadata") or {}
                items.append(
                    (
                        item_id,
                        item_to_corpus.get(item_id),
                        input_data.get("title_hint") or "Unknown Title",
                        _place(input_data.get("place_hint")),
                        _year(input_data.get("date_hint")),
                        embedded.get("period"),
                        embedded.get("medium_norm") or metadata.get("medium"),
                        (record.get("timestamps") or {}).get("created_at"),
                        (record.get("timestamps") or {}).get("updated_at"),
                    )
                )

                for result in (record.get("webscout") or {}).get("search_results", []):
                    evidence_id = result.get("evidence_id")
                    key = (item_id, evidence_id)
                    if not evidence_id or key in seen_evidence:
                        continue
                    seen_evidence.add(key)
                    evidence.append(
                        (
                            item_id,
                            evidence_id,
                            result.get("source_type"),
                            result.get("title"),
                            result.get("url"),
                            result.get("abnt_citation"),
                            result.get("notes"),
                        )
                    )

                for code in (record.get("iconocode") or {}).get("codes", []):
                    notation = code.get("notation")
                    key = (item_id, notation)
                    if not notation or key in seen_iconclass:
                        continue
                    seen_iconclass.add(key)
                    iconclass.append((item_id, notation, code.get("confidence")))

            db.executemany(
                "INSERT INTO items VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", items
            )
            db.executemany(
                "INSERT INTO evidence VALUES (?, ?, ?, ?, ?, ?, ?)", evidence
            )
            db.executemany(
                "INSERT INTO item_iconclass VALUES (?, ?, ?)", iconclass
            )

            coding_rows: list[tuple] = []
            for coding in codings:
                source_id = coding["id"]
                item_id = _resolve_item_id(source_id, corpus_to_item, known_item_ids)
                coding_rows.append(
                    (
                        _coding_id(coding, item_id),
                        item_id,
                        source_id,
                        *(coding.get(field) for field in INDICATOR_FIELDS),
                        coding.get("purificacao_composto"),
                        coding.get("regime_iconocratico"),
                        coding.get("coded_by") or "unknown",
                        coding.get("coded_at") or "unknown",
                        coding.get("coding_round") or 1,
                        coding.get("prompt_version"),
                        coding.get("adjudication_status"),
                        coding.get("notes"),
                    )
                )

            placeholders = ", ".join("?" for _ in range(21))
            db.executemany(
                f"INSERT INTO purification VALUES ({placeholders})", coding_rows
            )
            for statement in INDEXES:
                db.execute(statement)

            foreign_key_errors = db.execute("PRAGMA foreign_key_check").fetchall()
            if foreign_key_errors:
                raise ValueError(f"SQLite foreign-key violations: {foreign_key_errors[:5]}")
            db.execute("INSERT INTO items_fts(items_fts) VALUES ('rebuild')")
            db.execute("ANALYZE")

            stats = {
                "items": len(items),
                "purification": len(coding_rows),
                "evidence": len(evidence),
                "iconclass": len(iconclass),
            }

        temporary_path.replace(sqlite_db)
    except Exception:
        temporary_path.unlink(missing_ok=True)
        raise

    if verify:
        verify_database(sqlite_db)
    return stats


def verify_database(sqlite_db: Path = SQLITE_DB) -> None:
    with sqlite3.connect(sqlite_db) as db:
        violations = db.execute("PRAGMA foreign_key_check").fetchall()
        if violations:
            raise ValueError(f"SQLite foreign-key violations: {violations[:5]}")
        counts = {
            table: db.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
            for table in ("items", "purification", "evidence", "item_iconclass")
        }
    print("SQLite projection verified:")
    for table, count in counts.items():
        print(f"  {table}: {count}")


def main() -> None:
    stats = build_database()
    print(f"SQLite projection written to: {SQLITE_DB}")
    print("Counts: " + ", ".join(f"{key}={value}" for key, value in stats.items()))


if __name__ == "__main__":
    main()
