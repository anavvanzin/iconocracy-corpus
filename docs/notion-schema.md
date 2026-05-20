# Notion Schema (Historical)

**Status:** archived  
**Superseded by:** [ADR-004](adr/004-vault-as-index.md)

Notion is no longer part of the active ICONOCRACY operating model.

Current workflow:

- `data/processed/records.jsonl` is the canonical operational ledger
- `vault/candidatos/` is the auxiliary cataloguing mirror
- `corpus/corpus-data.json` is the public-facing export

The old Notion mapping is preserved only as historical context in git history.
Do not build new workflow or automation against `notion_sync.py`.

Use instead:

```bash
python tools/scripts/vault_sync.py status
python tools/scripts/vault_sync.py diff
python tools/scripts/vault_sync.py sync
```
