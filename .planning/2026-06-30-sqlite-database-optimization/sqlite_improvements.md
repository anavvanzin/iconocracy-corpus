# SQLite Database Improvement Proposals

Based on the `SQLite Database Expert` guidelines, here are the recommendations for improving the Iconocracy SQLite database (`corpus.sqlite`) and its ingestion pipeline (`records_to_sqlite.py`).

## 1. Full-Text Search (FTS5) Integration

Currently, there is no optimized text search capability for item titles or evidence notes. Implementing an FTS5 virtual table will drastically speed up keyword searches, which is highly recommended for embedded desktop databases.

**Proposed Schema Addition:**
```sql
CREATE VIRTUAL TABLE IF NOT EXISTS items_fts USING fts5(
    title, period, country, medium_norm, content=items, content_rowid=rowid
);

-- Triggers to keep FTS table in sync
CREATE TRIGGER items_ai AFTER INSERT ON items BEGIN
    INSERT INTO items_fts(rowid, title, period, country, medium_norm)
    VALUES (new.rowid, new.title, new.period, new.country, new.medium_norm);
END;
-- (Similar triggers for UPDATE and DELETE would be added)
```

## 2. Performance & Reliability PRAGMAs

The current script only enables `PRAGMA foreign_keys = ON;`. We should add the recommended performance PRAGMAs to optimize for read-heavy operations and concurrent access.

**Proposed Initialization PRAGMAs:**
```sql
PRAGMA journal_mode = WAL;         -- Better concurrency and write performance
PRAGMA synchronous = NORMAL;       -- Safe in WAL mode, much faster than FULL
PRAGMA temp_store = MEMORY;        -- Store temporary tables/indexes in memory
PRAGMA mmap_size = 30000000000;    -- Memory mapping for faster reads
PRAGMA page_size = 4096;           -- Standard page size alignment
```

## 3. Python Ingestion Optimization (Batching)

`tools/scripts/records_to_sqlite.py` currently executes individual `INSERT` statements inside a loop for each record. This should be refactored to use `executemany` with batched data arrays to improve ingestion speed, adhering to Pattern 2: Batch Inserts.

**Proposed Python Refactor:**
```python
# Accumulate records into lists
items_batch = []
purification_batch = []

# Inside the loop:
items_batch.append((item_id, corpus_id, title, country, year, period, medium_norm, created_at, updated_at))

# Outside the loop:
cursor.executemany(
    "INSERT INTO items (...) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
    items_batch
)
```

## 4. Maintenance Operations

Adding a post-ingestion optimization step ensures the database remains defragmented and statistics are up-to-date after the complete table rebuild.

**Proposed Cleanup at end of `records_to_sqlite.py`:**
```python
cursor.execute("PRAGMA optimize;")
cursor.execute("VACUUM;")
```

> [!NOTE]
> Se você aprovar essas melhorias, posso refatorar o script `tools/scripts/records_to_sqlite.py` para implementá-las e reconstruir a base com a nova arquitetura.
