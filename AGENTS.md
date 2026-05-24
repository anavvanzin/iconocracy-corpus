# AGENTS.md — ICONOCRACY Quick Brief

## Context
Monorepo for the doctoral thesis **"Iconocracia: Alegoria Feminina na História da Cultura Jurídica (Séculos XIX–XX)"** — PPGD/UFSC, Ana Vanzin, defense 2026. Companion file for Claude Code sessions: `CLAUDE.md`.

## Data Hierarchy (counts 2026-05-24)
1. `data/processed/records.jsonl` — 265 records (canonical)
2. `corpus/corpus-data.json` — 264 items (public export)
3. `data/processed/purification.jsonl` — 264 records (endurecimento coding)
4. `vault/candidatos/` — 314 catalog cards (auxiliary mirror)

## Environment
```bash
conda activate iconocracy
python tools/scripts/<script>.py           # always from repo root
pytest tests/                              # full suite (24 test files)
```

## Key Commands
```bash
# Validation
python tools/scripts/validate_schemas.py data/processed/records.jsonl --schema master-record --verbose

# Export diff (run before touching corpus-data.json)
python tools/scripts/records_to_corpus.py --diff

# Vault sync
python tools/scripts/vault_sync.py pull|push|sync|diff|status

# Endurecimento coding
python tools/scripts/code_purification.py --status|--item ID|--batch SIGLA|--export-csv

# Thesis compilation
make -C vault/tese/ docx     # full thesis → DOCX
make -C vault/tese/ pdf      # full thesis → PDF (requires LaTeX)

# Release gate (run in order before HF release)
python tools/scripts/validate_schemas.py
python tools/scripts/vault_sync.py status
python tools/scripts/records_to_corpus.py --diff
python tools/scripts/code_purification.py --status
python tools/scripts/build_hf_release.py
```

## Thesis Architecture
4 case studies: **Brasil-República** (1889–1930) · **Brasil-Tribunais** (Justiça vendada no STF) · **França-Marianne** (1789–1946) · **UK-Britannia** (1800–1950). Three argumentative versions: historical · theoretical-conceptual · comparative-postcolonial. Four theoretical clusters: Legal History · Visual Culture · Feminist Theory · Post-colonial.

## 10 Purification Indicators (ordinal 0–3)
desincorporação · rigidez_postural · dessexualização · uniformização_facial · heraldização · enquadramento_arquitetônico · apagamento_narrativo · monocromatização · serialidade · inscrição_estatal

Three iconocratic regimes: FUNDACIONAL → NORMATIVO → MILITAR → CONTRA-ALEGORIA.

## Mandatory Terminology
- **endurecimento** — NEVER "hardening" / "embrutecimento"
- **Contrato Sexual Visual**, **Feminilidade de Estado**, **Contrato Racial Visual**, **Purificação Clássica** — original thesis concepts (Vanzin 2026)
- **Pathosformel**, **Zwischenraum**, **Nachleben** — always in German (Warburg)
- Citations: ABNT NBR 6023:2025; Mondzain = 2002 edition

## Traceability
Every corpus item must exist in: (1) Google Drive + `data/raw/drive-manifest.json`, (2) `vault/candidatos/CC-NNN Title.md`, (3) `data/processed/records.jsonl`.

## Guardrails
- `tese/manuscrito/*_original` is read-only; work on `*_rev` copies
- `data/raw/` is metadata-only in git (ADR-001); binaries on Google Drive
- Never edit `corpus/corpus-data.json` directly — use Python scripts
- Vault notes follow `XX-NNN Title.md` pattern in Obsidian Flavored Markdown
- `vault_backup.py` for snapshots; never mix backups on `main`
- `python tools/scripts/validate_schemas.py` must pass before any commit
