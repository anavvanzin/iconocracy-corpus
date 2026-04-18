# Hub Consistency Validation Log

Data: 2026-04-17
Branch: `infra/hub-consistency-refactor`
Worktree: `/Users/ana/Research/.worktrees/iconocracy-corpus-hub-consistency`

## Structural checks

### Nested `.git` directories inside the hub
Command:
```bash
find /Users/ana/Research/.worktrees/iconocracy-corpus-hub-consistency -mindepth 2 -maxdepth 4 -name .git | cat
```

Result:
- no nested `.git` directories found in the inspected depth range

### Working tree hygiene check
Command:
```bash
git diff --check && git status --short
```

Result:
- `git diff --check` returned clean (no whitespace/conflict-marker issues)
- working tree contains only the intended refactor edits for docs, ignore policy, root moves, and new inventory/ADR files

## Canonical operational checks

### Schema validation
Command:
```bash
conda run -n iconocracy python tools/scripts/validate_schemas.py data/processed/records.jsonl --schema master-record --verbose
```

Result:
- failed before and after the refactor
- current blocker is pre-existing data drift in `records.jsonl`
- reported errors:
  - `iconocode.pre_iconographic` missing
  - `iconocode.codes` missing
  - `iconocode.validation.claim_ledger` missing
- affected records: 2/2 in the current local ledger snapshot

Interpretation:
- failure is not introduced by the consistency refactor
- it confirms that repo-level data repair remains a separate task

### `records_to_corpus.py --diff`
Command:
```bash
conda run -n iconocracy python tools/scripts/records_to_corpus.py --diff
```

Result:
- command succeeded
- still shows severe pre-existing divergence:
  - `records.jsonl`: 2 items
  - `corpus-data.json`: 165 items
  - 163 items exist only in `corpus-data.json`

Interpretation:
- divergence is baseline project debt, not caused by root-taxonomy cleanup

### ENDURECIMENTO coding status
Command:
```bash
conda run -n iconocracy python tools/scripts/code_purification.py --status
```

Result:
- succeeded
- reported:
  - total items: 165
  - coded: 0
  - remaining: 165

### Vault sync status
Command:
```bash
conda run -n iconocracy python tools/scripts/vault_sync.py status
```

Result:
- succeeded
- reported:
  - `records.jsonl`: 2 registros
  - `vault/candidatos/`: 193 notas
  - with corpus ID: 26
  - SCOUT notes: 142
  - others: 25

Interpretation:
- confirms pre-existing mismatch between canonical ledger and vault mirror

## Refactor-specific validation

### Root taxonomy outcome
Observed root after refactor:
- removed from root:
  - `PHD/`
  - `biblio/`
  - `fix_records_schema.py`
  - duplicate `companion-data.json`
- added/documented:
  - `archive/root-legacy/PHD/`
  - `archive/root-legacy/scripts/fix_records_schema.py`
  - `tese/bibliografia/ICONOCRACY_Cap3.bib`
  - `docs/root-inventory.md`
  - `docs/generated-artifacts-policy.md`
  - `docs/adr/006-hub-root-taxonomy.md`

### Plan/spec location policy
Validated by docs updates:
- `docs/plans/` = canonical location for plans and operational memos
- `docs/superpowers/specs/` = reusable specs/guides
- `docs/superpowers/plans/` is not treated as canonical in this branch

### Symlink policy
Retained and documented as compatibility surfaces:
- `Atlas`
- `indexing`
- `iurisvision`
- `js-genai`

## Conclusion

The consistency refactor completed its structural/documentation goals.

What is now true:
- root taxonomy is clearer and less ambiguous
- plan/spec locations are normalized in documentation
- duplicate root companion export is removed
- one-off/historical assets were moved out of the root
- new inventory, ADR, and artifact policy documents were added

What remains unresolved but is explicitly pre-existing:
- schema-invalid `records.jsonl`
- major `records.jsonl` ↔ `corpus-data.json` divergence
- major `records.jsonl` ↔ `vault/candidatos/` divergence

Next recommended follow-up after merging this branch:
1. separate data-repair branch for canonical ledger restoration
2. only after that, rerun the release gate expecting green results
