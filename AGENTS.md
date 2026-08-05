# AGENTS.md — ICONOCRACY Quick Reference

> **This is the quick-reference card.** For full architecture, mode routing, hooks, skills, terminology tables, known data issues, and corpus parameters, see [`CLAUDE.md`](CLAUDE.md).

## Data Hierarchy (audit 2026-07-31)

| # | Layer | Count | Role |
|---|-------|-------|------|
| 1 | `data/processed/records.jsonl` | 335 | Canonical operational ledger |
| 2 | `corpus/corpus-data.json` | 335 | Public-facing export |
| 3 | `data/processed/purification.jsonl` | 279 | Endurecimento coding ledger |
| 4 | `vault/candidatos/` | 410 | Auxiliary cataloguing mirror |

## Environment

```bash
conda activate iconocracy
python tools/scripts/<script>.py           # always from repo root
pytest tests/                              # full suite (~24 test files)
```

## Essential Commands

```bash
# Validation (CLAUDE.md §Quick Commands for full list)
python tools/scripts/validate_schemas.py
python tools/scripts/validate_schemas.py data/processed/records.jsonl --schema master-record --verbose
python tools/scripts/check_thesis_terms.py   # forbidden terms + misattributions

# Export diff (run before touching corpus-data.json)
python tools/scripts/records_to_corpus.py --diff

# Vault sync
python tools/scripts/vault_sync.py status|sync|pull|push|diff

# Endurecimento coding
python tools/scripts/code_purification.py --status
python tools/scripts/code_purification.py --item ID|--batch SIGLA|--export-csv

# Thesis compilation
make -C vault/tese/ docx     # full thesis → DOCX
make -C vault/tese/ pdf      # full thesis → PDF (requires LaTeX)

# Release gate (run in this order before HF release)
python tools/scripts/validate_schemas.py
python tools/scripts/code_purification.py --status
python tools/scripts/vault_sync.py status
python tools/scripts/records_to_corpus.py --diff
python tools/scripts/build_hf_release.py
```

## Guardrails

- `tese/manuscrito/*_original` is read-only; work on `*_rev` copies
- `data/raw/` is metadata-only in git (ADR-001); binaries on Google Drive
- Never edit `corpus/corpus-data.json` directly — use Python scripts
- All Codebook v2 allegory fields (`subtipo`, `familia_alegorica`, `vetor_colonial`, `hipotese_racial`) nest under `"purificacao"` key in `records.jsonl`; `records_to_corpus.py` flattens them to `corpus-data.json` root
- Vault notes: `XX-NNN Title.md` (e.g., `FR-013 Déclaration des droits.md`) in Obsidian Flavored Markdown
- `vault_backup.py` for snapshots; never mix backups on `main`
- `python tools/scripts/validate_schemas.py` must pass before any commit

## Traceability

Every corpus item must exist in three places: (1) Google Drive + `data/raw/drive-manifest.json`, (2) `vault/candidatos/XX-NNN Title.md`, (3) `data/processed/records.jsonl`.

## Canonical Terminology

- **iconometria** — framework guarda-chuva (medição/análise de padrões iconográficos); `iconometria ⊇ endurecimento` (decisão 2026-07-11)
- **endurecimento** — eixo de fixidez dentro da iconometria; NEVER "hardening" / "embrutecimento"; campo de dados canônico `endurecimento_score` (chave estável)
- **Contrato Sexual Visual**, **Feminilidade de Estado**, **Contrato Racial Visual**, **Purificação Clássica** — original thesis concepts (Vanzin 2026)
- **Pathosformel**, **Zwischenraum**, **Nachleben** — always in German (Warburg)
- Citations: ABNT NBR 6023:2025; Mondzain = 2002 edition
- 10 purification indicators (ordinal 0–3) + 3 iconocratic regimes → see [`CLAUDE.md`](CLAUDE.md)
