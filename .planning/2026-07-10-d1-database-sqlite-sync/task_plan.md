# Task Plan: D1 Database Cloudflare Sync

**Goal:** Create a pipeline step (and subsequent execution plan) to synchronize the cleaned local SQLite corpus (`data/processed/corpus.sqlite`) into the Cloudflare D1 database (`CORPUS_DB`) used by the Iconocracia Companion App, ensuring the remote backend has the updated N=328 items / N=161 coded structure.

## Context
The companion API (`iconocracia.com/api/corpus/stats` etc.) reads directly from Cloudflare D1. We already synced the static JSON (scout-data.json) and the KV cache, but the D1 database needs to be updated or initialized with the new canonical SQLite data. 

## Phases

### Phase 1: Survey and Schema Verification
- **Status:** complete
- **Tasks:**
  - Locate the script that generates the local SQLite database from `records.jsonl` (likely `tools/scripts/make_sqlite.py` or `records_to_sqlite.py`).
  - Verify the SQLite structure and ensure it reflects the Codebook v2 schema (without fake zeros).
  - Check the companion's `wrangler.toml` for the D1 database binding (`CORPUS_DB`).

### Phase 2: D1 Migration/Sync Script Auth
- **Status:** complete

### Phase 3: Execution and Verification
- **Status:** complete
- **Tasks:**
  - Execute the SQL dump against the Cloudflare D1 database (`wrangler d1 execute CORPUS_DB --remote`).
  - Verify the upload by hitting the Companion's `/api/corpus/stats` endpoint.
  - Confirm the total items match N=328 and the analyzed count is accurate.

## Errors Encountered
| Error | Attempt | Resolution |
|-------|---------|------------|
| | | |

## Verification
- [ ] Local SQLite database successfully rebuilt from the canonical `records.jsonl`.
- [ ] SQL dump accurately reflects the schema needed by D1.
- [ ] D1 upload successful.
- [ ] Companion API `/api/corpus/stats` returns the expected cleaned values.