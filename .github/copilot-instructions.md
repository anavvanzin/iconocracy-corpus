# Copilot instructions for `iconocracy-corpus`

`iconocracy-corpus` is the canonical thesis hub inside `/Users/ana/Research`. Read `README.md`, `AGENTS.md`, `CLAUDE.md`, and `docs/OPERATING_MODEL.md` before changing workflow or data contracts; they define the current operating model.

## Build and test commands

Run Python commands from the repository root after activating the project environment:

```bash
conda activate iconocracy
python tools/scripts/validate_schemas.py
python tools/scripts/validate_schemas.py data/processed/records.jsonl --schema master-record --verbose
python tools/scripts/validate_schemas.py data/processed/purification.jsonl --schema purification-record --verbose
python tools/scripts/records_to_corpus.py --diff
python tools/scripts/vault_sync.py status
python tools/scripts/code_purification.py --status
```

Tests use `unittest`, not `pytest`:

```bash
python -m unittest discover -s tests
python -m unittest tests.argos.test_smoke
python -m unittest tests.argos.test_manifest_builder.ManifestBuilderTests.test_build_manifest_only_includes_pending_items_with_source_metadata
python -m unittest tests.training.test_compare_iconocracy_eval_runs
```

Thesis builds are driven by Pandoc from `vault/tese/`:

```bash
make -C vault/tese/ docx
make -C vault/tese/ pdf
make -C vault/tese/ capitulo-1.docx
make -C vault/tese/ clean
```

TypeScript subprojects with their own build commands:

```bash
cd indexing/gallica-mcp-server && npm run build
cd indexing/gallica-mcp-server && npm run dev
cd indexing/corpus-scout-agent && npm run build
cd indexing/corpus-scout-agent && npm run dev
```

Project MCP servers are declared in `.mcp.json`. At the moment it wires the local `gallica-mcp-server` build and a Playwright MCP server for browser automation workflows.

## High-level architecture

This repository is the **canonical source** in a wider research workspace. Workspace-facing paths under `/Users/ana/Research/pipelines/*` and `/Users/ana/Research/vaults/*` may be symlinks back into directories tracked here, so edits made through those aliases can still modify this repo.

The repo operates across three durable surfaces:

1. **Local research surface** for corpus expansion, endurecimento coding, vault work, and manuscript drafting.
2. **GitHub surface** for canonical history, CI, and release preparation.
3. **Hugging Face surface** for frozen public dataset snapshots.

The main corpus pipeline is:

```text
WebScout archive discovery
-> IconoCode visual analysis
-> data/processed/records.jsonl
-> corpus/corpus-data.json
-> dashboards and Hugging Face releases
```

`tools/schemas/` defines the contracts for these ledgers and `.github/workflows/validate.yml` re-validates them in CI. The public corpus dashboard and browser-facing artifacts read from `corpus/corpus-data.json`, but the operational ledger remains `data/processed/records.jsonl`.

There is also a separate acquisition pipeline around ARGOS:

```text
corpus/corpus-data.json + data/raw/drive-manifest.json
-> tools/scripts/argos_build_manifest.py
-> data/raw/argos/manifest.json
-> per-item acquisition/report scripts
```

`vault/candidatos/` is an Obsidian mirror of corpus items, `vault/tese/` is the Pandoc thesis build surface, and the repository root `.mcp.json` points local MCP clients at both `indexing/gallica-mcp-server` and Playwright MCP.

## Key conventions

### Canonical data order

Preserve this source-of-truth order:

1. `data/processed/records.jsonl`
2. `corpus/corpus-data.json`
3. `data/processed/purification.jsonl`
4. `vault/candidatos/`

Update the canonical ledger first and derive public exports from it. Do not treat vault notes as the primary source.

### Data handling rules

- `data/raw/` is metadata-only in git. Raw binaries live in Google Drive, and CI rejects non-manifest files there.
- Use repo scripts for data movement: `records_to_corpus.py` for export, `vault_sync.py` for vault reconciliation, `build_hf_release.py` for public snapshots.
- Prefer scripted or full-file JSON rewrites over partial manual edits for corpus artifacts.

### Thesis and corpus conventions

- Run Python utilities from repo root as `python tools/scripts/<name>.py`.
- `tese/manuscrito/*_original` is not the working surface for edits.
- Vault candidate notes follow `CC-NNN Title.md`; session notes follow `vault/sessoes/SCOUT-SESSION-YYYY-MM-DD.md`.
- Every corpus item is expected to stay traceable across Drive/manifest data, the vault note, and `data/processed/records.jsonl`.

### Terminology and writing constraints

- Keep **endurecimento** in Portuguese.
- Keep **Contrato Sexual Visual** and **Feminilidade de Estado** as thesis-native concepts.
- Keep **Pathosformel**, **Zwischenraum**, and **Nachleben** in German.
- Use **ABNT NBR 6023:2025** for citations.
- Maintain the repository's juridico-penal framing; do not recast thesis material in anthropological or sociological terms.

### Release gate

Before public corpus or site releases, the standard sequence is:

```bash
python tools/scripts/validate_schemas.py
python tools/scripts/vault_sync.py status
python tools/scripts/records_to_corpus.py --diff
python tools/scripts/code_purification.py --status
python tools/scripts/build_hf_release.py
```
