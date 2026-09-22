# Walkthrough - Corpus Validation and Database Synchronization

## Changes Made
- Executed JSON Schema validation on the canonical ledger ([records.jsonl](file:///Users/ana/Research/hub/iconocracy-corpus/data/processed/records.jsonl)) and the purification ledger ([purification.jsonl](file:///Users/ana/Research/hub/iconocracy-corpus/data/processed/purification.jsonl)).
- Executed `records_to_corpus.py --diff` to verify sync between the ledger and public export.
- Identified that the local SQLite replica ([corpus.sqlite](file:///Users/ana/Research/hub/iconocracy-corpus/data/processed/corpus.sqlite)) was out of sync (containing 280 items instead of 328).
- **SQLite Performance Refactoring**: 
  - Added a Full-Text Search Virtual Table (`items_fts`) with insert/update/delete triggers for immediate search synchronization.
  - Enabled aggressive SQLite performance `PRAGMA` variables (`WAL` mode, `temp_store=MEMORY`, `synchronous=NORMAL`).
  - Refactored python data inserts to utilize massive `executemany` batch operations to eliminate transaction overhead.
  - Added SQLite maintenance triggers (`PRAGMA optimize` and `VACUUM`).
- Synchronized `corpus.sqlite` by executing the newly optimized `tools/scripts/records_to_sqlite.py`.

## What Was Tested
- Validated all 328 records in `records.jsonl` (100% valid, 0 warnings).
- Validated all 236 records in `purification.jsonl` (100% valid).
- Verified `corpus-data.json` is perfectly in sync with `records.jsonl`.
- Verified the SQLite database now contains all 328 items, 287 purification records, 21 evidence sources, and 260 Iconclass mappings.
- Ran the full test suite with `pytest` multiple times (before and after SQLite script modifications).

## Validation Results
- All schema validations passed successfully.
- Database checks executed successfully with correct aggregations.
- All 181 unit and integration tests passed successfully on the final optimized state.
