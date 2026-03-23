# Pipeline Scripts

All scripts live in `tools/scripts/`. Run from repository root:

```bash
python tools/scripts/<script_name>.py [args]
```

## Script Reference

| Script | Purpose | Key Dependencies |
|--------|---------|-----------------|
| `abnt_citations.py` | Generate ABNT NBR 6023:2025 citations from corpus records | stdlib |
| `batch_example.py` | Demo batch processing for dual-agent corpus builder | stdlib (`uuid`, `hashlib`) |
| `extract_feminist_network.py` | Extract feminist iconography subnetwork (Iconclass 48C51) | stdlib |
| `make_index.py` | Generate search index from Iconclass textbase | `textbase`, `sqlite3` |
| `make_skos.py` | Generate SKOS/RDF vocabulary from Iconclass data | `textbase`, `rich` |
| `make_sqlite.py` | Build SQLite database from Iconclass data | stdlib (`sqlite3`) |
| `trace_evidence.py` | Generate evidence traceability reports from corpus records | stdlib |
| `validate_schemas.py` | Validate JSON records against dual-agent schemas | `jsonschema` (optional fallback) |

## Details

### `abnt_citations.py`

Generates bibliographic citations following ABNT NBR 6023:2025 standard. Handles institutional records, IIIF manifests, and persistent identifiers. Functions: `normalize_name()`, `format_abnt_web_source()`.

### `batch_example.py`

Demonstrates the batch processing pipeline for the dual-agent corpus builder (see `docs/dual-agent-corpus-builder.md`). Creates batch manifests with UUID-based item tracking and SHA256 deduplication via `generate_item_hash()`.

### `extract_feminist_network.py`

Extracts the feminist iconography subnetwork from Iconclass notation 48C51. Output: `data/processed/feminist_network_48C51_pt.json`.

### `make_index.py` / `make_skos.py` / `make_sqlite.py`

Iconclass data processing utilities. Require the `textbase` library for parsing Iconclass textbase files. `make_sqlite.py` uses only stdlib `sqlite3`.

### `trace_evidence.py`

Generates traceability reports linking each corpus item to its evidence chain: Origin (Drive) → Process (GitHub) → Description (Notion).

### `validate_schemas.py`

Validates JSON records against the schemas in `tools/schemas/`. Gracefully falls back if `jsonschema` is not installed.

```bash
python tools/scripts/validate_schemas.py examples/batch_001/master_record_*.json
```
