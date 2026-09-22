# Plan: Integrate Curated Contra-Allegory Cases

## Objective
Integrate CONTRA-002, CONTRA-003, and CONTRA-004 into the research corpus and update thesis drafts in `vault/tese/drafts/sumario-iconocracia.md` and `tese/manuscrito/sumario_iconocracia.md`.

## Milestones
1. **Source Verification & Candidate Creation**
   - Verify institutional STF report for CONTRA-002.
   - Locate high-quality visual/archival sources for CONTRA-004 (Getty/AFP).
   - Create Markdown files under `vault/candidatos/` using standard metadata schema and naming convention:
     - `vault/candidatos/BR-1975-STF.md` or naming convention (e.g. `BR-051` or `SCOUT-` number or `BR-051 Escultura de 1975 Sala dos Bustos STF.md`). Wait, let's check what country/numbers are next.
     - `vault/candidatos/FR-024` or `SCOUT-` next number.
     - Let's check sequence numbers in `vault/candidatos/`.
2. **Thesis Draft Update**
   - Update `vault/tese/drafts/sumario-iconocracia.md` and `tese/manuscrito/sumario_iconocracia.md` §3.4.
3. **Schema Validation & Sync**
   - Run `python tools/scripts/vault_sync.py sync` to sync candidates.
   - Run `python tools/scripts/validate_schemas.py` to ensure schema validation succeeds.

## Verification
- Run schema validation script on `records.jsonl`.
- Verify the references in the draft summaries.
