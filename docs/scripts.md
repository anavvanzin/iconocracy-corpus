# Pipeline Scripts

All scripts live in `tools/scripts/`. Run from repository root:

```bash
python tools/scripts/<script_name>.py [args]
```

## Script Reference

| Script | Purpose | Key Dependencies |
|--------|---------|-----------------|
| `csv_to_records.py` | **Migra** `corpus-data.json` + `corpus_dataset.csv` → `records.jsonl` | stdlib |
| `records_to_corpus.py` | **Exporta** `records.jsonl` → `corpus/corpus-data.json` (merge ou replace) | stdlib |
| `vault_sync.py` | **Sincroniza** `records.jsonl` ↔ `vault/candidatos/` (Obsidian) | stdlib |
| `abnt_citations.py` | Generate ABNT NBR 6023:2025 citations from corpus records | stdlib |
| `batch_example.py` | Demo batch processing for dual-agent corpus builder | stdlib (`uuid`, `hashlib`) |
| `extract_feminist_network.py` | Extract feminist iconography subnetwork (Iconclass 48C51) | stdlib |
| `make_index.py` | Generate search index from Iconclass textbase | `textbase`, `sqlite3` |
| `make_skos.py` | Generate SKOS/RDF vocabulary from Iconclass data | `textbase`, `rich` |
| `make_sqlite.py` | Build SQLite database from Iconclass data | stdlib (`sqlite3`) |
| `trace_evidence.py` | Generate evidence traceability reports from corpus records | stdlib |
| `notion_sync.py` | **DESCONTINUADO** — redireciona para `vault_sync.py` | — |
| `validate_schemas.py` | Validate JSON records against dual-agent schemas | `jsonschema` |
| `code_purification.py` | Interactive CLI for coding 10 purification indicators (0–3) per corpus item | stdlib |

## Details

### `abnt_citations.py`

Generates bibliographic citations following ABNT NBR 6023:2025 standard. Handles institutional records, IIIF manifests, and persistent identifiers. Functions: `normalize_name()`, `format_abnt_web_source()`.

### `batch_example.py`

Demonstrates the batch processing pipeline for the dual-agent corpus builder (see `docs/dual-agent-corpus-builder.md`). Creates batch manifests with UUID-based item tracking and SHA256 deduplication via `generate_item_hash()`.

### `extract_feminist_network.py`

Extracts the feminist iconography subnetwork from Iconclass notation 48C51. Output: `data/processed/feminist_network_48C51_pt.json`.

### `make_index.py` / `make_skos.py` / `make_sqlite.py`

Iconclass data processing utilities. Require the `textbase` library for parsing Iconclass textbase files. `make_sqlite.py` uses only stdlib `sqlite3`.

### `csv_to_records.py`

Migrates `corpus/corpus-data.json` + `data/processed/corpus_dataset.csv` into
`data/processed/records.jsonl`, conforming to `master-record.schema.json`.
Uses corpus-data.json as the primary source (richest data, 139 items) and
merges purification indicators from corpus_dataset.csv.

```bash
python tools/scripts/csv_to_records.py               # write records.jsonl
python tools/scripts/csv_to_records.py --dry-run     # preview only
python tools/scripts/csv_to_records.py --item BR-001 # single item
```

### `records_to_corpus.py`

Exports `records.jsonl` → `corpus/corpus-data.json`. In merge mode (default),
rich fields that exist in the current corpus (panofsky, institution, etc.) are
preserved for unmatched keys; records.jsonl fields overwrite overlapping ones.

```bash
python tools/scripts/records_to_corpus.py             # merge export
python tools/scripts/records_to_corpus.py --replace   # full replace
python tools/scripts/records_to_corpus.py --diff      # show differences
python tools/scripts/records_to_corpus.py --dry-run   # preview only
```

### `vault_sync.py`

Bidirectional sync between `data/processed/records.jsonl` and `vault/candidatos/`
(Obsidian). The vault is the auxiliary cataloging mirror; records.jsonl is canonical.

```bash
python tools/scripts/vault_sync.py status   # count items in each
python tools/scripts/vault_sync.py diff     # show differences
python tools/scripts/vault_sync.py pull     # vault → records.jsonl (new items)
python tools/scripts/vault_sync.py push     # records.jsonl → vault (new notes)
python tools/scripts/vault_sync.py sync     # pull then push
```

### `notion_sync.py` *(DESCONTINUADO)*

O Notion não é mais usado. Este script emite um aviso de deprecação e
redireciona automaticamente para `vault_sync.py`.

### `validate_schemas.py`

Validates JSON records against the schemas in `tools/schemas/`. Gracefully falls back if `jsonschema` is not installed.

```bash
python tools/scripts/validate_schemas.py examples/batch_001/master_record_*.json
```

### `code_purification.py`

Interactive CLI for coding the 10 ordinal purification indicators (0–3) on corpus items. Reads from `corpus/corpus-data.json`, writes to `data/processed/purification.jsonl`. See `data/docs/codebook.md` for scale definitions.

```bash
python tools/scripts/code_purification.py                  # code next uncoded item
python tools/scripts/code_purification.py --resume         # skip already-coded
python tools/scripts/code_purification.py --item BR-001    # code specific item
python tools/scripts/code_purification.py --batch FR       # code all FR-* items
python tools/scripts/code_purification.py --status         # show progress
python tools/scripts/code_purification.py --export-csv     # export corpus_dataset.csv
```
