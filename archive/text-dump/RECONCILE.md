# Corpus Reconciliation

The ICONOCRACY corpus lives in **two canonical stores** that must stay
coherent:

| Store | Role | IDs |
|-------|------|-----|
| `data/processed/records.jsonl` | Operational canonical ledger (WebScout → IconoCode pipeline output) | deterministic UUID5 per item |
| `corpus/corpus-data.json`      | Public-facing export (dashboards, HF release, HTML browser)       | human codes (e.g. `AR-001`, `FR-013`) |

A third file, `data/processed/purification.jsonl`, carries the
endurecimento coding ledger and is reconciled separately by
`code_purification.py`.

## When to reconcile

- Whenever items are added or removed in either store
- Before a thesis compile or HF release
- After importing new DOCX fichas, SCOUT batches, or CSV ingest
- As part of the release gate in `docs/OPERATING_MODEL.md`

## Scripts

Both scripts live in `tools/scripts/`. Run from the repo root with the
conda `iconocracy` environment active.

### 1. `reconcile_data.py` — read-only audit

```bash
python tools/scripts/reconcile_data.py            # full report (text)
python tools/scripts/reconcile_data.py --dry-run  # summary counts only
python tools/scripts/reconcile_data.py --json     # machine-readable
```

Matching strategy:

1. Primary key: normalized URL (lower-cased, protocol-stripped)
2. Fallback: normalized title + date

Reports: matched pairs, orphans in each store, field divergences
(title / date / url / iconocode-vs-coded mismatch).

Exit code is `0` whether or not divergences were found — parse stdout
(or the `--json` output) to decide.

### 2. `records_to_corpus.py` — rebuild the public export

```bash
python tools/scripts/records_to_corpus.py --diff      # preview only
python tools/scripts/records_to_corpus.py             # merge (default)
python tools/scripts/records_to_corpus.py --dry-run   # show size, no write
python tools/scripts/records_to_corpus.py --replace   # full overwrite
```

Default `--merge` mode is **safe**: existing enriched fields in
`corpus-data.json` (e.g. `panofsky` blocks, hand-curated `indicadores`,
institution tags) are preserved and only the authoritative fields from
`records.jsonl` are updated. Use `--replace` only when intentionally
discarding enrichment.

Writes are atomic (temp file + `os.replace`) so a half-written
`corpus-data.json` cannot occur.

## Coherence regression test

`tests/tools/test_reconcile_coherence.py` runs both scripts and asserts
zero divergences. It freezes the aligned state — if it fails, one of
the two stores drifted and must be re-merged before committing.

As of the T2 commit, both diagnostics report **0 divergences across
165 items**.
