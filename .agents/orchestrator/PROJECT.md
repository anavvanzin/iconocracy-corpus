# Project: ICONOCRACIA Contra-Allegories Integration

## Architecture
- **Corpus Data Flow**: `vault/candidatos/` (Obsidian Markdown candidates) ↔ `data/processed/records.jsonl` (canonical master record ledger, synchronized via `tools/scripts/vault_sync.py`) ↔ `corpus/corpus-data.json` (public-facing export, synchronized via `tools/scripts/records_to_corpus.py`).
- **Thesis Drafts**: `vault/tese/drafts/sumario-iconocracia.md` and `tese/manuscrito/sumario_iconocracia.md` are edited to integrate reference cases in section §3.4.

## Milestones
| # | Name | Scope | Dependencies | Status |
|---|---|---|---|---|
| 1 | Source Verification & Candidate Creation | Verify sources for CONTRA-002, CONTRA-003, and CONTRA-004. Create Obsidian Markdown candidate files in `vault/candidatos/` following the project schema and naming conventions. | none | DONE |
| 2 | Thesis Draft Update | Integrate the three selected cases into the §3.4 drafts in `vault/tese/drafts/sumario-iconocracia.md` and `tese/manuscrito/sumario_iconocracia.md`. | M1 | DONE |
| 3 | Validation and Sync | Synchronize candidates to `records.jsonl` using `vault_sync.py` and run `validate_schemas.py` to ensure schema validation passes with 100% success. | M2 | DONE |

## Code Layout
- `vault/candidatos/` - Directory for case candidate files.
- `vault/tese/drafts/sumario-iconocracia.md` - Thesis summary draft in vault.
- `tese/manuscrito/sumario_iconocracia.md` - Thesis manuscript summary in source.
- `data/processed/records.jsonl` - Canonical operational ledger.
- `tools/scripts/vault_sync.py` - Bidirectional sync tool.
- `tools/scripts/validate_schemas.py` - JSON schema validation script.
